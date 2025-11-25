"""Email processing"""
import json
from typing import List, Dict, Any
from app.models import Email, PromptConfig
from app.services.llm_client import llm_client


class EmailProcessor:
    def __init__(self):
        self.llm = llm_client

    def process_emails(self, emails: List[Email], prompts: PromptConfig) -> List[Email]:
        processed = []
        for email in emails:
            try:
                result = self.categorize_email(email, prompts.categorization_prompt)
                email.category = result.get("category", "Important")
                email.actions = self.extract_actions(email, prompts.action_item_prompt)
                processed.append(email)
            except:
                email.category = "Important"
                email.actions = []
                processed.append(email)
        return processed

    def categorize_email(self, email: Email, prompt: str) -> Dict[str, Any]:
        context = {
            "email_subject": email.subject,
            "email_body": email.body,
            "email_sender": email.sender
        }
        response = self.llm.run_llm(prompt, context)
        try:
            return json.loads(response)
        except:
            return {"category": "Important", "reason": "Error"}

    def extract_actions(self, email: Email, prompt: str) -> List[Dict[str, Any]]:
        context = {
            "email_subject": email.subject,
            "email_body": email.body
        }
        response = self.llm.run_llm(prompt, context)
        try:
            actions = json.loads(response)
            return actions if isinstance(actions, list) else []
        except:
            return []


email_processor = EmailProcessor()
