import requests
from urllib.parse import urlencode

# ===============================
# CONFIG (put your API here)
# ===============================
SHORTLINK_API_KEY = "YOUR_SHORTLINK_API_KEY"
SHORTLINK_API_URL = "https://shrinkme.io/api"  # Example


# ===============================
# 1) Generate Shortlink for User
# ===============================
def generate_shortlink(original_url: str, user_id: int) -> str:
    """
    Creates a shortlink with user tracking
    """
    params = {
        "api": SHORTLINK_API_KEY,
        "url": original_url,
        "alias": f"user{user_id}"
    }

    try:
        response = requests.get(SHORTLINK_API_URL, params=params, timeout=10)
        data = response.json()
        if "shortenedUrl" in data:
            return data["shortenedUrl"]
    except Exception as e:
        print("Shortlink error:", e)

    # fallback
    return original_url


# ===============================
# 2) Verify Shortlink Completion (basic logic)
# ===============================
def verify_shortlink_click(user_id: int) -> bool:
    """
    This is a placeholder.
    Real verification depends on your shortlink provider webhook or stats API.
    """
    # For now always return True after delay
    return True
