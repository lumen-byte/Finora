import { useState, useEffect } from 'react';
import { X, PlayCircle, BarChart3, MessageSquare, Lightbulb, Receipt } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function DemoGuide() {
  const [isVisible, setIsVisible] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const hasSeen = localStorage.getItem('finora_demo_seen');
    if (!hasSeen) {
      setIsVisible(true);
    }
  }, []);

  const dismiss = () => {
    setIsVisible(false);
    localStorage.setItem('finora_demo_seen', 'true');
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-6 right-6 w-96 bg-white rounded-2xl shadow-2xl border border-slate-200 z-50 overflow-hidden flex flex-col">
      <div className="bg-finora-600 px-5 py-4 flex items-center justify-between">
        <h3 className="text-white font-semibold flex items-center">
          <PlayCircle className="w-5 h-5 mr-2" />
          Welcome to the Finora Demo
        </h3>
        <button onClick={dismiss} className="text-white/80 hover:text-white transition-colors">
          <X className="w-5 h-5" />
        </button>
      </div>
      
      <div className="p-5 space-y-4">
        <p className="text-sm text-slate-600 leading-relaxed">
          Finora is fully populated with 6 months of deterministic financial data. Try exploring:
        </p>
        
        <ul className="space-y-3">
          <li>
            <button onClick={() => navigate('/dashboard')} className="flex items-start text-left group">
              <BarChart3 className="w-4 h-4 mr-2 text-finora-500 mt-0.5 group-hover:text-finora-600 transition-colors" />
              <span className="text-sm font-medium text-slate-700 group-hover:text-finora-600 transition-colors">Dashboard & Analytics</span>
            </button>
          </li>
          <li>
            <button onClick={() => navigate('/insights')} className="flex items-start text-left group">
              <Lightbulb className="w-4 h-4 mr-2 text-finora-500 mt-0.5 group-hover:text-finora-600 transition-colors" />
              <span className="text-sm font-medium text-slate-700 group-hover:text-finora-600 transition-colors">Insights (Anomalies & Subscriptions)</span>
            </button>
          </li>
          <li>
            <button onClick={() => navigate('/copilot')} className="flex items-start text-left group">
              <MessageSquare className="w-4 h-4 mr-2 text-finora-500 mt-0.5 group-hover:text-finora-600 transition-colors" />
              <span className="text-sm font-medium text-slate-700 group-hover:text-finora-600 transition-colors">FinoraAI</span>
            </button>
          </li>
        </ul>

        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
          <p className="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wider">Try asking the AI:</p>
          <p className="text-xs italic text-slate-600">"Why did I spend more this month?"</p>
          <p className="text-xs italic text-slate-600 mt-1">"Did anything unusual happen?"</p>
        </div>

        <button 
          onClick={dismiss}
          className="w-full bg-slate-100 hover:bg-slate-200 text-slate-700 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          Got it
        </button>
      </div>
    </div>
  );
}
