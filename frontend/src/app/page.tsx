import Link from "next/link";
import ProductCard from "@/components/ProductCard";
import { Product } from "@/lib/api";

async function featured() { try { const serverApi=process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api"; const r=await fetch(`${serverApi}/products/?ordering=-rating&page_size=8`,{cache:"no-store"}); return (await r.json()).results as Product[]; } catch { return []; } }
export default async function Home() { const products=await featured(); return <>
  <section className="mx-auto grid min-h-[65vh] max-w-7xl place-items-center px-5 text-center"><div><p className="text-sm uppercase tracking-[.4em] text-amber-400">Threaded with character</p><h1 className="mt-5 text-5xl font-black md:text-8xl">Wear the artwork.</h1><p className="mx-auto mt-6 max-w-xl text-lg text-zinc-400">Premium embroidered essentials designed to become the pieces you reach for every day.</p><Link href="/products" className="mt-8 inline-block rounded-full bg-amber-400 px-7 py-3 font-bold text-black">Explore collection</Link></div></section>
  <section className="mx-auto max-w-7xl px-5 py-16"><div className="mb-8 flex justify-between"><h2 className="text-3xl font-bold">Featured pieces</h2><Link href="/products">View all →</Link></div><div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">{products.map(p=><ProductCard key={p.id} product={p}/>)}</div></section>
  </>; }
