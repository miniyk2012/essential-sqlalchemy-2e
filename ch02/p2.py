from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine, insert)
from sqlalchemy.sql import select

metadata = MetaData()
cookies = Table('cookies', metadata,
                Column('cookie_id', Integer(), primary_key=True),
                Column('cookie_name', String(50), index=True),
                Column('cookie_recipe_url', String(255)),
                Column('cookie_sku', String(55)),
                Column('quantity', Integer()),
                Column('unit_cost', Numeric(12, 2))
                )

users = Table('users', metadata,
              Column('user_id', Integer(), primary_key=True),
              Column('username', String(15), nullable=False, unique=True),
              Column('email_address', String(255), nullable=False),
              Column('phone', String(20), nullable=False),
              Column('password', String(25), nullable=False),
              Column('created_on', DateTime(), default=datetime.now),
              Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
              )

orders = Table('orders', metadata,
               Column('order_id', Integer(), primary_key=True),
               Column('user_id', ForeignKey('users.user_id')),
               Column('shipped', Boolean(), default=False)
               )

line_items = Table('line_items', metadata,
                   Column('line_items_id', Integer(), primary_key=True),
                   Column('order_id', ForeignKey('orders.order_id')),
                   Column('cookie_id', ForeignKey('cookies.cookie_id')),
                   Column('quantity', Integer()),
                   Column('extended_cost', Numeric(12, 2))
                   )


def create_tables(uri='sqlite:///:memory:', create=True):
    engine = create_engine(uri)
    if create:
        metadata.drop_all(engine)
        metadata.create_all(engine)
    return engine


def insert_data(connection):
    ins1 = cookies.insert().values(
        cookie_name="chocolate chip",
        cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
        cookie_sku="CC01",
        quantity="12",
        unit_cost="0.50"
    )
    connection.execute(ins1)

    ins2 = insert(cookies).values(
        cookie_name="chocolate chip",
        cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
        cookie_sku="CC01",
        quantity="12",
        unit_cost="0.50"
    )
    connection.execute(ins2)

    ins3 = cookies.insert()
    connection.execute(ins3, cookie_name='dark chocolate chip',
                       cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
                       cookie_sku='CC02',
                       quantity='1',
                       unit_cost='0.75')
    inventory_list = [
        {
            'cookie_name': 'peanut butter',
            'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
            'cookie_sku': 'PB01',
            'quantity': '24',
            'unit_cost': '0.25'
        },
        {
            'cookie_name': 'oatmeal raisin',
            'cookie_recipe_url': 'http://some.okay.me/cookie/raisin.html',
            'cookie_sku': 'EWW01',
            'quantity': '100',
            'unit_cost': '1.00'
        }
    ]
    connection.execute(ins3, inventory_list)


engine = create_tables('sqlite:///cookies.db', create=False)
connection = engine.connect()
insert_data(connection)
s = select([cookies])
rp = connection.execute(s)
results = rp.fetchall()
print(results)

s = cookies.select()
rp2 = connection.execute(s)

for record in rp2:
    print(record)

print('first' + '*' * 10)
rp3 = connection.execute(s)
print(rp3.first())

rp4 = connection.execute(s)
print(rp4.first())

