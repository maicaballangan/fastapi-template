from tortoise import fields
from tortoise import models


class BaseDBModel(models.Model):
    id = fields.BigIntField(primary_key=True, db_index=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
