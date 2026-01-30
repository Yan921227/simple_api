from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("data.db", check_same_thread=False)  
cursor = conn.cursor()

# 建立資料表 id INTEGER PRIMARY KEY AUTOINCREMENT 
# id 是整數 PRIMARY KEY 代表它是「每一筆資料的唯一身份證」
# AUTOINCREMENT 代表「新增一筆就自動 +1」（你不用自己算 id）
#name TEXT NOT NULL 代表 name 是文字，且 NOT NULL 代表「這個欄位不能是空的」
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")
conn.commit()

items = []

# 用來描述「前端會送來什麼資料」 前端會送一個叫 name 的文字過來
class ItemCreate(BaseModel):
    name: str


@app.get("/")
def root():
    return {"message": "Hello, Simple API"}


@app.post("/items")
def create_item(item: ItemCreate):
    # 我要新增一筆資料到 items 表，這筆資料的 name 是某個值 
    # ? 是「佔位符」
    cursor.execute(
        "INSERT INTO items (name) VALUES (?)",
        (item.name,)
    )
    #我真的確定要寫進硬碟，請保存這個動作
    conn.commit()

    return {"name": item.name}

    
@app.get("/items")
def list_items():
    #從 items 表拿出每一筆的 id 和 name。
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()

    return [
        {"id": row[0], "name": row[1]}
        for row in rows
    ]
