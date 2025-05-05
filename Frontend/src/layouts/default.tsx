import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import Navbar from "@/components/globales/Navbar";
import { Header } from "@/components/globales/Header";

export default function DefaultLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();

  const [isSidebarOpen, setIsSidebarOpen] = useState(() => {
    if (!isAuthenticated) return false;
    const savedState = localStorage.getItem("sidebarOpen");
    return savedState ? JSON.parse(savedState) : true;
  });

  useEffect(() => {
    localStorage.setItem("sidebarOpen", JSON.stringify(isSidebarOpen));
  }, [isSidebarOpen]);

  useEffect(() => {
    if (!isAuthenticated) {
      setIsSidebarOpen(false);
    }
  }, [isAuthenticated]);

  return (
    <div className="relative flex h-screen">
      <Navbar isOpen={isSidebarOpen} toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
      <div className="flex flex-col flex-grow transition-all duration-300" style={{ marginLeft: isSidebarOpen ? "250px" : "70px" }}>
        <Header isSidebarOpen={isSidebarOpen} />
        <main className="container mx-auto max-w-7xl px-6 flex-grow pt-20">{children}</main>
      </div>
    </div>
  );
}