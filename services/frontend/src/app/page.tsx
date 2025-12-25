"use client";

import { useState } from "react";
import Link from "next/link";

export default function Home() {
  const [productId, setProductId] = useState("prod-123");

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-100">
      <h1 className="text-4xl font-bold mb-8">Istio E-Commerce Demo 🎄</h1>

      <div className="mb-4">
        <label className="mr-2">Product ID:</label>
        <select
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
          className="p-2 border rounded"
        >
          <option value="prod-123">Wireless Headphones</option>
          <option value="prod-456">Smart Watch</option>
        </select>
      </div>

      <Link
        href={`/product/${productId}`}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        View Product
      </Link>
    </main>
  );
}

