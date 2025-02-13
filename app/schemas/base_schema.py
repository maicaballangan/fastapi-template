from tortoise.contrib.pydantic import PydanticModel


class BaseInputSchema(PydanticModel):
    def create_update_dict(self):
        return self.model_dump(
            exclude_unset=True,
            exclude={'id'},
        )

    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={'id'})


class BaseOutputSchema(PydanticModel):
    id: int
