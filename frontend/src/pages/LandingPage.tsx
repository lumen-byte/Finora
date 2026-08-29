import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Hexagon, ArrowRight, BrainCircuit, Activity, BarChart3, MessageSquare, Database, ArrowDown } from 'lucide-react';
import { apiClient } from '../api/client';

export default function LandingPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDemoLogin = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await apiClient.post('/auth/demo');
      localStorage.setItem('finora_token', response.data.access_token);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError('Could not access demo. Please ensure the backend is running and seeded.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      <nav className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Hexagon className="w-8 h-8 text-finora-600 fill-finora-100" />
          <span className="text-2xl font-bold tracking-tight">Finora</span>
        </div>
        <div className="flex space-x-4">
          <button 
            onClick={handleDemoLogin}
            disabled={loading}
            className="bg-finora-600 text-white px-5 py-2.5 rounded-full text-sm font-medium hover:bg-finora-700 transition-colors flex items-center"
          >
            {loading ? 'Entering Demo...' : 'Explore Demo'}
          </button>
        </div>
      </nav>

      <main>
        {/* Hero Section */}
        <section className="max-w-4xl mx-auto px-6 pt-24 pb-20 text-center">
          <div className="inline-flex items-center space-x-2 bg-finora-50 text-finora-700 px-4 py-1.5 rounded-full text-sm font-semibold mb-8">
            <BrainCircuit className="w-4 h-4" />
            <span>AI-Powered Financial Intelligence</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 mb-6 leading-tight">
            Your financial data, explained.
          </h1>
          <p className="text-xl text-slate-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            An AI-powered financial intelligence platform that analyzes transactions, detects recurring expenses and unusual spending, and answers financial questions using grounded, deterministic data.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
            <button 
              onClick={handleDemoLogin}
              disabled={loading}
              className="w-full sm:w-auto bg-finora-600 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-finora-700 transition-all flex items-center justify-center shadow-lg shadow-finora-200"
            >
              {loading ? 'Entering Demo...' : 'Explore Demo'}
              {!loading && <ArrowRight className="w-5 h-5 ml-2" />}
            </button>
          </div>
          {error && <p className="text-red-500 mt-4 font-medium">{error}</p>}
        </section>

        {/* Value Flow Section */}
        <section className="bg-white py-24 border-y border-slate-200">
          <div className="max-w-7xl mx-auto px-6 text-center">
            <h2 className="text-3xl font-bold mb-16">How Finora Works</h2>
            
            <div className="grid md:grid-cols-3 gap-12 text-left relative">
              <div className="hidden md:block absolute top-12 left-1/6 right-1/6 h-0.5 bg-slate-100 -z-10 w-2/3 mx-auto"></div>
              
              <div className="bg-white">
                <div className="w-16 h-16 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center text-finora-600 mb-6 shadow-sm mx-auto md:mx-0">
                  <Database className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-3 text-center md:text-left">1. Connect Your Financial Data</h3>
                <p className="text-slate-600 leading-relaxed text-center md:text-left">
                  Accounts and transactions become structured financial data ready for analysis.
                </p>
              </div>

              <div className="bg-white">
                <div className="w-16 h-16 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center text-finora-600 mb-6 shadow-sm mx-auto md:mx-0">
                  <Activity className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-3 text-center md:text-left">2. Understand Your Spending</h3>
                <p className="text-slate-600 leading-relaxed text-center md:text-left">
                  Finora calculates trends, category breakdowns, recurring expenses, anomalies, and financial insights.
                </p>
              </div>

              <div className="bg-white">
                <div className="w-16 h-16 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center text-finora-600 mb-6 shadow-sm mx-auto md:mx-0">
                  <MessageSquare className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-3 text-center md:text-left">3. Ask Finora AI</h3>
                <p className="text-slate-600 leading-relaxed text-center md:text-left">
                  FinoraAI selects backend tools and explains the actual data in natural language.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* AI That Doesn't Guess Section */}
        <section className="bg-slate-900 text-white py-24">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold mb-6">AI that doesn't guess.</h2>
            <p className="text-lg text-slate-400 mb-12 max-w-2xl mx-auto">
              FinoraAI does not directly query the database or generate financial numbers from imagination. It uses strict Function Calling to ensure accuracy.
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-4 font-mono text-sm">
              <div className="px-4 py-3 bg-slate-800 rounded-lg text-slate-300">Question</div>
              <ArrowRight className="hidden md:block w-5 h-5 text-finora-500" />
              <ArrowDown className="md:hidden w-5 h-5 text-finora-500" />
              <div className="px-4 py-3 bg-slate-800 rounded-lg text-slate-300">Tool Selection</div>
              <ArrowRight className="hidden md:block w-5 h-5 text-finora-500" />
              <ArrowDown className="md:hidden w-5 h-5 text-finora-500" />
              <div className="px-4 py-3 bg-slate-800 rounded-lg border border-finora-500/30 text-finora-400">Deterministic Analytics</div>
              <ArrowRight className="hidden md:block w-5 h-5 text-finora-500" />
              <ArrowDown className="md:hidden w-5 h-5 text-finora-500" />
              <div className="px-4 py-3 bg-finora-600 rounded-lg text-white font-semibold">Grounded Explanation</div>
            </div>
          </div>
        </section>
        
        {/* Final CTA */}
        <section className="py-24 text-center bg-white">
          <h2 className="text-3xl font-bold mb-8">Ready to see it in action?</h2>
          <button 
            onClick={handleDemoLogin}
            disabled={loading}
            className="bg-finora-600 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-finora-700 transition-all shadow-lg"
          >
            {loading ? 'Entering Demo...' : 'Explore Demo Now'}
          </button>
        </section>
      </main>
    </div>
  );
}
