import numpy as np
import pandas as pd

class Supplier:
    def __init__(self, id, avg, risk, comp_rate, ordera_rate):
        self.id = id
        self.avg = avg
        self.risk = risk
        self.comp_rate = comp_rate
        self.ordera_rate = ordera_rate

    def get_data(self):
        return [self.avg, self.risk, self.comp_rate, self.ordera_rate]

# 读取Excel文件中的order和supply表
order_df = pd.read_excel(r'd:\mypython\math_modeling\21_C\.venv\1.xlsx', sheet_name='order', header=0)
supply_df = pd.read_excel(r'd:\mypython\math_modeling\21_C\.venv\1.xlsx', sheet_name='supply', header=0)

# 计算comp_rate和order_rate
comp_rate = supply_df['sum_s'] / order_df['sum_o']

# 计算order_rate
order_rate = []
for index, row in supply_df.iterrows():
    count = sum(cell > 10 for cell in row[2:])
    order_rate.append(count / 240)

# 创建一个字典来存储 Supplier 实例
suppliers_dict = {}

for i, (avg, risk, comp_rate_val, order_rate_val) in enumerate(zip(supply_df['avg'], supply_df['risk'], comp_rate, order_rate)):
    supplier = Supplier(id=i + 1, avg=avg, risk=risk, comp_rate=comp_rate_val, ordera_rate=order_rate_val)
    suppliers_dict[supplier.id] = supplier

# 获取所有供应商的数据
data = np.array([supplier.get_data() for supplier in suppliers_dict.values()])

# 使用区间法进行适度指标的正向化和标准化
def normalize_with_interval(matrix):
    normalized_matrix = np.zeros_like(matrix, dtype=float)
    a = np.min(matrix[:, 2])
    b = np.max(matrix[:, 2])
    range_val = max(0.8 - a, b - 1.2)
    
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if j == 1:  # risk 是负向指标
                normalized_matrix[i, j] = 1 - (matrix[i, j] - np.min(matrix[:, j])) / (np.max(matrix[:, j]) - np.min(matrix[:, j]))
            elif j == 2:  # comp_rate 是适度指标
                if matrix[i, j] < 0.8:
                    normalized_matrix[i, j] = 1 - (0.8 - matrix[i, j]) / range_val
                elif matrix[i, j] >= 0.8 and matrix[i, j] <= 1.2:
                    normalized_matrix[i, j] = 1
                else:
                    normalized_matrix[i, j] = 1 - (matrix[i, j] - 1.2) / range_val
            else:  # avg 和 order_rate 是正向指标
                normalized_matrix[i, j] = (matrix[i, j] - np.min(matrix[:, j])) / (np.max(matrix[:, j]) - np.min(matrix[:, j]))
    return normalized_matrix

normalized_data = normalize_with_interval(data)

# 计算正理想解和负理想解
positive_ideal = np.max(normalized_data, axis=0)
negative_ideal = np.min(normalized_data, axis=0)

# 计算每个供应商到正理想解和负理想解的距离
def distances(matrix, positive_ideal, negative_ideal):
    positive_distances = np.sqrt(np.sum((matrix - positive_ideal) ** 2, axis=1))
    negative_distances = np.sqrt(np.sum((matrix - negative_ideal) ** 2, axis=1))
    return positive_distances, negative_distances

positive_distances, negative_distances = distances(normalized_data, positive_ideal, negative_ideal)

# 计算相对接近度
relative_closeness = negative_distances / (positive_distances + negative_distances)

# 排序并输出结果
sorted_indices = np.argsort(relative_closeness)[::-1]
rank_data = []
for rank, index in enumerate(sorted_indices[:50],1):
    supplier_id = list(suppliers_dict.keys())[index]
    rank_data.append([rank, supplier_id, relative_closeness[index]])

# 将结果输出到Excel表格
rank_df = pd.DataFrame(rank_data, columns=['Rank', 'Supplier ID', 'Relative Closeness'])
rank_df.to_excel('Q1_answer_rank.xlsx', index=False)
