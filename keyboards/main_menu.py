from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===============================
# Main Menu Keyboard
# ===============================
def main_menu():
    """
    Returns the main menu keyboard for users
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🎯 Tasks", callback_data="menu_tasks"),
        InlineKeyboardButton("👥 Refer", callback_data="menu_refer"),
        InlineKeyboardButton("🎁 Daily", callback_data="menu_daily"),
        InlineKeyboardButton("💰 Wallet", callback_data="menu_wallet"),
        InlineKeyboardButton("🏆 Levels", callback_data="menu_levels"),
        InlineKeyboardButton("📊 Stats", callback_data="menu_stats")
    )
    return keyboard

# ===============================
# Back to Menu Keyboard
# ===============================
def back_to_menu():
    """
    Returns a simple keyboard with a 'Back to Menu' button
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu_back"))
    return keyboard

# ===============================
# Admin Panel Keyboard
# ===============================
def admin_menu():
    """
    Returns the admin panel keyboard
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👥 Total Users", callback_data="admin_total_users"),
        InlineKeyboardButton("🚫 Ban/Unban User", callback_data="admin_ban_user"),
        InlineKeyboardButton("➕ Add/Remove Points", callback_data="admin_points"),
        InlineKeyboardButton("💰 Wallet Management", callback_data="admin_wallet"),
        InlineKeyboardButton("📝 Manage Tasks", callback_data="admin_tasks"),
        InlineKeyboardButton("📢 Sponsor Channels", callback_data="admin_sponsors"),
        InlineKeyboardButton("📨 Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton("💳 Withdrawals", callback_data="admin_withdrawals"),
    )
    return keyboard
