from typing import Union

from tortoise.exceptions import DoesNotExist

from app.db import models


class User(models.User):
    """
    User model, contains all methods for working with users.
    """

    @classmethod
    async def is_registered(cls, telegram_id: int) -> Union[models.User, bool]:
        try:
            return await cls.get(telegram_id=telegram_id)
        except DoesNotExist:
            return False

    @classmethod
    async def register(
            cls,
            telegram_id: int,
    ):
        await User(
            telegram_id=telegram_id,
        ).save()

    @classmethod
    async def get_count(cls) -> int:
        users_count = await cls.all()
        return len(users_count)

    @classmethod
    async def get_step(cls, telegram_id: int) -> int:
        user = await cls.get(telegram_id=telegram_id)
        return user.step_title

    @classmethod
    async def update(cls, user: models.User, **kwargs):
        await cls.filter(id=user.id).update(**kwargs)
