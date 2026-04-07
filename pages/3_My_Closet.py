import json
import os
import streamlit as st

st.set_page_config(
    page_title="My Closet",
    page_icon="🧥",
    layout="wide"
)

CLOSET_FILE = "closet_items.json"

COLOR_OPTIONS = [
    "not specified",
    "black", "white", "gray", "charcoal", "silver",
    "cream", "beige", "tan", "camel", "brown", "espresso", "taupe",
    "navy", "blue", "light blue", "denim", "teal",
    "green", "olive", "sage", "mint", "emerald",
    "yellow", "mustard", "gold",
    "orange", "peach", "coral",
    "red", "burgundy", "maroon",
    "pink", "blush", "hot pink",
    "purple", "lavender", "lilac", "violet", "plum",
    "multicolor", "print", "custom"
]

STYLE_OPTIONS = [
    "not specified",
    "classic", "minimal", "casual", "elegant", "edgy", "trendy"
]

SEASON_OPTIONS = [
    "not specified",
    "all", "warm", "cold"
]

FORMALITY_OPTIONS = [
    "not specified",
    "casual",
    "smart_casual",
    "business_casual",
    "business_formal",
    "formal",
    "cocktail",
    "streetwear",
    "date_night"
]

OCCASION_OPTIONS = [
    "not specified",
    "class", "office", "dinner", "wedding", "brunch", "party", "date"
]

CATEGORY_OPTIONS = [
    "top", "bottom", "shoes", "outerwear", "one_piece", "accessory"
]

if "closet_message" not in st.session_state:
    st.session_state.closet_message = ""


def load_closet_items():
    if os.path.exists(CLOSET_FILE):
        with open(CLOSET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_closet_items(items):
    with open(CLOSET_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


def display_value(value, fallback="Not specified"):
    if value is None:
        return fallback
    text = str(value).strip()
    if text == "" or text.lower() == "not specified":
        return fallback
    return text.replace("_", " ").title()


closet_items = load_closet_items()

st.markdown("## My Closet")
st.caption("Add pieces you already own. Optional fields can be left unspecified.")

if st.session_state.closet_message:
    st.toast(st.session_state.closet_message)
    st.session_state.closet_message = ""

with st.form("add_closet_item"):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        item_name = st.text_input("Item name", placeholder="White Button Down")
        category = st.selectbox("Category", CATEGORY_OPTIONS)

    with c2:
        color = st.selectbox("Color", COLOR_OPTIONS)
        custom_color = ""
        if color == "custom":
            custom_color = st.text_input("Custom color", placeholder="Ex: taupe")
        style = st.selectbox("Style", STYLE_OPTIONS)

    with c3:
        brand = st.text_input("Brand", placeholder="Everlane")
        season = st.selectbox("Season", SEASON_OPTIONS)

    with c4:
        formality = st.selectbox("Dress code", FORMALITY_OPTIONS)
        occasion = st.selectbox("Occasion", OCCASION_OPTIONS)

    add_item = st.form_submit_button("Add to Closet")

if add_item and item_name.strip():
    if color == "custom":
        final_color = custom_color.strip().lower() if custom_color.strip() else "not specified"
    else:
        final_color = color.lower()

    final_style = style.lower()
    final_season = season.lower()
    final_formality = formality.lower()
    final_occasion = occasion.lower()

    closet_items.append({
        "item_name": item_name.strip(),
        "category": category,
        "color": final_color,
        "style": final_style,
        "brand": brand.strip() if brand.strip() else "Unknown",
        "season": final_season,
        "formality": final_formality,
        "occasion": final_occasion
    })

    save_closet_items(closet_items)
    st.session_state.closet_message = f'"{item_name.strip()}" added to closet.'
    st.rerun()

if not closet_items:
    st.info("Your closet is empty. Add a few staple pieces to get started.")
else:
    st.markdown("### Closet Items")
    cols_per_row = 3

    for row_start in range(0, len(closet_items), cols_per_row):
        cols = st.columns(cols_per_row)
        for offset, col in enumerate(cols):
            if row_start + offset >= len(closet_items):
                continue

            idx = row_start + offset
            item = closet_items[idx]

            with col:
                st.markdown(
                    f"""
                    <div style="
                        background:white;
                        border:1px solid #e8e3eb;
                        border-radius:22px;
                        padding:1rem;
                        min-height:220px;
                        box-shadow:0 8px 20px rgba(40,36,48,0.04);
                        margin-bottom:1rem;
                    ">
                        <div style="font-size:1.05rem;font-weight:800;color:#1f2230;margin-bottom:0.35rem;">
                            {item.get('item_name', 'Unnamed Item')}
                        </div>
                        <div style="color:#6d7283;font-size:0.94rem;">Category: {display_value(item.get('category'), 'Unknown')}</div>
                        <div style="color:#6d7283;font-size:0.94rem;">Color: {display_value(item.get('color'))}</div>
                        <div style="color:#6d7283;font-size:0.94rem;">Style: {display_value(item.get('style'))}</div>
                        <div style="color:#6d7283;font-size:0.94rem;">Brand: {item.get('brand', 'Unknown')}</div>
                        <div style="color:#6d7283;font-size:0.94rem;">Season: {display_value(item.get('season'))}</div>
                        <div style="color:#6d7283;font-size:0.94rem;">Dress code: {display_value(item.get('formality'))}</div>
                        <div style="color:#6d7283;font-size:0.94rem;">Occasion: {display_value(item.get('occasion'))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(f'Delete {item.get("item_name", "Item")}', key=f"delete_closet_{idx}"):
                    closet_items.pop(idx)
                    save_closet_items(closet_items)
                    st.session_state.closet_message = "Closet item removed."
                    st.rerun()