# standard lib
from typing import Annotated

# 3rd party
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# local
from app.database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]