from tortoise import fields
from tortoise import models


class BaseDBModel(models.Model):
    id = fields.BigIntField(primary_key=True, db_index=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created', 'id']

    class PydanticMeta:
        exclude = ['created', 'modified']


class BaseAuditedDBModel(BaseDBModel):
    created_by = fields.BigIntField()

    class Meta:
        abstract = True
        ordering = ['-created']

    class PydanticMeta:
        exclude = ['created', 'modified', 'created_by']
