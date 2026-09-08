import { useState, useEffect } from 'react';
import { X, Loader2 } from 'lucide-react';
import { apiClient } from '../../api/client';
import type { Account, Category } from '../../types';

interface TransactionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  defaultAccountId?: string;
}

export default function TransactionModal({ isOpen, onClose, onSuccess, defaultAccountId }: TransactionModalProps) {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  
  const [type, setType] = useState('EXPENSE');
  const [amount, setAmount] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [merchant, setMerchant] = useState('');
  const [description, setDescription] = useState('Manual Transaction');
  const [accountId, setAccountId] = useState(defaultAccountId || '');
  const [categoryId, setCategoryId] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      // Fetch options when modal opens
      Promise.all([
        apiClient.get('/accounts'),
        apiClient.get('/categories')
      ]).then(([accountsRes, categoriesRes]) => {
        setAccounts(accountsRes.data);
        setCategories(categoriesRes.data);
        // Auto-select first account if default is not provided or not in list
        if (accountsRes.data.length > 0) {
          if (defaultAccountId && accountsRes.data.some((a: any) => a.id === defaultAccountId)) {
            setAccountId(defaultAccountId);
          } else {
            setAccountId(accountsRes.data[0].id);
          }
        }
      }).catch(err => console.error('Failed to fetch modal dependencies', err));
    }
  }, [isOpen, defaultAccountId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await apiClient.post('/transactions', {
        account_id: accountId,
        category_id: categoryId || null,
        type,
        amount: parseFloat(amount),
        merchant: merchant || 'Unknown',
        description,
        transaction_date: date
      });
      onSuccess();
      onClose();
      // Reset form
      setAmount('');
      setMerchant('');
      setCategoryId('');
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to add transaction');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const filteredCategories = categories.filter(c => c.type === type);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4 sm:p-0">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-lg font-bold text-slate-900">Add Transaction</h3>
          <button 
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="flex space-x-4 mb-6">
            <button
              type="button"
              onClick={() => setType('EXPENSE')}
              className={`flex-1 py-2 text-sm font-semibold rounded-lg border transition-colors ${
                type === 'EXPENSE' 
                  ? 'bg-rose-50 border-rose-200 text-rose-700' 
                  : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              Expense
            </button>
            <button
              type="button"
              onClick={() => setType('INCOME')}
              className={`flex-1 py-2 text-sm font-semibold rounded-lg border transition-colors ${
                type === 'INCOME' 
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-700' 
                  : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              Income
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Amount</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-medium">₹</span>
              <input
                type="number"
                step="0.01"
                min="0"
                required
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="w-full pl-8 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-finora-500 focus:border-finora-500 transition-colors outline-none font-medium"
                placeholder="0.00"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Date</label>
              <input
                type="date"
                required
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-finora-500 focus:border-finora-500 transition-colors outline-none text-slate-700"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Department</label>
              <select
                required
                value={accountId}
                onChange={(e) => setAccountId(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-finora-500 focus:border-finora-500 transition-colors outline-none text-slate-700 bg-white"
              >
                {accounts.map(acc => (
                  <option key={acc.id} value={acc.id}>{acc.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Merchant / Source</label>
            <input
              type="text"
              required
              value={merchant}
              onChange={(e) => setMerchant(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-finora-500 focus:border-finora-500 transition-colors outline-none"
              placeholder={type === 'EXPENSE' ? 'e.g., Starbucks, Amazon' : 'e.g., Employer, Freelance'}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Category</label>
            <select
              value={categoryId}
              onChange={(e) => setCategoryId(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-finora-500 focus:border-finora-500 transition-colors outline-none text-slate-700 bg-white"
            >
              <option value="">Select a category</option>
              {filteredCategories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>

          {error && (
            <div className="text-red-500 text-sm bg-red-50 p-2 rounded border border-red-100">
              {error}
            </div>
          )}

          <div className="pt-4 mt-6 border-t border-slate-100">
            <button
              type="submit"
              disabled={loading || accounts.length === 0}
              className="w-full bg-finora-600 hover:bg-finora-700 text-white font-semibold py-2.5 rounded-lg transition-colors flex items-center justify-center disabled:opacity-70 shadow-sm shadow-finora-200"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Save Transaction'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
