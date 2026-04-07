import json
import os
import streamlit as st
from outfit_engine import generate_outfit

st.set_page_config(
    page_title="Generate Outfit",
    page_icon="✨",
    layout="wide"
)

SAVE_FILE = "saved_outfits.json"

COLOR_OPTIONS = [
    "any",
    "black",
    "white",
    "gray",
    "charcoal",
    "silver",
    "cream",
    "beige",
    "tan",
    "camel",
    "brown",
    "espresso",
    "taupe",
    "navy",
    "blue",
    "light blue",
    "denim",
    "teal",
    "green",
    "olive",
    "sage",
    "mint",
    "emerald",
    "yellow",
    "mustard",
    "gold",
    "orange",
    "peach",
    "coral",
    "red",
    "burgundy",
    "maroon",
    "pink",
    "blush",
    "hot pink",
    "purple",
    "lavender",
    "lilac",
    "violet",
    "plum",
    "multicolor",
    "print",
    "custom"
]

DEFAULT_FILTERS = {
    "dress_code": "casual",
    "occasion": "class",
    "weather": "all",
    "style": "any",
    "color": "any",
    "vibe": "polished"
}

if "prefill_filters" in st.session_state:
    prefill = st.session_state.pop("prefill_filters")
    st.session_state.filter_dress_code = prefill.get("dress_code", DEFAULT_FILTERS["dress_code"])
    st.session_state.filter_occasion = prefill.get("occasion", DEFAULT_FILTERS["occasion"])
    st.session_state.filter_weather = prefill.get("weather", DEFAULT_FILTERS["weather"])
    st.session_state.filter_style = prefill.get("style", DEFAULT_FILTERS["style"])
    st.session_state.filter_color = prefill.get("color", DEFAULT_FILTERS["color"])
    st.session_state.filter_vibe = prefill.get("vibe", DEFAULT_FILTERS["vibe"])

if "current_outfit" not in st.session_state:
    st.session_state.current_outfit = None
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = DEFAULT_FILTERS.copy()
if "show_save_form" not in st.session_state:
    st.session_state.show_save_form = False
if "save_message" not in st.session_state:
    st.session_state.save_message = ""
if "action_message" not in st.session_state:
    st.session_state.action_message = ""
if "do_reset_filters" not in st.session_state:
    st.session_state.do_reset_filters = False


def load_saved_outfits():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_outfit_to_file(entry):
    outfits = load_saved_outfits()
    outfits.append(entry)
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(outfits, f, indent=2)


def reset_filters():
    st.session_state.filter_dress_code = DEFAULT_FILTERS["dress_code"]
    st.session_state.filter_occasion = DEFAULT_FILTERS["occasion"]
    st.session_state.filter_weather = DEFAULT_FILTERS["weather"]
    st.session_state.filter_style = DEFAULT_FILTERS["style"]
    st.session_state.filter_color = DEFAULT_FILTERS["color"]
    st.session_state.filter_vibe = DEFAULT_FILTERS["vibe"]
    st.session_state.current_outfit = None
    st.session_state.show_save_form = False


def generate_and_store_outfit(dress_code, occasion, weather, style, color, vibe):
    result = generate_outfit(
        dress_code=dress_code,
        occasion=occasion,
        weather=weather,
        style=style,
        color=color
    )
    st.session_state.current_outfit = result
    st.session_state.last_inputs = {
        "dress_code": dress_code,
        "occasion": occasion,
        "weather": weather,
        "style": style,
        "color": color,
        "vibe": vibe
    }


if st.session_state.do_reset_filters:
    reset_filters()
    st.session_state.do_reset_filters = False

st.markdown("## Generate Outfit")
st.caption("Build a look using your preferred dress code, occasion, and vibe.")

if st.session_state.action_message:
    st.toast(st.session_state.action_message)
    st.session_state.action_message = ""

if st.session_state.save_message:
    st.success(st.session_state.save_message)
    st.session_state.save_message = ""

with st.form("outfit_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        dress_code = st.selectbox(
            "Dress code",
            ["casual", "smart_casual", "business_casual", "business_formal", "formal", "cocktail", "streetwear", "date_night"],
            key="filter_dress_code"
        )
        occasion = st.selectbox(
            "Occasion",
            ["class", "office", "dinner", "wedding", "brunch", "party", "date"],
            key="filter_occasion"
        )

    with col2:
        weather = st.selectbox("Weather", ["warm", "cold", "all"], key="filter_weather")
        style = st.selectbox("Preferred style", ["any", "classic", "minimal", "casual", "elegant", "edgy", "trendy"], key="filter_style")

    with col3:
        color = st.selectbox("Preferred color", COLOR_OPTIONS, key="filter_color")
        custom_color = ""
        if color == "custom":
            custom_color = st.text_input("Custom color", placeholder="Ex: taupe")
        vibe = st.selectbox("Vibe", ["polished", "effortless", "chic", "cool", "romantic", "modern"], key="filter_vibe")

    btn1, btn2, btn3 = st.columns([2, 2, 6])
    with btn1:
        submitted = st.form_submit_button("Generate Outfit")
    with btn2:
        reset_clicked = st.form_submit_button("Reset")

if reset_clicked:
    st.session_state.do_reset_filters = True
    st.rerun()

if submitted:
    final_color = custom_color.strip().lower() if color == "custom" else color.lower()
    if not final_color:
        final_color = "any"
    generate_and_store_outfit(dress_code, occasion, weather, style, final_color, vibe)


def display_item_card(category, item):
    st.markdown(
        f"""
        <div style="
            background:white;
            border:1px solid #e8e3eb;
            border-radius:22px;
            padding:1rem;
            min-height:210px;
            box-shadow:0 8px 20px rgba(40,36,48,0.04);
            margin-bottom:1rem;
        ">
            <div style="font-size:0.86rem;font-weight:700;text-transform:uppercase;color:#b06a8d;margin-bottom:0.5rem;">
                {category.replace('_', ' ')}
            </div>
            <div style="font-size:1.08rem;font-weight:800;color:#1f2230;margin-bottom:0.5rem;">
                {item['item_name']}
            </div>
            <div style="color:#6d7283;font-size:0.94rem;">Brand: {item.get('brand', 'Unknown')}</div>
            <div style="color:#6d7283;font-size:0.94rem;">Color: {str(item.get('color', 'Unknown')).title()}</div>
            <div style="color:#6d7283;font-size:0.94rem;">Style: {str(item.get('style', 'Unknown')).title()}</div>
            <div style="color:#6d7283;font-size:0.94rem;">Occasion: {str(item.get('occasion', 'Unknown')).title()}</div>
            <a href="{item['product_url']}" target="_blank" style="
                display:inline-block;
                margin-top:0.9rem;
                padding:0.62rem 1rem;
                border-radius:10px;
                background:#f7e5ee;
                color:#4a2f3d;
                text-decoration:none;
                font-weight:700;
            ">Shop Similar</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if st.session_state.current_outfit and st.session_state.current_outfit["success"]:
    result = st.session_state.current_outfit

    st.success("Outfit generated successfully.")

    st.markdown("### Why this was chosen")
    badge_html = ""
    for badge in result.get("badges", []):
        badge_html += f"""
        <span style="
            display:inline-block;
            background:#f7e5ee;
            color:#4a2f3d;
            padding:0.45rem 0.8rem;
            border-radius:999px;
            margin-right:0.45rem;
            margin-bottom:0.45rem;
            font-weight:700;
            font-size:0.9rem;
        ">{badge}</span>
        """
    st.markdown(badge_html, unsafe_allow_html=True)

    items = list(result["items"].items())
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(items):
                category, item = items[i + j]
                with col:
                    display_item_card(category, item)

    st.info(result["explanation"])

    action_col1, action_col2, action_col3 = st.columns([1, 1, 4])

    with action_col1:
        if st.button("Save Look"):
            st.session_state.show_save_form = True

    with action_col2:
        if st.button("Hide Save") and st.session_state.show_save_form:
            st.session_state.show_save_form = False
            st.rerun()

    if st.session_state.show_save_form:
        st.markdown("### Save This Outfit")

        existing_outfits = load_saved_outfits()
        existing_folders = sorted(
            {o.get("folder", "Uncategorized") for o in existing_outfits if o.get("folder")}
        )

        folder_choices = existing_folders + ["Work", "Weekend", "Going Out", "Date Night", "Events", "Favorites"]
        folder_choices = list(dict.fromkeys(folder_choices))
        folder_choices.append("Custom")

        with st.form("save_outfit_form"):
            save_col1, save_col2 = st.columns(2)

            with save_col1:
                outfit_name = st.text_input("Outfit name", placeholder="Ex: Minimal Work Look")

            with save_col2:
                folder = st.selectbox("Folder", folder_choices)

            custom_folder = ""
            if folder == "Custom":
                custom_folder = st.text_input("Custom folder name", placeholder="Ex: Spring Looks")

            save_submit = st.form_submit_button("Confirm Save")

        if save_submit:
            final_folder = custom_folder.strip() if folder == "Custom" else folder
            final_name = outfit_name.strip() if outfit_name.strip() else "Untitled Outfit"

            save_entry = {
                "name": final_name,
                "folder": final_folder if final_folder else "Uncategorized",
                "filters": st.session_state.last_inputs,
                "outfit": st.session_state.current_outfit
            }

            save_outfit_to_file(save_entry)
            st.session_state.show_save_form = False
            st.session_state.save_message = f'"{final_name}" was saved to {save_entry["folder"]}.'
            st.rerun()

elif st.session_state.current_outfit and not st.session_state.current_outfit["success"]:
    st.error(st.session_state.current_outfit["message"])