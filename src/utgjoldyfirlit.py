import pandas as pd

def lesa_gogn():
    df = pd.read_excel('data/arionbanki.xlsx', header=2) #skipa fyrstu 2 raðir
    df = df.dropna(how='all') #eyða auðar línar
    return df

df = lesa_gogn()
print(df)