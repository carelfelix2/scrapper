"use client"

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { Product } from '@/types';

interface AnalyticsProps {
  products: Product[];
}

export function Analytics({ products }: AnalyticsProps) {
  // Price distribution data
  const priceDistribution = [
    { range: 'Under 50K', count: products.filter(p => (p.price || 0) < 50000).length },
    { range: '50K-100K', count: products.filter(p => (p.price || 0) >= 50000 && (p.price || 0) < 100000).length },
    { range: '100K-500K', count: products.filter(p => (p.price || 0) >= 100000 && (p.price || 0) < 500000).length },
    { range: '500K+', count: products.filter(p => (p.price || 0) >= 500000).length },
  ];

  // Platform distribution
  const platformData = [
    { name: 'Shopee', value: products.filter(p => p.platform === 'shopee').length },
    { name: 'Tokopedia', value: products.filter(p => p.platform === 'tokopedia').length },
    { name: 'TikTok Shop', value: products.filter(p => p.platform === 'tiktok_shop').length },
  ];

  const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899'];

  // Rating distribution
  const ratingData = [
    { rating: '5.0', count: products.filter(p => (p.rating || 0) >= 4.8).length },
    { rating: '4.5', count: products.filter(p => (p.rating || 0) >= 4.3 && (p.rating || 0) < 4.8).length },
    { rating: '4.0', count: products.filter(p => (p.rating || 0) >= 3.8 && (p.rating || 0) < 4.3).length },
    { rating: 'Below 4.0', count: products.filter(p => (p.rating || 0) < 3.8).length },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card className="border-slate-700 bg-slate-800">
        <CardHeader>
          <CardTitle className="text-white">Price Range Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={priceDistribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="range" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
              <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="border-slate-700 bg-slate-800">
        <CardHeader>
          <CardTitle className="text-white">Platform Distribution</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={platformData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name}: ${entry.value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {platformData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="border-slate-700 bg-slate-800 lg:col-span-2">
        <CardHeader>
          <CardTitle className="text-white">Rating Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ratingData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis type="number" stroke="#94a3b8" />
              <YAxis dataKey="rating" type="category" stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
              <Bar dataKey="count" fill="#8b5cf6" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
