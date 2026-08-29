import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle } from '../components/ui/Card';
import { Lightbulb, AlertTriangle, Repeat, Activity, AlertCircle, CheckCircle2, Cpu, FileSearch } from 'lucide-react';
import { apiClient } from '../api/client';
import type { Insight, RecurringTransaction, Anomaly } from '../types';
import { CardSkeleton } from '../components/ui/Loaders';
import { EmptyState } from '../components/ui/States';

export default function Insights() {
  const [insights, setInsights] = useState<Insight[]>([]);
  const [recurring, setRecurring] = useState<RecurringTransaction[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [insightsRes, recurringRes, anomaliesRes] = await Promise.all([
          apiClient.get('/insights'),
          apiClient.get('/analytics/recurring-transactions'),
          apiClient.get('/analytics/anomalies')
        ]);
        setInsights(insightsRes.data);
        setRecurring(recurringRes.data);
        setAnomalies(anomaliesRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Financial Insights</h1>
          <p className="text-slate-500 mt-1">AI-generated deterministic analysis of your financial behavior.</p>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <CardSkeleton className="col-span-full" />
          <CardSkeleton />
          <CardSkeleton />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Key Observations */}
          <Card className="col-span-full border-l-4 border-l-finora-500 shadow-sm">
            <CardHeader>
              <CardTitle className="flex items-center text-finora-700">
                <Lightbulb className="w-5 h-5 mr-2" /> Key Observations
              </CardTitle>
            </CardHeader>
            <div className="space-y-4">
              {insights.map((insight) => (
                <div key={insight.id} className="flex items-start bg-slate-50 p-4 rounded-xl border border-slate-100">
                  {insight.severity === 'IMPORTANT' ? (
                    <AlertTriangle className="w-5 h-5 text-amber-500 mt-0.5 mr-3 flex-shrink-0" />
                  ) : insight.severity === 'WARNING' ? (
                    <AlertCircle className="w-5 h-5 text-rose-500 mt-0.5 mr-3 flex-shrink-0" />
                  ) : (
                    <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-0.5 mr-3 flex-shrink-0" />
                  )}
                  <div>
                    <h4 className="text-sm font-semibold text-slate-900">{insight.title}</h4>
                    <p className="text-sm text-slate-600 mt-1 leading-relaxed">{insight.message}</p>
                  </div>
                </div>
              ))}
              {insights.length === 0 && (
                <EmptyState 
                  icon={CheckCircle2} 
                  title="No urgent observations" 
                  message="Your finances are looking stable. We will notify you when significant events occur." 
                />
              )}
            </div>
          </Card>

          {/* Recurring Expenses */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-slate-800">
                <Repeat className="w-5 h-5 mr-2 text-indigo-500" /> Recurring Expenses
              </CardTitle>
            </CardHeader>
            <div className="divide-y divide-slate-100">
              {recurring.map((item, idx) => (
                <div key={idx} className="py-4 flex justify-between items-center">
                  <div>
                    <p className="font-medium text-slate-900">{item.merchant}</p>
                    <p className="text-xs text-slate-500 mt-1 capitalize">{item.frequency.toLowerCase()} • {item.transaction_count} past payments</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-slate-900">₹{item.average_amount.toFixed(2)}</p>
                    <span className="inline-block mt-1.5 px-2 py-0.5 bg-indigo-50 text-indigo-600 rounded text-[10px] font-bold uppercase tracking-wider border border-indigo-100">
                      {Math.round(item.confidence_score * 100)}% Match
                    </span>
                  </div>
                </div>
              ))}
              {recurring.length === 0 && (
                <div className="pt-2">
                  <EmptyState 
                    icon={FileSearch} 
                    title="No recurring expenses" 
                    message="We couldn't identify any repeating subscriptions." 
                  />
                </div>
              )}
            </div>
          </Card>

          {/* Anomalies */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-slate-800">
                <Activity className="w-5 h-5 mr-2 text-rose-500" /> Detected Anomalies
              </CardTitle>
            </CardHeader>
            <div className="divide-y divide-slate-100">
              {anomalies.map((item, idx) => (
                <div key={idx} className="py-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <p className="font-medium text-slate-900">{item.transaction.merchant}</p>
                      <p className="text-xs text-slate-500 mt-1">
                        {new Date(item.transaction.transaction_date).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-rose-600">₹{item.transaction.amount.toFixed(2)}</p>
                    </div>
                  </div>
                  <div className="bg-rose-50 px-3 py-2.5 rounded-lg border border-rose-100">
                    <p className="text-xs text-rose-700 font-medium leading-relaxed">
                      {item.reason}
                    </p>
                  </div>
                </div>
              ))}
              {anomalies.length === 0 && (
                <div className="pt-2">
                  <EmptyState 
                    icon={CheckCircle2} 
                    title="No anomalous spending" 
                    message="Your recent transactions are perfectly aligned with your typical statistical ranges." 
                  />
                </div>
              )}
            </div>
          </Card>

          {/* System Intelligence Explanation */}
          <Card className="col-span-full bg-slate-900 border-none text-white">
            <CardHeader className="border-b border-slate-800 pb-4 mb-6">
              <CardTitle className="flex items-center text-white">
                <Cpu className="w-5 h-5 mr-2 text-finora-400" /> System Intelligence
              </CardTitle>
            </CardHeader>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                {
                  title: "Deterministic Analytics",
                  desc: "Analyzes exact raw values from PostgreSQL without guessing."
                },
                {
                  title: "Recurring Detection",
                  desc: "Groups transactions by merchant and analyzes frequency, consistency, and amount variation."
                },
                {
                  title: "Statistical Anomalies",
                  desc: "Uses historical category spending patterns and Z-scores to identify unusual expenses."
                },
                {
                  title: "AI Function Calling",
                  desc: "The LLM selects approved backend tools instead of generating financial numbers directly."
                }
              ].map(item => (
                <div key={item.title}>
                  <div className="flex items-center text-sm font-semibold text-finora-300 mb-2">
                    <CheckCircle2 className="w-4 h-4 mr-1.5" />
                    {item.title}
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {item.desc}
                  </p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
