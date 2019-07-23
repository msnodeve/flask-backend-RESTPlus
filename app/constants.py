"""
    상수 클래스
"""

SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8")
SQLALCHEMY_DATABASE_URI_FORMAT = SQLALCHEMY_DATABASE_URI.format(
        USER="root",
        PASSWORD="1234",
        ADDR="127.0.0.1",
        PORT=3306,
        NAME="board"
    )