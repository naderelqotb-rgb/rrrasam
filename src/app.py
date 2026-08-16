"""
Rasam Demo - Simple Entry Point

This is the main entry point for the Rasam demo application.
Currently displays a simple welcome page with product description.
"""

import streamlit as st


def main():
    """Main function to run the Rasam demo page."""
    
    # Page configuration
    st.set_page_config(
        page_title="Rasam",
        page_icon="📊",
        layout="centered"
    )
    
    # Main title
    st.title("Rasam")
    
    # Product description
    st.markdown("""
    ### درباره محصول Rasam
    
    Rasam یک پلتفرم تحلیل داده‌های صنعتی است که به مشتریان امکان می‌دهد 
    داده‌های تجهیزات و سنسورهای خود را رصد کرده و بینش‌های ارزشمند کسب کنند.
    
    این نسخه یک Demo ساده است که ساختار پایه پروژه را نشان می‌دهد.
    
    ---
    
    **ویژگی‌های آینده:**
    - اتصال به منابع داده مختلف
    - تحلیل هوشمند داده‌ها
    - داشبوردهای تعاملی
    - گزارش‌گیری پیشرفته
    """)
    
    # Simple footer
    st.markdown("---")
    st.caption("نسخه Demo - در حال توسعه")


if __name__ == "__main__":
    main()
