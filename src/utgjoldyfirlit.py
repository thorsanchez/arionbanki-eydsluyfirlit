import pandas as pd
import json
import os
import requests

# sækja ip
with open('config.json') as f:
    config = json.load(f)
    GEMMA_HOST = config["GEMMA_HOST"]


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

def flokka_med_gemma(faerslu_listi):
    """
    Þar sem "Nafn viðtakanda eða greiðanda" dálkur er messy þá ætlar gemini að categorize-a
    """

    gjold = df[df['Amount'] < 0].copy()
    gjold = gjold.head(5)
    #bua til dictionaries
    faerslu_listi = gjold[['Date', 'Amount', 'Explanation']].to_dict('records')

    transaction_text = "\n".join([
        f"{t['Date']}: {t['Amount']} kr - {t['Explanation']}"
        for t in faerslu_listi
    ])

    prompt = f"""
    Þú ert fjármálasérfræðingur. Flokkaðu þessar færslur í flokka.
    
    Flokkar:
    - Matur: matvörur, veitingastaðir, kaffihús
    - Húsnæði: húsaleiga, veitur, íbúðafélag
    - Samgöngur: bensín, strætó, bílaleiga
    - Afþreying: bíó, netflix, íþróttir
    - Fatnaður: föt, skór
    - Heilsa: apótek, læknar
    - Reikningar: sími, internet, tryggingar
    - Millifærslur: til annarra einstaklinga
    - Annað: allt annað
    
    Færslur:
    {transaction_text}
    
    Svaraðu BARA með JSON:
    [
        {{"explanation": "BONUS FISKISLOD", "category": "Matur", "confidence": 0.95}},
        ...
    ]
    """
    
    try:
        response = requests.post(
            f"{GEMMA_HOST}/api/generate",
            json={
                "model": "gemma2:9b",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.3
                }
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()
        categories = json.loads(result["response"])
        return categories.get("results", categories) if isinstance(categories, dict) else categories

    except Exception as e:
        print(f"error í gemma api kall: {e}")
        return []

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


df = lesa_gogn()
#print(df.head)
#df = hreinsa_gogn(df)
#print(df.head())
#print(utgjold_yfirlit(df))
#print(top5_utgjold(df))
#print(top_vidtakendur(df,10))
print(flokka_med_gemma(df))
#print("\n Útgjöld eftir mánuðum:")
#print(manadar_utgjold(df))