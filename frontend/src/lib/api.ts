export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "/api";
const MEDIA_ORIGIN = (process.env.NEXT_PUBLIC_MEDIA_URL ?? "").replace(/\/$/, "");

export type Product = {
  id: number; name: string; slug: string; description: string; price: string;
  discount_price: string | null; current_price: string; brand: string; stock: number;
  rating: string; image: string; sizes_list: string[]; colors_list: string[];
  category_detail: { id: number; name: string; slug: string; gender: string };
};

export type Cart = { id: number; total_price: string; total_items: number; items: Array<{
  id: number; quantity: number; size: string; color: string; subtotal: string; product_detail: Product;
}> };

export type Order = { id: number; full_name: string; total_amount: string; status: string;
  created_at: string; cancellable: boolean; items: Array<{id:number; product_name:string; quantity:number; price:string; size:string; color:string}>;
  payment?: { payment_method: string; status: string };
};

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access") : null;
  const headers = new Headers(options.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (options.body && !(options.body instanceof FormData)) headers.set("Content-Type", "application/json");
  const response = await fetch(`${API_URL}${path}`, { ...options, headers, cache: "no-store" });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(payload.detail ?? Object.values(payload).flat().join(" ") ?? "Request failed");
  }
  return response.status === 204 ? (undefined as T) : response.json();
}

export const money = (value: string | number) => new Intl.NumberFormat("en-IN", {
  style: "currency", currency: "INR", maximumFractionDigits: 2,
}).format(Number(value));

export const mediaUrl = (url?: string) => !url ? "/file.svg" : url.startsWith("http") ? url : `${MEDIA_ORIGIN}${url.startsWith("/") ? url : `/${url}`}`;
