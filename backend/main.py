import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ Falta GEMINI_API_KEY en .env")

client = genai.Client(api_key=api_key)

if not firebase_admin._apps:
    cred_path = "serviceAccountKey.json"
    
    if os.path.exists("/etc/secrets/serviceAccountKey.json"):
        cred_path = "/etc/secrets/serviceAccountKey.json"

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

class PromptRequest(BaseModel):
    mensaje: str

@app.post("/test-gemini")
def test_stack(request: PromptRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=request.mensaje
        )
        
        ai_text = response.text

        doc_ref = db.collection('test_logs').add({
            'prompt': request.mensaje,
            'response': ai_text,
            'model': 'gemini-3-flash-preview',
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return {
            "exito": True,
            "gemini_dijo": ai_text,
            "firestore_id": doc_ref[1].id
        }

    except Exception as e:
        print(f"❌ Error Backend: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)