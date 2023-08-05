from typing import Optional
from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select
import sqlalchemy


class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str
    value: float
    category: str
    comment: str


sqlite_file_name = "networth.db"
sqlite_url = f"sqlite:///data/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    folder_path = Path.cwd() / 'data'
    folder_path.mkdir(exist_ok=True)
    SQLModel.metadata.create_all(engine)


def add_deal(date: str, value: float, category: str, comment: str):
    """Adds an entry to the table."""
    deal = Deal(
        date=date,
        value=value,
        category=category,
        comment=comment
    )

    with Session(engine) as session: 
        session.add(deal)
        session.commit()


def select_deals():
    """Gets all reacords from the table."""
    with Session(engine) as session:
        statement = select(Deal)
        results = session.exec(statement)
        return results.all()
    

def delete_deal(id_: int):
    """Deletes an entry from a given id."""
    with Session(engine) as session:
        statement = select(Deal).where(Deal.id == id_)
        results = session.exec(statement)

        try:
            deal = results.one()
        except sqlalchemy.exc.NoResultFound:
            pass
        except Exception as err:
            print(repr(err))
        else:
            session.delete(deal)
            session.commit()
