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

i1 = Item(name='Chair', cost_price=9.21, selling_price=10.81, quantity=5)
i2 = Item(name='Pen', cost_price=3.45, selling_price=4.51, quantity=3)
i3 = Item(name='Headphone', cost_price=15.52, selling_price=16.81, quantity=50)
i4 = Item(name='Travel Bag', cost_price=20.1, selling_price=24.21, quantity=50)
i5 = Item(name='Keyboard', cost_price=20.1, selling_price=22.11, quantity=50)
i6 = Item(name='Monitor', cost_price=200.14, selling_price=212.89, quantity=50)
i7 = Item(name='Watch', cost_price=100.58, selling_price=104.41, quantity=50)
i8 = Item(name='Water Bottle', cost_price=20.89, selling_price=25, quantity=50)

session.add_all([i1, i2, i3, i4, i5, i6, i7, i8])
session.commit()

o1 = Order(customer=c1)
o2 = Order(customer=c1)

line_item1 = OrderLine(order=o1, item=i1, quantity=3)
line_item2 = OrderLine(order=o1, item=i2, quantity=2)
line_item3 = OrderLine(order=o2, item=i1, quantity=1)
line_item3 = OrderLine(order=o2, item=i2, quantity=4)

session.add_all([o1, o2])

session.new
session.commit()


o3 = Order(customer=c1)
orderline1 = OrderLine(item=i1, quantity=5)
orderline2 = OrderLine(item=i2, quantity=10)

o3.order_lines.append(orderline1)
o3.order_lines.append(orderline2)

session.add_all([o3])

session.commit()

for ol in c1.orders[0].order_lines:
    ol.id, ol.item, ol.quantity

print('-------')

for ol in c1.orders[1].order_lines:
    ol.id, ol.item, ol.quantity

session.query(Item).filter(Item.name.ilike("wa%")).all()
session.query(Item).filter(Item.name.ilike("wa%")).order_by(Item.cost_price).all()

# descending order
session.query(Item).filter(Item.name.ilike("wa%")).order_by(desc(Item.cost_price)).all()

session.query(Customer).join(Order).all()

# print(session.query(Customer).join(Order))

session.query(Customer.id, Customer.username, Order.id).join(Order).all()


# find all customers who either live in Peterbrugh or Norfolk

session.query(Customer).filter(or_(
    Customer.town == 'Peterbrugh',
    Customer.town == 'Norfolk'
)).all()


# find all customers whose first name is John and live in Norfolk

session.query(Customer).filter(and_(
    Customer.first_name == 'John',
    Customer.town == 'Norfolk'
)).all()