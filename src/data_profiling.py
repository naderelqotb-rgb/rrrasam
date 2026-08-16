"""
Data Profiling Script for Rasam Project
این اسکریپت چهار فایل CSV اصلی را بررسی و گزارش کامل تولید می‌کند
"""

import pandas as pd
from pathlib import Path

# مسیر داده‌ها
DATA_DIR = Path("data/raw")

# لیست فایل‌های CSV
CSV_FILES = [
    "solar_telemetry.inverter_data.csv",
    "solar_telemetry.lvpanel_data.csv",
    "solar_telemetry.mvpanel_data.csv",
    "solar_telemetry.string_data.csv"
]

def profile_csv(file_path):
    """پروفایل کامل یک فایل CSV"""
    print(f"\n{'='*80}")
    print(f"فایل: {file_path.name}")
    print(f"{'='*80}")
    
    # خواندن فایل
    df = pd.read_csv(file_path)
    
    # اطلاعات پایه
    print(f"\n📊 تعداد ردیف: {df.shape[0]:,}")
    print(f"📏 تعداد ستون: {df.shape[1]}")
    
    # نام ستون‌ها
    print(f"\n📋 نام ستون‌ها ({len(df.columns)} عدد):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    
    # dtype و nullها
    print(f"\n🔍 نوع داده و مقادیر null:")
    null_counts = df.isnull().sum()
    for col in df.columns:
        dtype = df[col].dtype
        null_count = null_counts[col]
        null_pct = (null_count / len(df)) * 100
        print(f"   {col}: {dtype}, null={null_count:,} ({null_pct:.2f}%)")
    
    # چند نمونه رکورد
    print(f"\n📄 نمونه رکوردها (3 ردیف اول):")
    print(df.head(3).to_string())
    
    # بررسی timestamp و ts
    if 'timestamp' in df.columns:
        print(f"\n⏰ بررسی ستون timestamp:")
        print(f"   نوع داده: {df['timestamp'].dtype}")
        print(f"   کمینه: {df['timestamp'].min()}")
        print(f"   بیشینه: {df['timestamp'].max()}")
        print(f"   نمونه مقادیر: {df['timestamp'].head(5).tolist()}")
    
    if 'ts' in df.columns:
        print(f"\n⏰ بررسی ستون ts:")
        print(f"   نوع داده: {df['ts'].dtype}")
        print(f"   کمینه: {df['ts'].min()}")
        print(f"   بیشینه: {df['ts'].max()}")
        print(f"   نمونه مقادیر: {df['ts'].head(5).tolist()}")
    
    # device_code یکتا
    if 'device_code' in df.columns:
        unique_devices = df['device_code'].nunique()
        print(f"\n🆔 device_codeهای یکتا: {unique_devices}")
        print(f"   مقادیر: {df['device_code'].unique().tolist()}")
    
    # device_type یکتا
    if 'device_type' in df.columns:
        unique_types = df['device_type'].nunique()
        print(f"\n🏷️ device_typeهای یکتا: {unique_types}")
        print(f"   مقادیر: {df['device_type'].unique().tolist()}")
    
    return df

def main():
    print("="*80)
    print("Rasam Data Profiling Report")
    print("گزارش بررسی دیتاست‌های پروژه رسام")
    print("="*80)
    
    all_dfs = {}
    
    for csv_file in CSV_FILES:
        file_path = DATA_DIR / csv_file
        if file_path.exists():
            df = profile_csv(file_path)
            all_dfs[csv_file] = df
        else:
            print(f"\n❌ فایل یافت نشد: {file_path}")
    
    # خلاصه مقایسه‌ای
    print(f"\n\n{'='*80}")
    print("خلاصه مقایسه‌ای چهار دیتاست")
    print("="*80)
    
    summary_data = []
    for name, df in all_dfs.items():
        summary_data.append({
            'فایل': name.replace('solar_telemetry.', '').replace('.csv', ''),
            'ردیف': f"{df.shape[0]:,}",
            'ستون': df.shape[1],
            'device_code یکتا': df.get('device_code', pd.Series()).nunique() if 'device_code' in df.columns else '-',
            'device_type یکتا': df.get('device_type', pd.Series()).nunique() if 'device_type' in df.columns else '-',
        })
    
    summary_df = pd.DataFrame(summary_data)
    print("\n" + summary_df.to_string(index=False))
    
    # تحلیل شباهت و تفاوت
    print(f"\n\n{'='*80}")
    print("تحلیل ساختار داده‌ها")
    print("="*80)
    
    print("""
📌 شباهت‌ها:
   - همه فایل‌ها ستون‌های مشترک دارند: _id, message_id, board_id, device_code, device_type
   - همه دارای timestamp و ts هستند (زمان به فرمت Unix epoch)
   - همه دارای ingested_at هستند (زمان به فرمت ISO8601)
   - همه دارای status یا work_state برای وضعیت تجهیز هستند

📌 تفاوت‌ها:
   - inverter_data: داده‌های اینورتر شامل ولتاژ، جریان، MPPTها، کارکرد
   - lvpanel_data: داده‌های پنل LV شامل انرژی فعال/واکنشی، توان، ضریب قدرت
   - mvpanel_data: داده‌های پنل MV مشابه LV اما با مقادیر ولتاژ بالاتر
   - string_data: ساده‌ترین فایل فقط شامل voltage, current, power برای هر رشته

📌 شناسایی ستون‌ها:
   - شناسه تجهیز: device_code
   - زمان: timestamp (Unix), ts (Unix), ingested_at (ISO)
   - اندازه‌گیری: بسته به نوع تجهیز (ولتاژ، جریان، توان، انرژی)
   - وضعیت: status یا work_state
   - اطلاعات کنترلی: device_type, board_id, message_id
""")

if __name__ == "__main__":
    main()
