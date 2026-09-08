import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle } from '../components/ui/Card';
import { apiClient } from '../api/client';
import type { Account } from '../types';
import { Landmark, CreditCard, Banknote, Wallet } from 'lucide-react';
import { CardSkeleton } from '../components/ui/Loaders';
import { EmptyState } from '../components/ui/States';
import DepartmentModal from '../components/accounts/DepartmentModal';
import { useNavigate } from 'react-router-dom';

export default function Accounts() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await apiClient.get('/accounts');
        setAccounts(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [refreshTrigger]);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900">Department Budgets</h1>
          <button className="bg-finora-600 hover:bg-finora-700 text-white px-4 py-2 rounded-lg font-medium transition-colors text-sm shadow-sm">
            Add Department
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <CardSkeleton /><CardSkeleton /><CardSkeleton />
        </div>
      </div>
    );
  }

  if (accounts.length === 0) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900">Department Budgets</h1>
          <button className="bg-finora-600 hover:bg-finora-700 text-white px-4 py-2 rounded-lg font-medium transition-colors text-sm shadow-sm">
            Add Department
          </button>
        </div>
        <EmptyState icon={Wallet} title="No departments linked" message="Link a department to get started." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Department Budgets</h1>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-finora-600 hover:bg-finora-700 text-white px-4 py-2 rounded-lg font-medium transition-colors text-sm shadow-sm"
        >
          Add Department
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {accounts.map(acc => (
          <div key={acc.id} onClick={() => navigate(`/transactions?account_id=${acc.id}`)} className="cursor-pointer transition-transform hover:-translate-y-1 hover:shadow-lg">
            <Card>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-finora-50 rounded-xl flex items-center justify-center text-finora-600">
                  {acc.account_type === 'BANK' ? <Landmark className="w-5 h-5" /> : acc.account_type === 'CREDIT' ? <CreditCard className="w-5 h-5" /> : <Banknote className="w-5 h-5" />}
                </div>
                <div>
                  <CardTitle className="text-lg">{acc.name}</CardTitle>
                  <p className="text-xs text-slate-500 capitalize font-medium">{acc.account_type.toLowerCase()} Department</p>
                </div>
              </div>
            </CardHeader>
            <div className="mt-4">
              <p className="text-3xl font-bold text-slate-900">
                ₹{acc.current_balance.toLocaleString()}
              </p>
            </div>
          </Card>
          </div>
        ))}
      </div>

      <DepartmentModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={() => setRefreshTrigger(prev => prev + 1)}
      />
    </div>
  );
}
