import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Hexagon, Lock, Mail, User, Loader2, ArrowRight } from 'lucide-react';
import { apiClient } from '../api/client';
import { useAuth } from '../contexts/AuthContext';

export default function Register() {
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await apiClient.post('/auth/register', {
        email,
        password,
        full_name: fullName
      });

      // Auto-login after successful registration
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const loginResponse = await apiClient.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      login(loginResponse.data.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      console.error(err);
      if (err.response?.status === 400) {
        setError(err.response.data.detail || 'Registration failed.');
      } else {
        setError('An error occurred during registration. Please try again later.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex font-sans">
      {/* Left side: Premium Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-slate-900 overflow-hidden">
        {/* Abstract Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-finora-900 via-slate-900 to-black"></div>
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-finora-600/30 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-finora-900/40 rounded-full blur-[100px]"></div>
        
        <div className="relative z-10 flex flex-col justify-between p-16 w-full h-full">
          <Link to="/" className="flex items-center space-x-3 group w-fit">
            <div className="bg-white/10 p-2 rounded-xl backdrop-blur-md border border-white/10 group-hover:bg-white/20 transition-all">
              <Hexagon className="w-8 h-8 text-white fill-finora-500" />
            </div>
            <span className="text-3xl font-bold tracking-tight text-white">Finora</span>
          </Link>

          <div className="max-w-lg">
            <h1 className="text-4xl font-bold text-white mb-6 leading-tight">
              Start mastering your corporate spend today.
            </h1>
            <p className="text-lg text-slate-300 mb-8 leading-relaxed">
              Join leading finance teams using deterministic AI and real-time ledger sync to control their budgets.
            </p>
            <div className="grid grid-cols-2 gap-6 text-sm font-medium text-finora-400 mt-8 border-t border-white/10 pt-8">
              <div>
                <div className="text-2xl font-bold text-white mb-1">100%</div>
                <div>Deterministic AI accuracy</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white mb-1">&lt;50ms</div>
                <div>Avg query latency</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right side: Registration Form */}
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-20 xl:px-24 bg-white relative">
        <div className="mx-auto w-full max-w-sm lg:w-[400px]">
          {/* Mobile logo */}
          <div className="flex lg:hidden items-center justify-center space-x-2 mb-10">
            <Hexagon className="w-10 h-10 text-finora-600 fill-finora-100" />
            <span className="text-3xl font-bold tracking-tight text-slate-900">Finora</span>
          </div>

          <div>
            <h2 className="text-3xl font-bold tracking-tight text-slate-900">
              Create an account
            </h2>
            <p className="mt-2 text-sm text-slate-500">
              Set up your workspace to get started.
            </p>
          </div>

          <div className="mt-8">
            <form className="space-y-6" onSubmit={handleRegister}>
              <div>
                <label htmlFor="fullName" className="block text-sm font-medium text-slate-700">
                  Full Name
                </label>
                <div className="mt-2 relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    id="fullName"
                    name="fullName"
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="block w-full pl-10 pr-3 py-3 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-finora-500/20 focus:border-finora-500 sm:text-sm transition-all duration-200 ease-in-out outline-none"
                    placeholder="Jane Doe"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-700">
                  Work Email
                </label>
                <div className="mt-2 relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full pl-10 pr-3 py-3 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-finora-500/20 focus:border-finora-500 sm:text-sm transition-all duration-200 ease-in-out outline-none"
                    placeholder="jane@company.com"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-slate-700">
                  Password
                </label>
                <div className="mt-2 relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="new-password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="block w-full pl-10 pr-3 py-3 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-finora-500/20 focus:border-finora-500 sm:text-sm transition-all duration-200 ease-in-out outline-none"
                    placeholder="••••••••"
                  />
                </div>
                <p className="mt-2 text-xs text-slate-500">Must be at least 8 characters.</p>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-100 text-red-600 text-sm p-3 rounded-xl flex items-center shadow-sm">
                  {error}
                </div>
              )}

              <div>
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex justify-center items-center space-x-2 py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-finora-600 hover:bg-finora-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-finora-500 transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed group"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      <span>Create account</span>
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </>
                  )}
                </button>
              </div>
            </form>

            <div className="mt-8 text-center text-sm text-slate-500">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-finora-600 hover:text-finora-700 transition-colors">
                Sign in
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
