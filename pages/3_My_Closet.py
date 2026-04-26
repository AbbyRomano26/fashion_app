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
    "red", "orange", "yellow", "green", "blue", "purple",
    "pink", "blush", "hot pink", "coral", "peach", "mustard",
    "mint", "sage", "olive", "emerald", "teal",
    "light blue", "navy", "denim",
    "lavender", "lilac", "violet", "plum",
    "burgundy", "maroon",
    "black", "white", "gray", "charcoal", "silver",
    "cream", "beige", "tan", "camel", "taupe",
    "brown", "espresso", "gold", "multicolor", "print", "custom"
]

STYLE_OPTIONS = [
    "not specified", "classic", "minimal", "casual", "elegant", "edgy", "trendy"
]

SEASON_OPTIONS = [
    "not specified", "all", "warm", "cold"
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
    "not specified", "class", "office", "dinner", "wedding", "brunch", "party", "date"
]

CATEGORY_OPTIONS = [
    "top", "bottom", "shoes", "outerwear", "one_piece", "accessory"
]

COMFORT_OPTIONS = [
    "not specified", "very comfortable", "balanced", "fashion first"
]

BODY_TYPE_OPTIONS = [
    "not specified", "petite", "tall", "curvy", "straight", "athletic"
]

if "closet_message" not in st.session_state:
    st.session_state.closet_message = ""


def clean_text(value, fallback="Not specified", title_case=True):
    if value is None:
        return fallback
    text = str(value).strip()
    if text == "" or text.lower() == "not specified":
        return fallback
    text = text.replace("_", " ")
    return text.title() if title_case else text


def load_closet_items():
    if os.path.exists(CLOSET_FILE):
        with open(CLOSET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_closet_items(items):
    with open(CLOSET_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


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
        category = st.selectbox("Category", CATEGORY_OPTIONS, format_func=lambda x: clean_text(x))
        image_url = st.text_input("Image URL", placeholder="Paste clothing image link")

    with c2:
        color = st.selectbox("Color", COLOR_OPTIONS, format_func=lambda x: clean_text(x))
        custom_color = ""
        if color == "custom":
            custom_color = st.text_input("Custom color", placeholder="Ex: taupe")

        style = st.selectbox("Style", STYLE_OPTIONS, format_func=lambda x: clean_text(x))

    with c3:
        brand = st.text_input("Brand", placeholder="Everlane")
        season = st.selectbox("Season", SEASON_OPTIONS, format_func=lambda x: clean_text(x))
        budget = st.text_input("Budget", placeholder="Ex: under $100")
        comfort = st.selectbox("Comfort level", COMFORT_OPTIONS, format_func=lambda x: clean_text(x))

    with c4:
        formality = st.selectbox("Dress code", FORMALITY_OPTIONS, format_func=lambda x: clean_text(x))
        occasion = st.selectbox("Occasion", OCCASION_OPTIONS, format_func=lambda x: clean_text(x))
        body_type = st.selectbox("Body type", BODY_TYPE_OPTIONS, format_func=lambda x: clean_text(x))
        avoid_colors = st.text_input("Colors to avoid", placeholder="Ex: neon, orange")

    add_item = st.form_submit_button("Add to Closet")

if add_item and item_name.strip():
    final_color = custom_color.strip().lower() if color == "custom" else color.lower()

    closet_items.append({
        "item_name": item_name.strip().replace("_", " "),
        "category": category,
        "color": final_color,
        "style": style.lower(),
        "brand": brand.strip() if brand.strip() else "Unknown",
        "season": season.lower(),
        "formality": formality.lower(),
        "occasion": occasion.lower(),
        "image_url": image_url.strip(),
        "budget": budget.strip(),
        "comfort": comfort.lower(),
        "body_type": body_type.lower(),
        "avoid_colors": avoid_colors.strip().lower()
    })

    save_closet_items(closet_items)
    st.session_state.closet_message = f'"{item_name}" added to closet.'
    st.rerun()

if not closet_items:
    st.info("Your closet is empty.")
else:
    st.markdown("### Closet Items")
    cols_per_row = 3

    for i in range(0, len(closet_items), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            if i + j >= len(closet_items):
                continue

            item = closet_items[i + j]

            with col:
                if item.get("image_url"):
                    st.image(item["image_url"], use_column_width=True)

                st.markdown(
                    f"""
                    **{clean_text(item.get('item_name'))}**

                    Category: {clean_text(item.get('category'))}

                    Color: {clean_text(item.get('color'))}

                    Style: {clean_text(item.get('style'))}

                    Brand: {item.get('brand')}

                    Budget: {item.get('budget', 'Not specified')}

                    Comfort: {clean_text(item.get('comfort'))}

                    Body type: {clean_text(item.get('body_type'))}
                    """
                )
