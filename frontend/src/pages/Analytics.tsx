import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle } from '../components/ui/Card';
import { apiClient } from '../api/client';
import type { CategoryBreakdown, TopMerchant } from '../types';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { CardSkeleton } from '../components/ui/Loaders';
import { EmptyState } from '../components/ui/States';
import { BarChart3 } from 'lucide-react';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#0ea5e9'];

export default function Analytics() {
  const [breakdown, setBreakdown] = useState<CategoryBreakdown[]>([]);
  const [merchants, setMerchants] = useState<TopMerchant[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [breakdownRes, merchantsRes] = await Promise.all([
          apiClient.get('/analytics/category-breakdown'),
          apiClient.get('/analytics/top-merchants')
        ]);
        setBreakdown(breakdownRes.data);
        setMerchants(merchantsRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-slate-900">Analytics</h1>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <CardSkeleton /><CardSkeleton />
        </div>
      </div>
    );
  }

  if (breakdown.length === 0 && merchants.length === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-slate-900">Analytics</h1>
        <EmptyState icon={BarChart3} title="No analytics data" message="Not enough transactions to generate analytics yet." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Analytics</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="h-[450px]">
          <CardHeader>
            <CardTitle>Spending by Category</CardTitle>
          </CardHeader>
          <div className="h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={breakdown}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={120}
                  paddingAngle={5}
                  dataKey="total_amount"
                  nameKey="category"
                >
                  {breakdown.map((_entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: any) => `₹${Number(value).toFixed(2)}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="h-[450px]">
          <CardHeader>
            <CardTitle>Top Merchants</CardTitle>
          </CardHeader>
          <div className="h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={merchants} layout="vertical" margin={{ left: 40 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                <XAxis type="number" tickFormatter={(v) => `₹${v}`} />
                <YAxis dataKey="merchant" type="category" width={100} tick={{fontSize: 12}} />
                <Tooltip formatter={(value: any) => `₹${Number(value).toFixed(2)}`} />
                <Bar dataKey="total_amount" fill="#6366f1" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
