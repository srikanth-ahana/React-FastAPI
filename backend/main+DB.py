from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String
from databases import Database

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/fruitsdb"

# SQLAlchemy setup
Base = declarative_base()

class FruitModel(Base):
    __tablename__ = "fruits"
    id = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String, nullable=False)

# Async engine and session setup
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Database connection for queries
database = Database(DATABASE_URL)

# FastAPI app
app = FastAPI()

# CORS setup
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Fruit(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]

# Events
@app.on_event("startup")
async def startup():
    await database.connect()
    # Create tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Routes
@app.get("/fruits", response_model=Fruits)
async def get_fruits():
    query = "SELECT * FROM fruits"
    rows = await database.fetch_all(query)
    fruits = [Fruit(**row) for row in rows]
    return Fruits(fruits=fruits)

@app.get("/fruits/{fruit_id}", response_model=Fruit)
async def get_fruit(fruit_id: str):
    query = f"SELECT * FROM fruits WHERE id = :id"
    row = await database.fetch_one(query=query, values={"id": fruit_id})
    if not row:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return Fruit(**row)

@app.post("/fruits", response_model=Fruit)
async def add_fruit(fruit: Fruit):
    query = "INSERT INTO fruits (id, name) VALUES (:id, :name)"
    await database.execute(query=query, values={"id": fruit.id, "name": fruit.name})
    return fruit

@app.delete("/fruits/{fruit_id}", response_model=dict)
async def delete_fruit(fruit_id: str):
    query = "DELETE FROM fruits WHERE id = :id"
    result = await database.execute(query=query, values={"id": fruit_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return {"detail": "Fruit deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
