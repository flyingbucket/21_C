import pandas as pd

# Reading the excel file
forwarder_df=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\2.xlsx')
forwarder_df['转运商ID']=forwarder_df['转运商ID'].str.replace('T','').astype(int)
#initializing result
result=pd.DataFrame(columns=['转运商ID','周数','损耗率'])
for index,row in forwarder_df.iterrows():
    forwarder_id=row['转运商ID']
    lose_rate=row[2:242].values
    for i in range(10):
        st=i*24
        ed=st+24
        week_data=row[st:ed]
        for j,data in enumerate(week_data):
            new_row=pd.DataFrame({
               '转运商ID':[forwarder_id],
               '周数':[j+1],
               '损耗率':[data] 
            })
            result=pd.concat([result,new_row],ignore_index=True)
result['损耗率']=pd.to_numeric(result['损耗率'],errors='coerce')
avg_lose_rate=result.groupby(['转运商ID','周数'])['损耗率'].mean().reset_index()
# 重新排列数据，使每行代表一个转运商，第二到第25列表示第1到24周对应转运商的损耗率
final_result = avg_lose_rate.pivot(index='转运商ID', columns='周数', values='损耗率')

# 重置索引并将转运商ID作为列
final_result = final_result.reset_index()

# 添加表头
final_result.columns = ['转运商ID'] + [f'第{i}周' for i in range(1, 25)]

# 保存结果到Excel文件
final_result.to_excel('forwarder_expectation.xlsx', index=False)

print('well done! Check the forwarder_expectation.xlsx file for the result.')




