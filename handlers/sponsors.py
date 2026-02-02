from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_session, Sponsor
from datetime import datetime, timedelta

router = Router()

# ===============================
# Helper: Get active sponsors
# ===============================
def get_active_sponsors():
    session = get_session()
    now = datetime.utcnow()
    sponsors = session.query(Sponsor).filter_by(active=True).all()
    # Optional: rotate sponsors every 24h
    for sponsor in sponsors:
        if not sponsor.rotation_date or (now - sponsor.rotation_date) > timedelta(hours=24):
            sponsor.rotation_date = now
    session.commit()
    session.close()
    return sponsors

# ===============================
# Menu Sponsors Callback
# ===============================
@router.callback_query(F.data == "menu_sponsors")
async def show_sponsors(call: CallbackQuery):
    sponsors = get_active_sponsors()
    if not sponsors:
        await call.message.answer("ℹ️ No sponsor channels are active at the moment.")
        await call.answer()
        return

    # Build sponsor list
    sponsor_text = "\n".join([f"🔹 {s.channel}" for s in sponsors])

    # Button to go back to main menu
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu_back"))

    await call.message.answer(
        f"📢 Please join these sponsor channels before accessing the bot:\n\n{sponsor_text}",
        reply_markup=keyboard
    )
    await call.answer()
