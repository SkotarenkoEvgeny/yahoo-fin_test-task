from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(
        BASE_DIR / 'data' / 'db.sqlite3'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
