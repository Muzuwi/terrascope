import datetime
from sqlalchemy import Column
from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column


class WorldSnapshot(Base):
    __tablename__ = "world_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    world_name: Mapped[str]
    timestamp: Mapped[datetime.datetime]
    cause: Mapped[str]
    snapshot_filename: Mapped[str]
