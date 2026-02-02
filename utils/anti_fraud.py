from database import get_session, User, UserTask, Referral
from datetime import datetime, timedelta

# ===============================
# 1) Self Referral Protection
# ===============================
def is_self_referral(referrer_tg_id: int, referred_tg_id: int) -> bool:
    return referrer_tg_id == referred_tg_id


# ===============================
# 2) Multiple Accounts Detection (basic logic)
# Detect same username pattern / fast joins
# ===============================
def is_suspicious_user(username: str) -> bool:
    """
    Very basic heuristic:
    usernames like user12345, test123, etc
    """
    if not username:
        return True
    suspicious_keywords = ["test", "user", "abc", "temp"]
    username = username.lower()

    for word in suspicious_keywords:
        if word in username:
            return True
    return False


# ===============================
# 3) Task Farming Detection
# Too many tasks completed in very short time
# ===============================
def is_task_farming(user_id: int) -> bool:
    session = get_session()
    ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)

    recent_tasks = session.query(UserTask).filter(
        UserTask.user_id == user_id,
        UserTask.timestamp >= ten_minutes_ago
    ).count()

    session.close()

    # If more than 5 tasks in 10 minutes → suspicious
    return recent_tasks > 5


# ===============================
# 4) Referral Farming Detection
# Many referrals but none active
# ===============================
def is_referral_farming(user_id: int) -> bool:
    session = get_session()

    total_refs = session.query(Referral).filter_by(referrer_id=user_id).count()
    completed_refs = session.query(Referral).filter_by(
        referrer_id=user_id,
        task_completed=True
    ).count()

    session.close()

    # If user has 10+ referrals but 0 completed → suspicious
    return total_refs >= 10 and completed_refs == 0


# ===============================
# 5) Mark User as Suspicious
# ===============================
def flag_user(user_id: int):
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.is_banned = True
        session.commit()
    session.close()
