from .xlsxdata.load import lesa_gogn
from .xlsxdata.hreinsa import hreinsa_gogn
from .analysis.utgjold import utgjold_yfirlit, top5_utgjold, top_vidtakendur, manadar_utgjold
from .gemma.flokka import flokka_med_gemma
from .gemma.chat import chat_med_gemma

df = lesa_gogn()
#print(df.head)
df = hreinsa_gogn(df)
#print(df.head())
#print(utgjold_yfirlit(df))
#print(top5_utgjold(df))
#print(top_vidtakendur(df,10))
#print(flokka_med_gemma(df))
#print("\n Útgjöld eftir mánuðum:")
print(manadar_utgjold(df))
#print(chat_med_gemma(df,"Hversu mikið eyddi ég í desember?"))