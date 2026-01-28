"use client"

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight, TrendingUp, Zap, BarChart3 } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Navigation */}
      <nav className="border-b border-slate-700 sticky top-0 z-50 backdrop-blur-sm bg-slate-900/80">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
            Scrapper
          </div>
          <div className="flex gap-4">
            <Button variant="ghost" className="text-slate-300 hover:text-white">
              Features
            </Button>
            <Button variant="ghost" className="text-slate-300 hover:text-white">
              Pricing
            </Button>
            <Link href="/login">
              <Button className="bg-blue-600 hover:bg-blue-700">Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
          Web Scraping Made Simple
          <br />
          <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
            For Indonesian E-commerce
          </span>
        </h1>
        <p className="text-xl text-slate-400 mb-8 max-w-2xl mx-auto">
          Track trending products, monitor prices, and gain market insights from Shopee, Tokopedia, and TikTok Shop in real-time.
        </p>
        <div className="flex gap-4 justify-center mb-16">
          <Link href="/dashboard">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 gap-2">
              Start Scraping <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
          <Button size="lg" variant="outline" className="border-slate-600 text-white hover:bg-slate-800">
            Watch Demo
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 py-16 grid md:grid-cols-3 gap-8">
        <div className="p-6 bg-slate-800 rounded-lg border border-slate-700 hover:border-blue-600 transition">
          <TrendingUp className="w-12 h-12 text-blue-400 mb-4" />
          <h3 className="text-xl font-bold mb-2">Real-time Tracking</h3>
          <p className="text-slate-400">
            Monitor product prices, stock levels, and ratings across multiple platforms instantly.
          </p>
        </div>

        <div className="p-6 bg-slate-800 rounded-lg border border-slate-700 hover:border-blue-600 transition">
          <Zap className="w-12 h-12 text-blue-400 mb-4" />
          <h3 className="text-xl font-bold mb-2">Fast & Reliable</h3>
          <p className="text-slate-400">
            Powered by Playwright with proxy rotation and bot-detection bypass technology.
          </p>
        </div>

        <div className="p-6 bg-slate-800 rounded-lg border border-slate-700 hover:border-blue-600 transition">
          <BarChart3 className="w-12 h-12 text-blue-400 mb-4" />
          <h3 className="text-xl font-bold mb-2">Smart Analytics</h3>
          <p className="text-slate-400">
            Visualize trends, export reports, and make data-driven decisions for your business.
          </p>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 py-16 text-center">
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-12">
          <h2 className="text-3xl font-bold mb-4">Ready to get started?</h2>
          <p className="text-blue-100 mb-8">
            Join thousands of e-commerce sellers optimizing their business with Scrapper.
          </p>
          <Link href="/login">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-slate-100 font-semibold">
              Start Free Trial
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-700 py-8 text-center text-slate-500">
        <p>&copy; 2024 Scrapper - Web Scraping SaaS Platform. All rights reserved.</p>
      </footer>
    </div>
  );
}
