import Image from "next/image";
import Link from "next/link";
import { mediaUrl, money, Product } from "@/lib/api";

export default function ProductCard({ product }: { product: Product }) {
  return <Link href={`/products/${product.slug}`} className="group overflow-hidden rounded-2xl border border-white/10 bg-zinc-900/60">
    <div className="relative aspect-square bg-zinc-900"><Image src={mediaUrl(product.image)} alt={product.name} fill className="object-cover transition group-hover:scale-105" unoptimized /></div>
    <div className="p-4"><p className="text-xs uppercase tracking-widest text-amber-400">{product.brand}</p><h3 className="mt-1 font-semibold">{product.name}</h3><p className="mt-2 text-zinc-300">{money(product.current_price)}</p></div>
  </Link>;
}
