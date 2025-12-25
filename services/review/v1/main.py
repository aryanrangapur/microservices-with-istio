from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import random  # For mock dates

app = FastAPI(title="Review Service v1")

# Mock data: Reviews per product
reviews_data = {
    "prod-123": {
        "averageRating": 4.2,
        "reviews": [
            {"id": "rev-1", "user": "Alice", "text": "Good product!", "rating": 4, "date": "2025-01-15"},
            {"id": "rev-2", "user": "Bob", "text": "Worth the price", "rating": 5, "date": "2025-01-10"},
            {"id": "rev-3", "user": "Charlie", "text": "Decent, but battery life short", "rating": 3, "date": "2025-01-05"}
        ]
    },
    "prod-456": {
        "averageRating": 3.8,
        "reviews": [
            {"id": "rev-4", "user": "Dana", "text": "Love the features!", "rating": 5, "date": "2025-01-20"},
            {"id": "rev-5", "user": "Eve", "text": "Screen is too small", "rating": 2, "date": "2025-01-18"}
        ]
    }
}

class Review(BaseModel):
    id: str
    user: str
    text: str
    rating: int
    date: str

class ReviewsResponse(BaseModel):
    averageRating: float
    reviews: List[Review]

@app.get("/api/v1/reviews/{productId}", response_model=ReviewsResponse)
async def get_reviews(productId: str, limit: int = 5, sort: str = "recent"):
    if productId not in reviews_data:
        raise HTTPException(status_code=404, detail="No reviews for this product")
    
    data = reviews_data[productId]
    # Simple sort: recent first (mock dates are strings, but we can reverse for demo)
    sorted_reviews = sorted(data["reviews"], key=lambda r: r["date"], reverse=True)[:limit]
    
    return {
        "averageRating": data["averageRating"],
        "reviews": sorted_reviews
    }

@app.post("/api/v1/reviews/{productId}")
async def add_review(productId: str, review: Review):  # For future; ignores input for mock
    if productId not in reviews_data:
        raise HTTPException(status_code=404, detail="Product not found")
    # Mock add: Just return success
    new_id = f"rev-{random.randint(1000, 9999)}"
    new_date = datetime.now().strftime("%Y-%m-%d")
    return {"id": new_id, "message": "Review added!", "date": new_date}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
