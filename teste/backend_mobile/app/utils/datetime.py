from datetime import datetime, timezone
import pytz

SP_TZ = pytz.timezone("America/Sao_Paulo")

def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(SP_TZ)

def utcnow() -> datetime:
    return datetime.now(timezone.utc)
