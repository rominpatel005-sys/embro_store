"use client";
import Link from "next/link";
import { useAuth } from "./AuthProvider";

export default function Header() {
  const { user, logout } = useAuth();
  return <header className="sticky top-0 z-50 border-b border-white/10 bg-black/85 backdrop-blur-xl">
    <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
      <Link href="/" className="text-xl font-black tracking-[.25em] text-amber-400">EMBRO</Link>
      <nav className="flex items-center gap-5 text-sm text-zinc-300">
        <Link href="/products">Shop</Link><Link href="/tracking">Track</Link><Link href="/contact">Contact</Link>
        {user && <><Link href="/wishlist">Wishlist</Link><Link href="/orders">Orders</Link><Link href="/cart">Cart</Link></>}
        {user?.is_staff && <Link href="/admin" className="text-amber-400">Dashboard</Link>}
        {user ? <button onClick={logout}>Logout</button> : <Link href="/login">Login</Link>}
      </nav>
    </div>
  </header>;
}
