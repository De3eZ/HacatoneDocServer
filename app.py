import random
from flask import *
from flask_sqlalchemy import *
from sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hacatone.db'
db = SQLAlchemy(app)


class Category(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    category_name = Column(String(50), nullable=False)

    def __repr__(self):
        return '<Category %r' % self.id


class Document(db.Model):
    id = Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    data = Column(db.String(500), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return '<Document %r' % self.id


class Employee(db.Model):
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'), nullable=False)
    date = Column(String(20))

    def __repr__(self):
        return '<Employee %r' % self.id


class Login(db.Model):
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)
    login = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return '<Login %r' % self.id


class Role(db.Model):
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    role = Column(String(50), nullable=False)

    def __repr__(self):
        return '<Role %r' % self.id


class Token(db.Model):
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    token = Column(String(300), nullable=False)
    refreshtoken = Column(String(300), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return '<Token %r' % self.id


@app.route('/api/mobile/registration', methods=['POST'])
def registration():
    data = request.get_json()

    nm = data['name']
    srnm = data['surname']
    ptrnymc = data['patronymic']
    login = data['login']
    password = data['password']

    try:

        employee = Employee.query.filter_by(name = nm, surname = srnm, patronymic=ptrnymc).first()

        if Login.query.filter_by(employee_id = employee.id).first().login == login and Login.query.filter_by(employee_id=employee.id).first().password == password:
            token = Token.query.filter_by(employee_id=employee.id).first()

        return jsonify({'token': token.token, 'refreshToken': token.refreshtoken})
    except:
        return "Error"

@app.route('/api/mobile/auth/', methods=['POST'])
def auth():
    data = request.get_json()

    lgn = data['login']
    pas = data['password']

    try:
        employeeLogin = Login.query.filter_by(login=lgn, password=pas).first()
        token = Token.query.filter_by(employee_id=employeeLogin.employee_id).first()

        return jsonify({'token': token.token, 'refreshToken': token.refreshtoken})
    except:
        return "Error, invalid login or password"


@app.route('/api/mobile/refresh', methods=['POST'])
def refresh():
    data = request.get_json()

    refreshToken = data['refreshtoken']

    try:
        token = Token.query.filter_by(refreshtoken=refreshToken).first()

        token.refreshtoken=random.randint(20, 35) * 100

        db.session.commit()

        return jsonify({'refreshToken': token.refreshtoken})
    except:
        return "Error, invalid refreshtoken"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
