import streamlit as st

st.set_page_config(
    page_title="SizzlClub",
    page_icon="🔥",
    layout="wide"
)

# -------------- HEADER --------------
st.markdown(
    """
    <style>
    .sizzl-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4D6D, #FF8E6E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sizzl-subtitle {
        font-size: 1.1rem;
        color: #f5f5f5cc;
    }
    .sizzl-section-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    .sizzl-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        border-radius: 999px;
        background-color: #2b2b2f;
        color: #ffdee7;
        font-size: 0.85rem;
        border: 1px solid #ff4d6d33;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="sizzl-title">🔥 SizzlClub</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sizzl-subtitle">A cozy corner for spicy romance readers — find books, share recs, and scream about tropes together.</div>',
    unsafe_allow_html=True
)

st.write("")  # spacer


# -------------- LAYOUT --------------
col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown("### What is SizzlClub?")
    st.write(
        "SizzlClub is your little romance nook on the internet. "
        "Search for books, track down your next spicy read, and (soon) chat with others about tropes, ships, and unhinged main characters."
    )

    st.markdown("### Start here")
    st.write("Use the sidebar or the shortcuts below:")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 Open Book Finder"):
            st.switch_page("pages/Book_Finder.py")

    with c2:
        st.caption("💬 Community & recs coming soon...")

    st.markdown("### Vibes & tropes")
    st.write(
        "SizzlClub is built for romance readers who love:"
    )

    tropes = [
        "🌶️ Slow burn",
        "💥 Enemies to lovers",
        "🧪 Forced proximity",
        "👑 Royalty & billionaires",
        "🧛‍♂️ Paranormal & fantasy",
        "🚩 Morally grey disasters",
        "🦋 Second chance",
        "📱 Online friends to lovers"
    ]

    trope_html = "".join([f'<span class="sizzl-pill">{t}</span>' for t in tropes])
    st.markdown(trope_html, unsafe_allow_html=True)

with col_right:
    st.markdown("### Quick info")
    st.markdown(
        """
        - 🔥 **Status:** Very much a WIP  
        - 📚 **Focus:** Romance, spice, tropes  
        - 🧪 **Built with:** Streamlit + Python  
        """
    )

    st.markdown("### Roadmap (rough)")
    st.write(
        "- Book Finder MVP (live)\n"
        "- Basic community threads\n"
        "- Taste-based recommendations\n"
        "- Profile-free, low-pressure book chat\n"
    )

    st.markdown("### How to use")
    st.write(
        "Head over to **Book Finder** to search for books. "
        "As the app grows, you'll see new pages in the sidebar for community and recs."
    )

st.markdown("---")
st.caption("Made with 💖 and unhinged book energy · SizzlClub")
