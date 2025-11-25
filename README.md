# 📧 Email Productivity Agent Pro

**A smart, fully offline email manager with AI-powered automation, built on Streamlit for productivity, clarity, and privacy. Featuring a custom dark theme and robust categorization.**

---

## 🚀 Features

- **Instant Email Categorization:** Accurately detects Spam, Newsletters, To-Do items (action required), and Important business communications using advanced rule logic.
- **Action Item Extraction:** Automatically finds and lists actionable tasks and deadlines directly from email content.
- **Draft Generator:** Produces context-aware reply drafts in professional, friendly, or formal tones with a single click.
- **AI Inbox Chat:** Lets you ask questions about your inbox, tasks, and urgent emails.
- **Dark Theme UI:** Gorgeous custom CSS for distraction-free focus.
- **Secure & Offline:** All data is processed and stored locally. No real email credentials or cloud access required.
- **One-Click Demo:** Includes 15 realistic, preloaded business emails to showcase all features instantly.

---

## 📦 Installation

1. **Unzip the Release**
   ```
   cd email-agent-assignment
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```
   streamlit run app/main.py
   ```
   Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🎯 How to Use

### 1. Load and Process Inbox
- Click **“📥 Load”** in the sidebar to load demo emails.
- Click **“⚡ Process”** to categorize and extract tasks.

### 2. Explore Email Tabs
- **Inbox:** See all emails sorted by auto-generated category badges.
- **Details:** Click **“View Details”** to see the full content, instant categorization, extracted action items, and draft reply options.
- **Chat:** Ask questions like “What tasks do I have?”, “Show me spam”, etc. and get smart answers.
- **Drafts:** Review or delete generated draft replies.

### 3. Sidebar Insights
- See live statistics for each category: To-Do, Spam, Newsletter, Important.

---

## ✨ AI Categorization Logic

Email categorization uses a strict priority cascade:
1. **Spam:** Phishing, scams, urgent/fake alerts
2. **Newsletter:** Newsletter format, sender patterns, unsubscribe links
3. **To-Do:** Action requests, deadlines, confirmation needed
4. **Important:** Remaining business communication

---

## 📊 Sample Data

- 15 business emails: includes budgets, code reviews, phishing, newsletters, project updates, RSVPs, receipts, research feedback, and more.
- Categorization is guaranteed: see a real spread of Spam, Newsletter, To-Do, and Important.

---

## 🔒 Security & Privacy

- **No cloud interaction:** All operations are local.
- **No credentials required:** Only demo data is used.
- **Draft replies only:** No real sending function.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** (UI)
- **Pydantic** (models)
- **Custom Python logic** for “AI” (no external API keys or cloud cost)
- **JSON data files** for inbox and drafts

---

## 📝 License

MIT License – Free to use, modify, and extend.

---

## 💡 Demo/Development Tips

- You can edit `data/mock_inbox.json` to try with your own email corpus (no authentication required!)
- All app logic is in the `app` folder, and all “AI” happens in `services/llm_client.py`.
- For more business emails, just add more to the `mock_inbox.json` file.

---

**Feel free to contribute or adapt!**