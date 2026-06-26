import streamlit as st
import anthropic
import requests
import json
import sys
from datetime import date
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
sys.path.append(".")
from rag.retriever import retrieve

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── Page config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Fides - Catholic AI Companion",
    page_icon="⛪",  # Changed to match your screenshot icon, or keep your purple cross "✝️"
    layout="centered"
)

st.markdown(
    """
    <style>
    /* Hide standard Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Elegant Title Container styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap');
    
    .title-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        margin-top: -30px; /* Pulls it up slightly since we hid the header space */
        margin-bottom: 10px;
    }
    
    .fides-title {
        font-size: 3.5rem;
        font-weight: 800; /* Extra bold */
        color: #111111;
        margin: 0;
        display: flex;
        align-items: baseline;
        line-height: 1.1;
    }
    
    /* Perfect circular gold/tan dot */
    .gold-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #C5A880; /* Perfectly matched liturgical gold/tan color */
        border-radius: 50%;
        margin-left: 4px;
        align-self: center;
        transform: translateY(12px); /* Aligns perfectly on the font's baseline */
    }
    
    .fides-subtitle {
        font-size: 1.25rem;
        color: #7A92A8; /* Elegant soft blue-gray color */
        font-weight: 400;
        letter-spacing: 0.5px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    
    .fides-divider {
        border: 0;
        height: 1px;
        background-color: #E2E8F0; /* Light elegant divider line */
        margin-top: 5px;
        margin-bottom: 30px;
    }
    </style>
    
    <div class="title-container">
        <h1 class="fides-title">Fides<span class="gold-dot"></span></h1>
        <p class="fides-subtitle">Your Catholic AI Companion</p>
        <hr class="fides-divider">
    </div>
    """,
    unsafe_allow_html=True
)

# ── Liturgical helpers ───────────────────────────────────────────────────────

def get_liturgical_day():
    try:
        today = date.today()
        month_day = today.strftime("%m-%d")
        year = today.strftime("%Y")
        url = f"https://cpbjr.github.io/catholic-readings-api/liturgical-calendar/{year}/{month_day}.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        response = requests.get(url, timeout=10, headers=headers)
        return response.json()
    except:
        return None

def get_todays_readings():
    try:
        today = date.today()
        month_day = today.strftime("%m-%d")
        year = today.strftime("%Y")
        url = f"https://cpbjr.github.io/catholic-readings-api/readings/{year}/{month_day}.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            data = response.json()
            r = data.get("readings", {})
            readings = {}
            if r.get("firstReading"):
                readings["first_reading"] = {"reference": r["firstReading"]}
            if r.get("secondReading"):
                readings["second_reading"] = {"reference": r["secondReading"]}
            if r.get("psalm"):
                readings["psalm"] = {"reference": r["psalm"]}
            if r.get("gospel"):
                readings["gospel"] = {"reference": r["gospel"]}
            return readings if readings else None
        return None
    except:
        return None
def get_saint_of_day():
    try:
        today = date.today()
        month_day = today.strftime("%m-%d")
        year = today.strftime("%Y")
        url = f"https://cpbjr.github.io/catholic-readings-api/liturgical-calendar/{year}/{month_day}.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        response = requests.get(url, timeout=10, headers=headers)
        data = response.json()
        celebration = data.get("celebration", {})
        name = celebration.get("name", "")

        ferial_keywords = ["FERIA", "WEEK", "SUNDAY", "MONDAY", "TUESDAY",
                          "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
        is_ferial = any(k in name.upper() for k in ferial_keywords)
        return "" if is_ferial else name
    except:
        return ""

def get_season_emoji(season):
    season_lower = season.lower()
    if "advent" in season_lower: return "🕯️"
    if "christmas" in season_lower: return "⭐"
    if "lent" in season_lower: return "✝️"
    if "easter" in season_lower: return "🌅"
    return "🌿"

# ── System prompt ────────────────────────────────────────────────────────────

system_prompt = """You are Fides, a humble and trustworthy Catholic AI companion.
Your purpose is to support — never replace — the rich interior life of a Catholic.

RESPONSE HIERARCHY — follow this always:

For personal, emotional, or spiritual moments (joy, struggle, confusion,
gratitude, grief, spiritual dryness, searching):
1. Acknowledge warmly — meet the person where they are, never with information first
2. Invite them to prayer or quiet time with God — He is the first answer
3. Point to a specific Scripture passage that speaks to their moment
4. Only if relevant — mention CCC or suggest speaking to a priest

For doctrinal or teaching questions:
1. Ground the answer in Scripture first
2. Cite the CCC — always include the paragraph number e.g. "CCC §1213"
3. Be clear, warm and pastoral in tone

For factual Church questions:
1. Cite the CCC directly with paragraph number
2. Support with Scripture where relevant
3. Encourage the user to read the original source themselves —
   "I'd encourage you to read CCC §1213 yourself — sitting with the
   original words is always richer than a summary."

For matters of conscience, sin, or spiritual direction:
1. Acknowledge warmly
2. Invite to prayer
3. Always redirect to a priest or confessor —
   "This is something worth bringing to your confessor,
   who can walk with you personally."

WHAT FIDES IS NOT:
- Not a replacement for the sacraments
- Not a spiritual director
- Not a substitute for your priest, your Bible, or your prayer life

STAY IN YOUR LANE:
Fides only answers questions related to Catholic faith, prayer, scripture,
sacraments, saints, Church teaching, and the spiritual life.
If asked anything outside this scope — news, finance, property, politics,
health advice, technology, or any non-faith topic — respond warmly but firmly:
"I'm Fides, a Catholic faith companion. That question is outside what I'm
here for. I'd gently invite you instead to bring whatever is on your heart
to God in prayer. Is there something about your faith I can help with?"
Never apologise excessively for staying in your lane — it is a feature,
not a limitation.

ALWAYS REMEMBER:
- The Word of God is living and active — it meets people where they are
- The CCC explains the faith; Scripture speaks to the heart
- Prayer and encounter with God always come before information
- You are a companion on the journey, not the destination
- Never include stage directions, tone indicators, or meta-instructions
  in brackets like "(Warmly)" or "(Pause)" — these are internal guides
  for you, never visible text for the user. Speak naturally and directly.
- Never ask multiple questions. If you need to ask anything, ask one
  gentle question at most — and only if truly necessary.
  Fides holds space, it does not interview the user.
- Fides is not a therapist and should never act like one. Do not probe
  emotions or ask follow-up questions about how someone is feeling.
  Acknowledge briefly, point to God and Scripture, and if someone appears
  to be in genuine distress or need ongoing support, gently suggest
  speaking to their priest, a pastoral counsellor, or a trusted person
  in their faith community. Then step back.
- Scripture before CCC, always. The Word of God is living and active —
  it speaks to every moment, joyful or sorrowful, curious or confused.
  When responding to any personal, emotional, or spiritual moment —
  acknowledge first with warmth, then invite the user to prayer or quiet
  time with God, then point to a specific Scripture passage that meets
  them there.
  Reserve the CCC for doctrinal questions, factual Church teaching,
  and when someone specifically needs to understand what the Church teaches.
  Never lead with the CCC for a human moment."""

# ── Initialize session state ─────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "liturgical_data" not in st.session_state:
    st.session_state.liturgical_data = None

if "readings" not in st.session_state:
    st.session_state.readings = None

if "saint" not in st.session_state:
    st.session_state.saint = None

if "today_loaded" not in st.session_state:
    st.session_state.today_loaded = False

# ── Load today's data once ───────────────────────────────────────────────────

if not st.session_state.today_loaded:
    st.session_state.liturgical_data = get_liturgical_day()
    st.session_state.readings = get_todays_readings()
    st.session_state.saint = get_saint_of_day()
    st.session_state.today_loaded = True

# ── UI ───────────────────────────────────────────────────────────────────────
# We let the elegant HTML block at the top handle the title. 
# We only need to define the tabs and put the disclaimer cleanly inside them!

tab1, tab2 = st.tabs(["💬 Ask Fides", "📅 Today"])

# ── Today tab ────────────────────────────────────────────────────────────────

with tab2:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("Today's Liturgical Day")
    with col2:
        if st.button("🔄 Refresh"):
            st.session_state.today_loaded = False
            st.rerun()

    data = st.session_state.liturgical_data
    readings = st.session_state.readings
    saint = st.session_state.saint

    if data:
        season = data.get("season", "Ordinary Time")
        celebration = data.get("celebration", {})
        celebration_name = celebration.get("name", "")
        season_emoji = get_season_emoji(season)

        st.markdown(f"### {season_emoji} {season}")
        st.markdown(f"**{celebration_name}**")

        st.divider()

        st.markdown("### 📖 Today's Mass Readings")

        if readings:
            first = readings.get("first_reading", {})
            if first:
                st.markdown(f"**First Reading** — {first.get('reference', '')}")

            second = readings.get("second_reading", {})
            if second:
                st.markdown(f"**Second Reading** — {second.get('reference', '')}")

            psalm = readings.get("psalm", {})
            if psalm:
                st.markdown(f"**Psalm** — {psalm.get('reference', '')}")

            gospel = readings.get("gospel", {})
            if gospel:
                st.markdown(f"**Gospel** — {gospel.get('reference', '')}")

            st.divider()

            if saint:
                st.markdown("**✨ Saint of the Day**")
                st.markdown(saint)
                if st.button("🙏 Pray with today's saint"):
                    st.info(f"Go to 💬 Ask Fides and type: 'Lead me in a short prayer to {saint}' 🙏")
            else:
                st.caption("No particular saint today — a beautiful day to pray freely with the Lord. 🌿")

            if gospel:
                gospel_ref = gospel.get("reference", "today's Gospel")
                if st.button("💭 Reflect on today's Gospel"):
                    st.info(f"Go to 💬 Ask Fides and type: 'Help me reflect on {gospel_ref}' 🙏")

        else:
            st.warning("Could not load today's readings. Try the 🔄 Refresh button above.")

    else:
        st.warning("Could not load today's liturgical data. Try the 🔄 Refresh button above.")

# ── Ask Fides tab ────────────────────────────────────────────────────────────

with tab1:
    st.info("🙏 Fides is a faith companion, not a substitute for your priest or spiritual director.")

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the faith..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Fides is reflecting..."):
                    context = retrieve(prompt)

                    # Build today's liturgical context
                    today_context = ""
                    if st.session_state.readings:
                        r = st.session_state.readings
                        today_context = f"\nTODAY'S LITURGICAL DATE: {date.today().strftime('%B %d, %Y')}\n"
                        today_context += f"LITURGICAL DAY: {st.session_state.liturgical_data.get('celebration', {}).get('name', '') if st.session_state.liturgical_data else ''}\n"
                        today_context += "TODAY'S MASS READINGS:\n"
                        if r.get("first_reading"):
                            today_context += f"- First Reading: {r['first_reading'].get('reference', '')}\n"
                        if r.get("psalm"):
                            today_context += f"- Psalm: {r['psalm'].get('reference', '')}\n"
                        if r.get("gospel"):
                            today_context += f"- Gospel: {r['gospel'].get('reference', '')}\n"

                    grounded_prompt = system_prompt + today_context + f"""

RELEVANT CHURCH DOCUMENTS:
{context}

Use the above documents to ground your answer where relevant.
Always cite the paragraph number when referencing the Catechism."""

                    response = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=1024,
                        system=grounded_prompt,
                        messages=st.session_state.messages
                    )
                    reply = response.content[0].text
                    st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
