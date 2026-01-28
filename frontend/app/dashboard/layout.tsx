"use client"

import { ReactNode } from 'react';
import { useAuth } from '@/hooks/useApi';
import { redirect } from 'next/navigation';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-900">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  if (!user) {
    redirect('/login');
  }

  return <>{children}</>;
}
