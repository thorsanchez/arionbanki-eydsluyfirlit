import json
import requests
from ..utils.config import GEMMA_HOST

def flokka_med_gemma(df):
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

    prompt = f"""You are a transaction categorizer. Categorize these Icelandic transactions.

        Categories:
        - Matur: BONUS, KRONAN, HAGKAUP, restaurants, cafes, KFC
        - Húsnæði: rent, utilities, housing
        - Samgöngur: N1, OLÍS, STRÆTÓ, gas, transport
        - Afþreying: BÍÓ, NETFLIX, SPOTIFY, games, entertainment
        - Fatnaður: clothes, shoes
        - Heilsa: pharmacy, doctors
        - Reikningar: SÍMINN, VODAFONE, NOVA, phone, internet, insurance
        - Millifærslur: Icelandic names (transfers to people)
        - Netverslun: PAYPAL, and other online fintech solutions
        - Annað: everything else including PAYPAL, unknown items

        Transactions:
        {transaction_text}

        RULES:
        1. Keep "explanation" field EXACTLY as shown - DO NOT add commentary
        2. Only output valid JSON array
        3. No markdown, no extra text

        Output format:
        [
        {{"explanation": "Austurver", "category": "Matur", "confidence": 0.95}},
        {{"explanation": "PAYPAL", "category": "Netverslun", "confidence": 0.7}},
        {{"explanation": "Guðmundur", "category": "Millifærslur", "confidence": 0.9}}
        ]"""

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
            timeout=700
        )

        response.raise_for_status()

        result = response.json()
        categories = json.loads(result["response"])
        return categories.get("results", categories) if isinstance(categories, dict) else categories

    except Exception as e:
        print(f"error í gemma api kall: {e}")
        return []
