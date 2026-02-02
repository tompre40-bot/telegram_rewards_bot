from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from database import get_session, User, Withdrawal, Task, Sponsor, Setting
from config import ADMIN_IDS
from datetime import datetime

router = Router()

# ===============================
# Admin Main Menu
# ===============================
def admin_keyboard():
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

# ===============================
# Middleware: Check Admin
# ===============================
async def is_admin(user_id: int):
    return user_id in ADMIN_IDS

# ===============================
# Admin Panel Entry
# ===============================
@router.callback_query(F.data == "menu_admin")
async def admin_panel(call: CallbackQuery):
    if not await is_admin(call.from_user.id):
        await call.answer("❌ You are not an admin.", show_alert=True)
        return
    await call.message.answer("⚙️ Admin Panel:", reply_markup=admin_keyboard())
    await call.answer()

# ===============================
# View Total Users
# ===============================
@router.callback_query(F.data == "admin_total_users")
async def view_total_users(call: CallbackQuery):
    if not await is_admin(call.from_user.id):
        await call.answer("❌ Not authorized.", show_alert=True)
        return

    session = get_session()
    total_users = session.query(User).count()
    banned_users = session.query(User).filter_by(is_banned=True).count()
    session.close()

    await call.message.answer(f"👥 Total Users: {total_users}\n🚫 Banned Users: {banned_users}")
    await call.answer()

# ===============================
# Withdrawals Management
# ===============================
@router.callback_query(F.data == "admin_withdrawals")
async def view_withdrawals(call: CallbackQuery):
    if not await is_admin(call.from_user.id):
        await call.answer("❌ Not authorized.", show_alert=True)
        return

    session = get_session()
    withdrawals = session.query(Withdrawal).filter_by(status="pending").all()
    if not withdrawals:
        await call.message.answer("💳 No pending withdrawals.")
        session.close()
        await call.answer()
        return

    for wd in withdrawals:
        user = session.query(User).filter_by(id=wd.user_id).first()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("✅ Approve", callback_data=f"withdraw_approve_{wd.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"withdraw_reject_{wd.id}")
        )
        await call.message.answer(
            f"💳 Withdrawal Request\n"
            f"User: {user.username or user.telegram_id}\n"
            f"Amount: ₹{wd.amount}\n"
            f"UPI: {wd.upi_id}\n"
            f"Status: {wd.status}",
            reply_markup=keyboard
        )
    session.close()
    await call.answer()

# ===============================
# Approve / Reject Withdrawals
# ===============================
@router.callback_query(F.data.startswith("withdraw_approve_") | F.data.startswith("withdraw_reject_"))
async def handle_withdraw_approval(call: CallbackQuery):
    if not await is_admin(call.from_user.id):
        await call.answer("❌ Not authorized.", show_alert=True)
        return

    session = get_session()
    action, wd_id = call.data.split("_")[1], call.data.split("_")[2]
    withdrawal = session.query(Withdrawal).filter_by(id=int(wd_id)).first()
    if not withdrawal:
        await call.answer("❌ Withdrawal not found.", show_alert=True)
        session.close()
        return

    if action == "approve":
        withdrawal.status = "approved"
    else:
        # Refund points to user on reject
        user = session.query(User).filter_by(id=withdrawal.user_id).first()
        points_to_refund = int(withdrawal.amount * 100)  # Assuming 100 points = ₹1
        user.points += points_to_refund
        withdrawal.status = "rejected"

    session.commit()
    session.close()
    await call.message.edit_text(f"💳 Withdrawal {withdrawal.status} ✅")
    await call.answer(f"Withdrawal {withdrawal.status}.")

# ===============================
# Other Admin Functions
# ===============================
# TODO: Implement Ban/Unban, Add/Remove Points/Wallet, Manage Tasks, Sponsor Channels, Broadcast
