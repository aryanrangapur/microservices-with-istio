from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Product Service")

# Mock data
products = {
    "prod-123": {
        "id": "prod-123",
        "name": "Wireless Headphones",
        "price": 99.99,
        "description": "Noise-cancelling bliss",
        "imageUrl": "https://example.com/headphones.jpg"
    },
    "prod-456": {
        "id": "prod-456",
        "name": "Smart Watch",
        "price": 199.99,
        "description": "Track your life",
        "imageUrl": "https://example.com/watch.jpg"
    }
}

class Product(BaseModel):
    id: str
    name: str
    price: float
    description: str
    imageUrl: str

@app.get("/api/v1/products/{id}", response_model=Product)
async def get_product(id: str):
    if id not in products:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return products[id]

@app.get("/api/v1/products", response_model=List[Product])
async def list_products(limit: int = 10, offset: int = 0):
    all_prods = list(products.values())[offset:offset + limit]
    return all_prods

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
