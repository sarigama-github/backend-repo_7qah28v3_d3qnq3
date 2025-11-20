import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from bson import ObjectId

from database import db, create_document, get_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Utility ----------

def serialize_doc(doc):
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    # Convert datetime to isoformat if present
    for k, v in list(d.items()):
        try:
            from datetime import datetime
            if isinstance(v, datetime):
                d[k] = v.isoformat()
        except Exception:
            pass
    return d


# ---------- Models (request bodies) ----------

class ReservationIn(BaseModel):
    name: str
    email: Optional[str] = None
    phone: str
    date: str
    time: str
    guests: int = Field(..., ge=1, le=20)
    notes: Optional[str] = None

class ContactMessageIn(BaseModel):
    name: str
    email: str
    message: str


# ---------- Base routes ----------

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


# ---------- Restaurant API ----------

@app.get("/api/menu")
def get_menu():
    """Return menu items; if empty, seed with a small sample for demo."""
    try:
        items = get_documents("menuitem")
        if len(items) == 0:
            sample = [
                {"name": "Margherita Pizza", "description": "San Marzano tomatoes, fresh mozzarella, basil", "price": 12.0, "category": "Mains", "is_vegetarian": True, "is_spicy": False},
                {"name": "Spicy Arrabbiata Pasta", "description": "Penne tossed in a spicy tomato-garlic sauce", "price": 14.0, "category": "Mains", "is_vegetarian": True, "is_spicy": True},
                {"name": "Caesar Salad", "description": "Romaine, parmesan, croutons, classic dressing", "price": 9.5, "category": "Starters", "is_vegetarian": False, "is_spicy": False},
                {"name": "Tiramisu", "description": "Espresso-soaked ladyfingers, mascarpone cream", "price": 8.0, "category": "Desserts", "is_vegetarian": True, "is_spicy": False},
                {"name": "Lemonade", "description": "Fresh squeezed with mint", "price": 4.0, "category": "Drinks", "is_vegetarian": True, "is_spicy": False},
            ]
            for it in sample:
                create_document("menuitem", it)
            items = get_documents("menuitem")
        return [serialize_doc(i) for i in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reservations")
def create_reservation(res: ReservationIn):
    try:
        inserted_id = create_document("reservation", res.model_dump())
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def create_contact(msg: ContactMessageIn):
    try:
        inserted_id = create_document("contactmessage", msg.model_dump())
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Diagnostics ----------

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
