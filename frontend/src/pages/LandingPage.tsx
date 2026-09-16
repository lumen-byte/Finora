import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Hexagon, ArrowRight, Activity, MessageSquare, Database, Loader2, Sparkles } from 'lucide-react';
import { apiClient } from '../api/client';
import { useAuth } from '../contexts/AuthContext';

export default function LandingPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleDemoLogin = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await apiClient.post('/auth/demo');
      login(response.data.access_token);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError('Could not access demo. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen w-full flex flex-col lg:flex-row font-sans overflow-hidden bg-slate-900">
      {/* Left side: Premium Branding & Hero (Dark) */}
      <div className="w-full lg:w-1/2 relative bg-slate-900 overflow-hidden flex flex-col justify-between p-8 sm:p-12 lg:p-16 h-full z-10">
        {/* Abstract Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-finora-900 via-slate-900 to-black pointer-events-none"></div>
        <div className={`absolute -top-40 -left-40 w-96 h-96 bg-finora-600/30 rounded-full blur-3xl transition-transform duration-1000 ease-out ${mounted ? 'translate-y-0 translate-x-0' : '-translate-y-20 -translate-x-20'}`}></div>
        <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-finora-900/40 rounded-full blur-[100px] transition-transform duration-1000 delay-300 ease-out ${mounted ? 'scale-100' : 'scale-90 opacity-0'}`}></div>
        
        <div className="relative z-10 flex flex-col justify-between h-full">
          {/* Header */}
          <nav className="flex items-center justify-between w-full">
            <Link to="/" className="flex items-center space-x-3 group w-fit">
              <div className="bg-white/10 p-2.5 rounded-xl backdrop-blur-md border border-white/10 group-hover:bg-white/20 transition-all shadow-xl">
                <Hexagon className="w-7 h-7 text-white fill-finora-500" />
              </div>
              <span className="text-3xl font-extrabold tracking-tight text-white">Finora</span>
            </Link>
            <div className="flex space-x-4 lg:hidden">
              <Link to="/login" className="text-sm font-medium text-slate-300 hover:text-white px-4 py-2 transition-colors">Log in</Link>
            </div>
          </nav>

          {/* Hero Content */}
          <div className="mt-12 lg:mt-0 flex-1 flex flex-col justify-center max-w-xl">
            <div className={`inline-flex items-center space-x-2 bg-finora-500/10 border border-finora-500/20 text-finora-400 px-4 py-1.5 rounded-full text-sm font-medium mb-8 w-fit backdrop-blur-sm transition-all duration-700 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
              <Sparkles className="w-4 h-4" />
              <span>Enterprise Financial Intelligence</span>
            </div>
            
            <h1 className={`text-5xl sm:text-6xl lg:text-7xl font-extrabold text-white mb-6 leading-[1.1] tracking-tight transition-all duration-700 delay-100 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
              AI that doesn't <span className="text-transparent bg-clip-text bg-gradient-to-r from-finora-400 to-finora-200">guess.</span>
            </h1>
            
            <p className={`text-lg sm:text-xl text-slate-300 mb-10 leading-relaxed font-light transition-all duration-700 delay-200 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
              Master your corporate spend. Track departmental budgets, monitor SaaS subscriptions, and detect spending anomalies with deterministically accurate AI.
            </p>
            
            <div className={`flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4 transition-all duration-700 delay-300 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
              <Link 
                to="/register"
                className="w-full sm:w-auto bg-finora-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-finora-500 transition-all flex items-center justify-center shadow-lg shadow-finora-900/20 group hover:shadow-finora-500/25 border border-finora-500/50"
              >
                <span>Get Started</span>
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Link>
              
              <button 
                onClick={handleDemoLogin}
                disabled={loading}
                className="w-full sm:w-auto bg-white/5 backdrop-blur-md text-white border border-white/10 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/10 transition-all flex items-center justify-center shadow-lg shadow-black/20 group"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Explore Demo'}
              </button>
            </div>
            {error && <p className="text-red-400 mt-4 font-medium text-sm bg-red-900/20 border border-red-900/50 px-4 py-2 rounded-lg backdrop-blur-sm animate-pulse">{error}</p>}
          </div>

          {/* Footer stats */}
          <div className={`hidden sm:flex mt-12 pt-8 border-t border-white/10 items-center space-x-6 text-sm font-medium text-finora-400 transition-all duration-700 delay-500 ${mounted ? 'opacity-100' : 'opacity-0'}`}>
            <div className="flex items-center space-x-2">
              <Database className="w-4 h-4" />
              <span>Real-time Ledger Sync</span>
            </div>
            <div className="w-1.5 h-1.5 rounded-full bg-slate-700"></div>
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4" />
              <span>&lt;50ms Analytics Latency</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right side: Interactive App Preview (Light) */}
      <div className="hidden lg:flex w-1/2 bg-slate-50 relative items-center justify-center p-12 overflow-hidden h-full z-0">
        {/* Abstract background mesh on the right side */}
        <div className="absolute inset-0 bg-[radial-gradient(#e2e8f0_1px,transparent_1px)] [background-size:20px_20px] opacity-60"></div>
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-finora-100 rounded-full blur-3xl opacity-50 -translate-y-1/3 translate-x-1/3"></div>
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-100 rounded-full blur-3xl opacity-40 translate-y-1/3 -translate-x-1/4"></div>

        {/* Top Navbar items for right side */}
        <div className="absolute top-8 right-12 z-20">
          <div className="flex items-center space-x-6">
            <Link to="/login" className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors">Log in</Link>
          </div>
        </div>

        {/* Faux Dashboard Container */}
        <div className={`relative z-10 w-full max-w-2xl bg-white/60 backdrop-blur-2xl border border-white/60 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)] rounded-3xl p-8 transform transition-all duration-1000 ease-out group ${mounted ? 'translate-y-0 opacity-100 scale-100' : 'translate-y-24 opacity-0 scale-95'}`}>
          
          {/* Floating UI Elements (Parallax effect) */}
          <div className="absolute -top-12 -right-12 bg-white p-4 rounded-2xl shadow-xl border border-slate-100 animate-bounce transition-transform hover:scale-105" style={{ animationDuration: '4s' }}>
            <div className="flex items-center space-x-4">
              <div className="bg-red-50 p-2.5 rounded-xl border border-red-100">
                <Activity className="w-5 h-5 text-red-600" />
              </div>
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider mb-0.5">Anomaly Detected</p>
                <p className="text-sm font-bold text-slate-900">Uber Eats (+$300.00)</p>
              </div>
            </div>
          </div>

          <div className="absolute -bottom-8 -left-12 bg-slate-900 p-4 rounded-2xl shadow-2xl border border-slate-700 animate-bounce transition-transform hover:scale-105" style={{ animationDuration: '5s', animationDelay: '1s' }}>
            <div className="flex items-center space-x-4">
              <div className="bg-finora-600 p-2.5 rounded-xl border border-finora-500">
                <MessageSquare className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-xs text-finora-300 font-semibold uppercase tracking-wider mb-0.5">Finora AI</p>
                <p className="text-sm font-medium text-white">Your Q3 run rate is down 14%.</p>
              </div>
            </div>
          </div>

          {/* Inner Mockup UI */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h3 className="text-xl font-bold text-slate-900 tracking-tight">Q3 Financial Overview</h3>
              <p className="text-sm text-slate-500 mt-1">Updated just now</p>
            </div>
            <div className="flex space-x-2">
              <div className="w-10 h-10 rounded-full bg-slate-100 border border-slate-200"></div>
              <div className="w-10 h-10 rounded-full bg-slate-100 border border-slate-200"></div>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-3 gap-5 mb-8">
            {[
              { label: 'Total Balance', value: '₹938,298.95', trend: '+2.4%', color: 'text-emerald-600', bg: 'bg-emerald-50' },
              { label: 'Monthly Spend', value: '₹42,150.00', trend: '-1.2%', color: 'text-emerald-600', bg: 'bg-emerald-50' },
              { label: 'Savings Rate', value: '34.2%', trend: '+5.1%', color: 'text-emerald-600', bg: 'bg-emerald-50' },
            ].map((stat, i) => (
              <div key={i} className="bg-white/80 rounded-2xl p-5 border border-slate-100 hover:bg-white hover:shadow-md transition-all duration-300 shadow-sm">
                <p className="text-xs font-semibold text-slate-500 mb-2">{stat.label}</p>
                <p className="text-xl font-extrabold text-slate-900 mb-3">{stat.value}</p>
                <div className={`flex items-center space-x-1 text-xs font-bold ${stat.color} ${stat.bg} w-fit px-2.5 py-1 rounded-full`}>
                  <ArrowRight className="w-3 h-3 -rotate-45" />
                  <span>{stat.trend}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Faux Chart Area */}
          <div className="bg-white/80 rounded-2xl border border-slate-100 p-6 h-56 flex items-end space-x-3 hover:shadow-md transition-shadow">
            {[40, 60, 45, 80, 55, 90, 75, 100, 85, 65, 50, 70].map((height, i) => (
              <div key={i} className="flex-1 bg-slate-100 rounded-t-lg relative group/bar h-full flex flex-col justify-end">
                <div 
                  className={`w-full bg-finora-500 rounded-t-lg transition-all duration-1000 ease-out group-hover/bar:bg-finora-400 ${mounted ? 'h-full' : 'h-0'}`}
                  style={{ height: mounted ? `${height}%` : '0%' }}
                ></div>
                <div className="opacity-0 group-hover/bar:opacity-100 absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-900 text-white text-[11px] font-bold px-2.5 py-1.5 rounded-lg shadow-xl transition-opacity whitespace-nowrap z-30 pointer-events-none">
                  {height}%
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
