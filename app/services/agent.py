"""Email agent"""
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models import Email, PromptConfig, Draft
from app.services.llm_client import llm_client


class EmailAgent:
    def __init__(self):
        self.llm = llm_client

    def run_query(self, user_query: str, selected_email: Optional[Email],
                  all_emails: List[Email], prompts: PromptConfig) -> str:
        try:
            context = self._build_context(user_query, selected_email, all_emails)
            prompt = self._select_prompt(user_query, prompts)
            context["query"] = user_query
            return self.llm.run_llm(prompt, context)
        except Exception as e:
            return f"Error: {str(e)}"

    def _build_context(self, query: str, selected_email: Optional[Email],
                      all_emails: List[Email]) -> Dict[str, Any]:
        context = {}
        if selected_email:
            context = {
                "email_subject": selected_email.subject,
                "email_body": selected_email.body,
                "email_category": selected_email.category,
            }
        return context

    def _select_prompt(self, query: str, prompts: PromptConfig) -> str:
        if "draft" in query.lower() or "reply" in query.lower():
            return prompts.auto_reply_prompt
        return "You are an email assistant. Answer based on context."

    def generate_reply_draft(self, email: Email, prompts: PromptConfig,
                            tone: str = "professional") -> Draft:
        context = {
            "email_subject": email.subject,
            "email_body": email.body,
            "email_sender": email.sender,
            "tone": tone
        }
        response = self.llm.run_llm(prompts.auto_reply_prompt, context)
        try:
            data = json.loads(response)
            return Draft(
                id=f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                email_id=email.id,
                subject=data.get("subject", f"Re: {email.subject}"),
                body=data.get("body", ""),
                metadata={"suggested_follow_ups": data.get("suggested_follow_ups", [])},
                created_at=datetime.now().isoformat()
            )
        except:
            return Draft(
                id=f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                email_id=email.id,
                subject=f"Re: {email.subject}",
                body="Thank you for your email. I will respond shortly.",
                metadata={},
                created_at=datetime.now().isoformat()
            )

    def generate_new_draft(self, prompts: PromptConfig, instruction: str,
                          to: str = "", subject: str = "") -> Draft:
        response = self.llm.run_llm("Generate email", {
            "instruction": instruction, "to": to, "subject": subject
        })
        try:
            data = json.loads(response)
            return Draft(
                id=f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                email_id=None,
                subject=data.get("subject", subject or "New Email"),
                body=data.get("body", ""),
                metadata={},
                created_at=datetime.now().isoformat()
            )
        except:
            return Draft(
                id=f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                email_id=None,
                subject=subject or "New Email",
                body=instruction,
                metadata={},
                created_at=datetime.now().isoformat()
            )


email_agent = EmailAgent()
