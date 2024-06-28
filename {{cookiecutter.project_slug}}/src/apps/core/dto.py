from __future__ import annotations

import abc
import dataclasses
from datetime import datetime
from itertools import chain


@dataclasses.dataclass
class BaseModelDto(abc.ABC):
    id: int

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @staticmethod
    def get_excluded_fields() -> list[str]:
        return None

    @classmethod
    def from_model(cls, obj, fields=None, exclude_fields: list[str] = None):
        opts = obj._meta
        data = {}
        excluded = cls.get_excluded_fields() or exclude_fields

        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if (fields is not None and f.name not in fields) or (
                excluded and f.name in excluded
            ):
                continue
            data[f.name] = f.value_from_object(obj)

        data.pop("pk", None)
        data.setdefault("id", obj.pk)
        return cls(**data)
