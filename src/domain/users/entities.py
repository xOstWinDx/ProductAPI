import bcrypt
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, str32, str16, id_


class User(Base):
    __tablename__ = "users"
    id: Mapped[id_]
    hashed_password: Mapped[bytes | None]
    email: Mapped[str32 | None] = mapped_column(index=True, unique=True)
    name: Mapped[str16] = mapped_column(index=True)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="false")

    def check_password(self, plain_password: str) -> bool:
        if self.hashed_password is None:
            return False
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password)  # noqa
