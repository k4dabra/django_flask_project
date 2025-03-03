from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from flask import Flask, request, jsonify

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


db = create_engine("sqlite:///project_base.db")
Session = sessionmaker(bind=db)
s = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column("id",Integer,primary_key=True,autoincrement=True)
    name = Column("name",String)
    login = Column("login",String)
    password = Column("password",String)
    timestamp = Column("timestamp",DateTime)

    def __init__(self,name,login,password,timestamp):
        self.name = name
        self.login = login
        self.password = password
        self.timestamp = timestamp

Base.metadata.create_all(bind=db)


app = Flask(__name__)

@app.route("/add",methods=["POST"])
def add():
    req = request.get_json()
    timestamp_str = datetime.now().strftime(TIMESTAMP_FORMAT)
    timestamp_db = datetime.strptime(timestamp_str,TIMESTAMP_FORMAT)
    user = User(name=req["name"],login=req["login"],password=req["password"],timestamp=timestamp_db)
    s.add(user)
    s.commit()
    res = {"msg":"Save operation completed!!"}
    return jsonify(res)

@app.route("/read",methods=["get"]) # a validação de campos vazios deve ser feita no django
def read():
    search_result = []
    name = request.args.get("name")
    login = request.args.get("login")
    if name:
        users_found = s.query(User).filter(User.name.like(f'%{name}%')).all()
        for i in users_found:
            res_obj = {
                "id": i.id,
                "name": i.name,
                "login": i.login,
                "timestamp":i.timestamp
            }
            search_result.append(res_obj)
    elif login:
        users_found = s.query(User).filter(User.login.like(f'%{login}%')).all()
        for i in users_found:
            res_obj = {
                "id": i.id,
                "name": i.name,
                "login": i.login,
                "timestamp":i.timestamp
            }
            search_result.append(res_obj)
    return search_result

if __name__ == '__main__':
    app.run(debug=True)
