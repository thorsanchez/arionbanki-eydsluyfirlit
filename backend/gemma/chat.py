import requests
from ..utils.config import GEMMA_HOST
from ..analysis.utgjold import utgjold_yfirlit, top5_utgjold, manadar_utgjold

def chat_med_gemma(df, user_question: str):
    """
    senda hvaða spurningu a gemma
    """
    # sækja data summary
    total_expenses = utgjold_yfirlit(df)
    top_expenses = top5_utgjold(df).to_dict('records')
    monthly_expenses = manadar_utgjold(df).to_dict('records')

    prompt = f"""Þú ert fjármálaráðgjafi sem greinir bankaviðskipti á íslensku.

    Notandi hefur hlaðið upp bankagögnum sínum. Hér er samantekt:
    - Heildarútgjöld: {total_expenses:.0f} kr
    - Stærstu útgjöldin: {top_expenses}
    - Útgjöld eftir mánuðum: {monthly_expenses}

    Spurning notanda: {user_question}

    Svaraðu stuttlega og skýrt á íslensku út frá gögnunum. Notaðu NÁKVÆMLEGA þær tölur sem eru í gögnunum hér fyrir ofan.
    """

    # DEBUG: Prenta prompt til að sjá hvað var sent
    print("\n" + "=" * 80)
    print("DEBUG - Data sent to Gemma:")
    print("=" * 80)
    print(f"Total expenses: {total_expenses:.0f} kr")
    print(f"\nTop 5 expenses:")
    for exp in top_expenses:
        print(f"  {exp}")
    print(f"\nMonthly expenses:")
    for month in monthly_expenses:
        print(f"  {month}")
    print("=" * 80 + "\n")

    try:
        response = requests.post(
            f"{GEMMA_HOST}/api/generate",
            json={
                "model": "gemma2:9b",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            },
            #timeout 30 sec var alltof stutt...
            timeout=200
        )
        
        result = response.json()
        return result["response"]
        
    except Exception as e:
        raise Exception(f"Gemma villa: {str(e)}")
