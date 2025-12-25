from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import random  # For initial mock stock

app = FastAPI(title="Inventory Service")

# Mock data: {productId: qty}
inventory = {
    "prod-123": random.randint(10, 20),  # e.g., 15
    "prod-456": random.randint(5, 15)    # e.g., 8
}
reservations: Dict[str, Dict[str, Any]] = {}  # {resId: {"productId": str, "qty": int}}

class InventoryResponse(BaseModel):
    productId: str
    quantity: int
    available: bool
    lowStockThreshold: int = 5

class ReserveRequest(BaseModel):
    productId: str
    quantity: int

class CommitRequest(BaseModel):
    reservationId: str
    commit: bool  # True=commit (deduct), False=cancel

@app.get("/api/v1/inventory/{productId}", response_model=InventoryResponse)
async def get_inventory(productId: str):
    if productId not in inventory:
        raise HTTPException(status_code=404, detail="Product not in inventory")
    qty = inventory[productId]
    return {
        "productId": productId,
        "quantity": qty,
        "available": qty > 0
    }

@app.post("/api/v1/inventory/reserve")
async def reserve_stock(req: ReserveRequest):
    if req.productId not in inventory or inventory[req.productId] < req.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    res_id = f"res-{random.randint(1000, 9999)}"
    reservations[res_id] = {"productId": req.productId, "qty": req.quantity}
    # Temp deduct (optimistic)
    inventory[req.productId] -= req.quantity
    return {"reservationId": res_id, "success": True}

@app.post("/api/v1/inventory/commit")
async def commit_reservation(req: CommitRequest):
    if req.reservationId not in reservations:
        raise HTTPException(status_code=404, detail="Reservation not found")
    res = reservations.pop(req.reservationId)
    if not req.commit:
        # Rollback: Add back qty
        inventory[res["productId"]] += res["qty"]
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
