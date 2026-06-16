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
    page_icon="✝️",
    layout="centered"
)

# ── Liturgical helpers ───────────────────────────────────────────────────────

def get_liturgical_day():
    try:
        today = date.today()
        month_day = today.strftime("%m-%d")
        year = today.strftime("%Y")
        url = f"https://cpbjr.github.io/catholic-readings-api/liturgical-calendar/{year}/{month_day}.json"
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return None

def get_todays_readings():
    try:
        today = date.today()
        date_str = today.strftime("%m%d%y")
        url = f"https://bible.usccb.org/bible/readings/{date_str}.cfm"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        readings = {}
        headers = soup.find_all("h3")

        for header in headers:
            text = header.get_text(strip=True)
            link = header.find_next("a")
            ref = link.get_text(strip=True) if link else ""

            if any(x in text for x in ["Reading I", "Reading 1", "First Reading"]):
                readings["first_reading"] = {"reference": ref}
            elif "Psalm" in text:
                readings["psalm"] = {"reference": ref}
            elif any(x in text for x in ["Reading II", "Reading 2", "Second Reading"]):
                readings["second_reading"] = {"reference": ref}
            elif "Gospel" in text:
                readings["gospel"] = {"reference": ref}

        return readings if readings else None
    except:
        return None

def get_saint_of_day():
    try:
        today = date.today()
        month_day = today.strftime("%m-%d")
        year = today.strftime("%Y")
        url = f"https://cpbjr.github.io/catholic-readings-api/liturgical-calendar/{year}/{month_day}.json"
        response = requests.get(url, timeout=5)
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

st.title("✝️ Fides")
st.caption("Your faithful Catholic AI companion")

tab1, tab2 = st.tabs(["💬 Ask Fides", "📅 Today"])

# ── Today tab ────────────────────────────────────────────────────────────────

with tab2:
    st.subheader("Today's Liturgical Day")

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
            st.warning("Could not load today's readings. Please check your internet connection.")

    else:
        st.warning("Could not load today's liturgical data. Please check your internet connection.")

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