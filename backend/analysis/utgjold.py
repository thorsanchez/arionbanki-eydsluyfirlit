import pandas as pd

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

def manadar_utgjold(df):
    utgjold = df[df['Amount'] < 0].copy()
    #bæta við mánuður col
    utgjold['Mánuður'] = utgjold['Date'].dt.to_period('M')
    #flokka eftir mánuði
    manadarlega = utgjold.groupby('Mánuður')['Amount'].sum().reset_index()
    #format
    manadarlega['Mánuður'] = manadarlega['Mánuður'].astype(str)
    manadarlega['Amount'] = manadarlega['Amount'].round(0)
    return manadarlega