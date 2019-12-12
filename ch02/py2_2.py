from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine, select, desc)
metadata = MetaData()
cookies = Table('cookies', metadata,
                Column('cookie_id', Integer(), primary_key=True),
                Column('cookie_name', String(50), index=True),
                Column('cookie_recipe_url', String(255)),
                Column('cookie_sku', String(55)),
                Column('quantity', Integer()),
                Column('unit_cost', Numeric(12, 2))
                )

engine = create_engine('sqlite:///cookies.db')
s1 = select([cookies.c.cookie_name, cookies.c.quantity])
s2 = s1.order_by(cookies.c.quantity, cookies.c.cookie_name)
print(s2)
connection = engine.connect()
rp1 = connection.execute(s2)
for cookie in rp1:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))

print()
s3 = s1.order_by(desc(cookies.c.quantity), desc(cookies.c.cookie_name))
print(s3)
rp2 = connection.execute(s2)
for cookie in rp2:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))

print()
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity)
s = s.limit(2)
print(s)
rp = connection.execute(s)
print([result.cookie_name for result in rp])
