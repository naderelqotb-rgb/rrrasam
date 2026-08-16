"""
اسکریپت ساده برای تبدیل CSVهای خام به SQLite database.
فقط از pandas و sqlite3 استاندارد استفاده می‌کند.
"""

import pandas as pd
import sqlite3
import os

# مسیرهای نسبی
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "telemetry.sqlite")

# نگاشت فایل‌های CSV به نام جدول‌ها
CSV_TO_TABLE = {
    "solar_telemetry.inverter_data.csv": "inverter_data",
    "solar_telemetry.lvpanel_data.csv": "lvpanel_data",
    "solar_telemetry.mvpanel_data.csv": "mvpanel_data",
    "solar_telemetry.string_data.csv": "string_data",
}


def build_database():
    """
    خواندن CSVها و انتقال به SQLite.
    اگر database وجود داشته باشد، حذف و دوباره ساخته می‌شود.
    """
    # اگر database وجود دارد، حذف کن تا از صفر شروع شود
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Database قدیمی حذف شد: {DB_PATH}")

    # اتصال به SQLite (اگر نباشد می‌سازد)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"شروع ساخت database در: {DB_PATH}\n")

    for csv_filename, table_name in CSV_TO_TABLE.items():
        csv_path = os.path.join(RAW_DATA_DIR, csv_filename)

        # بررسی وجود فایل
        if not os.path.exists(csv_path):
            print(f"❌ فایل یافت نشد: {csv_path}")
            continue

        # خواندن CSV با pandas
        print(f"در حال خواندن: {csv_filename}")
        df = pd.read_csv(csv_path)

        # انتقال به SQLite (بدون index)
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"✅ جدول '{table_name}' با {len(df)} رکورد ساخته شد.")

    conn.commit()
    conn.close()

    print(f"\n🎉 Database با موفقیت ساخته شد.")


def verify_database():
    """
    بررسی ساده database ساخته‌شده.
    """
    if not os.path.exists(DB_PATH):
        print("❌ Database وجود ندارد.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n" + "=" * 50)
    print("بررسی Database ساخته‌شده")
    print("=" * 50)

    # لیست جدول‌ها
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\nجدول‌های موجود ({len(tables)} عدد):")
    for table in tables:
        print(f"  - {table}")

    # تعداد رکورد هر جدول
    print("\nتعداد رکوردها:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"  - {table}: {count:,} رکورد")

    # بررسی ستون‌های هر جدول
    print("\nستون‌های هر جدول:")
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"  - {table} ({len(columns)} ستون):")
        # نمایش ۵ ستون اول
        sample_cols = columns[:5]
        print(f"      نمونه: {', '.join(sample_cols)}")
        if len(columns) > 5:
            print(f"      ... و {len(columns) - 5} ستون دیگر")

    conn.close()
    print("\n" + "=" * 50)


if __name__ == "__main__":
    build_database()
    verify_database()
