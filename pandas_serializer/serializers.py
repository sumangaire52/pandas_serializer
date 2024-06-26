from abc import ABC, abstractmethod

import pandas as pd
from sqlalchemy import create_engine
from .utils.db import get_connection_string

engine = create_engine(get_connection_string(), echo=False)


class Serializer(ABC):
    model = None
    fields = []

    def __init__(self, instance=None, data=None, **kwargs):
        if self.model is None:
            raise Exception("model must be defined")
        self.request_data = data or kwargs.get("request", {}).get("data")
        self.instance = instance
        self.table = self.model._meta.db_table
        self.pk_field = self.model._meta.pk.name

    @property
    def data(self) -> dict:
        with engine.connect() as conn:
            df = pd.read_sql_query(self.query(), conn)
            return df.to_dict(orient="records")

    def query(self) -> str:
        fields = ", ".join(self.fields) or "*"
        return (
            f"SELECT {fields} FROM {self.table} WHERE {self.pk_field} EQUALS {self.instance.pk}"
            if self.instance
            else f"SELECT {fields} FROM {self.table}"
        )

    def save(self, **kwargs):
        instance = (
            self.model.objects.filter(pk=self.instance.pk).update(**self.request_data)
            if self.instance
            else self.model.objects.create(**self.request_data)
        )
        return instance

    @abstractmethod
    def is_valid(self):
        """Developer needs to implement validations themselves for now"""
        pass
