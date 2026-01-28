"use client"

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { LogOut, Home, BarChart3, Menu } from 'lucide-react';
import { useState } from 'react';

export function Header() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <header className="border-b border-slate-700 bg-slate-800">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-white hidden sm:block">Scrapper</span>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          {user && (
            <>
              <div className="hidden sm:block text-right">
                <p className="text-white font-semibold">{user.full_name || user.username}</p>
                <p className="text-sm text-slate-400">{user.email}</p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                className="gap-2 text-slate-300 hover:text-white hover:bg-slate-700"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:block">Logout</span>
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
