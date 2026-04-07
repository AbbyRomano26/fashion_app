import pandas as pd
import random

DATA_PATH = "data/clothing_items.csv"

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


def load_clothing_data():
    return pd.read_csv(DATA_PATH, encoding="utf-8-sig")


def score_item(row, dress_code, occasion, weather, style, color):
    score = 0
    reasons = []

    item_formality = str(row["formality"]).strip().lower()
    item_occasion = str(row["occasion"]).strip().lower()
    item_season = str(row["season"]).strip().lower()
    item_style = str(row["style"]).strip().lower()
    item_color = str(row["color"]).strip().lower()

    # Formality scoring
    if item_formality == "not specified":
        score += 1
    elif item_formality == dress_code:
        score += 5
        reasons.append("exact dress code match")
    elif dress_code in FORMALITY_COMPATIBILITY and item_formality in FORMALITY_COMPATIBILITY[dress_code]:
        score += 3
        reasons.append("compatible dress code")

    # Occasion scoring
    if item_occasion == "not specified":
        score += 1
    elif item_occasion == occasion:
        score += 4
        reasons.append("occasion match")

    # Weather/season scoring
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

    # Style scoring
    if style == "any":
        score += 1
    elif item_style == "not specified":
        score += 1
    elif item_style == style:
        score += 3
        reasons.append("style match")

    # Color scoring
    if color == "any":
        score += 1
    elif item_color == "not specified":
        score += 1
    elif item_color == color:
        score += 2
        reasons.append("color preference")

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
            "product_url": row["product_url"] if pd.notna(row["product_url"]) else "",
            "brand": row["brand"] if pd.notna(row["brand"]) else "Unknown",
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
        explanation_parts.append(f"It also takes {weather} weather into account.")

    if style != "any":
        explanation_parts.append(f"The pieces lean {style.replace('_', ' ')} in style.")

    if color != "any":
        explanation_parts.append(f"It includes your preference for {color} tones where possible.")

    explanation_parts.append(f"Selected pieces: {', '.join(piece_names)}.")
    return " ".join(explanation_parts)


def build_reason_summary(outfit_items):
    badge_counts = {
        "exact dress code match": 0,
        "compatible dress code": 0,
        "occasion match": 0,
        "seasonal fit": 0,
        "all-season piece": 0,
        "style match": 0,
        "color preference": 0
    }

    for item in outfit_items.values():
        for reason in item.get("reasons", []):
            if reason in badge_counts:
                badge_counts[reason] += 1

    badges = []

    if badge_counts["exact dress code match"] >= 2:
        badges.append("strong dress code fit")
    elif badge_counts["compatible dress code"] >= 2:
        badges.append("flexible dress code fit")

    if badge_counts["occasion match"] >= 2:
        badges.append("occasion-ready")

    if badge_counts["seasonal fit"] + badge_counts["all-season piece"] >= 2:
        badges.append("weather-aware")

    if badge_counts["style match"] >= 1:
        badges.append("style-aligned")

    if badge_counts["color preference"] >= 1:
        badges.append("color-aware")

    if not badges:
        badges.append("balanced recommendation")

    return badges


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
            used_names.add(outerwear["item_name"])

        if accessory and accessory["item_name"] not in used_names:
            outfit["accessory"] = accessory
            used_names.add(accessory["item_name"])

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
    if outerwear and outerwear["item_name"] not in used_names:
        used_names.add(outerwear["item_name"])

    accessory = pick_best_item(scored_items, "accessory", used_names)
    if accessory and accessory["item_name"] not in used_names:
        used_names.add(accessory["item_name"])

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
        "message": "Not enough pieces were available to build this outfit. Try adding more items or broadening your preferences."
    }