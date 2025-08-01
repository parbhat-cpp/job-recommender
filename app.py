from fastapi import FastAPI,Request, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import numpy as np

from src.components.prediction import Prediction
from src.logger import logging

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class TextBasedPrediction(BaseModel):
    text: str

@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse(request, 'index.html')

@app.post('/predict-from-pdf')
async def predict_from_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        prediction = Prediction()
        
        reader = PdfReader(file.file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        text = text.strip()
        
        if text == "":
            raise HTTPException(status_code=422, detail="Unable to process PDF")
        
        output_df = prediction.predict(text)
        output_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        output_df.fillna(-1, inplace=True)
        response = output_df.to_dict(orient='records')
        
        return JSONResponse(
            status_code=200,
            content=response
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Failed to process PDF file")
    finally:
        file.file.close()

@app.post('/predict-from-text')
async def predict_from_text(req_body: TextBasedPrediction):
    if req_body.text == "":
        raise HTTPException(status_code=400, detail="Please provide some text to predict")
    
    try:
        prediction = Prediction()
        
        text = req_body.text
        
        output_df = prediction.predict(text)
        output_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        output_df.fillna(-1, inplace=True)
        response = output_df.to_dict(orient='records')
        
        return JSONResponse(
            status_code=200,
            content=response
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Cannot predict job recommendation")
