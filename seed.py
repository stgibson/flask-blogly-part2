from app import app
from models import db, User

db.drop_all()
db.create_all()

User.query.delete()

users = []
users.append(User(first_name="Alan", last_name="Alda", image_url=
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Alan_Alda_circa_1960s.JPG/800px-Alan_Alda_circa_1960s.JPG"
))
users.append(User(first_name="Joel", last_name="Burton"))
users.append(User(first_name="Jane", last_name="Smith"))

db.session.add_all(users)
db.session.commit()