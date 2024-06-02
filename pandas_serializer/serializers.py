import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db.sqlite3', echo=False)


class Serializer:
    model = None
    fields = []

    def __init__(self, instance=None, **kwargs):
        if self.model is None:
            raise Exception('model must be defined')
        self.request = kwargs.get('request')
        self.instance = instance
        self.table = self.model._meta.db_table
        self.pk_field = self.model._meta.pk.name

    @property
    def data(self):
        with engine.connect() as conn:
            df = pd.read_sql_query(self.query(), conn)
            return df.to_dict(orient='records')

    def query(self):
        fields = ', '.join(self.fields) or '*'
        return f"SELECT {fields} FROM {self.table} WHERE {self.pk_field} EQUALS {self.instance.pk}" if self.instance else f"SELECT {fields} FROM {self.table}"

    def save(self, **kwargs):
        df = pd.DataFrame(self.request.data)
        df.to_sql(self.table, con=engine, if_exists='replace')


