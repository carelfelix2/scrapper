"use client"

import Link from 'next/link';
import { BarChart3, Zap, Database, Settings } from 'lucide-react';

export function Sidebar() {
  return (
    <aside className="w-64 border-r border-slate-700 bg-slate-800 p-6 hidden sm:block">
      <div className="space-y-8">
        <div>
          <Link href="/dashboard" className="flex items-center gap-2 mb-8">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <span className="font-bold text-white text-lg">Scrapper</span>
          </Link>

          <nav className="space-y-2">
            <SidebarLink href="/dashboard" icon={<BarChart3 className="w-5 h-5" />} label="Dashboard" />
            <SidebarLink href="/dashboard#scraper" icon={<Zap className="w-5 h-5" />} label="Create Task" />
            <SidebarLink href="/dashboard#tasks" icon={<Database className="w-5 h-5" />} label="My Tasks" />
            <SidebarLink href="/dashboard#analytics" icon={<BarChart3 className="w-5 h-5" />} label="Analytics" />
          </nav>
        </div>

        <div className="border-t border-slate-700 pt-8">
          <nav className="space-y-2">
            <SidebarLink href="#settings" icon={<Settings className="w-5 h-5" />} label="Settings" />
          </nav>
        </div>

        <div className="bg-slate-700/30 border border-slate-700 rounded-lg p-4">
          <p className="text-sm text-slate-400 mb-2">Pro Plan</p>
          <p className="text-xs text-slate-500">Unlimited scraping tasks</p>
        </div>
      </div>
    </aside>
  );
}

function SidebarLink({ href, icon, label }: { href: string; icon: React.ReactNode; label: string }) {
  return (
    <Link
      href={href}
      className="flex items-center gap-3 px-4 py-2 text-slate-300 hover:text-white hover:bg-slate-700 rounded-lg transition"
    >
      {icon}
      <span>{label}</span>
    </Link>
  );
}
