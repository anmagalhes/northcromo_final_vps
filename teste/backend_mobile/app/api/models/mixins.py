from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.utils.datetime import get_current_time_in_sp
from sqlalchemy import DateTime
from typing import Optional


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_time_in_sp
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time_in_sp,
        onupdate=get_current_time_in_sp,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
