from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    DB model for users.

    Fields:
        id: int
        telegram_id: int
        step_title: str
    """
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField()

    step_title = fields.CharField(max_length=255, default="start")
