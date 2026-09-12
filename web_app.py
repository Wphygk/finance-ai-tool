import streamlit as st
import pandas as pd

# 网页的大标题
st.title("📊 财务流水自动汇总工具")
st.write("上传 Excel 表格，自动帮你分类汇总金额！")

# 让用户上传文件
uploaded_file = st.file_uploader("请选择 Excel 文件", type=["xlsx", "xls"])

# 如果用户上传了文件，就执行下面的处理
if uploaded_file is not None:
    # 读取 Excel
    df = pd.read_excel(uploaded_file)
    
    st.subheader("1. 原始数据预览")
    st.dataframe(df) # 在网页上显示表格
    
    # 检查表头是否包含“分类”和“金额”
    if '分类' in df.columns and '金额' in df.columns:
        # 自动汇总
        summary = df.groupby('分类')['金额'].sum().reset_index()
        
        st.subheader("2. 自动汇总结果")
        st.dataframe(summary)
        
        # 提供下载按钮
        csv = summary.to_csv(index=False).encode('utf-8-sig') # 防止中文乱码
        st.download_button(
            label="📥 点击下载汇总结果",
            data=csv,
            file_name='汇总结果.csv',
            mime='text/csv'
        )
    else:
        st.error("⚠️ 表格里找不到'分类'或'金额'列，请检查表头！")