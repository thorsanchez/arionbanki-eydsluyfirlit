import pandas as pd
import json
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

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

def flokka_med_gemini(faerslu_listi):
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
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type='application/json',
                temperature=0.3
            )
        )
        
        categories = json.loads(response.text)
        return categories
        
    except Exception as e:
        print(f"villa i api request: {e}")
        return []


df = lesa_gogn()
#print(df.head)
#df = hreinsa_gogn(df)
#print(df.head())
#print(utgjold_yfirlit(df))
#print(top5_utgjold(df))
#print(top_vidtakendur(df,10))
print(flokka_med_gemini(df))