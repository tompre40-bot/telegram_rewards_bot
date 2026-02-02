from database import get_session, Setting, UserTask, Referral, Checkin
from datetime import datetime

# ===============================
# 1) Get Setting Value
# ===============================
def get_setting(key: str, default=None):
    session = get_session()
    setting = session.query(Setting).filter_by(key=key).first()
    session.close()
    if setting:
        return setting.value
    return default


# ===============================
# 2) Points → Wallet Conversion
# ===============================
def points_to_wallet(points: int) -> float:
    rate = get_setting("points_to_wallet", 100)  # Default 100 points = ₹1
    try:
        rate = float(rate)
    except:
        rate = 100
    return round(points / rate, 2)


# ===============================
# 3) Daily Streak Bonus Logic
# ===============================
def calculate_streak_bonus(streak: int) -> int:
    """
    Day 1: 10 points
    Day 5: +20 bonus
    Day 10: +50 bonus
    """
    base_points = 10
    bonus = 0

    if streak == 5:
        bonus = 20
    elif streak == 10:
        bonus = 50

    return base_points + bonus


# ===============================
# 4) Level / Milestone Rewards (Referrals)
# ===============================
def referral_milestone_bonus(total_referrals: int) -> int:
    """
    10 referrals → 100 points
    50 referrals → 700 points
    100 referrals → 2000 points
    """
    if total_referrals == 10:
        return 100
    elif total_referrals == 50:
        return 700
    elif total_referrals == 100:
        return 2000
    return 0


# ===============================
# 5) Check Withdraw Activity Requirements
# ===============================
def check_withdraw_requirements(user_id: int) -> bool:
    session = get_session()

    tasks_done = session.query(UserTask).filter_by(user_id=user_id, completed=True).count()
    referrals_done = session.query(Referral).filter_by(
        referrer_id=user_id,
        task_completed=True
    ).count()
    checkins_done = session.query(Checkin).filter_by(user_id=user_id).count()

    session.close()

    return tasks_done >= 5 and referrals_done >= 3 and checkins_done >= 3


# ===============================
# 6) Format Username Safe
# ===============================
def safe_username(username: str, telegram_id: int) -> str:
    if username:
        return username
    return f"User{telegram_id}"
