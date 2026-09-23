import streamlit as st
import pandas as pd

st.title("📊 财务流水批量汇总工具")
st.write("支持一次上传多个 Excel 文件，自动合并并汇总金额！")

# 关键升级1：允许上传多个文件（accept_multiple_files=True）
uploaded_files = st.file_uploader("请选择 Excel 文件（可多选）", type=["xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    all_dfs = [] # 用来装所有读取进来的表格
    
    # 关键升级2：循环读取每一个上传的文件
    for file in uploaded_files:
        df_temp = pd.read_excel(file)
        # 在表格里加一列“来源文件”，方便以后核对数据是哪个表来的
        df_temp['来源文件'] = file.name
        all_dfs.append(df_temp)
    
    # 关键升级3：把所有表格拼在一起
    df = pd.concat(all_dfs, ignore_index=True)
    
    # 去掉全空的行
    df = df.dropna(how='all')
    
    # 智能识别列名（兼容各种奇葩表头）
    possible_cat_cols = ['分类', '类别', '科目', '费用类型', '类型', '用途']
    possible_amt_cols = ['金额', '发生额', '报销金额', '金额(元)', '金额（元）', '费用']
    
    cat_col = None
    amt_col = None
    
    for col in df.columns:
        col_str = str(col).strip()
        if any(keyword in col_str for keyword in possible_cat_cols):
            cat_col = col
        if any(keyword in col_str for keyword in possible_amt_cols):
            amt_col = col

    st.subheader("1. 合并后的原始数据预览")
    st.dataframe(df.head(100)) # 只展示前100行，防止网页卡死
    
    # 判断是否找到了对应列
    if cat_col and amt_col:
        # 强制将金额列转为数字，处理文本格式的金额
        df[amt_col] = pd.to_numeric(df[amt_col], errors='coerce').fillna(0)
        
        # 按分类汇总
        summary = df.groupby(cat_col)[amt_col].sum().reset_index()
        summary.columns = ['分类', '汇总金额']
        
        st.subheader("2. 自动汇总结果")
        st.dataframe(summary)
        
        # 提供下载
        csv = summary.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 点击下载汇总结果", csv, "汇总结果.csv", "text/csv")
        
    else:
        st.error(f"⚠️ 智能识别失败！当前表格的列名是：{list(df.columns)}。请确保表格里含有'分类/类别/科目'和'金额/发生额'等字眼。")