"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ScrapingTask } from '@/types';
import { Badge } from '@/components/ui/badge';
import { Loader2, CheckCircle, AlertCircle, Clock } from 'lucide-react';

interface TasksListProps {
  tasks: ScrapingTask[];
  loading: boolean;
}

export function TasksList({ tasks, loading }: TasksListProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Loader2 className="w-4 h-4 animate-spin text-blue-400" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'failed':
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-400" />;
      default:
        return null;
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, string> = {
      running: 'bg-blue-900/50 text-blue-400 border-blue-700',
      completed: 'bg-green-900/50 text-green-400 border-green-700',
      failed: 'bg-red-900/50 text-red-400 border-red-700',
      pending: 'bg-yellow-900/50 text-yellow-400 border-yellow-700',
    };
    return variants[status] || '';
  };

  if (loading && tasks.length === 0) {
    return (
      <Card className="border-slate-700 bg-slate-800">
        <CardContent className="p-8 text-center text-slate-400">
          Loading tasks...
        </CardContent>
      </Card>
    );
  }

  if (tasks.length === 0) {
    return (
      <Card className="border-slate-700 bg-slate-800">
        <CardContent className="p-8 text-center text-slate-400">
          No tasks yet. Create one to get started!
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <Card key={task.id} className="border-slate-700 bg-slate-800">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4 flex-1">
                {getStatusIcon(task.status)}
                <div className="flex-1">
                  <p className="font-semibold text-white">
                    {task.platform.toUpperCase()} - {task.task_type}
                  </p>
                  <p className="text-sm text-slate-400">
                    ID: {task.id} • Results: {task.results_count}
                  </p>
                </div>
              </div>
              <Badge className={`border ${getStatusBadge(task.status)}`}>
                {task.status}
              </Badge>
            </div>
            {task.error_message && (
              <p className="text-xs text-red-400 mt-2">{task.error_message}</p>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
