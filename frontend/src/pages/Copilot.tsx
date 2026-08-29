import { useState, useEffect, useRef } from 'react';
import { Card } from '../components/ui/Card';
import { Bot, Send, BrainCircuit, MessageSquare, Loader2, Plus, Trash2, AlertCircle } from 'lucide-react';
import { apiClient } from '../api/client';
import type { CopilotConversation, CopilotMessage } from '../types';
import { cn } from '../utils/cn';

const TOOL_NAMES: Record<string, string> = {
  get_dashboard_summary: "Financial Overview",
  get_category_breakdown: "Spending Analysis",
  get_month_comparison: "Month Comparison",
  get_recurring_transactions: "Recurring Expense Detection",
  get_anomalies: "Anomaly Detection",
  get_top_merchants: "Merchant Analysis"
};

export default function Copilot() {
  const [conversations, setConversations] = useState<CopilotConversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [messages, setMessages] = useState<CopilotMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingConversations, setLoadingConversations] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (activeId) {
      fetchMessages(activeId);
    } else {
      setMessages([]);
    }
  }, [activeId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const fetchConversations = async () => {
    try {
      const res = await apiClient.get('/copilot/conversations');
      setConversations(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingConversations(false);
    }
  };

  const fetchMessages = async (id: string) => {
    try {
      const res = await apiClient.get(`/copilot/conversations/${id}`);
      setMessages(res.data.messages || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = input;
    setInput('');
    const tempId = Date.now().toString();
    setMessages(prev => [...prev, { id: tempId, role: 'USER', content: userMessage, created_at: new Date().toISOString() }]);
    setLoading(true);

    try {
      const payload: any = { message: userMessage };
      if (activeId) payload.conversation_id = activeId;

      const res = await apiClient.post('/copilot/chat', payload);
      
      if (!activeId) {
        setActiveId(res.data.conversation_id);
        fetchConversations();
      }

      // Instead of raw parsing, we assume backend adds tools_used to the message natively or we format it elegantly
      let content = res.data.answer;
      if (res.data.tools_used && res.data.tools_used.length > 0) {
         const badges = res.data.tools_used.map((t: string) => `[TOOL_USED:${t}]`).join(' ');
         content = `${content}\n\n${badges}`;
      }

      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'ASSISTANT', content, created_at: new Date().toISOString() }]);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || "Sorry, I encountered an error connecting to the AI. Please verify OPENAI_API_KEY is configured correctly.";
      setMessages(prev => [...prev, { 
        id: Date.now().toString(), 
        role: 'ASSISTANT', 
        content: `[ERROR] ${errorMsg}`, 
        created_at: new Date().toISOString() 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await apiClient.delete(`/copilot/conversations/${id}`);
      setConversations(prev => prev.filter(c => c.id !== id));
      if (activeId === id) setActiveId(null);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex h-[calc(100vh-100px)] gap-6">
      <Card className="w-80 flex flex-col p-4 shadow-sm border-slate-200">
        <button 
          onClick={() => setActiveId(null)}
          className="w-full bg-finora-50 text-finora-700 py-2.5 rounded-lg font-medium flex items-center justify-center mb-4 hover:bg-finora-100 transition-colors"
        >
          <Plus className="w-5 h-5 mr-2" /> New Chat
        </button>
        <div className="flex-1 overflow-y-auto space-y-2">
          {loadingConversations ? (
            <div className="animate-pulse space-y-3">
              <div className="h-10 bg-slate-100 rounded-lg"></div>
              <div className="h-10 bg-slate-100 rounded-lg"></div>
            </div>
          ) : (
            conversations.map(c => (
              <div 
                key={c.id} 
                onClick={() => setActiveId(c.id)}
                className={cn(
                  "p-3 rounded-lg cursor-pointer group flex justify-between items-center transition-colors",
                  activeId === c.id ? "bg-slate-100" : "hover:bg-slate-50"
                )}
              >
                <div className="truncate text-sm font-medium text-slate-700">
                  <MessageSquare className="inline w-4 h-4 mr-2 text-slate-400" />
                  {c.title || 'New Conversation'}
                </div>
                <button onClick={(e) => handleDelete(c.id, e)} className="text-slate-400 hover:text-rose-500 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))
          )}
        </div>
      </Card>

      <Card className="flex-1 flex flex-col p-0 overflow-hidden relative shadow-sm border-slate-200">
        {!activeId && messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8 bg-slate-50/50">
            <div className="w-16 h-16 bg-finora-50 text-finora-600 rounded-2xl flex items-center justify-center mb-6 shadow-sm">
              <BrainCircuit className="w-8 h-8" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">FinoraAI</h2>
            <p className="text-slate-600 max-w-md mb-8">
              Ask me anything about your finances. I use your actual data to give grounded, deterministic answers.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl w-full">
              {[
                "How are my finances this month?",
                "Where am I spending the most?",
                "What subscriptions do I have?",
                "Did anything unusual happen?",
                "Compare this month with last month."
              ].map(q => (
                <button 
                  key={q}
                  onClick={() => {
                    setInput(q);
                  }}
                  className="p-4 bg-white border border-slate-200 rounded-xl text-sm font-medium text-slate-700 hover:border-finora-300 hover:bg-finora-50 hover:shadow-sm transition-all text-left"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/30">
            {messages.map((msg, idx) => {
              const isAssistant = msg.role === 'ASSISTANT';
              const isError = msg.content.startsWith('[ERROR]');
              
              if (isError) {
                return (
                  <div key={idx} className="flex justify-start">
                    <div className="flex max-w-[80%] rounded-2xl p-4 shadow-sm bg-rose-50 border border-rose-100 text-rose-800">
                      <div className="w-8 h-8 bg-rose-100 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                        <AlertCircle className="w-5 h-5 text-rose-600" />
                      </div>
                      <div className="text-sm leading-relaxed mt-1.5 font-medium">
                        {msg.content.replace('[ERROR] ', '')}
                      </div>
                    </div>
                  </div>
                );
              }

              return (
                <div key={idx} className={cn("flex", isAssistant ? "justify-start" : "justify-end")}>
                  <div className={cn(
                    "flex max-w-[80%] rounded-2xl p-4 shadow-sm",
                    isAssistant ? "bg-white border border-slate-200 text-slate-800" : "bg-finora-600 text-white"
                  )}>
                    {isAssistant && (
                      <div className="w-8 h-8 bg-finora-50 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                        <Bot className="w-5 h-5 text-finora-600" />
                      </div>
                    )}
                    <div className="text-sm leading-relaxed whitespace-pre-wrap">
                      {msg.content.split(/(\[TOOL_USED:.*?\])/).map((part, i) => {
                        if (part.startsWith('[TOOL_USED:')) {
                          const toolRaw = part.replace('[TOOL_USED:', '').replace(']', '').trim();
                          const humanName = TOOL_NAMES[toolRaw] || toolRaw;
                          return (
                            <span key={i} className="inline-flex items-center px-2.5 py-1.5 bg-finora-50 text-finora-700 text-xs font-semibold rounded-md mr-1.5 mt-3 border border-finora-100 shadow-sm" title={`Backend Tool: ${toolRaw}`}>
                              <BrainCircuit className="w-3.5 h-3.5 mr-1.5" />
                              Analyzed using: {humanName}
                            </span>
                          );
                        }
                        return <span key={i}>{part}</span>;
                      })}
                    </div>
                  </div>
                </div>
              );
            })}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center">
                  <div className="w-8 h-8 bg-finora-50 rounded-full flex items-center justify-center mr-3">
                    <Bot className="w-5 h-5 text-finora-600" />
                  </div>
                  <Loader2 className="w-5 h-5 text-slate-400 animate-spin mr-2" />
                  <span className="text-sm text-slate-500 font-medium">Finora is analyzing your financial data...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        <div className="p-4 bg-white border-t border-slate-200">
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
            className="flex items-center max-w-4xl mx-auto relative"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
              placeholder="Ask about your finances..."
              className="w-full bg-slate-50 border border-slate-200 rounded-full pl-6 pr-14 py-3.5 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-finora-500 focus:border-transparent transition-all shadow-inner disabled:opacity-50"
            />
            <button 
              type="submit" 
              disabled={loading || !input.trim()}
              className="absolute right-2 p-2 bg-finora-600 text-white rounded-full hover:bg-finora-700 disabled:opacity-50 transition-colors shadow-sm"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>
      </Card>
    </div>
  );
}
