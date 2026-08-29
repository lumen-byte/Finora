export interface User {
  id: string;
  email: string;
  full_name?: string;
}

export interface DashboardMetrics {
  total_balance: number;
  total_income: number;
  total_expenses: number;
  net_cash_flow: number;
  savings_rate: number;
  income_change_percentage?: number;
  expense_change_percentage?: number;
  cash_flow_change_percentage?: number;
}

export interface CategoryBreakdown {
  category: string;
  total_amount: number;
  transaction_count: number;
  percentage_of_total_expenses: number;
}

export interface MonthlyTrend {
  month: string;
  income: number;
  expenses: number;
  cash_flow: number;
}

export interface TopMerchant {
  merchant: string;
  total_amount: number;
  transaction_count: number;
}

export interface RecurringTransaction {
  merchant: string;
  average_amount: number;
  frequency: string;
  estimated_next_date?: string;
  transaction_count: number;
  confidence_score: number;
}

export interface Anomaly {
  transaction: any;
  expected_amount: number;
  deviation_percentage: number;
  reason: string;
}

export interface Insight {
  id: string;
  title: string;
  message: string;
  severity: 'INFO' | 'WARNING' | 'IMPORTANT';
  related_category?: string;
  related_transaction_id?: string;
}

export interface Transaction {
  id: string;
  amount: number;
  transaction_date: string;
  merchant: string;
  description?: string;
  transaction_type: string;
  category?: { name: string };
  account?: { name: string };
}

export interface Account {
  id: string;
  name: string;
  account_type: string;
  current_balance: number;
  currency: string;
}

export interface CopilotMessage {
  id: string;
  role: 'USER' | 'ASSISTANT';
  content: string;
  created_at: string;
}

export interface CopilotConversation {
  id: string;
  title?: string;
  updated_at: string;
  messages?: CopilotMessage[];
}
