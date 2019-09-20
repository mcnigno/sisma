from app import db
from sqlalchemy import create_engine


def query(connection, sqlquery):
    engine = create_engine(connection)
    con = engine.connect()
    data = con.execute(sqlquery)

    return data


