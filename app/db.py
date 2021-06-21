import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Number(ormar.Model):
    class Meta(BaseMeta):
        tablename = "numbers"

    id: int = ormar.Integer(primary_key=True)
    number1: int = ormar.Integer()
    number2: int = ormar.Integer()
    answer: int = ormar.Integer()


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
