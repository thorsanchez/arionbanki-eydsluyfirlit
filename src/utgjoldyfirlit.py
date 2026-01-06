import pandas as pd

def lesa_gogn():
    df = pd.read_excel('data/arionbanki.xlsx', header=3) #skipa fyrstu 2 raðir
    #df = df.dropna(how='all') #eyða auðar línar (virkar ekki?)
    return df

def hreinsa_gogn(df):
    #breyta date texta i datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    #amount yfir i number
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce') #ef villa breyta yfir í nan
    #bætti við nokkrar færslur sem eru ekki í rettri röð
    df = df.sort_values('Date', ascending=False) #raða frá hæsa til lægsta
    #nýtt row numer eftir sort
    df = df.reset_index(drop=True)
    return df

def utgjold_yfirlit(df):
    """
    Sýna yfirlit yfir útgjöld.
    Skilar eina tölu, heildar utgjöld 
    """
    #velja bara utfærslur (neikkvæðar tölur) og sum af öllum
    utgjold = df[df['Amount']<0]['Amount'].sum()
    return utgjold

def top5_utgjold(df):
    utgjold_raðir = df[df['Amount']<0]
    top5 = utgjold_raðir.nsmallest(5, 'Amount') #stærstu neikvæðu tölu
    return top5


df = lesa_gogn()
#print(df.head)
#df = hreinsa_gogn(df)
#print(df.head())
#print(utgjold_yfirlit(df))
print(top5_utgjold(df))