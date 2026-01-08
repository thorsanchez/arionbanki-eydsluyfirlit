import pandas as pd

def hreinsa_gogn(df):
    # halda bara i dalkana sem við þurfum
    columns_to_keep = ['Date', 'Amount', 'Explanation']
    df = df[columns_to_keep].copy()

    # breyta date texta i datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    # amount yfir i number
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce') # ef villa breyta yfir í nan
    # bætti við nokkrar færslur sem eru ekki í rettri röð
    df = df.sort_values('Date', ascending=False) # raða frá hæsta til lægsta
    # nýtt row numer eftir sort
    df = df.reset_index(drop=True)
    return df
