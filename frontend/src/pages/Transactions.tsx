import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { apiClient } from '../api/client';
import type { Transaction } from '../types';
import { Search, ChevronLeft, ChevronRight } from 'lucide-react';
import { TableSkeleton } from '../components/ui/Loaders';
import { EmptyState } from '../components/ui/States';

export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState('');
  const [type, setType] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [skip, setSkip] = useState(0);
  const limit = 20;

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const params = new URLSearchParams({
          skip: skip.toString(),
          limit: limit.toString()
        });
        if (search) params.append('search', search);
        if (type) params.append('type', type);
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);

        const res = await apiClient.get(`/transactions?${params.toString()}`);
        setTransactions(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    // Add a small debounce for search
    const timeout = setTimeout(fetchData, 300);
    return () => clearTimeout(timeout);
  }, [search, type, startDate, endDate, skip]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-slate-900">Transactions</h1>
      </div>

      <Card className="p-4 bg-slate-50 border border-slate-200">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setSkip(0); }}
              placeholder="Search merchants..."
              className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-finora-500 bg-white shadow-sm"
            />
          </div>

          <select
            value={type}
            onChange={(e) => { setType(e.target.value); setSkip(0); }}
            className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-finora-500 bg-white shadow-sm"
          >
            <option value="">All Types</option>
            <option value="INCOME">Income</option>
            <option value="EXPENSE">Expense</option>
          </select>

          <input
            type="date"
            value={startDate}
            onChange={(e) => { setStartDate(e.target.value); setSkip(0); }}
            className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-finora-500 bg-white shadow-sm text-slate-600"
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => { setEndDate(e.target.value); setSkip(0); }}
            className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-finora-500 bg-white shadow-sm text-slate-600"
          />
        </div>
      </Card>

      {loading ? (
        <TableSkeleton rows={10} />
      ) : transactions.length === 0 ? (
        <EmptyState title="No transactions found" message="Try adjusting your filters or date range." />
      ) : (
        <Card className="p-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-slate-50 text-slate-500 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-4 font-medium">Date</th>
                  <th className="px-6 py-4 font-medium">Merchant</th>
                  <th className="px-6 py-4 font-medium">Category</th>
                  <th className="px-6 py-4 font-medium text-right">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {transactions.map(t => (
                  <tr key={t.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-6 py-4 text-slate-600 whitespace-nowrap">
                      {new Date(t.transaction_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 font-medium text-slate-900">
                      {t.merchant}
                    </td>
                    <td className="px-6 py-4 text-slate-600">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
                        {t.category?.name || 'Uncategorized'}
                      </span>
                    </td>
                    <td className={`px-6 py-4 text-right font-semibold ${t.transaction_type === 'INCOME' ? 'text-emerald-600' : 'text-slate-900'}`}>
                      {t.transaction_type === 'INCOME' ? '+' : '-'}₹{Math.abs(t.amount).toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="border-t border-slate-100 p-4 bg-slate-50 flex items-center justify-between">
            <span className="text-sm text-slate-500">
              Showing {skip + 1} to {skip + transactions.length}
            </span>
            <div className="flex space-x-2">
              <button
                onClick={() => setSkip(s => Math.max(0, s - limit))}
                disabled={skip === 0}
                className="p-2 bg-white border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 disabled:opacity-50 transition-colors shadow-sm"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setSkip(s => s + limit)}
                disabled={transactions.length < limit}
                className="p-2 bg-white border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 disabled:opacity-50 transition-colors shadow-sm"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
