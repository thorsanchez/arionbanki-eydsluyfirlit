import pandas as pd

def lesa_gogn():
    df = pd.read_excel('../data/arionbanki.xlsx', header=3) # skipa fyrstu 3 raðir
    return df
