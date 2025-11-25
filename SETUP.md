# 🚀 Quick Setup Guide

## Installation

### 1. Extract Files
Extract the zip to your desired location.

### 2. Open Terminal
Navigate to the project directory:
```bash
cd email-agent-dark-fixed
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If "pip not found":
```bash
python -m pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app/main.py
```

If "streamlit not found":
```bash
python -m streamlit run app/main.py
```

### 5. Access the App
Open your browser at: `http://localhost:8501`

## 🎉 You're Ready!

1. Click "📥 Load Inbox"
2. Click "⚡ Process"
3. Explore all features!

## ⚠️ Troubleshooting

**Port in use?**
```bash
streamlit run app/main.py --server.port 8502
```

**Module errors?**
```bash
pip install streamlit pydantic python-dotenv
```

## 💡 Tips

- View Details button now works instantly (no loading)
- Chat feature works smoothly (no infinite loop)
- Input clears automatically after sending

Happy emailing! 🌙
