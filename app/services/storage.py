"""Storage service"""
import json
from pathlib import Path
from typing import List
from app.models import PromptConfig, Draft, Email


class StorageService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.prompts_file = self.data_dir / "default_prompts.json"
        self.drafts_file = self.data_dir / "drafts.json"
        self.inbox_file = self.data_dir / "mock_inbox.json"
        self.data_dir.mkdir(exist_ok=True)

    def load_prompts(self) -> PromptConfig:
        try:
            if self.prompts_file.exists():
                with open(self.prompts_file, 'r', encoding='utf-8') as f:
                    return PromptConfig(**json.load(f))
            return self.get_default_prompts()
        except:
            return self.get_default_prompts()

    def save_prompts(self, prompts: PromptConfig) -> bool:
        try:
            with open(self.prompts_file, 'w', encoding='utf-8') as f:
                json.dump(prompts.model_dump(), f, indent=2)
            return True
        except:
            return False

    def get_default_prompts(self) -> PromptConfig:
        return PromptConfig(
            categorization_prompt="Categorize emails into: Important, Newsletter, Spam, To-Do. To-Do emails must include a direct request requiring user action. Respond with JSON: { \"category\": \"Important|Newsletter|Spam|To-Do\", \"reason\": \"...\" }.",
            action_item_prompt="Extract tasks from the email. Respond in JSON array: [ { \"task\": \"...\", \"deadline\": \"...\" }, ... ]. If no clear deadline, set deadline to null.",
            auto_reply_prompt="If an email is a meeting request, draft a polite reply asking for an agenda. Otherwise, write a brief, polite reply that acknowledges the email and suggests next steps. Reply in JSON: { \"subject\": \"...\", \"body\": \"...\", \"suggested_follow_ups\": [\"...\"] }."
        )

    def load_drafts(self) -> List[Draft]:
        try:
            if self.drafts_file.exists():
                with open(self.drafts_file, 'r', encoding='utf-8') as f:
                    return [Draft(**d) for d in json.load(f)]
            return []
        except:
            return []

    def save_draft(self, draft: Draft) -> bool:
        try:
            drafts = self.load_drafts()
            drafts = [d for d in drafts if d.id != draft.id] + [draft]
            with open(self.drafts_file, 'w', encoding='utf-8') as f:
                json.dump([d.model_dump() for d in drafts], f, indent=2)
            return True
        except:
            return False

    def delete_draft(self, draft_id: str) -> bool:
        try:
            drafts = [d for d in self.load_drafts() if d.id != draft_id]
            with open(self.drafts_file, 'w', encoding='utf-8') as f:
                json.dump([d.model_dump() for d in drafts], f, indent=2)
            return True
        except:
            return False

    def load_inbox(self) -> List[Email]:
        try:
            if self.inbox_file.exists():
                with open(self.inbox_file, 'r', encoding='utf-8') as f:
                    return [Email(**e) for e in json.load(f)]
            return []
        except:
            return []


storage = StorageService()
