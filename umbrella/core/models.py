from model_utils.models import UUIDModel


class CustomModel(UUIDModel):
    class Meta:
        abstract = True

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)

        obj.full_clean()
        obj.save()
        return obj

    def update(self, **data):
        for name, value in data.items():
            setattr(self, name, value)

        self.full_clean()
        self.save()
        return self
