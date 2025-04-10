
# 🧠 AC Chatbot

**AC Chatbot** is an intelligent, locally hosted question-answering system built with Python, Flask, and Sentence Transformers. It reads a training manual and a QA dataset to provide contextual and accurate responses. Ideal for onboarding, training, or support scenarios within organizations.

---

## 🚀 Features

- 🔍 Semantic search using `sentence-transformers`
- 📄 Supports .docx training manuals
- 📁 Uses a JSON QA dataset for predefined responses
- 🧠 Fallback to vector similarity-based retrieval if no direct match
- 🌐 Flask-powered web interface (HTML frontend)
- 🧪 Validation capability to test model accuracy

---

## 🗂️ Project Structure

```
.
├── AC_chatbot.py              # Main application script
├── qa_dataset.json            # Predefined QA pairs (train & validation)
├── training_manual.docx       # Source manual content
├── templates/
│   └── index.html             # Frontend UI (Flask template)
├── static/                    # (Optional) Styles or assets
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ac-chatbot.git
cd ac-chatbot
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist, you can generate it:
> ```bash
> pip freeze > requirements.txt
> ```

### 4. Add your content

- Replace `training_manual.docx` with your own document.
- Update `qa_dataset.json` with your own Q&A pairs.

### 5. Run the app

```bash
python AC_chatbot.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧪 Validation

When you start the app, it will automatically validate performance using the `"validation"` section in `qa_dataset.json` and print the accuracy to the console.

---

## 📦 Dependencies

- Flask  
- sentence-transformers  
- docx  
- torch  
- numpy  
- (see `requirements.txt` for the full list)

---

## 📄 License

MIT License *(or insert your preferred license)*

---

## 🙌 Acknowledgements

- [Hugging Face – Sentence Transformers](https://www.sbert.net/)
- [Flask Web Framework](https://flask.palletsprojects.com/)
- Your organization or team if applicable
# AlertCreatorChatbot
