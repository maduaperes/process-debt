from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Classe base para todos os modelos do SQLAlchemy."""

    pass


# Configuração específica para SQLite
connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    """
    Cria uma sessão com o banco para cada requisição
    e garante seu fechamento ao final.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


from sqlalchemy import text


def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Banco conectado com sucesso!")
    except Exception as error:
        print(f"❌ Erro ao conectar: {error}")
        raise
