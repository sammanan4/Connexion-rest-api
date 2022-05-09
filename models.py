import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

engine = sa.create_engine("sqlite:///db.sqlite")
Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    id = sa.Column(sa.Integer, primary_key=True)
    checked = sa.Column(sa.Boolean)
    name = sa.Column(sa.String, nullable=False)
    person_type = sa.Column(sa.String)
    age = sa.Column(sa.Float)
    description = sa.Column(sa.Text)
    date = sa.Column(sa.DateTime)

    def __repr__(self):
        return "<Person(name={self.name!r})>".format(self=self)



Base.metadata.create_all(engine)
