# standard lib

# 3rd party
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

# local
from app.database import Base
from app.enums import Priority

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    todos: Mapped[list["Todo"]] = relationship(back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    priority: Mapped[Priority] = mapped_column(Enum(Priority, name="priority_enum"))
    completed: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="todos")