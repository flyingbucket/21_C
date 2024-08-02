import pandas as pd

# 读取数据
scores_df = pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\scores.xlsx')
suppliers_df = pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\1.xlsx',sheet_name='supply')

# 提取高分的研究对象的供货商ID
filtered_supplier_ids = scores_df['Supplier ID'].unique()
# 去掉1.xlsx中供货商ID的前缀'S'
suppliers_df['供应商ID'] = suppliers_df['供应商ID'].str.replace('S', '').astype(int)
# 从1.xlsx中提取这些供货商的原始数据
filtered_data = suppliers_df[suppliers_df['供应商ID'].isin(filtered_supplier_ids)]

# filtered_data.to_excel('filtered_data.xlsx', index=False)
# print('done')

# 初始化结果DataFrame
results = pd.DataFrame(columns=['供应商ID', '材料分类', '周数', '供货量'])

# 对每个供应商的数据进行分析
for index, row in filtered_data.iterrows():
    supplier_id = row['供应商ID']
    material_category = row['材料分类']  # 假设材料类别在'材料类别'列中
    weekly_data = row[3:243].values  # 提取每周的供货量数据
    
    # 按24周为一个周期进行分割
    for period in range(10):  # 240周 / 24周 = 10个周期
        start_idx = period * 24
        end_idx = start_idx + 24
        period_data = weekly_data[start_idx:end_idx]
        
        # 将每个周期的数据添加到结果DataFrame中
        for week, supply in enumerate(period_data):
            results = results._append({
                '供应商ID': supplier_id,
                '材料分类': material_category,
                '周数': week + 1,
                '供货量': supply
            }, ignore_index=True)

# 计算每个供应商在每个周期内每周供货量的平均值
average_results = results.groupby(['供应商ID', '材料分类', '周数'])['供货量'].mean().reset_index()

# 确保输出的表格有51行26列（包括材料类别）
# 假设有50个供应商，每个供应商有24周的数据
expected_results = average_results.pivot(index=['供应商ID', '材料分类'], columns='周数', values='供货量')

# 重置索引并将供应商ID和材料类别作为列
expected_results = expected_results.reset_index()

# 添加表头
expected_results.columns = ['供应商ID', '材料分类'] + [f'第{i}周' for i in range(1, 25)]

# 保存结果到Excel文件
expected_results.to_excel('supply_expectation.xlsx', index=False)

print("well done! check file:'supply_expectation.xlsx'")
