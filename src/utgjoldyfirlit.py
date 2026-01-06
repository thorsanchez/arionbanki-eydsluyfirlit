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

def top_vidtakendur(df,n):
    utgjold_radir = df[df['Amount'] < 0].copy()
    #öll rows með sama explanation í saman og viljum bara amount col
    grouped = utgjold_radir.groupby('Explanation')['Amount'].sum().reset_index()
    topN = grouped.nsmallest(n, 'Amount')
    fjarslur_per_vidtakandi = utgjold_radir['Explanation'].value_counts()
    topN['Fjöldi færslna'] = topN['Explanation'].map(fjarslur_per_vidtakandi)

    return topN

df = lesa_gogn()
#print(df.head)
#df = hreinsa_gogn(df)
#print(df.head())
#print(utgjold_yfirlit(df))
#print(top5_utgjold(df))
print(top_vidtakendur(df,10))