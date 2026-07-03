# 🌍 AI City Assistant

An intelligent AI-powered city assistant built with **LangChain**, **Mistral AI**, and **Streamlit** that provides real-time **weather updates** and **latest news** for any city using AI tool calling.

---

## 🚀 Features

- 🌦️ Get real-time weather information
- 📰 Fetch the latest news about any city
- 🤖 AI Agent powered by Mistral AI
- 🔧 LangChain Tool Calling
- ✅ Human Approval Middleware before every tool execution
- 💬 Interactive Streamlit Chat Interface
- 🔐 Secure API key management using `.env`

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- Tavily Search API
- OpenWeather API
- Python Dotenv
- Requests

---

## 📂 Project Structure

```
AI-City-Assistant/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
```

---

## ⚙️ Installation

### Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
OPENWEATHER_API_KEY=YOUR_OPENWEATHER_API_KEY

TAVILY_API_KEY=YOUR_TAVILY_API_KEY

MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

---

## 💬 Example Questions

```
What's the weather in Jaipur?

Latest news in Delhi

Tell me the weather in Mumbai

News about Bangalore

Weather and news of Pune
```

---

## 🧠 How It Works

1. User enters a question.
2. Mistral AI understands the request.
3. LangChain Agent selects the appropriate tool.
4. Human approval middleware confirms tool execution.
5. The selected tool retrieves live data.
6. The AI formats and returns the response in the Streamlit interface.

---

---

## 📌 Future Improvements

- Voice Assistant
- 5-Day Weather Forecast
- Global Weather Support
- Weather Charts
- AI Memory
- Conversation History Database
- Docker Support
- Multi-language Support
- Deployment on Streamlit Cloud

---

## 👨‍💻 Author

Pankaj Jangid

AI & Machine Learning Enthusiast


---
