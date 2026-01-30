from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items = []

# 用來描述「前端會送來什麼資料」 前端會送一個叫 name 的文字過來
class ItemCreate(BaseModel):
    name: str


@app.get("/")
def root():
    return {"message": "Hello, Simple API"}


@app.post("/items")
def create_item(item: ItemCreate):
    new_item = {
        "id": len(items) + 1,
        "name": item.name
        }  
    items.append(new_item)   # ✅ 把資料存進清單

    return new_item
    
@app.get("/items")
def list_items():
    return items