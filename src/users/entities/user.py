from src.utils.utils import format_date


class User:

    validatable_fields = {
        "nameComplete": {'required': True, 'type': 'string', 'maxlength': 255},
        "age": {'required':True,'type': 'integer'}
    
    }

    UNIQUE_FIELDS = {
        "nameComplete"
    }

    def __init__(
        self,
        id,
        nameComplete,
        age,
        created_at=None,
        updated_at=None,
        deleted_at=None,
    ):
        self.id = id
        self.nameComplete = nameComplete
        self.age = age
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "nameComplete": self.nameComplete,
            "age": self.age,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self, include_deleted_at = False):
        data = self.to_dict()
        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])
        if include_deleted_at:
            data["deleted_at"] = format_date(data["deleted_at"])
        else:
            data.pop("deleted_at")
        return data

    @classmethod
    def from_dict(cls, dict):
        id = dict.get("id")
        nameComplete = dict.get("nameComplete")
        age = dict.get("age")
        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return User(
            id,
            nameComplete,
            age,
            created_at,
            updated_at,
            deleted_at,
        )
