import sqlalchemy
import psycopg2
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class publisher(Base):
    __tablename__ = 'publisher'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=60), unique=True)

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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_publishers(names): #принимает на вход список
    for name in names:
        n = publisher(name=name)
        session.add(n)
    session.commit()
    print('Publisher(s) added')

def publisher_inf(id=None,name=None):


# создаем движок
DSN = "postgresql://postgres:treeWQ1846VjJ@localhost:5432/book_shop_db"
engine = sqlalchemy.create_engine(DSN)
# создаем таблицы
create_tables(engine)
# создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

#добавляем publishers в БД
names_pub = input('Введите издателя или издателей через запятую: ').split(',')  #для ввода - Elsevier,Bertelsmann,Pearson plc
add_publishers(names_pub)



session.close()
