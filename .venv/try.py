import pandas as pd
suppliers_scores = pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\scores.xlsx', header=0)
supplier_id=suppliers_scores['Supplier ID']
print(supplier_id)