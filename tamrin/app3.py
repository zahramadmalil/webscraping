import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.title("📱 موبایل‌های تکنولایف")

conn = sqlite3.connect("MobileData.db")
df = pd.read_sql("select * from mobile_techno", conn)

st.write(f"تعداد محصولات: {len(df)}")

cols = st.columns(4)
for i, row in df.iterrows():
    with cols[i % 4]:
        st.image(row["image_url"])
        st.markdown(f"**{row['description']}**")
        st.write(f"برند: {row['brand']}")
        st.write(f"حافظه داخلی: {row['storage']}")
        st.write(f"RAM: {row['ram']}")
        st.write(f"رنگ: {row['color']}")
        st.write(f"⭐ امتیاز: {row['rating']}")
        st.link_button("مشاهده محصول", row["link"])
        st.divider()