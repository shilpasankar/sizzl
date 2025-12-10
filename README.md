# 🔥 SizzlClub

**SizzlClub** is a cozy little corner of the internet for romance readers — especially the ones who love tropes, spice, and yelling “ONE MORE CHAPTER” at 3am.

Live app: **https://sizzlclub.streamlit.app/**

> _Find books. Follow vibes. Community coming soon._

---

## ✨ What’s inside (so far)

### 📚 Book Finder

A simple, vibes-first book search built on top of the free **Open Library** API.

You can:

- Search by **title, author, or trope**
- See subjects/tags associated with each book
- Get a very soft “spice guess” based on metadata
- Use the sidebar to tweak result count & high-level vibes

_File: `sizzl/pages/Book_Finder.py`_

---

### 💬 Community (placeholder)

This page is a designed placeholder for the future **SizzlClub community**.

Planned features:

- Topic-based threads (per book or trope)  
- Discussions like “rate the spice”, “is this really enemies to lovers”, etc.  
- Book-linked posts created directly from search results  
- Community-voted spice meters  

_File: `sizzl/pages/Community.py`_

---

## 🧱 Tech stack

- **Python**
- **Streamlit** for the UI
- **Requests** for Open Library queries
- (Later: simple JSON or SQLite-based storage for community threads)

Minimal `requirements.txt`:

```txt
streamlit>=1.36
requests>=2.31
