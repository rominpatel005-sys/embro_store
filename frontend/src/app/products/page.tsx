"use client";
import { useEffect, useState } from "react";
import ProductCard from "@/components/ProductCard";
import { api, Product } from "@/lib/api";

export default function ProductsPage(){ const [products,setProducts]=useState<Product[]>([]); const [search,setSearch]=useState(""); const [loading,setLoading]=useState(true);
  useEffect(()=>{const timer=setTimeout(()=>api<{results:Product[]}>(`/products/?search=${encodeURIComponent(search)}`).then(x=>setProducts(x.results)).finally(()=>setLoading(false)),250); return()=>clearTimeout(timer)},[search]);
  return <div className="mx-auto max-w-7xl px-5 py-12"><div className="mb-10 flex flex-col justify-between gap-4 md:flex-row"><div><h1 className="text-4xl font-black">The collection</h1><p className="mt-2 text-zinc-400">Original embroidery, premium construction.</p></div><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search products" className="rounded-xl border border-white/10 bg-zinc-900 px-4 py-3"/></div>{loading?<p>Loading…</p>:<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">{products.map(p=><ProductCard key={p.id} product={p}/>)}</div>}</div> }
