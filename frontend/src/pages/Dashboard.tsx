import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle } from '../components/ui/Card';
import { ArrowUpRight, ArrowDownRight, Wallet, TrendingUp, TrendingDown, PiggyBank, RefreshCcw } from 'lucide-react';
import { apiClient } from '../api/client';
import type { DashboardMetrics, MonthlyTrend } from '../types';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { cn } from '../utils/cn';
import { CardSkeleton } from '../components/ui/Loaders';

export default function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [trends, setTrends] = useState<MonthlyTrend[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [metricsRes, trendsRes] = await Promise.all([
          apiClient.get('/analytics/dashboard'),
          apiClient.get('/analytics/monthly-trends')
        ]);
        setMetrics(metricsRes.data);
        setTrends(trendsRes.data);
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
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <CardSkeleton /><CardSkeleton /><CardSkeleton /><CardSkeleton />
        </div>
        <CardSkeleton />
      </div>
    );
  }

  if (!metrics) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Overview</h1>
        <button className="flex items-center text-sm font-medium text-slate-600 hover:text-slate-900 bg-white px-4 py-2 rounded-lg border border-slate-200 shadow-sm transition-colors">
          <RefreshCcw className="w-4 h-4 mr-2" /> Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Total Balance" value={`₹${metrics.total_balance}`} icon={Wallet} />
        <MetricCard 
          title="Monthly Income" 
          value={`₹${metrics.total_income}`} 
          trend={metrics.income_change_percentage}
          icon={TrendingUp} 
          trendGood={true}
        />
        <MetricCard 
          title="Monthly Expenses" 
          value={`₹${metrics.total_expenses}`} 
          trend={metrics.expense_change_percentage}
          icon={TrendingDown}
          trendGood={false} 
        />
        <MetricCard 
          title="Savings Rate" 
          value={`${metrics.savings_rate}%`} 
          icon={PiggyBank} 
        />
      </div>

      <Card className="col-span-4 h-[400px]">
        <CardHeader>
          <CardTitle>Cash Flow Trends</CardTitle>
        </CardHeader>
        <div className="h-[300px] mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trends}>
              <defs>
                <linearGradient id="colorIncome" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorExpense" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} tickFormatter={(value) => `₹${value}`} />
              <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                formatter={(value: any) => [`₹${value}`, undefined]}
              />
              <Area type="monotone" dataKey="income" stroke="#10b981" fillOpacity={1} fill="url(#colorIncome)" />
              <Area type="monotone" dataKey="expenses" stroke="#ef4444" fillOpacity={1} fill="url(#colorExpense)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
}

function MetricCard({ title, value, trend, icon: Icon, trendGood }: any) {
  const isPositive = trend > 0;
  const showGoodColor = trendGood ? isPositive : !isPositive;
  const colorClass = showGoodColor ? 'text-emerald-600' : 'text-rose-600';
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-slate-500 font-medium text-sm">{title}</CardTitle>
        <div className="p-2 bg-finora-50 text-finora-600 rounded-lg">
          <Icon className="w-5 h-5" />
        </div>
      </CardHeader>
      <div className="mt-2">
        <div className="text-3xl font-bold tracking-tight text-slate-900">{value}</div>
        {trend !== undefined && trend !== null && (
          <div className={cn("flex items-center mt-2 text-sm font-medium", colorClass)}>
            {isPositive ? <ArrowUpRight className="w-4 h-4 mr-1" /> : <ArrowDownRight className="w-4 h-4 mr-1" />}
            {Math.abs(trend)}% from last month
          </div>
        )}
      </div>
    </Card>
  );
}
