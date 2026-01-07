from data.load import lesa_gogn
from data.hreinsa import hreinsa_gogn
from analysis.utgjold import utgjold_yfirlit, top5_utgjold, top_vidtakendur, manadar_utgjold
from ai.flokka import flokka_med_gemma

df = lesa_gogn()
#print(df.head)
df = hreinsa_gogn(df)
#print(df.head())
#print(utgjold_yfirlit(df))
#print(top5_utgjold(df))
#print(top_vidtakendur(df,10))
print(flokka_med_gemma(df))
#print("\n Útgjöld eftir mánuðum:")
#print(manadar_utgjold(df))