from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from io import BytesIO

from .xlsxdata.hreinsa import hreinsa_gogn
from .analysis.utgjold import (
    utgjold_yfirlit,
    top5_utgjold,
    top_vidtakendur,
    manadar_utgjold,
)
from .gemma.flokka import flokka_med_gemma
from .gemma.chat import chat_med_gemma

app = FastAPI(title="Bankayfirlit API", version="1.0")

# CORS fyrir React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#store-a i memory
current_df: pd.DataFrame | None = None

# Request model fyrir chat
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "API virkt!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global current_df
    if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(400, "aðeins csv eða xlsx skrár leyfðar")
    
    contents = await file.read()
    
    try:
        if file.filename.lower().endswith('.csv'):
            #fyrstu þrjár línur eru ekki með hjá arion
            df = pd.read_csv(BytesIO(contents), header=3) 
        else:
            df = pd.read_excel(BytesIO(contents), header=3)

        #hvaða col erum við að finna
        print(f"dálkar í skrá: {list(df.columns)}")

        df = hreinsa_gogn(df)
        current_df = df

        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns)
        }
    except ValueError as e:
        #Villa frá hreinsa gogn um missing columns
        raise HTTPException(400, str(e))
    except Exception as e:
        #almennar villur við lestur skráar
        raise HTTPException(500, f"error við lestur skráar: {str(e)}")

@app.get("/analysis/utgjold-yfirlit")
def get_utgjold_yfirlit():
    if current_df is None:
        raise HTTPException(status_code=400, detail="engin skrá hefur verið hlaðið upp")
    
    total = utgjold_yfirlit(current_df)
    return {
        "total_utgjold": float(total),
        "formatted": f"{total:,.0f} kr."
    }

@app.get("/analysis/top5-utgjold")
def get_top5_utgjold():
      if current_df is None:
          raise HTTPException(400, "engin skrá hefur verið hlaðið upp")

      top5 = top5_utgjold(current_df)
      # Breyta NaN gildi með egin (bakendi alltaf að crasha i þetta endpoint)
      top5 = top5.fillna('')
      return top5.to_dict('records')

@app.get("/analysis/top-vidtakendur")
def get_top_vidtakendur():
    if current_df is None:
        raise HTTPException(400, "engin skrá hefur verið hlaðið upp")

    top = top_vidtakendur(current_df, 5)
    top = top.fillna('')
    return top.to_dict('records')

@app.get("/analysis/manadar-utgjold")
def get_manadar_utgjold():
    if current_df is None:
        raise HTTPException(400, "engin skrá hefur verið hlaðið upp")

    manadar = manadar_utgjold(current_df)
    manadar = manadar.fillna('')
    return manadar.to_dict('records')

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    svarar spurningum um bankagögnin með Gemma
    """
    if current_df is None:
        raise HTTPException(400, "engin skrá hefur verið hlaðið upp")

    try:
        answer = chat_med_gemma(current_df, request.question)
        return {
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(500, f"Villa í chat: {str(e)}")
    


