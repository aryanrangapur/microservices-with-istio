"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
  imageUrl: string;
}

interface Review {
  id: string;
  user: string;
  text: string;
  rating: number;
  date: string;
}

interface Inventory {
  quantity: number;
  available: boolean;
}

interface Reviews {
  averageRating: number;
  reviews: Review[];
}

export default function ProductPage({ params }: { params: { id: string } }) {
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Reviews | null>(null);
  const [inventory, setInventory] = useState<Inventory | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [orderStatus, setOrderStatus] = useState<string>("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const [prodRes, revRes, invRes] = await Promise.all([
          axios.get(`/api/product/${params.id}`),
          axios.get(`/api/review/${params.id}`),
          axios.get(`/api/inventory/${params.id}`),
        ]);

        setProduct(prodRes.data);
        setReviews(revRes.data);
        setInventory(invRes.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to load product");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [params.id]);

  const handleOrder = async () => {
    try {
      const res = await axios.post("/api/order", {
        productId: params.id,
        quantity: 1,
        userId: "demo-user",
      });

      setOrderStatus(`Order placed! ID: ${res.data.orderId}`);
    } catch (err: any) {
      setOrderStatus(
        `Order failed: ${err.response?.data?.detail || "Unknown error"}`
      );
    }
  };

  if (loading) return <p className="text-xl">Loading gifts… 🎁</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">{product?.name}</h1>

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <img
            src={product?.imageUrl}
            alt={product?.name}
            className="w-full h-64 object-cover rounded"
          />

          <p className="text-2xl font-semibold mt-4">
            ${product?.price}
          </p>

          <p className="mt-2">{product?.description}</p>

          <div className="mt-4">
            <span
              className={`px-2 py-1 rounded ${
                inventory?.available ? "bg-green-200" : "bg-red-200"
              }`}
            >
              {inventory?.available
                ? `In Stock: ${inventory.quantity}`
                : "Out of Stock"}
            </span>
          </div>

          {inventory?.available && (
            <button
              onClick={handleOrder}
              className="mt-4 bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600"
            >
              Add to Cart (Demo Order)
            </button>
          )}

          {orderStatus && (
            <p
              className={`mt-2 ${
                orderStatus.includes("failed")
                  ? "text-red-500"
                  : "text-green-500"
              }`}
            >
              {orderStatus}
            </p>
          )}
        </div>

        <div>
          <h2 className="text-2xl font-semibold mb-2">
            Reviews ({reviews?.averageRating}/5)
          </h2>

          <ul className="space-y-2">
            {reviews?.reviews.map((rev) => (
              <li key={rev.id} className="border p-3 rounded">
                <div className="flex justify-between">
                  <span>{rev.user}</span>
                  <span>{rev.rating}⭐</span>
                </div>
                <p>{rev.text}</p>
                <small>{rev.date}</small>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <a href="/" className="block mt-8 text-blue-500">
        ← Back to Home
      </a>
    </div>
  );
}

