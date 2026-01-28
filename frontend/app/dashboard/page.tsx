"use client"

import { useState } from 'react';
import { Sidebar } from '@/components/layout/sidebar';
import { Header } from '@/components/layout/header';
import { TaskForm } from '@/components/forms/task-form';
import { TasksList } from '@/components/tasks/tasks-list';
import { ProductsTable } from '@/components/products/products-table';
import { Analytics } from '@/components/analytics/analytics';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useScrapingTasks, useProducts } from '@/hooks/useApi';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('overview');
  const { tasks, loading: tasksLoading } = useScrapingTasks();
  const { products, loading: productsLoading } = useProducts();

  return (
    <div className="flex h-screen bg-slate-900 text-white">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-auto">
          <div className="max-w-7xl mx-auto p-6">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="grid w-full grid-cols-4 bg-slate-800">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="scraper">Scraper</TabsTrigger>
                <TabsTrigger value="tasks">Tasks</TabsTrigger>
                <TabsTrigger value="analytics">Analytics</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
                    <p className="text-slate-400 text-sm">Total Tasks</p>
                    <p className="text-3xl font-bold text-white">{tasks.length}</p>
                  </div>
                  <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
                    <p className="text-slate-400 text-sm">Total Products</p>
                    <p className="text-3xl font-bold text-white">{products.length}</p>
                  </div>
                  <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
                    <p className="text-slate-400 text-sm">Running Tasks</p>
                    <p className="text-3xl font-bold text-blue-400">
                      {tasks.filter(t => t.status === 'running').length}
                    </p>
                  </div>
                </div>

                <Analytics products={products} />
              </TabsContent>

              <TabsContent value="scraper" className="space-y-6">
                <TaskForm />
              </TabsContent>

              <TabsContent value="tasks" className="space-y-6">
                <TasksList tasks={tasks} loading={tasksLoading} />
              </TabsContent>

              <TabsContent value="analytics" className="space-y-6">
                <Analytics products={products} />
              </TabsContent>
            </Tabs>

            <div className="mt-8">
              <h2 className="text-2xl font-bold mb-4">Recent Products</h2>
              <ProductsTable products={products} loading={productsLoading} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
