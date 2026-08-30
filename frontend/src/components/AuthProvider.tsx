"use client";
import { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

type User = { username: string; email: string; first_name: string; last_name: string; is_staff: boolean };
type AuthContextValue = { user: User | null; loading: boolean; login: (u:string,p:string)=>Promise<void>; logout:()=>void; reload:()=>Promise<void> };
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const reload = async () => { try { setUser(await api<User>("/auth/me/")); } catch { setUser(null); } finally { setLoading(false); } };
  useEffect(() => {
    let active = true;
    api<User>("/auth/me/")
      .then((value) => { if (active) setUser(value); })
      .catch(() => { if (active) setUser(null); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);
  const login = async (username:string,password:string) => {
    const tokens = await api<{access:string;refresh:string}>("/auth/login/", {method:"POST", body:JSON.stringify({username,password})});
    localStorage.setItem("access", tokens.access); localStorage.setItem("refresh", tokens.refresh); await reload();
  };
  const logout = () => { localStorage.removeItem("access"); localStorage.removeItem("refresh"); setUser(null); router.push("/"); };
  return <AuthContext.Provider value={{user,loading,login,logout,reload}}>{children}</AuthContext.Provider>;
}
export const useAuth = () => { const value=useContext(AuthContext); if(!value) throw new Error("Missing AuthProvider"); return value; };
