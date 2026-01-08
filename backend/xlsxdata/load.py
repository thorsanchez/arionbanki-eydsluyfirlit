import pandas as pd
from pathlib import Path

def lesa_gogn():
    data_path = Path(__file__).parent.parent.parent / 'data' / 'arionbanki.xlsx'
    df = pd.read_excel(data_path, header=3) # skipa fyrstu 3 raðir
    return df
