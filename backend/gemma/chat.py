import requests
from ..utils.config import GEMMA_HOST

def chat_med_gemma(df, user_question: str):
    """
    senda hvaða spurningu a gemma
    """
    
    # geyma dataset
    df_copy = df.copy()

    # bara 2025 spurning inniheldur það
    if '2025' in user_question:
        df_filtered = df_copy[df_copy['Date'].dt.year == 2025].copy()
    else:
        df_filtered = df_copy.copy()

    # hraði test, bara fyrstu 20 línurnar
    df_filtered = df_filtered.head(20)

    # df hefur bara Date, Amount, Explanation (hreinsuð í hreinsa.py)

    df_filtered['Date'] = df_filtered['Date'].dt.strftime('%Y-%m-%d')
    df_filtered['Amount'] = df_filtered['Amount'].round(0).astype(int)
    all_transactions = df_filtered.to_dict('records')

    print(f"hversu margar linur til gemma: {len(df_filtered)}")
    
    
    prompt = f"""Þú ert fjármálaráðgjafi sem greinir bankaviðskipti á íslensku.

    HÉR ERU ALLAR FÆRSLURNAR FRÁ BANKAYFIRLITINU:
    ===========================================

    {all_transactions}

    LEIÐBEININGAR:
    =============
    - Amount sem er neikvæð (< 0) er ÚTGJALD
    - Amount sem er jákvæð (> 0) er TEKJUR
    - Date er dagsetning í sniðinu YYYY-MM-DD
    - Explanation er nafn viðtakanda/greiðanda

    SPURNING FRÁ NOTANDA:
    ======================
    {user_question}

    MIKILVÆGT:
    - Greindu ALLAR færslurnar hér að ofan til að svara spurningunni
    - Ef spurningin er um "10 dýrustu dagana", reiknaðu samtals útgjöld fyrir hvern dag og finna þá 10 dýrustu
    - Ef spurningin er um "hversu oft", teldu færslurnar
    - Ef spurningin er um "daga án útgjalda", teldu alla daga í tímabilinu og dragðu frá daga með útgjöldum
    - Svaraðu NÁKVÆMLEGA út frá þessum gögnum
    - Sýndu útreikninga þína ef það hjálpar
    - Svaraðu á íslensku

    Svaraðu nú!
    """

    try:
        response = requests.post(
            f"{GEMMA_HOST}/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    #latt fyrir calculation
                    "temperature": 0.1,
                    "num_ctx": 8192, 
                    "num_predict": 1000 
                }
            },
            #timeout 30 sec var alltof stutt...
            timeout=None
        )
        
        result = response.json()
        return result["response"]
        
    except Exception as e:
            raise Exception(f"Gemma villa: {str(e)}")

