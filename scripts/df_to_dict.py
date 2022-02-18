import pandas as pd
df = pd.DataFrame({'col1': [1, 2],

                   'col2': [0.5, 0.75]},

                  index=['row1', 'row2'])
print(df)
print(df.T.to_dict().get("row1"))
