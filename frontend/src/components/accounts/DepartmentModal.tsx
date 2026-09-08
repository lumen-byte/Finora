import { useState } from 'react';
import { X, Loader2 } from 'lucide-react';
import { apiClient } from '../../api/client';

interface DepartmentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function DepartmentModal({ isOpen, onClose, onSuccess }: DepartmentModalProps) {
  const [name, setName] = useState('');
  const [accountType, setAccountType] = useState('BANK');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await apiClient.post('/accounts', {
        name,
        account_type: accountType,
        currency: 'INR'
      });
      onSuccess();
      onClose();
      setName('');
      setAccountType('BANK');
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to add department');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4 sm:p-0">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-lg font-bold text-slate-900">Add Department</h3>
          <button 
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Department Name</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-finora-500 focus:border-finora-500 transition-colors outline-none"
              placeholder="e.g. Research & Development"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Type</label>
            <select
              value={accountType}
              onChange={(e) => setAccountType(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-finora-500 focus:border-finora-500 transition-colors outline-none text-slate-700 bg-white"
            >
              <option value="BANK">Standard Budget</option>
              <option value="CREDIT_CARD">Credit/Liability</option>
              <option value="CASH">Petty Cash</option>
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
              disabled={loading || !name.trim()}
              className="w-full bg-finora-600 hover:bg-finora-700 text-white font-semibold py-2.5 rounded-lg transition-colors flex items-center justify-center disabled:opacity-70 shadow-sm shadow-finora-200"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Create Department'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
