import json
import os
import random
import pandas as pd

DATA_PATH = "data/clothing_items.csv"
CLOSET_FILE = "closet_items.json"

FORMALITY_COMPATIBILITY = {
    "casual": ["casual", "smart_casual", "streetwear"],
    "smart_casual": ["smart_casual", "casual", "business_casual"],
    "business_casual": ["business_casual", "smart_casual", "business_formal"],
    "business_formal": ["business_formal", "business_casual", "formal"],
    "formal": ["formal", "business_formal", "cocktail"],
    "cocktail": ["cocktail", "date_night", "formal"],
    "streetwear": ["streetwear", "casual", "smart_casual"],
    "date_night": ["date_night", "cocktail", "formal"]
}

SAMPLE_ITEMS = [
    {
        "item_name": "White Button Down",
        "category": "top",
        "formality": "business_casual",
        "season": "all",
        "color": "white",
        "style": "minimal",
        "occasion": "office",
        "product_url": "",
        "brand": "Everlane",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c",
        "budget": "under $100",
        "comfort": "balanced",
        "body_type": "not specified",
        "avoid_colors": ""
    },
    {
        "item_name": "Black Straight Pants",
        "category": "bottom",
        "formality": "business_casual",
        "season": "all",
        "color": "black",
        "style": "classic",
        "occasion": "office",
        "product_url": "",
        "brand": "Uniqlo",
        "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1",
        "budget": "under $100",
        "comfort": "very comfortable",
        "body_type": "straight",
        "avoid_colors": ""
    },
    {
        "item_name": "Black Loafers",
        "category": "shoes",
        "formality": "smart_casual",
        "season": "all",
        "color": "black",
        "style": "classic",
        "occasion": "office",
        "product_url": "",
        "brand": "Sam Edelman",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2",
        "budget": "under $150",
        "comfort": "balanced",
        "body_type": "not specified",
        "avoid_colors": ""
    },
    {
        "item_name": "Black Mini Dress",
        "category": "one_piece",
        "formality": "date_night",
        "season": "all",
        "color": "black",
        "style": "elegant",
        "occasion": "dinner",
        "product_url": "",
        "brand": "Zara",
        "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8",
        "budget": "under $100",
        "comfort": "balanced",
        "body_type": "straight",
        "avoid_colors": "neon"
    },
    {
        "item_name": "Cream Cardigan",
        "category": "outerwear",
        "formality": "smart_casual",
        "season": "cold",
        "color": "cream",
        "style": "minimal",
        "occasion": "brunch",
        "product_url": "",
        "brand": "Aritzia",
        "image_url": "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7",
        "budget": "under $150",
        "comfort": "very comfortable",
        "body_type": "petite",
        "avoid_colors": ""
    },
    {
        "item_name": "Gold Hoop Earrings",
        "category": "accessory",
        "formality": "smart_casual",
        "season": "all",
        "color": "gold",
        "style": "classic",
        "occasion": "dinner",
        "product_url": "",
        "brand": "Mejuri",
        "image_url": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908",
        "budget": "under $100",
        "comfort": "very comfortable",
        "body_type": "not specified",
        "avoid_colors": ""
    }
]


def normalize_item(item):
    defaults = {
        "item_name": "Unnamed Item",
        "category": "top",
        "formality": "not specified",
        "season": "all",
        "color": "not specified",
        "style": "not specified",
        "occasion": "not specified",
        "product_url": "",
        "brand": "Unknown",
        "image_url": "",
        "budget": "Not specified",
        "comfort": "not specified",
        "body_type": "not specified",
        "avoid_colors": ""
    }

    normalized = {}
    for key, default in defaults.items():
        value = item.get(key, default)
        if pd.isna(value):
            value = default
        normalized[key] = str(value).strip()

    return normalized


def load_closet_items():
    if os.path.exists(CLOSET_FILE):
        with open(CLOSET_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
        return [normalize_item(item) for item in items]
    return []


def load_csv_items():
    if not os.path.exists(DATA_PATH) or os.path.getsize(DATA_PATH) == 0:
        return SAMPLE_ITEMS

    try:
        df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
        if df.empty:
            return SAMPLE_ITEMS
        return [normalize_item(row.to_dict()) for _, row in df.iterrows()]
    except Exception:
        return SAMPLE_ITEMS


def load_clothing_data():
    closet_items = load_closet_items()
    csv_items = load_csv_items()

    # Use user's closet first. If closet is too small, add sample items so recommendations still work.
    all_items = closet_items + csv_items
    return pd.DataFrame(all_items)


def score_item(row, dress_code, occasion, weather, style, color):
    score = 0
    reasons = []

    item_formality = str(row["formality"]).strip().lower()
    item_occasion = str(row["occasion"]).strip().lower()
    item_season = str(row["season"]).strip().lower()
    item_style = str(row["style"]).strip().lower()
    item_color = str(row["color"]).strip().lower()

    if item_formality == "not specified":
        score += 1
    elif item_formality == dress_code:
        score += 5
        reasons.append("exact dress code match")
    elif dress_code in FORMALITY_COMPATIBILITY and item_formality in FORMALITY_COMPATIBILITY[dress_code]:
        score += 3
        reasons.append("compatible dress code")

    if item_occasion == "not specified":
        score += 1
    elif item_occasion == occasion:
        score += 4
        reasons.append("occasion match")

    if weather == "all":
        score += 1
    elif item_season == "not specified":
        score += 1
    elif item_season == weather:
        score += 3
        reasons.append("seasonal fit")
    elif item_season == "all":
        score += 2
        reasons.append("all-season piece")

    if style == "any":
        score += 1
    elif item_style == "not specified":
        score += 1
    elif item_style == style:
        score += 3
        reasons.append("style match")

    if color == "any":
        score += 1
    elif item_color == "not specified":
        score += 1
    elif item_color == color:
        score += 2
        reasons.append("color preference")

    if str(row.get("image_url", "")).strip():
        score += 1
        reasons.append("visual available")

    return score, reasons


def prepare_scored_items(df, dress_code, occasion, weather, style, color):
    scored_items = []

    for _, row in df.iterrows():
        score, reasons = score_item(row, dress_code, occasion, weather, style, color)

        item = {
            "item_name": row["item_name"],
            "category": row["category"],
            "formality": row["formality"],
            "season": row["season"],
            "color": row["color"],
            "style": row["style"],
            "occasion": row["occasion"],
            "product_url": row.get("product_url", ""),
            "brand": row.get("brand", "Unknown"),
            "image_url": row.get("image_url", ""),
            "budget": row.get("budget", "Not specified"),
            "comfort": row.get("comfort", "not specified"),
            "body_type": row.get("body_type", "not specified"),
            "avoid_colors": row.get("avoid_colors", ""),
            "score": score,
            "reasons": reasons
        }
        scored_items.append(item)

    return scored_items


def pick_best_item(items, category, used_names=None):
    if used_names is None:
        used_names = set()

    category_items = [
        item for item in items
        if item["category"] == category and item["item_name"] not in used_names
    ]

    if not category_items:
        return None

    category_items.sort(key=lambda x: x["score"], reverse=True)
    top_choices = category_items[:3] if len(category_items) >= 3 else category_items
    return random.choice(top_choices)


def generate_explanation(outfit_items, dress_code, occasion, weather, style, color):
    piece_names = [item["item_name"] for item in outfit_items.values()]

    explanation_parts = [
        f"This outfit is built for a {dress_code.replace('_', ' ')} look",
        f"with a focus on {occasion}."
    ]

    if weather != "all":
        explanation_parts.append(f"It also considers {weather} weather.")

    if style != "any":
        explanation_parts.append(f"The pieces lean {style.replace('_', ' ')} in style.")

    if color != "any":
        explanation_parts.append(f"It includes your preference for {color} tones where possible.")

    explanation_parts.append("It also shows images when available, so users can evaluate the look visually.")
    explanation_parts.append(f"Selected pieces: {', '.join(piece_names)}.")

    return " ".join(explanation_parts)


def build_reason_summary(outfit_items):
    badges = []

    for item in outfit_items.values():
        for reason in item.get("reasons", []):
            if reason not in badges:
                badges.append(reason)

    if not badges:
        badges.append("balanced recommendation")

    return badges[:5]


def generate_outfit(dress_code, occasion, weather, style, color):
    df = load_clothing_data()
    scored_items = prepare_scored_items(df, dress_code, occasion, weather, style, color)

    used_names = set()

    one_piece = pick_best_item(scored_items, "one_piece", used_names)
    shoes = pick_best_item(scored_items, "shoes", used_names)
    outerwear = pick_best_item(scored_items, "outerwear", used_names)
    accessory = pick_best_item(scored_items, "accessory", used_names)

    if one_piece and shoes:
        outfit = {
            "main_piece": one_piece,
            "shoes": shoes
        }

        used_names.update([one_piece["item_name"], shoes["item_name"]])

        if outerwear and outerwear["item_name"] not in used_names:
            outfit["outerwear"] = outerwear

        if accessory and accessory["item_name"] not in used_names:
            outfit["accessory"] = accessory

        return {
            "success": True,
            "items": outfit,
            "explanation": generate_explanation(outfit, dress_code, occasion, weather, style, color),
            "badges": build_reason_summary(outfit)
        }

    top = pick_best_item(scored_items, "top", used_names)
    if top:
        used_names.add(top["item_name"])

    bottom = pick_best_item(scored_items, "bottom", used_names)
    if bottom:
        used_names.add(bottom["item_name"])

    shoes = pick_best_item(scored_items, "shoes", used_names)
    if shoes:
        used_names.add(shoes["item_name"])

    outerwear = pick_best_item(scored_items, "outerwear", used_names)
    accessory = pick_best_item(scored_items, "accessory", used_names)

    if top and bottom and shoes:
        outfit = {
            "top": top,
            "bottom": bottom,
            "shoes": shoes
        }

        if outerwear:
            outfit["outerwear"] = outerwear

        if accessory:
            outfit["accessory"] = accessory

        return {
            "success": True,
            "items": outfit,
            "explanation": generate_explanation(outfit, dress_code, occasion, weather, style, color),
            "badges": build_reason_summary(outfit)
        }

    return {
        "success": False,
        "message": "Not enough pieces were available to build this outfit. Try adding more items."
    }
