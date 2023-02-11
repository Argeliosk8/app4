from app import db
from models import *


# u1 = User(username = 'argeliosk8', email = 'argelio@gmail.com', password_hash = 'test')

# db.session.add(u1)
# db.session.commit()

all_users = User.query.all()

for user in all_users:
    print(user.id)
    print(user.username)

# v1 = Vehicle(brand = 'Toyota', model = 'Rav-4', user_id = 5)
# db.session.add(v1)
# db.session.commit()

# all_vehicles = Vehicle.query.all()

# for vehicle in all_vehicles:
#     print(vehicle.brand)
#     print(vehicle.user_id)