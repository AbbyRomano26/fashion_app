import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def get_image_from_product_page(url: str) -> str:
    """
    Try to extract a main image URL from a product or search page.
    Returns an empty string if nothing usable is found.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # 1. Best case: Open Graph image
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        return og_image["content"]

    # 2. Twitter card image
    twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
    if twitter_image and twitter_image.get("content"):
        return twitter_image["content"]

    # 3. Common lazy-loaded image patterns
    for img in soup.find_all("img"):
        for attr in ["src", "data-src", "data-original", "srcset"]:
            value = img.get(attr)
            if value:
                # If srcset exists, take the first URL
                if attr == "srcset":
                    first_url = value.split(",")[0].strip().split(" ")[0]
                    if first_url.startswith("http"):
                        return first_url
                    return urljoin(url, first_url)

                if value.startswith("http"):
                    return value
                return urljoin(url, value)

    return ""