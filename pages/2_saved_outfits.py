import json
import os
import streamlit as st

st.set_page_config(
    page_title="Saved Outfits",
    page_icon="🖤",
    layout="wide"
)

SAVE_FILE = "saved_outfits.json"

if "saved_page_message" not in st.session_state:
    st.session_state.saved_page_message = ""


def load_saved_outfits():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_all_outfits(outfits):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(outfits, f, indent=2)


def delete_outfit_by_index(index):
    outfits = load_saved_outfits()
    if 0 <= index < len(outfits):
        deleted_name = outfits[index].get("name", "Outfit")
        outfits.pop(index)
        save_all_outfits(outfits)
        st.session_state.saved_page_message = f'"{deleted_name}" was deleted.'


def update_outfit(index, new_name=None, new_folder=None):
    outfits = load_saved_outfits()
    if 0 <= index < len(outfits):
        if new_name is not None:
            outfits[index]["name"] = new_name
        if new_folder is not None:
            outfits[index]["folder"] = new_folder
        save_all_outfits(outfits)
        st.session_state.saved_page_message = "Outfit updated."


saved_outfits = load_saved_outfits()

st.markdown(
    """
    <style>
    .main {
        background-color: #fffafc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1240px;
    }

    .hero-box {
        background: linear-gradient(135deg, #fff3f8, #f7f1ff);
        padding: 1.6rem;
        border-radius: 24px;
        margin-bottom: 1.4rem;
        border: 1px solid #f0dce8;
        text-align: center;
        box-shadow: 0 8px 24px rgba(68, 38, 58, 0.05);
    }

    .hero-subtitle {
        color: #6f5a67;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 1.32rem;
        font-weight: 700;
        margin-top: 0.4rem;
        margin-bottom: 0.9rem;
        color: #31222e;
    }

    .subtle-text {
        color: #7a6673;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    .saved-card {
        background: white;
        border: 1px solid #efdfe7;
        border-radius: 20px;
        padding: 1.1rem;
        box-shadow: 0 6px 18px rgba(68, 38, 58, 0.05);
        margin-bottom: 1rem;
        min-height: 260px;
    }

    .saved-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #2d1d2a;
        margin-bottom: 0.4rem;
    }

    .saved-meta {
        color: #6d5865;
        font-size: 0.94rem;
        margin-bottom: 0.22rem;
    }

    .folder-label {
        display: inline-block;
        padding: 0.34rem 0.72rem;
        border-radius: 999px;
        background-color: #f7e5ee;
        color: #4a2f3d;
        font-weight: 700;
        font-size: 0.84rem;
        margin-bottom: 0.6rem;
    }

    .empty-state {
        background: white;
        border: 1px dashed #e8cfe0;
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        color: #735f6c;
        box-shadow: 0 4px 14px rgba(68, 38, 58, 0.03);
        margin-top: 0.5rem;
    }

    .sidebar-note {
        background: #fff3f8;
        border: 1px solid #efd9e6;
        border-radius: 16px;
        padding: 0.9rem;
        color: #5d4754;
        font-size: 0.92rem;
        line-height: 1.45;
        margin-top: 1rem;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #df7fa8, #ba83e8);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.66rem 1rem;
        font-size: 0.94rem;
        font-weight: 700;
        box-shadow: 0 6px 16px rgba(186, 131, 232, 0.18);
    }

    div[data-testid="stSelectbox"] > label,
    div[data-testid="stTextInput"] > label {
        font-weight: 700;
        color: #4a3643;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.markdown("### Saved Looks")
    st.markdown("Rename outfits, move them between folders, or delete them.")
    st.markdown(
        """
        <div class="sidebar-note">
            <strong>Tips</strong><br>
            • Use folder filters to keep things organized.<br>
            • Rename generic saves so they’re easy to find later.<br>
            • Open each look to view shopping links.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin-bottom: 0.3rem;">Saved Outfits</h1>
        <p class="hero-subtitle">Browse, organize, rename, and manage your saved looks.</p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.saved_page_message:
    st.toast(st.session_state.saved_page_message)
    st.session_state.saved_page_message = ""

if not saved_outfits:
    st.markdown(
        """
        <div class="empty-state">
            <h3 style="margin-bottom: 0.5rem;">Nothing saved yet</h3>
            <p style="margin: 0;">Go to the Home page, generate a look, and save it here.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown('<div class="section-title">Your Closet of Looks</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle-text">Filter by folder and manage each saved outfit below.</div>', unsafe_allow_html=True)

    all_folders = sorted({outfit.get("folder", "Uncategorized") for outfit in saved_outfits})

    filter_col1, filter_col2 = st.columns([2, 5])

    with filter_col1:
        selected_folder = st.selectbox("Filter by folder", ["All"] + all_folders)

    with filter_col2:
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.caption(f"{len(saved_outfits)} saved look(s) total")

    if selected_folder == "All":
        display_indices = list(range(len(saved_outfits)))
    else:
        display_indices = [
            i for i, outfit in enumerate(saved_outfits)
            if outfit.get("folder", "Uncategorized") == selected_folder
        ]

    if not display_indices:
        st.markdown(
            """
            <div class="empty-state">
                <h3 style="margin-bottom: 0.5rem;">No looks in this folder</h3>
                <p style="margin: 0;">Try another folder or save a new outfit from the Home page.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        cols_per_row = 2

        for row_start in range(0, len(display_indices), cols_per_row):
            cols = st.columns(cols_per_row, gap="large")

            for col_offset, col in enumerate(cols):
                if row_start + col_offset >= len(display_indices):
                    continue

                idx = display_indices[row_start + col_offset]
                outfit = saved_outfits[idx]
                pieces = outfit["outfit"]["items"]
                piece_names = [piece["item_name"] for piece in pieces.values()]
                filters = outfit.get("filters", {})

                with col:
                    st.markdown(
                        f"""
                        <div class="saved-card">
                            <div class="folder-label">{outfit.get("folder", "Uncategorized")}</div>
                            <div class="saved-title">{outfit.get("name", "Untitled Outfit")}</div>
                            <div class="saved-meta"><strong>Dress code:</strong> {filters.get("dress_code", "").replace("_", " ").title()}</div>
                            <div class="saved-meta"><strong>Occasion:</strong> {filters.get("occasion", "").title()}</div>
                            <div class="saved-meta"><strong>Style:</strong> {filters.get("style", "").title()}</div>
                            <div class="saved-meta"><strong>Color:</strong> {filters.get("color", "").title()}</div>
                            <div class="saved-meta"><strong>Vibe:</strong> {filters.get("vibe", "").title()}</div>
                            <div class="saved-meta"><strong>Pieces:</strong> {", ".join(piece_names)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    with st.expander(f'View shopping links: {outfit.get("name", "Untitled Outfit")}'):
                        for category, piece in pieces.items():
                            st.markdown(f'**{category.replace("_", " ").title()}**: {piece["item_name"]}')
                            st.markdown(f'[Shop Similar]({piece["product_url"]})')

                    with st.expander(f'Edit: {outfit.get("name", "Untitled Outfit")}'):
                        with st.form(f"edit_form_{idx}"):
                            new_name = st.text_input(
                                "Rename outfit",
                                value=outfit.get("name", "Untitled Outfit")
                            )

                            folder_options = all_folders.copy()
                            if "Custom" not in folder_options:
                                folder_options.append("Custom")

                            current_folder = outfit.get("folder", "Uncategorized")
                            if current_folder not in folder_options:
                                folder_options.insert(0, current_folder)

                            selected_new_folder = st.selectbox(
                                "Move to folder",
                                folder_options,
                                index=folder_options.index(current_folder) if current_folder in folder_options else 0
                            )

                            custom_folder = ""
                            if selected_new_folder == "Custom":
                                custom_folder = st.text_input("Custom folder name")

                            save_changes = st.form_submit_button("Save Changes")

                        if save_changes:
                            final_folder = custom_folder.strip() if selected_new_folder == "Custom" else selected_new_folder
                            final_folder = final_folder if final_folder else "Uncategorized"

                            update_outfit(
                                idx,
                                new_name=new_name.strip() if new_name.strip() else "Untitled Outfit",
                                new_folder=final_folder
                            )
                            st.rerun()

                    if st.button(f'Delete "{outfit.get("name", "Untitled Outfit")}"', key=f"delete_{idx}"):
                        delete_outfit_by_index(idx)
                        st.rerun()