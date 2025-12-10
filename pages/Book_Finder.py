import streamlit as st
import requests

st.set_page_config(
    page_title="SizzlClub · Book Finder",
    page_icon="📚",
    layout="wide"
)

# -------------- STYLES --------------
st.markdown(
    """
    <style>
    .sizzl-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4D6D, #FF8E6E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sizzl-subtitle {
        font-size: 1rem;
        color: #f5f5f5cc;
        margin-bottom: 1rem;
    }
    .sizzl-pill {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        margin-right: 0.3rem;
        margin-bottom: 0.3rem;
        border-radius: 999px;
        background-color: #2b2b2f;
        color: #ffdee7;
        font-size: 0.8rem;
        border: 1px solid #ff4d6d33;
    }
    .sizzl-card {
        padding: 0.9rem 1rem;
        border-radius: 0.8rem;
        background-color: #121218;
        border: 1px solid #ffffff10;
        margin-bottom: 0.8rem;
    }
    .sizzl-meta {
        color: #cfcfd9;
        font-size: 0.9rem;
    }
    .sizzl-badge-soft {
        display: inline-block;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        font-size: 0.75rem;
        background-color: #ff4d6d22;
        color: #ff9bb0;
        margin-left: 0.4rem;
    }
    .sizzl-cover-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------- HEADER --------------
st.markdown('<div class="sizzl-title">📚 SizzlClub · Book Finder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sizzl-subtitle">Search for romance & spicy reads, then browse your results in a Sizzl shelf layout.</div>',
    unsafe_allow_html=True
)

st.write("")


# -------------- FILTER OPTIONS --------------
SPICE_LEVELS = ["🌶 1", "🌶🌶 2", "🌶🌶🌶 3", "🌶🌶🌶🌶 4", "🌶🌶🌶🌶🌶 5"]
GENRES = [
    "Contemporary", "Historical", "Fantasy", "Paranormal",
    "Dark Romance", "Romantic Suspense", "Sci-Fi", "Sports Romance"
]
RELATIONSHIP = [
    "1-on-1", "Love Triangle", "Why Are There 4 Of Them",
    "Reverse Harem / Why Choose", "Polyamory"
]
TROPES = [
    "Enemies to Lovers", "Friends to Lovers", "Childhood Friends",
    "Fake Dating", "Forced Proximity", "Marriage of Convenience",
    "Grumpy / Sunshine", "Boss / Employee", "Bodyguard",
    "Second Chance", "Single Parent", "Forbidden Romance",
]
CONTENT_WARNINGS = [
    "Violence", "Abuse", "Cheating", "Death", "Addiction",
    "Dubious Consent", "Non-Consensual", "Mental Health", "Self-Harm"
]
HERO_TRAITS = [
    "Morally Grey", "Sunshine", "Grumpy", "Alpha", "Soft Dom",
    "Cinnamon Roll", "Tattooed", "Biker", "Royalty", "Billionaire"
]
HEROINE_TRAITS = [
    "Sunshine", "Grumpy", "Strong-willed", "Reluctant",
    "Morally Grey", "Bookworm", "STEM Girl", "Single Mom", "Princess"
]


# -------------- SIDEBAR --------------
with st.sidebar:
    st.markdown("### 🔎 Search")

    query = st.text_input(
        "Title / author / keyword",
        placeholder="e.g. 'fake dating', 'dark romance', 'Ali Hazelwood'"
    )
    max_results = st.slider("Max results", 5, 40, 16, step=4)

    st.markdown("---")
    st.markdown("### 🌶 Sizzl filters (vibe only)")

    # Spice Level
    st.caption("**Spice Level (1–5 chillies)**")
    col_inc, col_exc = st.columns(2)
    with col_inc:
        spice_inc = st.multiselect("Include", SPICE_LEVELS, key="spice_inc")
    with col_exc:
        spice_exc = st.multiselect("Exclude", SPICE_LEVELS, key="spice_exc")

    # Genre
    st.caption("**Genre**")
    col_inc_g, col_exc_g = st.columns(2)
    with col_inc_g:
        genre_inc = st.multiselect("Include", GENRES, key="genre_inc")
    with col_exc_g:
        genre_exc = st.multiselect("Exclude", GENRES, key="genre_exc")

    # Relationship
    st.caption("**Relationship (number of people)**")
    col_inc_r, col_exc_r = st.columns(2)
    with col_inc_r:
        rel_inc = st.multiselect("Include", RELATIONSHIP, key="rel_inc")
    with col_exc_r:
        rel_exc = st.multiselect("Exclude", RELATIONSHIP, key="rel_exc")

    # Tropes
    st.caption("**Tropes**")
    col_inc_t, col_exc_t = st.columns(2)
    with col_inc_t:
        tropes_inc = st.multiselect("Include", TROPES, key="tropes_inc")
    with col_exc_t:
        tropes_exc = st.multiselect("Exclude", TROPES, key="tropes_exc")

    # Content Warnings
    st.caption("**Content Warnings**")
    col_inc_cw, col_exc_cw = st.columns(2)
    with col_inc_cw:
        cw_inc = st.multiselect("Okay with", CONTENT_WARNINGS, key="cw_inc")
    with col_exc_cw:
        cw_exc = st.multiselect("Avoid", CONTENT_WARNINGS, key="cw_exc")

    # Hero traits
    st.caption("**Hero personality / appearance**")
    col_inc_h, col_exc_h = st.columns(2)
    with col_inc_h:
        hero_inc = st.multiselect("Include", HERO_TRAITS, key="hero_inc")
    with col_exc_h:
        hero_exc = st.multiselect("Exclude", HERO_TRAITS, key="hero_exc")

    # Heroine traits
    st.caption("**Heroine personality / appearance**")
    col_inc_he, col_exc_he = st.columns(2)
    with col_inc_he:
        heroine_inc = st.multiselect("Include", HEROINE_TRAITS, key="heroine_inc")
    with col_exc_he:
        heroine_exc = st.multiselect("Exclude", HEROINE_TRAITS, key="heroine_exc")

    st.markdown("---")
    search_clicked = st.button("Search Open Library")

st.markdown("---")


# -------------- COVER HELPER --------------
def get_cover_url(doc):
    cover_id = doc.get("cover_i")
    if cover_id:
        # Open Library cover API
        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    return None


# -------------- MAIN SEARCH LOGIC --------------
if search_clicked:
    if not query.strip():
        st.warning("Type in a title, author, or trope to search.")
    else:
        with st.spinner("Looking through the stacks at Open Library..."):
            url = "https://openlibrary.org/search.json"
            params = {"q": query, "limit": max_results}
            try:
                resp = requests.get(url, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                docs = data.get("docs", [])
            except Exception as e:
                st.error(f"Something went wrong while searching: {e}")
                docs = []

        if not docs:
            st.info("No results found. Try tweaking your keywords.")
        else:
            st.markdown(f"#### Results for **{query}**")

            # ---------- FEATURED ROW (Goodreads-style) ----------
            st.markdown("### Your Sizzl shelf for this search")
            featured = docs[:4]
            cols = st.columns(4)

            for col, doc in zip(cols, featured):
                title = doc.get("title", "Unknown title")
                authors = ", ".join(doc.get("author_name", [])[:2]) or "Unknown author"
                key = doc.get("key", "")
                work_url = f"https://openlibrary.org{key}" if key else None
                cover_url = get_cover_url(doc)

                with col:
                    if cover_url:
                        col.image(cover_url, use_column_width=True)
                    else:
                        col.write("📕 (no cover)")

                    if work_url:
                        col.markdown(
                            f'<div class="sizzl-cover-title"><a href="{work_url}" target="_blank">{title}</a></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        col.markdown(f'<div class="sizzl-cover-title">{title}</div>', unsafe_allow_html=True)

                    col.caption(authors)

            st.markdown("---")

            # ---------- REST OF RESULTS (list view) ----------
            st.markdown("### More results")

            for doc in docs:
                title = doc.get("title", "Unknown title")
                authors = ", ".join(doc.get("author_name", [])[:3]) or "Unknown author"
                year = doc.get("first_publish_year", "N/A")
                subjects = doc.get("subject", []) or []
                key = doc.get("key", "")
                work_url = f"https://openlibrary.org{key}" if key else None

                with st.container():
                    st.markdown('<div class="sizzl-card">', unsafe_allow_html=True)
                    if work_url:
                        st.markdown(f"**[{title}]({work_url})**")
                    else:
                        st.markdown(f"**{title}**")
                    st.markdown(
                        f'<span class="sizzl-meta">{authors} · First published: {year}</span>',
                        unsafe_allow_html=True
                    )

                    if subjects:
                        chips = ", ".join(subjects[:8])
                        st.write(f"**Subjects:** {chips}")
                    else:
                        st.write("_No subject tags available._")

                    lower_subj = " ".join(subjects).lower()
                    spice_guess = ""
                    if any(word in lower_subj for word in ["erotic", "sex", "adult", "explicit"]):
                        spice_guess = "🌶🌶🌶 Probably high spice"
                    elif any(word in lower_subj for word in ["romance", "love", "relationship"]):
                        spice_guess = "🌶🌶 Likely romantic"
                    elif subjects:
                        spice_guess = "🌶 Might be more general fiction"

                    if spice_guess:
                        st.markdown(
                            f'<span class="sizzl-badge-soft">{spice_guess}</span>',
                            unsafe_allow_html=True
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Start by searching for a book, trope, or author using the controls in the sidebar.")
    st.write("Try something like **'enemies to lovers'**, **'college romance'**, or an author you adore.")
