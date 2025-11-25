"""
Email Productivity Agent - Dark Theme Edition
Smart Email Management System
"""
import streamlit as st
from datetime import datetime
from typing import Optional
from app.models import Email, PromptConfig, Draft
from app.services.storage import storage
from app.services.email_processing import email_processor
from app.services.agent import email_agent


# Page configuration
st.set_page_config(
    page_title="📧 Email Agent Pro",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme custom CSS
def load_custom_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Dark theme colors */
    :root {
        --bg-dark: #0E1117;
        --bg-secondary: #1A1D24;
        --bg-tertiary: #262B35;
        --accent-primary: #6366F1;
        --accent-secondary: #8B5CF6;
        --accent-success: #10B981;
        --accent-warning: #F59E0B;
        --accent-danger: #EF4444;
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --border-color: #374151;
    }

    /* Main background */
    .main {
        background: linear-gradient(135deg, #0E1117 0%, #1A1D24 100%);
        color: var(--text-primary);
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }

    h1 {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 3px solid var(--accent-primary);
        padding-bottom: 12px !important;
        margin-bottom: 24px !important;
    }

    /* Sidebar dark theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1D24 0%, #262B35 100%) !important;
        border-right: 1px solid var(--border-color);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: none !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
        background: linear-gradient(135deg, #7C3AED, #A78BFA) !important;
    }

    /* Email cards with dark theme */
    .email-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--accent-primary);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .email-card:hover {
        transform: translateX(8px);
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.3);
        border-left-color: var(--accent-secondary);
        background: var(--bg-tertiary);
    }

    /* Category badges */
    .badge {
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85em;
        display: inline-block;
        margin: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-important {
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: white;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }

    .badge-todo {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }

    .badge-newsletter {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        color: white;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }

    .badge-spam {
        background: linear-gradient(135deg, #6B7280, #4B5563);
        color: white;
        box-shadow: 0 2px 8px rgba(107, 114, 128, 0.3);
    }

    /* Input fields dark theme */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: var(--bg-tertiary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 12px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }

    /* Tabs dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        color: var(--text-secondary);
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white !important;
        border-color: var(--accent-primary);
    }

    /* Chat messages */
    .chat-message {
        padding: 16px;
        margin: 12px 0;
        border-radius: 12px;
        border-left: 4px solid;
    }

    .chat-user {
        background: var(--bg-secondary);
        border-color: var(--accent-primary);
        border-left-width: 4px;
    }

    .chat-agent {
        background: var(--bg-tertiary);
        border-color: var(--accent-success);
        border-left-width: 4px;
    }

    /* Metric cards */
    .metric-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border-top: 3px solid var(--accent-primary);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
    }

    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        font-size: 1em;
        color: var(--text-secondary);
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Success/Error/Warning messages */
    .stSuccess {
        background: linear-gradient(135deg, #10B981, #059669) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 16px !important;
        border-left: 4px solid #047857 !important;
    }

    .stError {
        background: linear-gradient(135deg, #EF4444, #DC2626) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 16px !important;
        border-left: 4px solid #B91C1C !important;
    }

    .stWarning {
        background: linear-gradient(135deg, #F59E0B, #D97706) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 16px !important;
        border-left: 4px solid #B45309 !important;
    }

    .stInfo {
        background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 16px !important;
        border-left: 4px solid #1D4ED8 !important;
    }

    /* Scrollbar dark theme */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7C3AED, #A78BFA);
    }

    /* Expander dark theme */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    .streamlit-expanderHeader:hover {
        background: var(--bg-tertiary) !important;
        border-color: var(--accent-primary) !important;
    }

    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, var(--accent-primary), transparent);
        margin: 32px 0;
    }

    /* Content boxes */
    .content-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_custom_css()


# Session state
def init_session_state():
    if "emails" not in st.session_state:
        st.session_state.emails = []
    if "prompts" not in st.session_state:
        st.session_state.prompts = storage.load_prompts()
    if "drafts" not in st.session_state:
        st.session_state.drafts = storage.load_drafts()
    if "selected_email_id" not in st.session_state:
        st.session_state.selected_email_id = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "inbox_loaded" not in st.session_state:
        st.session_state.inbox_loaded = False
    if "chat_input_key" not in st.session_state:
        st.session_state.chat_input_key = 0


def get_selected_email() -> Optional[Email]:
    if st.session_state.selected_email_id:
        for email in st.session_state.emails:
            if email.id == st.session_state.selected_email_id:
                return email
    return None


def load_inbox():
    try:
        emails = storage.load_inbox()
        if emails:
            st.session_state.emails = emails
            st.session_state.inbox_loaded = True
            st.success(f"✅ Successfully loaded {len(emails)} emails")
        else:
            st.error("❌ No emails found")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def process_inbox():
    if not st.session_state.emails:
        st.warning("⚠️ Please load inbox first")
        return

    try:
        with st.spinner("Processing emails..."):
            st.session_state.emails = email_processor.process_emails(
                st.session_state.emails,
                st.session_state.prompts
            )
        st.success("✅ All emails processed successfully!")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def save_prompts():
    try:
        if storage.save_prompts(st.session_state.prompts):
            st.success("✅ Prompts saved successfully!")
        else:
            st.error("❌ Failed to save prompts")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def render_sidebar():
    st.sidebar.markdown("# 📧 Email Agent Pro")
    st.sidebar.markdown("### Control Panel")
    st.sidebar.markdown("---")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📥 Load Inbox", use_container_width=True, key="load_btn"):
            load_inbox()

    with col2:
        if st.button("⚡ Process", use_container_width=True, key="process_btn"):
            process_inbox()

    if st.session_state.inbox_loaded:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Statistics")

        total = len(st.session_state.emails)
        categorized = len([e for e in st.session_state.emails if e.category])
        todos = len([e for e in st.session_state.emails if e.category == "To-Do"])

        st.sidebar.metric("Total Emails", total)
        st.sidebar.metric("Categorized", categorized)
        st.sidebar.metric("Action Items", todos, delta=f"{todos} pending")

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🏷️ Filter")
        categories = list(set([e.category for e in st.session_state.emails if e.category]))
        if categories:
            selected_cats = st.sidebar.multiselect(
                "Select categories",
                options=categories,
                default=categories
            )
            return selected_cats

    return None


def get_category_badge(category: str) -> str:
    badge_map = {
        "Important": ("🔴", "badge-important"),
        "To-Do": ("📝", "badge-todo"),
        "Newsletter": ("📰", "badge-newsletter"),
        "Spam": ("🗑️", "badge-spam")
    }
    emoji, css_class = badge_map.get(category, ("📧", "badge"))
    return f'<span class="badge {css_class}">{emoji} {category}</span>'


def render_inbox(category_filter=None):
    st.markdown("## 📬 Inbox")

    if not st.session_state.emails:
        st.info("👆 Load emails from the sidebar to get started")
        return

    display_emails = st.session_state.emails
    if category_filter:
        display_emails = [e for e in display_emails if e.category in category_filter]

    for email in display_emails:
        card_html = f"""
        <div class="email-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h3 style="margin: 0; color: #F9FAFB;">{email.subject}</h3>
                    <p style="margin: 8px 0; color: #9CA3AF;">
                        📨 <strong>{email.sender}</strong>
                    </p>
                    <p style="margin: 5px 0; color: #6B7280; font-size: 0.9em;">
                        🕐 {email.timestamp}
                    </p>
                </div>
                <div style="text-align: right;">
                    {get_category_badge(email.category) if email.category else ""}
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        # FIX: Use callback to set selected email instead of rerun
        if st.button(f"👁️ View Details", key=f"view_{email.id}", use_container_width=True):
            st.session_state.selected_email_id = email.id

        st.markdown("<br>", unsafe_allow_html=True)


def render_email_detail():
    st.markdown("## 📧 Email Details")

    email = get_selected_email()
    if not email:
        st.info("👈 Select an email from the inbox")
        return

    st.markdown(f"### {email.subject}")
    st.markdown(f"**From:** {email.sender}")
    st.markdown(f"**To:** {email.recipient}")
    st.markdown(f"**Date:** {email.timestamp}")

    if email.category:
        st.markdown(get_category_badge(email.category), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📄 Message")
    st.markdown(f'<div class="content-box">{email.body}</div>', unsafe_allow_html=True)

    if email.actions:
        st.markdown("---")
        st.markdown("### 📋 Action Items")
        for idx, action in enumerate(email.actions, 1):
            task = action.get("task", "N/A")
            deadline = action.get("deadline", "No deadline")
            st.markdown(f"""
            <div style="background: #262B35; padding: 16px; margin: 12px 0; border-radius: 8px; border-left: 4px solid #10B981;">
                <strong>{idx}. {task}</strong><br>
                <span style="color: #9CA3AF;">⏰ Deadline: {deadline}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✍️ Generate Reply")
    col1, col2 = st.columns([3, 1])

    with col1:
        tone = st.selectbox("Reply tone", ["professional", "friendly", "formal"])

    with col2:
        if st.button("✍️ Create Draft", use_container_width=True):
            with st.spinner("Generating draft..."):
                draft = email_agent.generate_reply_draft(
                    email,
                    st.session_state.prompts,
                    tone
                )
                storage.save_draft(draft)
                st.session_state.drafts = storage.load_drafts()
                st.success("✅ Draft created! Check the Drafts tab.")


def render_agent_chat():
    st.markdown("## 💬 Chat with Agent")

    st.info("💡 Ask the agent questions about your emails, request summaries, or get task lists!")

    email_options = ["All emails"] + [
        f"{e.id}: {e.subject[:45]}..." for e in st.session_state.emails
    ]
    selected = st.selectbox("Context", email_options)

    selected_email = None
    if selected != "All emails":
        email_id = selected.split(":")[0]
        selected_email = next((e for e in st.session_state.emails if e.id == email_id), None)

    # Display chat history
    for msg in st.session_state.chat_history:
        role = msg.get("role")
        content = msg.get("content")

        if role == "user":
            st.markdown(f"""
            <div class="chat-message chat-user">
                <strong>🧑 You:</strong> {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message chat-agent">
                <strong>🤖 Agent:</strong> {content}
            </div>
            """, unsafe_allow_html=True)

    # FIX: Use form to prevent infinite loop
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_query = st.text_input(
                "Ask a question:", 
                placeholder="e.g., Summarize this email",
                key=f"chat_input_{st.session_state.chat_input_key}"
            )

        with col2:
            send_btn = st.form_submit_button("📤 Send", use_container_width=True)

    if send_btn and user_query:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_query,
            "timestamp": datetime.now().isoformat()
        })

        # Get agent response
        with st.spinner("Agent is thinking..."):
            response = email_agent.run_query(
                user_query,
                selected_email,
                st.session_state.emails,
                st.session_state.prompts
            )

        # Add agent response
        st.session_state.chat_history.append({
            "role": "agent",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        # Increment key to clear input
        st.session_state.chat_input_key += 1

        # Rerun to show new messages
        st.rerun()


def render_drafts():
    st.markdown("## ✍️ Email Drafts")

    st.markdown("All drafts are stored locally and never sent automatically.")

    st.session_state.drafts = storage.load_drafts()

    with st.expander("➕ Create New Draft", expanded=False):
        to = st.text_input("To:")
        subject = st.text_input("Subject:")
        instruction = st.text_area(
            "Instructions for the agent:",
            height=100,
            placeholder="e.g., Write a professional email requesting a project status update"
        )

        if st.button("🤖 Generate with AI"):
            if instruction:
                with st.spinner("Generating draft..."):
                    draft = email_agent.generate_new_draft(
                        st.session_state.prompts,
                        instruction,
                        to,
                        subject
                    )
                    storage.save_draft(draft)
                    st.session_state.drafts = storage.load_drafts()
                    st.success("✅ Draft created!")
                    st.rerun()
            else:
                st.warning("Please provide instructions")

    if st.session_state.drafts:
        st.markdown("---")
        st.markdown("### 📝 Saved Drafts")

        for draft in reversed(st.session_state.drafts):
            with st.expander(f"📧 {draft.subject} - {draft.created_at[:16]}"):
                st.markdown(f"**Subject:** {draft.subject}")

                if draft.email_id:
                    st.markdown(f"**In reply to:** Email {draft.email_id}")

                st.markdown("**Body:**")
                st.text_area(
                    "Draft content",
                    value=draft.body,
                    height=200,
                    key=f"draft_body_{draft.id}",
                    disabled=True,
                    label_visibility="collapsed"
                )

                if draft.metadata.get("suggested_follow_ups"):
                    st.markdown("**Suggested Follow-ups:**")
                    for followup in draft.metadata["suggested_follow_ups"]:
                        st.markdown(f"• {followup}")

                if st.button("🗑️ Delete", key=f"delete_{draft.id}"):
                    storage.delete_draft(draft.id)
                    st.session_state.drafts = storage.load_drafts()
                    st.rerun()
    else:
        st.info("No drafts yet. Create one using the button above or reply to an email.")


def render_prompt_config():
    st.markdown("## 🧠 Prompt Configuration")

    st.info("💡 Customize how the AI agent behaves by editing the prompts below. Changes take effect immediately!")

    st.markdown("### 1️⃣ Email Categorization Prompt")
    cat_prompt = st.text_area(
        "Categorization",
        value=st.session_state.prompts.categorization_prompt,
        height=120,
        label_visibility="collapsed"
    )

    st.markdown("### 2️⃣ Action Item Extraction Prompt")
    action_prompt = st.text_area(
        "Action Extraction",
        value=st.session_state.prompts.action_item_prompt,
        height=120,
        label_visibility="collapsed"
    )

    st.markdown("### 3️⃣ Auto-Reply Prompt")
    reply_prompt = st.text_area(
        "Auto-Reply",
        value=st.session_state.prompts.auto_reply_prompt,
        height=120,
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Changes", use_container_width=True):
            st.session_state.prompts = PromptConfig(
                categorization_prompt=cat_prompt,
                action_item_prompt=action_prompt,
                auto_reply_prompt=reply_prompt
            )
            save_prompts()

    with col2:
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.session_state.prompts = storage.get_default_prompts()
            save_prompts()
            st.rerun()

    with col3:
        if st.button("📖 Help", use_container_width=True):
            st.info("""
            **How to customize:**
            1. Edit the text in the boxes above
            2. Click 'Save Changes'
            3. Re-process your emails to see the effect
            """)


def main():
    init_session_state()

    st.markdown("# 📧 Email Productivity Agent Pro")
    st.markdown("### Smart Email Management & AI-Powered Assistance")
    st.markdown("---")

    category_filter = render_sidebar()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📬 Inbox",
        "📧 Details",
        "💬 Chat",
        "✍️ Drafts",
        "🧠 Settings"
    ])

    with tab1:
        render_inbox(category_filter)

    with tab2:
        render_email_detail()

    with tab3:
        render_agent_chat()

    with tab4:
        render_drafts()

    with tab5:
        render_prompt_config()


if __name__ == "__main__":
    main()
