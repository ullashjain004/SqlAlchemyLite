from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


# create a Session object to use Session class from sqlalchemy.orm
# Creating connection between alchemy and sql lite
engine = create_engine('sqlite:////web/Sqlite-Data/example5.db')

Base = declarative_base()

# A Session() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit().


class Customer(Base):
    __tablename__ = 'Customer'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String)
    address = Column(String)
    town = Column(String)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer(), nullable=False)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    date_placed = Column(DateTime(), default=datetime.now, nullable=False)
    date_shipped = Column(DateTime())

class OrderLine(Base):
    __tablename__ = 'order_lines'
    id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.id'))
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(Integer())
    order = relationship("Order", backref='order_lines')
    item = relationship("Item")


def dispatch_order(order_id):
    # check whether order_id is valid or not
    order = session.query(Order).get(order_id)

    if not order:
        raise ValueError("Invalid order id: {}.".format(order_id))

    if order.date_shipped:
        print("Order already shipped.")
        return

    try:
        for i in order.order_lines:
            i.item.quantity = i.item.quantity - i.quantity

        order.date_shipped = datetime.now()
        session.commit()
        print("Transaction completed.")

    except IntegrityError as e:
        print(e)
        print("Rolling back ...")
        session.rollback()
        print("Transaction failed.")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

c1 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )

c2 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )

session.add(c1)
session.add(c2)

session.commit()

c3 = Customer(
    first_name="John",
    last_name="Lara",
    username="johnlara",
    email="johnlara@mail.com",
    address="3073 Derek Drive",
    town="Norfolk"
)

c4 = Customer(
    first_name="Sarah",
    last_name="Tomlin",
    username="sarahtomlin",
    email="sarahtomlin@mail.com",
    address="3572 Poplar Avenue",
    town="Norfolk"
)

c5 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )

c6 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )

session.add_all([c3, c4, c5, c6])
session.commit()