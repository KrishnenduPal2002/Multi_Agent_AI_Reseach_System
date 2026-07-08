🧠 ResearchMind — Multi-Agent AI Research System

Four specialized AI agents collaborate — searching, scraping, writing, and critiquing — to automatically deliver a polished research report on any topic.


📸 Demo

Enter a topic  →  ResearchMind runs 4 agents in sequence  →  Get a full report + critic review


Built with a custom Streamlit UI featuring a live pipeline tracker, topic chips,
research output cards, session history, and a settings panel.




🔁 How the Pipeline Works

ResearchMind runs 4 LangChain-powered agents in a strict handoff sequence.
Each agent's output feeds directly into the next.

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   🔍 Search Agent                                              |
│      Uses Tavily to find 5 recent, reliable web results         │
│      Returns: titles, URLs, and content snippets                │
│                          │                                      │
│                          ▼                                      │
│   📄 Reader Agent                                              │
│      Picks the most relevant URL from search results            │
│      Scrapes the full page using BeautifulSoup                  │
│                          │                                      │
│                          ▼                                      │
│   ✍️  Writer Chain                                              │
│      Combines search results + scraped content                  │
│      Writes a structured report: Intro → Findings → Conclusion  │
│                          │                                      │
│                          ▼                                      │
│   🧠 Critic Chain                                               │
│      Reviews the report and scores it out of 10                 │
│      Returns: Score, Strengths, Areas to Improve, Verdict       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


📁 Project Structure

ResearchMind/
│
├── agents.py          # All 4 agent & chain definitions
│                      #   build_search_agent()  — Tavily web search
│                      #   build_reader_agent()  — URL scraper
│                      #   writer_chain          — GPT-4o-mini report writer
│                      #   critic_chain          — GPT-4o-mini report reviewer
│
├── tools.py           # Custom LangChain tools
│                      #   @tool web_search()    — Tavily search wrapper
│                      #   @tool scrape_url()    — BeautifulSoup scraper
│
├── pipeline.py        # Orchestrator — runs all 4 agents in order
│                      #   run_research_pipline(topic) → dict
│
├── app.py             # Streamlit UI (Research / History / Settings tabs)
│
├── .env               # Your API keys — NEVER commit this
└── requirements.txt   # Python dependencies



LangChain — agent and chain framework
OpenAI — gpt-4o-mini LLM
Tavily — AI-optimised web search API
Streamlit — UI framework
BeautifulSoup — HTML parsing & scraping
