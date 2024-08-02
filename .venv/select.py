import pandas as pd

# 读取scores.xlsx中的数据
scores_df = pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\scores.xlsx')
# 读取1.xlsx中的数据
suppliers_df = pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\1.xlsx',sheet_name='order')

# 提取感兴趣的研究对象的供货商ID
interested_supplier_ids = scores_df['Supplier ID'].unique()
# 去掉1.xlsx中供货商ID的前缀'S'
suppliers_df['供应商ID'] = suppliers_df['供应商ID'].str.replace('S', '').astype(int)
print(suppliers_df['供应商ID'])
# 从1.xlsx中提取这些供货商的原始数据
order = suppliers_df[suppliers_df['供应商ID'].isin(interested_supplier_ids)]

# 将结果保存到新的Excel文件中
order.to_excel(r'D:\mypython\math_modeling\21_C\data\order_choice.xlsx', index=False)
