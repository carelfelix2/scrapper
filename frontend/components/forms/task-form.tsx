"use client"

import { useState } from 'react';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Zap } from 'lucide-react';

export function TaskForm() {
  const [platform, setPlatform] = useState('shopee');
  const [taskType, setTaskType] = useState('keyword_search');
  const [keyword, setKeyword] = useState('');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);

    try {
      const input_data = taskType === 'keyword_search' 
        ? { keyword }
        : { url };

      await api.createScrapingTask({
        platform,
        task_type: taskType,
        input_data,
      });

      setSuccess(true);
      setKeyword('');
      setUrl('');
    } catch (error) {
      console.error('Failed to create task:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="border-slate-700 bg-slate-800">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-blue-400" />
          Create Scraping Task
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label className="text-slate-300 mb-2 block">Platform</Label>
              <Select value={platform} onValueChange={setPlatform}>
                <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-700 border-slate-600">
                  <SelectItem value="shopee">Shopee</SelectItem>
                  <SelectItem value="tokopedia">Tokopedia</SelectItem>
                  <SelectItem value="tiktok_shop">TikTok Shop</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label className="text-slate-300 mb-2 block">Task Type</Label>
              <Select value={taskType} onValueChange={setTaskType}>
                <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-700 border-slate-600">
                  <SelectItem value="keyword_search">Keyword Search</SelectItem>
                  <SelectItem value="url_scrape">URL Scrape</SelectItem>
                  <SelectItem value="shop_monitor">Shop Monitor</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {taskType === 'keyword_search' ? (
            <div>
              <Label htmlFor="keyword" className="text-slate-300 mb-2 block">Keyword</Label>
              <Input
                id="keyword"
                placeholder="e.g., iPhone 15 Pro"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-500"
                required
              />
            </div>
          ) : (
            <div>
              <Label htmlFor="url" className="text-slate-300 mb-2 block">URL</Label>
              <Input
                id="url"
                placeholder="https://shopee.co.id/..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-500"
                required
              />
            </div>
          )}

          {success && (
            <div className="p-3 bg-green-900/20 border border-green-700 rounded-lg text-green-400 text-sm">
              Task created successfully! Check the tasks list to monitor progress.
            </div>
          )}

          <Button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Start Scraping'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
