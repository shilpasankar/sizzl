import streamlit as st
import pandas as pd
from pathlib import Path

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
    '<div class="sizzl-subtitle">Browsing only Sizzl’s romance catalogue — filtered by vibes, spice and tropes, not the whole internet.</div>',
    unsafe_allow_html=True
)

st.write("")


# -------------- LOAD CATALOGUE (ONLY FROM CSV) --------------
@st.cache_data
def load_catalogue() -> pd.DataFrame:
    """
    Load the curated romance catalogue from data/romance_catalogue.csv.
    """
    path = Path("data") / "romance_catalogue.csv"
    df = pd.read_csv(path)
    # Normalise string columns to avoid NaN issues
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("")
    return df


df_catalogue = load_catalogue()

# -------------- FILTER OPTIONS --------------
SPICE_LEVELS = ["🌶 1", "🌶🌶 2", "🌶🌶🌶 3", "🌶🌶🌶🌶 4", "🌶🌶🌶🌶🌶 5"]
GENRES = [
    "Contemporary", "Historical", "Fantasy", "Paranormal",
    "Dark Romance", "Romantic Suspense", "Sci-Fi", "Sports Romance"
]
RELATIONSHIP = [
    "1-on-1",
    "Love Triangle",
    "Why Are There 4 Of Them",  # your chaotic phrasing
    "Why Choose",               # genre label
    "Polyamory"
]
TROPES = [
    "Enemies to Lovers",
    "Friends to Lovers",
    "Childhood Friends",
    "Fake Dating",
    "Forced Proximity",
    "Marriage of Convenience",
    "Fated Mates",
    "Second Chance",
    "Single Parent",
    "Forbidden Romance",
    "Grumpy / Sunshine",
    "Boss / Employee",
    "Bodyguard",
    "Only One Bed",
    "Slow Burn",
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


# -------------- SIDEBAR WITH FORM (ENTER TO SUBMIT) --------------
with st.sidebar:
    with st.form("search_form", clear_on_submit=False):
        st.markdown("### 🔎 Search within Sizzl catalogue")
        query = st.text_input(
            "Title / author / trope (optional)",
            placeholder="Leave blank to just use filters"
        )
        max_results = st.slider("Max results", 5, 80, 24, step=4)

        st.markdown("---")
        st.markdown("### 🌶 Sizzl filters")

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
        search_clicked = st.form_submit_button("Filter Sizzl catalogue")

st.markdown("---")


# -------------- FILTER HELPERS --------------

def text_match(df: pd.DataFrame, q: str) -> pd.DataFrame:
    """Filter by query in title / author / tropes (if query not empty)."""
    if not q.strip():
        return df
    q = q.lower()
    cols = []
    for c in ["title", "author", "tropes"]:
        if c in df.columns:
            cols.append(df[c].astype(str).str.lower().str.contains(q, na=False))
    if not cols:
        return df
    mask = cols[0]
    for m in cols[1:]:
        mask |= m
    return df[mask]


def include_any(df: pd.DataFrame, col: str, selected: list):
    """Keep rows where 'col' contains ANY of selected values (pipe-separated semantics)."""
    if not selected or col not in df.columns:
        return df
    def row_ok(val: str) -> bool:
        text = str(val).lower()
        return any(s.lower() in text for s in selected)
    return df[df[col].apply(row_ok)]


def exclude_any(df: pd.DataFrame, col: str, selected: list):
    """Drop rows where 'col' contains ANY of selected values."""
    if not selected or col not in df.columns:
        return df
    def row_bad(val: str) -> bool:
        text = str(val).lower()
        return any(s.lower() in text for s in selected)
    return df[~df[col].apply(row_bad)]


def spice_string_to_int(s: str) -> int:
    """Map '🌶 3' → 3."""
    try:
        return int(s.split()[-1])
    except Exception:
        return 0


# -------------- MAIN LOGIC --------------

if search_clicked:
    # Check if literally no query AND no filters
    any_filters = any([
        spice_inc, spice_exc,
        genre_inc, genre_exc,
        rel_inc, rel_exc,
        tropes_inc, tropes_exc,
        cw_inc, cw_exc,
        hero_inc, hero_exc,
        heroine_inc, heroine_exc,
    ])
    if not query.strip() and not any_filters:
        st.info("Type a search OR pick at least one filter to browse the Sizzl catalogue.")
    else:
        df = df_catalogue.copy()

        # Query filter
        df = text_match(df, query)

        # Spice filters assume a numeric 'spice_level' column in your CSV
        if "spice_level" in df.columns:
            if spice_inc:
                nums = [spice_string_to_int(s) for s in spice_inc]
                df = df[df["spice_level"].isin(nums)]
            if spice_exc:
                nums = [spice_string_to_int(s) for s in spice_exc]
                df = df[~df["spice_level"].isin(nums)]

        # Other filters based on pipe-separated fields
        df = include_any(df, "genres", genre_inc)
        df = exclude_any(df, "genres", genre_exc)

        df = include_any(df, "relationship", rel_inc)
        df = exclude_any(df, "relationship", rel_exc)

        df = include_any(df, "tropes", tropes_inc)
        df = exclude_any(df, "tropes", tropes_exc)

        df = include_any(df, "content_warnings", cw_inc)
        df = exclude_any(df, "content_warnings", cw_exc)

        df = include_any(df, "hero_traits", hero_inc)
        df = exclude_any(df, "hero_traits", hero_exc)

        df = include_any(df, "heroine_traits", heroine_inc)
        df = exclude_any(df, "heroine_traits", heroine_exc)

        # Limit rows
        df = df.head(max_results)

        if df.empty:
            st.warning("No books match this combination yet. Try relaxing a filter or two.")
        else:
            st.markdown(f"#### Showing {len(df)} book(s) from the Sizzl catalogue")

            # Featured row: first up to 4
            featured = df.head(4)
            cols = st.columns(len(featured))

            for (idx, row), col in zip(featured.iterrows(), cols):
                with col:
                    cover_url = row.get("cover_url", "")
                    if isinstance(cover_url, str) and cover_url:
                        col.image(cover_url, use_column_width=False, width=110)
                    else:
                        col.write("📕 (no cover)")

                    title = row.get("title", "Untitled")
                    link = row.get("link", "")
                    author = row.get("author", "Unknown")

                    if isinstance(link, str) and link:
                        col.markdown(
                            f'<div class="sizzl-cover-title"><a href="{link}" target="_blank">{title}</a></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        col.markdown(
                            f'<div class="sizzl-cover-title">{title}</div>',
                            unsafe_allow_html=True
                        )
                    col.caption(author)

            st.markdown("---")
            st.markdown("### More details")

            # List view (skip the ones already shown in featured)
            remaining = df.iloc[4:]
            for _, row in remaining.iterrows():
                title = row.get("title", "Untitled")
                author = row.get("author", "Unknown")
                year = row.get("year", "")
                series_name = row.get("series_name", "")
                series_order = row.get("series_order", "")
                link = row.get("link", "")
                desc = row.get("description", "")

                meta_bits = [author]
                if year:
                    meta_bits.append(str(year))
                if series_name:
                    s = series_name
                    if series_order not in ("", None):
                        s += f" · #{series_order}"
                    meta_bits.append(s)
                meta_line = " · ".join(meta_bits)

                with st.container():
                    st.markdown('<div class="sizzl-card">', unsafe_allow_html=True)
                    if link:
                        st.markdown(f"**[{title}]({link})**")
                    else:
                        st.markdown(f"**{title}**")
                    st.markdown(
                        f'<span class="sizzl-meta">{meta_line}</span>',
                        unsafe_allow_html=True
                    )
                    if desc:
                        st.write(desc[:400] + ("..." if len(desc) > 400 else ""))

                    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Use the sidebar to search or just pick filters — you don’t have to type anything if you already know your vibes.")
