from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import DATABASE_URL

def create_database_engine(url):
    from sqlalchemy.engine import make_url
    sqlite = make_url(url).get_backend_name() == "sqlite"
    result = create_engine(url, connect_args={"check_same_thread": False} if sqlite else {}, pool_pre_ping=True)
    if sqlite:
        @event.listens_for(result, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    elif result.dialect.name == "mssql":
        from backend.sqlserver import configure_sqlserver
        configure_sqlserver(result)
    else:
        raise ValueError("Only SQLite and SQL Server are supported")
    return result


engine = create_database_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def initialize_database(target=engine):
    with target.begin() as connection:
        Base.metadata.create_all(connection)
        if target.dialect.name == "mssql":
            from backend.sqlserver import install_delete_triggers
            install_delete_triggers(connection, Base.metadata)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
