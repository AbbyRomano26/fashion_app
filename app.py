import json
import os
import streamlit as st
from outfit_engine import generate_outfit

st.set_page_config(
    page_title="Fitly",
    page_icon="👗",
    layout="wide"
)

CLOSET_FILE = "closet_items.json"

DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1445205170230-053b83016050"

RECOMMENDED_LOOKS = [
    {
        "title": "Minimal Work Look",
        "subtitle": "Clean lines and polished staples",
        "dress_code": "business_casual",
        "occasion": "office",
        "style": "minimal",
        "weather": "all",
        "color": "any",
        "vibe": "polished"
    },
    {
        "title": "Dinner Edit",
        "subtitle": "Elevated pieces for evening plans",
        "dress_code": "date_night",
        "occasion": "dinner",
        "style": "elegant",
        "weather": "all",
        "color": "black",
        "vibe": "romantic"
    },
    {
        "title": "Weekend Chic",
        "subtitle": "Relaxed but put together",
        "dress_code": "smart_casual",
        "occasion": "brunch",
        "style": "classic",
        "weather": "all",
        "color": "any",
        "vibe": "effortless"
    }
]

if "home_open_sections" not in st.session_state:
    st.session_state.home_open_sections = {
        "today": False,
        "look_0": False,
        "look_1": False,
        "look_2": False
    }


def clean_text(value, title_case=True):
    text = str(value).replace("_", " ")
    return text.title() if title_case else text


def load_closet_items():
    if os.path.exists(CLOSET_FILE):
        with open(CLOSET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_today_suggestion():
    return generate_outfit(
        dress_code="smart_casual",
        occasion="brunch",
        weather="all",
        style="classic",
        color="any"
    )


def get_look_result(look):
    return generate_outfit(
        dress_code=look["dress_code"],
        occasion=look["occasion"],
        weather=look["weather"],
        style=look["style"],
        color=look["color"]
    )


def toggle_section(section_key):
    for key in st.session_state.home_open_sections:
        if key != section_key:
            st.session_state.home_open_sections[key] = False
    st.session_state.home_open_sections[section_key] = not st.session_state.home_open_sections[section_key]


def get_image_url(item):
    image_url = str(item.get("image_url", "")).strip()

    if not image_url or image_url.lower() in ["not specified", "none", "nan"]:
        return DEFAULT_IMAGE_URL

    return image_url


def render_piece_card(category, item):
    image_url = get_image_url(item)
    st.image(image_url, use_column_width=True)

    product_url = item.get("product_url", "")
    shop_link_html = ""

    if product_url:
        shop_link_html = f'<a href="{product_url}" target="_blank" class="shop-link">Browse Similar</a>'

    st.markdown(
        f"""
        <div class="piece-card">
            <div class="piece-label">{clean_text(category)}</div>
            <div class="piece-name">{clean_text(item.get("item_name", "Unnamed Item"))}</div>
            <div class="piece-meta">Brand: {item.get("brand", "Unknown")}</div>
            <div class="piece-meta">Color: {clean_text(item.get("color", "Unknown"))}</div>
            <div class="piece-meta">Style: {clean_text(item.get("style", "Unknown"))}</div>
            <div class="piece-meta">Occasion: {clean_text(item.get("occasion", "Unknown"))}</div>
            <div class="piece-meta">Comfort: {clean_text(item.get("comfort", "Not specified"))}</div>
            <div class="piece-meta">Body Type: {clean_text(item.get("body_type", "Not specified"))}</div>
            <div class="piece-meta">Avoid Colors: {item.get("avoid_colors", "Not specified") or "Not specified"}</div>
            {shop_link_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_badges(badges):
    if not badges:
        return

    badge_html = ""
    for badge in badges:
        badge_html += f'<span class="pill">{clean_text(badge)}</span>'

    st.markdown(badge_html, unsafe_allow_html=True)


def render_outfit_summary(result):
    if not result["success"]:
        st.markdown(
            """
            <div class="empty-note-box">
                Not enough matching pieces were found for this look yet.
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    st.markdown(
        f"""
        <div class="summary-box">
            <div class="summary-title">Why this works</div>
            <div class="summary-text">{clean_text(result["explanation"], title_case=False)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    render_badges(result.get("badges", []))

    items = list(result["items"].items())

    for i in range(0, len(items), 2):
        cols = st.columns(2, gap="large")

        for j, col in enumerate(cols):
            if i + j < len(items):
                category, item = items[i + j]

                with col:
                    render_piece_card(category, item)


def render_closet_preview_items(closet_items):
    if not closet_items:
        st.markdown(
            '<div class="empty-note">No closet items yet. Add pieces in My Closet to get started.</div>',
            unsafe_allow_html=True
        )
        return

    newest_items = list(reversed(closet_items))[:4]

    for item in newest_items:
        st.image(get_image_url(item), use_column_width=True)

        st.markdown(
            f"""
            <div class="closet-mini-card">
                <div class="closet-mini-name">{clean_text(item.get("item_name", "Unnamed Item"))}</div>
                <div class="closet-mini-meta">
                    {clean_text(item.get("category", "item"))} • {item.get("brand", "Unknown")}
                </div>
                <div class="closet-mini-meta">
                    Comfort: {clean_text(item.get("comfort", "Not specified"))}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


closet_items = load_closet_items()
today_result = get_today_suggestion()
recommended_results = [get_look_result(look) for look in RECOMMENDED_LOOKS]

st.markdown(
    """
    <style>
    .main {
        background-color: #f8f7fa;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 2.2rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
        max-width: 1280px;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .sidebar-note {
        background: #f7f0f5;
        border: 1px solid #e8dbe4;
        border-radius: 16px;
        padding: 0.9rem;
        color: #5d4d57;
        font-size: 0.92rem;
        line-height: 1.45;
        margin-top: 1rem;
    }

    .hero-wrap {
        margin-top: 0.35rem;
        margin-bottom: 1.6rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1f2230;
        margin-bottom: 0.2rem;
        line-height: 1.08;
    }

    .hero-subtitle {
        color: #6c7285;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .top-card {
        background: #ffffff;
        border: 1px solid #e8e3eb;
        border-radius: 26px;
        padding: 1.25rem;
        box-shadow: 0 8px 20px rgba(40, 36, 48, 0.05);
        height: 100%;
    }

    .suggested-card {
        background: #eef4ff;
        border: 1px solid #d7e2f8;
    }

    .card-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #1f2230;
        margin-bottom: 0.2rem;
    }

    .card-subtitle {
        color: #71778a;
        font-size: 0.97rem;
        margin-bottom: 1rem;
        line-height: 1.45;
    }

    .pill {
        display: inline-block;
        background: white;
        border: 1px solid #d8dbe6;
        color: #4e5364;
        border-radius: 10px;
        padding: 0.38rem 0.8rem;
        margin-right: 0.45rem;
        margin-bottom: 0.45rem;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .section-title {
        font-size: 1.42rem;
        font-weight: 800;
        color: #1f2230;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .look-card {
        background: white;
        border: 1px solid #e8e3eb;
        border-radius: 24px;
        padding: 1.1rem;
        min-height: 210px;
        box-shadow: 0 8px 20px rgba(40, 36, 48, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .look-title {
        font-size: 1.12rem;
        font-weight: 800;
        color: #1f2230;
        margin-bottom: 0.3rem;
    }

    .look-subtitle {
        color: #767b8d;
        font-size: 0.93rem;
        margin-bottom: 0.9rem;
        line-height: 1.45;
    }

    .look-tag {
        display: inline-block;
        background: #f7f0f5;
        border: 1px solid #eadce6;
        color: #5d4d57;
        border-radius: 999px;
        padding: 0.28rem 0.65rem;
        margin-right: 0.35rem;
        margin-bottom: 0.55rem;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .summary-box {
        background: #fdfbff;
        border: 1px solid #e7deef;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .summary-title {
        font-size: 1rem;
        font-weight: 800;
        color: #1f2230;
        margin-bottom: 0.4rem;
    }

    .summary-text {
        color: #666d80;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .piece-card {
        background: white;
        border: 1px solid #e8e3eb;
        border-radius: 20px;
        padding: 1rem;
        min-height: 210px;
        box-shadow: 0 8px 18px rgba(40, 36, 48, 0.04);
        margin-top: 0.8rem;
        margin-bottom: 0.6rem;
    }

    .piece-label {
        font-size: 0.84rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #b06a8d;
        margin-bottom: 0.45rem;
    }

    .piece-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #1f2230;
        margin-bottom: 0.45rem;
    }

    .piece-meta {
        color: #6d7283;
        font-size: 0.93rem;
        margin-bottom: 0.22rem;
    }

    .shop-link {
        display: inline-block;
        margin-top: 0.8rem;
        padding: 0.58rem 0.95rem;
        border-radius: 10px;
        background: #f7e5ee;
        color: #4a2f3d !important;
        text-decoration: none;
        font-weight: 700;
    }

    .closet-mini-card {
        background: #faf9fc;
        border: 1px solid #e7e2eb;
        border-radius: 16px;
        padding: 0.85rem 0.95rem;
        margin-bottom: 0.65rem;
    }

    .closet-mini-name {
        font-size: 0.98rem;
        font-weight: 750;
        color: #1f2230;
        margin-bottom: 0.18rem;
    }

    .closet-mini-meta {
        color: #74798b;
        font-size: 0.9rem;
    }

    .closet-footer {
        margin-top: 0.9rem;
        color: #767b8d;
        font-size: 0.94rem;
    }

    .empty-note {
        color: #767b8d;
        font-size: 0.95rem;
        margin-top: 0.7rem;
    }

    .empty-note-box {
        background: #fff;
        border: 1px dashed #d9dce4;
        border-radius: 16px;
        padding: 1rem;
        color: #767b8d;
        margin-top: 1rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #df7fa8, #ba83e8);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.72rem 1rem;
        font-weight: 700;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)

    st.markdown("### Navigation")
    st.page_link("app.py", label="Home", icon="🏠")

    if os.path.exists("pages/3_My_Closet.py"):
        st.page_link("pages/3_My_Closet.py", label="My Closet", icon="🧥")

    st.markdown(
        """
        <div class="sidebar-note">
            Browse curated looks here and use My Closet to add personalized items with images.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-title">Good morning</div>
        <div class="hero-subtitle">Here’s your best visual outfit recommendation for today.</div>
    </div>
    """,
    unsafe_allow_html=True
)

top_col1, top_col2 = st.columns(2, gap="large")

with top_col1:
    st.markdown(
        """
        <div class="top-card suggested-card">
            <div class="card-title">Today’s Suggested Outfit</div>
            <div class="card-subtitle">A visual outfit recommendation using available closet and sample items.</div>
        """,
        unsafe_allow_html=True
    )

    if today_result["success"]:
        for piece in today_result["items"].values():
            st.markdown(
                f'<span class="pill">{clean_text(piece.get("item_name", "Unnamed Item"))}</span>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="empty-note">No strong suggestion available yet.</div>', unsafe_allow_html=True)

    if st.button("View Today’s Outfit Summary", key="today_summary_btn"):
        toggle_section("today")

    st.markdown("</div>", unsafe_allow_html=True)

with top_col2:
    st.markdown(
        """
        <div class="top-card">
            <div class="card-title">Your Closet</div>
            <div class="card-subtitle">Newest personalized items you’ve added.</div>
        """,
        unsafe_allow_html=True
    )

    render_closet_preview_items(closet_items)

    closet_footer_col1, closet_footer_col2 = st.columns([2, 1])

    with closet_footer_col1:
        st.markdown(
            f'<div class="closet-footer">{len(closet_items)} item(s) saved</div>',
            unsafe_allow_html=True
        )

    with closet_footer_col2:
        if os.path.exists("pages/3_My_Closet.py"):
            if st.button("See All Closet", key="see_all_closet_btn"):
                st.switch_page("pages/3_My_Closet.py")

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.home_open_sections["today"]:
    render_outfit_summary(today_result)

st.markdown('<div class="section-title">Recommended Looks</div>', unsafe_allow_html=True)

look_cols = st.columns(3, gap="large")

for i, look in enumerate(RECOMMENDED_LOOKS):
    with look_cols[i]:
        st.markdown(
            f"""
            <div class="look-card">
                <div>
                    <div class="look-title">{look["title"]}</div>
                    <div class="look-subtitle">{look["subtitle"]}</div>
                    <span class="look-tag">{clean_text(look["dress_code"])}</span>
                    <span class="look-tag">{clean_text(look["occasion"])}</span>
                    <span class="look-tag">{clean_text(look["style"])}</span>
                </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("View Details", key=f"view_look_{i}"):
            toggle_section(f"look_{i}")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.home_open_sections[f"look_{i}"]:
            render_outfit_summary(recommended_results[i])

st.caption("AI App Development Prototype • Fitly")
