from dotenv import load_dotenv
import os
import requests
import streamlit as st

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from tavily import TavilyClient

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="🌍 City AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================
# Custom CSS
# ==========================

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#4CAF50;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

.toolbox{
    background:#262730;
    padding:15px;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🌍 City AI Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Weather + Latest News using Mistral AI</div>", unsafe_allow_html=True)

# ==========================
# Weather Tool
# ==========================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# ==========================
# News Tool
# ==========================

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news = []

    for r in results:
        title = r.get("title", "")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news.append(
            f"""• {title}

🔗 {url}

📝 {snippet[:120]}...
"""
        )

    return "Latest News\n\n" + "\n".join(news)

# ==========================
# LLM
# ==========================

llm = ChatMistralAI(model="mistral-small-2506")

# ==========================
# Human Approval Middleware
# ==========================

approval = st.sidebar.checkbox(
    "✅ Approve Tool Calls",
    value=True
)

@wrap_tool_call
def human_approval(request, handler):

    tool_name = request.tool_call["name"]

    if not approval:
        return ToolMessage(
            content=f"{tool_name} denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request)

# ==========================
# Agent
# ==========================

agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="you are a helpful city assistant.",
    middleware=[human_approval]
)

# ==========================
# Session State
# ==========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================
# Chat Input
# ==========================

prompt = st.chat_input("Ask about weather or news...")

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = agent.invoke(
                {
                    "messages":[
                        {
                            "role":"user",
                            "content":prompt
                        }
                    ]
                }
            )

            response = result["messages"][-1].content

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )

# ==========================
# Sidebar
# ==========================

st.sidebar.title("⚙️ Settings")

st.sidebar.info("""
### Available Tools

🌦️ Weather

📰 News

---

Toggle approval above to allow or deny tool calls.
""")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()