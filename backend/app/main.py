from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, products, cart, try_on
from .database import engine, Base, SessionLocal, init_db

# Create Tables
Base.metadata.create_all(bind=engine)

# Seed Data
db = SessionLocal()
init_db(db)
db.close()

app = FastAPI(
    title="Virtual Wardrobe API",
    description="Backend for Virtual Wardrobe application",
    version="1.0.0"
)

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(try_on.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Virtual Wardrobe API"}
