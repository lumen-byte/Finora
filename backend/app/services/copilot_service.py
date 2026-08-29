import json
import os
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from openai import OpenAI

from backend.app.core.config import settings
from backend.app.models.copilot import Role
from backend.app.repositories.copilot_repository import CopilotRepository
from backend.app.services.analytics_service import AnalyticsService
from backend.app.services.recurring_detection_service import RecurringDetectionService
from backend.app.services.anomaly_detection_service import AnomalyDetectionService
from backend.app.services.insight_service import InsightService

class CopilotService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = CopilotRepository(session)
        self.analytics = AnalyticsService(session)
        self.recurring = RecurringDetectionService(session)
        self.anomaly = AnomalyDetectionService(session)
        self.insight = InsightService(session)
        
        # Initialize OpenAI client for Groq
        api_key = settings.GROQ_API_KEY
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        ) if api_key else None
        self.model = settings.GROQ_MODEL

    def _get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_dashboard_summary",
                    "description": "Get a high-level summary of the user's finances for the current month, including total balance, income, expenses, net cash flow, savings rate, and percentage changes from the previous month.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_category_breakdown",
                    "description": "Get a breakdown of expenses grouped by category for the current month.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_month_comparison",
                    "description": "Compare spending this month vs last month, including detailed category-by-category changes.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_monthly_trends",
                    "description": "Get month-over-month historical trends for income, expenses, and cash flow.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_top_merchants",
                    "description": "Get the user's top merchants where they spend the most money.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_recurring_transactions",
                    "description": "Detect subscriptions, rent, and other recurring transactions and bills.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_anomalies",
                    "description": "Detect highly unusual or suspicious spending anomalies based on historical spending.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_financial_insights",
                    "description": "Generate rule-based financial advice and insights based on the user's data.",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]

    def _execute_tool(self, name: str, user_id: UUID) -> Any:
        today = date.today()
        year = today.year
        month = today.month
        start_date = date(year, month, 1)
        end_date = today

        if name == "get_dashboard_summary":
            return self.analytics.get_dashboard(user_id, year, month).model_dump()
        elif name == "get_category_breakdown":
            return [x.model_dump() for x in self.analytics.get_category_breakdown(user_id, start_date, end_date)]
        elif name == "get_month_comparison":
            return self.analytics.get_month_comparison(user_id, year, month).model_dump()
        elif name == "get_monthly_trends":
            return [x.model_dump() for x in self.analytics.get_monthly_trends(user_id)]
        elif name == "get_top_merchants":
            return [x.model_dump() for x in self.analytics.get_top_merchants(user_id, start_date, end_date)]
        elif name == "get_recurring_transactions":
            res = []
            for item in self.recurring.detect_recurring(user_id):
                d = item.model_dump()
                if d["estimated_next_date"]:
                    d["estimated_next_date"] = str(d["estimated_next_date"])
                res.append(d)
            return res
        elif name == "get_anomalies":
            res = []
            for item in self.anomaly.detect_anomalies(user_id):
                d = item.model_dump()
                d["transaction"]["transaction_date"] = str(d["transaction"]["transaction_date"])
                if d["transaction"].get("created_at"):
                    d["transaction"]["created_at"] = str(d["transaction"]["created_at"])
                if d["transaction"].get("updated_at"):
                    d["transaction"]["updated_at"] = str(d["transaction"]["updated_at"])
                res.append(d)
            return res
        elif name == "get_financial_insights":
            return [x.model_dump() for x in self.insight.generate_insights(user_id)]
        else:
            return {"error": f"Unknown tool: {name}"}

    def chat(self, user_id: UUID, message: str, conversation_id: Optional[UUID] = None) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("OPENAI_API_KEY is not configured.")

        # 1. Manage Conversation
        if conversation_id:
            conversation = self.repo.get_conversation(conversation_id, user_id)
            if not conversation:
                raise ValueError("Conversation not found or unauthorized.")
        else:
            title = message[:40] + ("..." if len(message) > 40 else "")
            conversation = self.repo.create_conversation(user_id, title=title)
            conversation_id = conversation.id

        # 2. Save user message
        self.repo.add_message(conversation_id, Role.USER, message)

        # 3. Retrieve history
        recent_messages = self.repo.get_recent_messages(conversation_id, limit=10)
        
        system_prompt = {
            "role": "system",
            "content": (
                "You are Finora, a financial intelligence assistant. "
                "Only use the financial data provided through tools or structured context. "
                "Never invent transaction amounts, balances, trends, or financial events. "
                "If sufficient data is not available, clearly say so. "
                "Phrase suggestions as informational observations rather than personalized professional financial advice. "
                "IMPORTANT: All monetary values MUST be formatted with the Indian Rupee symbol (₹) instead of the Dollar sign ($). "
                "IMPORTANT: Provide your final response directly. Do not include any internal reasoning, thoughts, or <think> tags in your output."
            )
        }

        messages_for_llm = [system_prompt]
        for msg in recent_messages:
            role = "user" if msg.role == Role.USER else "assistant"
            messages_for_llm.append({"role": role, "content": msg.content})

        tools_used = []

        # 4. Call OpenAI with tools
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages_for_llm,
            tools=self._get_tools(),
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # 5. Handle Tool Calls
        if response_message.tool_calls:
            messages_for_llm.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                tools_used.append(function_name)
                
                tool_result = self._execute_tool(function_name, user_id)
                
                messages_for_llm.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(tool_result, default=str)
                })
                
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages_for_llm
            )
            final_answer = second_response.choices[0].message.content
        else:
            final_answer = response_message.content

        # 6. Save assistant message
        if final_answer:
            self.repo.add_message(conversation_id, Role.ASSISTANT, final_answer)

        return {
            "conversation_id": conversation_id,
            "answer": final_answer or "I could not process your request.",
            "tools_used": tools_used
        }
