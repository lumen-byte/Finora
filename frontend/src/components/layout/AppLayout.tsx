import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { 
  LayoutDashboard, 
  BarChart3, 
  Receipt, 
  Lightbulb, 
  MessageSquare, 
  Landmark,
  LogOut,
  Hexagon,
  Menu,
  X
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import DemoGuide from '../ui/DemoGuide';

function cn(...inputs: (string | undefined | null | false)[]) {
  return twMerge(clsx(inputs));
}

const navItems = [
  { path: '/dashboard', label: 'Overview', icon: LayoutDashboard },
  { path: '/transactions', label: 'Transactions', icon: Receipt },
  { path: '/analytics', label: 'Analytics', icon: BarChart3 },
  { path: '/insights', label: 'Insights', icon: Lightbulb },
  { path: '/copilot', label: 'FinoraAI', icon: MessageSquare },
  { path: '/accounts', label: 'Accounts', icon: Landmark },
];

export default function AppLayout() {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('finora_token');
    navigate('/');
  };

  const closeSidebar = () => setMobileOpen(false);

  return (
    <div className="flex h-screen bg-slate-50 relative">
      
      {/* Mobile Sidebar Overlay */}
      {mobileOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/50 z-20 lg:hidden"
          onClick={closeSidebar}
        />
      )}

      {/* Sidebar */}
      <aside className={cn(
        "fixed lg:static inset-y-0 left-0 w-64 bg-white border-r border-slate-200 flex flex-col shadow-sm z-30 transition-transform duration-200 ease-in-out",
        mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}>
        <div className="h-16 flex items-center justify-between px-6 border-b border-slate-100">
          <div className="flex items-center">
            <Hexagon className="w-6 h-6 text-finora-600 mr-2 fill-finora-100" />
            <span className="text-xl font-bold tracking-tight text-slate-900">Finora</span>
          </div>
          <button className="lg:hidden text-slate-500 hover:text-slate-900" onClick={closeSidebar}>
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={closeSidebar}
              className={({ isActive }) =>
                cn(
                  "flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                  isActive 
                    ? "bg-finora-50 text-finora-700" 
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                )
              }
            >
              <item.icon className={cn("w-5 h-5 mr-3 flex-shrink-0", window.location.pathname === item.path ? "text-finora-600" : "text-slate-400")} />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-100">
          <button
            onClick={handleLogout}
            className="flex items-center w-full px-3 py-2.5 text-sm font-medium text-slate-600 rounded-lg hover:bg-slate-50 hover:text-slate-900 transition-colors"
          >
            <LogOut className="w-5 h-5 mr-3 text-slate-400" />
            Logout
          </button>
        </div>
      </aside>

      <main className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* Mobile Header */}
        <div className="lg:hidden h-16 bg-white border-b border-slate-200 flex items-center px-4 shrink-0">
          <button onClick={() => setMobileOpen(true)} className="p-2 -ml-2 text-slate-600 hover:text-slate-900">
            <Menu className="w-6 h-6" />
          </button>
          <div className="flex items-center ml-2">
            <Hexagon className="w-5 h-5 text-finora-600 mr-2 fill-finora-100" />
            <span className="text-lg font-bold tracking-tight text-slate-900">Finora</span>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 sm:p-8">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </div>
      </main>
      <DemoGuide />
    </div>
  );
}
