import pandas as pd
df_doc = (pd.read_csv(
    r'C:\Users\1\Dev\UI_lab\func\data\creat_pass_doc\2021-07-02-Yar_Allele Table_COrDIS Cattle.txt', 
    sep='\t', decimal=',', encoding='utf-8'))
print(df_doc.head())