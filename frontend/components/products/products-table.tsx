"use client"

import type { Product } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface ProductsTableProps {
  products: Product[];
  loading: boolean;
}

export function ProductsTable({ products, loading }: ProductsTableProps) {
  if (loading && products.length === 0) {
    return (
      <Card className="border-slate-700 bg-slate-800">
        <CardContent className="p-8 text-center text-slate-400">
          Loading products...
        </CardContent>
      </Card>
    );
  }

  if (products.length === 0) {
    return (
      <Card className="border-slate-700 bg-slate-800">
        <CardContent className="p-8 text-center text-slate-400">
          No products found. Create a scraping task to start collecting data.
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-slate-700 bg-slate-800 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700 bg-slate-700/50">
              <th className="px-6 py-3 text-left font-semibold text-slate-300">Product Name</th>
              <th className="px-6 py-3 text-left font-semibold text-slate-300">Platform</th>
              <th className="px-6 py-3 text-right font-semibold text-slate-300">Price</th>
              <th className="px-6 py-3 text-right font-semibold text-slate-300">Discount</th>
              <th className="px-6 py-3 text-right font-semibold text-slate-300">Rating</th>
              <th className="px-6 py-3 text-right font-semibold text-slate-300">Sold</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id} className="border-b border-slate-700 hover:bg-slate-700/30">
                <td className="px-6 py-4 text-white truncate max-w-xs">
                  {product.product_name}
                </td>
                <td className="px-6 py-4">
                  <Badge variant="outline" className="bg-slate-700 border-slate-600 text-slate-300">
                    {product.platform}
                  </Badge>
                </td>
                <td className="px-6 py-4 text-right text-white font-semibold">
                  Rp {product.price?.toLocaleString('id-ID') || '-'}
                </td>
                <td className="px-6 py-4 text-right">
                  {product.discount_percentage ? (
                    <span className="text-green-400 font-semibold">-{product.discount_percentage}%</span>
                  ) : (
                    <span className="text-slate-400">-</span>
                  )}
                </td>
                <td className="px-6 py-4 text-right">
                  {product.rating ? (
                    <span className="text-yellow-400">★ {product.rating}</span>
                  ) : (
                    <span className="text-slate-400">-</span>
                  )}
                </td>
                <td className="px-6 py-4 text-right text-slate-400">
                  {product.sold_count?.toLocaleString() || '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
