"""LLM Client"""
import json
import os
from typing import Dict, Any


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "mock")
        self.model = os.getenv("LLM_MODEL", "gpt-4")
        self.debug = os.getenv("DEBUG", "True") == "True"

    def run_llm(self, prompt: str, context: Dict[str, Any]) -> str:
        try:
            return self.mock_llm_call(prompt, context)
        except Exception as e:
            if self.debug:
                print(f"[LLM ERROR] {str(e)}")
            return json.dumps({"error": str(e), "status": "failed"})

    def mock_llm_call(self, prompt: str, context: Dict[str, Any]) -> str:
        """Mock LLM with smart categorization"""
        prompt_lower = prompt.lower()
        email_body = context.get("email_body", "").lower()
        email_subject = context.get("email_subject", "").lower()

        # CATEGORIZATION
        if "categorize" in prompt_lower:
            if any(kw in email_body for kw in ["$", "budget", "payment", "cost", "funding"]):
                if any(kw in email_body for kw in ["urgent", "asap", "immediately", "confirm"]):
                    return json.dumps({
                        "category": "To-Do",
                        "reason": "Financial matter requiring immediate action"
                    })

            if any(kw in email_body for kw in ["meeting", "schedule", "calendar", "appointment", "call"]):
                return json.dumps({
                    "category": "To-Do",
                    "reason": "Meeting request requiring response"
                })

            if any(kw in email_body for kw in ["urgent", "asap", "critical", "immediate", "deadline"]):
                return json.dumps({
                    "category": "Important",
                    "reason": "Marked as urgent or time-sensitive"
                })

            if any(kw in email_body for kw in ["unsubscribe", "newsletter", "weekly", "digest"]):
                return json.dumps({
                    "category": "Newsletter",
                    "reason": "Newsletter or promotional content"
                })

            if any(kw in email_body + email_subject for kw in [
                "click here", "win", "prize", "lottery", "congratulations",
                "verify account", "limited offer", "act now", "claim"
            ]):
                return json.dumps({
                    "category": "Spam",
                    "reason": "Contains spam indicators and urgency tactics"
                })

            return json.dumps({
                "category": "Important",
                "reason": "Requires attention"
            })

        # ACTION EXTRACTION
        elif "extract" in prompt_lower and "task" in prompt_lower:
            actions = []

            if "meeting" in email_body or "schedule" in email_body:
                actions.append({
                    "task": "Confirm meeting attendance and schedule",
                    "deadline": "2025-11-28"
                })

            if "review" in email_body or "feedback" in email_body:
                actions.append({
                    "task": "Review and provide feedback",
                    "deadline": "2025-11-30"
                })

            if any(kw in email_body for kw in ["submit", "send", "share", "upload"]):
                actions.append({
                    "task": "Complete and submit required items",
                    "deadline": "2025-11-30"
                })

            if "rsvp" in email_body.lower():
                actions.append({
                    "task": "RSVP for event",
                    "deadline": "2025-11-27"
                })

            return json.dumps(actions if actions else [])

        # AUTO-REPLY
        elif "draft" in prompt_lower and "reply" in prompt_lower:
            tone = context.get("tone", "professional")

            if "meeting" in email_body or "schedule" in email_body:
                if tone == "friendly":
                    body = "Hi,\n\nThank you for the meeting invite! I'd be happy to join. Could you please share the agenda and meeting details?\n\nLooking forward to it!\n\nBest regards"
                else:
                    body = "Dear Sir/Madam,\n\nThank you for your email. I confirm my availability for the meeting. Kindly share the agenda and necessary details.\n\nRegards"

                return json.dumps({
                    "subject": f"Re: {context.get('email_subject', 'Meeting')}",
                    "body": body,
                    "suggested_follow_ups": [
                        "Request meeting agenda",
                        "Confirm calendar availability",
                        "Ask about other participants"
                    ]
                })

            elif "partnership" in email_body or "collaboration" in email_body:
                body = "Dear Sir/Madam,\n\nThank you for reaching out. We're interested in exploring this opportunity. Could we schedule a call next week to discuss further?\n\nPlease let me know your availability.\n\nBest regards"

                return json.dumps({
                    "subject": f"Re: {context.get('email_subject', 'Partnership')}",
                    "body": body,
                    "suggested_follow_ups": [
                        "Schedule introductory call",
                        "Share company information",
                        "Discuss terms"
                    ]
                })

            else:
                if tone == "friendly":
                    greeting = "Hi"
                    closing = "Best regards"
                else:
                    greeting = "Dear Sir/Madam"
                    closing = "Regards"

                body = f"{greeting},\n\nThank you for your email. I have received your message and will review it carefully. I'll get back to you shortly.\n\n{closing}"

                return json.dumps({
                    "subject": f"Re: {context.get('email_subject', 'Your Email')}",
                    "body": body,
                    "suggested_follow_ups": [
                        "Provide requested information",
                        "Schedule follow-up"
                    ]
                })

        # SUMMARIZATION
        elif "summarize" in prompt_lower:
            summary_parts = []

            if "$" in email_body or "budget" in email_body:
                summary_parts.append("• Contains financial/budget information")

            if "meeting" in email_body:
                summary_parts.append("• Meeting or schedule request")

            if "deadline" in email_body or "urgent" in email_body:
                summary_parts.append("• Time-sensitive matter")

            summary = "\n".join(summary_parts) if summary_parts else "• General communication"

            return f"**Email Summary:**\n\n{summary}\n\n**Action Required:** Review and respond appropriately."

        # GENERAL QUERY
        elif "query" in context:
            user_query = context.get("query", "").lower()

            if "urgent" in user_query:
                return "Found 2 urgent emails in your inbox:\n1. Budget Meeting - $500K allocation\n2. Performance Review - Deadline Nov 30"
            elif "task" in user_query or "todo" in user_query:
                return "**Your pending tasks:**\n\n1. Meeting confirmation (Due: Nov 28)\n2. Code review feedback (Due: Nov 27)\n3. Performance review (Due: Nov 30)\n4. Speaker presentation (Due: Dec 5)"
            else:
                return f"Processed your query. Please provide more details for better assistance."

        return json.dumps({"response": "Processing complete"})

    def real_llm_call(self, prompt: str, context: Dict[str, Any]) -> str:
        """Real LLM (uncomment to use)"""
        raise NotImplementedError("Configure .env for real LLM")


llm_client = LLMClient()
