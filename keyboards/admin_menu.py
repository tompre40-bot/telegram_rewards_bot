from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===============================
# Admin Main Menu Keyboard
# ===============================
def admin_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👥 Total Users", callback_data="admin_total_users"),
        InlineKeyboardButton("🚫 Ban / Unban User", callback_data="admin_ban_user"),
        InlineKeyboardButton("➕ Add / Remove Points", callback_data="admin_points"),
        InlineKeyboardButton("💰 Wallet Management", callback_data="admin_wallet"),
        InlineKeyboardButton("📝 Manage Tasks", callback_data="admin_tasks"),
        InlineKeyboardButton("📢 Sponsor Channels", callback_data="admin_sponsors"),
        InlineKeyboardButton("📨 Broadcast Message", callback_data="admin_broadcast"),
        InlineKeyboardButton("💳 Withdraw Requests", callback_data="admin_withdrawals"),
    )
    return keyboard


# ===============================
# Back to Admin Menu Button
# ===============================
def back_to_admin():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("⬅️ Back to Admin Panel", callback_data="menu_admin")
    )
    return keyboard


# ===============================
# Approve / Reject Keyboard
# ===============================
def approve_reject_keyboard(withdraw_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✅ Approve", callback_data=f"withdraw_approve_{withdraw_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"withdraw_reject_{withdraw_id}"),
    )
    return keyboard
