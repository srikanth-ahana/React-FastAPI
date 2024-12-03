from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List
import uvicorn

class Fruit(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
memory_db: dict[str, List[Fruit]] = {"fruits": []}

# Fetch all fruits
@app.get("/fruits", response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory_db["fruits"])

# Fetch a single fruit by ID
@app.get("/fruits/{id}", response_model=Fruit)
def get_fruit(id: str):
    for fruit in memory_db["fruits"]:
        if fruit.id == id:
            return fruit
    raise HTTPException(status_code=404, detail="Fruit not found")

# Add a fruit
@app.post("/fruits", response_model=Fruit)
def add_fruit(fruit: Fruit):
    memory_db["fruits"].append(fruit)
    return fruit

# Delete a fruit by ID
@app.delete("/fruits/{fruit_id}", response_model=dict)
def delete_fruit(fruit_id: str):
    for index, fruit in enumerate(memory_db["fruits"]):
        if fruit.id == fruit_id:
            del memory_db["fruits"][index]
            return {"detail": "Fruit deleted successfully"}
    raise HTTPException(status_code=404, detail="Fruit not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
