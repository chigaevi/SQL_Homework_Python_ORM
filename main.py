import os
import sqlalchemy
import psycopg2
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class publisher(Base):
    __tablename__ = 'publisher'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=60), unique=True)
    def __str__(self):
        return f'id: {self.id}, name: {self.name}'

class book(Base):
    __tablename__ = 'book'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=100), unique=True, nullable=False)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(publisher.id), nullable=False)
    publisher = relationship(publisher, backref='books')  # ХЗ почему stocks и зачем нужны именно тут

class shop(Base):
    __tablename__ = 'shop'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=40), unique=True)

class stock(Base):
    __tablename__ = 'stock'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(book.id), nullable=False)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(shop.id), nullable=False)
    book = relationship(book, backref='stocks')  # ХЗ почему stocks и зачем нужны именно тут
    shop = relationship(shop, backref='stocks')

class sale(Base):
    __tablename__ = 'sale'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.DECIMAL(5, 2), nullable=False)
    data_sale = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(stock.id), nullable=False)
    stock = relationship(stock, backref='sales')


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_publishers(names): #принимает на вход список
    for name in names:
        n = publisher(name=name)
        session.add(n)
    session.commit()
    print('Publisher(s) added')

def publisher_inf(id=None,name=None):
    if id is not None:
        pubs_inf = session.query(publisher).filter(publisher.id == id)
        for pub_inf in pubs_inf:
            print(pub_inf)
    elif name is not None:
        pubs_inf = session.query(publisher).filter(publisher.name == name)
        for pub_inf in pubs_inf:
            print(pub_inf)

def get_DB_data():
    global DB
    global DB_login
    global DB_name
    global DB_host
    with open('DB_data.txt','r') as file_DB_data:
        DB_data = file_DB_data.read().strip('\n')
        data_list = []
        for data in DB_data.split('\n'):
            data_list.append(data)
    DB = data_list[0]
    DB_login = data_list[1]
    DB_name = data_list[2]
    DB_host = data_list[3]

# создаем движок
get_DB_data()
DB_pas = os.getenv('PAS')
DSN = f"{DB}://{DB_login}:{DB_pas}@{DB_host}/{DB_name}"
engine = sqlalchemy.create_engine(DSN)
# создаем таблицы
create_tables(engine)
# создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

#добавляем publishers в БД
#для ввода - Elsevier,Bertelsmann,Pearson plc
# add_names_pub = input('Введите издателя или издателей через запятую: ').split(',')
# add_publishers(add_names_pub)

id_pub = input('Введите ID издателя: ')
publisher_inf(id=id_pub)
name_pub = input('Введите издателя: ')
publisher_inf(name=name_pub)


session.close()

