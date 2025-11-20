import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Digital Products API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/products")
def list_products():
    """Return a basic catalog of digital products (static for demo)."""
    return {
        "items": [
            {
                "id": "preset-pack-1",
                "title": "Cinematic LUT Pack",
                "description": "20 handcrafted LUTs for filmic color grading.",
                "price": 19.0,
                "image": "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?w=1200&q=80&auto=format&fit=crop"
            },
            {
                "id": "font-bundle-1",
                "title": "Modern Font Bundle",
                "description": "8 sleek sans-serif fonts for brands & UI.",
                "price": 24.0,
                "image": "https://images.unsplash.com/photo-1554933753-49365efbcf56?w=1200&q=80&auto=format&fit=crop"
            },
            {
                "id": "ui-kit-1",
                "title": "Neo UI Kit",
                "description": "200+ responsive components for Figma.",
                "price": 29.0,
                "image": "https://images.unsplash.com/photo-1559028012-481c04fa702d?w=1200&q=80&auto=format&fit=crop"
            },
            {
                "id": "sfx-pack-1",
                "title": "SFX Starter Pack",
                "description": "120 whooshes, hits, and risers in WAV.",
                "price": 15.0,
                "image": "https://images.unsplash.com/photo-1510915228340-29c85a43dcfe?w=1200&q=80&auto=format&fit=crop"
            }
        ]
    }

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
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
