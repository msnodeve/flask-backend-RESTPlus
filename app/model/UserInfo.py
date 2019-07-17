from sqlalchemy.sql import text

class UserInfo(DB.Model):
    """ UserInfo model """
    __tablename__ = "userinfo"
    __table_args__ = {'mysql_collate' : 'utf8_general_ci'}
    id = DB.Column("id", DB.Integer, primary_key=True)
    name = DB.Column("name", DB.String(250), nullable=False)
    age = DB.Column("age", DB.Integer, nullable=False)
    tel = DB.Column("tel", DB.String(20), nullable=False)
    email = DB.Column("email", DB.String(50), nullable=False)
    created = DB.Column(DB.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    def __init__(self, name, age, tel, email):
        self.name = name
        self.age = age
        self.tel = tel
        self.email = email