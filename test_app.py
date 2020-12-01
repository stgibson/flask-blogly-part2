from unittest import TestCase
from app import app
from models import db, User, Post

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()

base_url = "http://localhost"

class UserViewsTestCase(TestCase):
    """
        Tests for views for Users.
    """
    def setUp(self):
        """
            Adds test users to test db
        """
        num_of_users = 3
        first_names = ["Alan", "Joel", "Jane"]
        last_names = ["Alda", "Burton", "Smith"]
        image_urls = [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Alan_Alda_circa_1960s.JPG/800px-Alan_Alda_circa_1960s.JPG",
            "",
            ""
        ]
        users = []
        for i in range(num_of_users):
            user = User(
                first_name=first_names[i],
                last_name=last_names[i],
                image_url=image_urls[i]
            )
            users.append(user)

        User.query.delete()
        db.session.add_all(users)
        db.session.commit()

        self.users = users
        self.num_of_users = num_of_users
        self.first_names = first_names
        self.last_names = last_names
        self.image_urls = image_urls

    def tearDown(self):
        """
            Undoes any failed transactions
        """
        db.session.rollback()
    
    def test_go_to_users_page(self):
        """
            Tests go_to_users_page() redirects correctly
        """
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"{base_url}/users")

    def test_show_user_list(self):
        """
            Tests show_user_list() renders users.html correctly with the users'
            names and correct links
        """
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            for user in self.users:
                self.assertIn(f"/users/{user.id}", html)
                self.assertIn(f"{user.first_name} {user.last_name}", html)
        
    def test_add_new_user(self):
        """
            Tests add_new_user() correctly adds user to db and redirects
        """
        with app.test_client() as client:
            first_name = "Sean"
            last_name = "Gibson"
            data = {
                "first-name": first_name,
                "last-name": last_name,
                "image-url": ""
            }
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{first_name} {last_name}", html)

    def test_show_user_details(self):
        """
            Tests show_user_details(user_id) renders user info correctly
        """
        with app.test_client() as client:
            for i in range(self.num_of_users):
                test_user = User.query.filter_by(
                    first_name=self.first_names[i]
                ).one()
                user_id = test_user.id
                resp = client.get(f"/users/{user_id}")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn( \
                    f"{self.first_names[i]} {self.last_names[i]}", \
                    html)
                if self.image_urls[i]:
                    self.assertIn(self.image_urls[i], html)
                else:
                    self.assertIn("/static/placeholder.jpg", html)

    def test_edit_user(self):
        """
            Tests edit_user(user_id) updates user info and redirects to user
            details page correctly
        """
        with app.test_client() as client:
            new_first_name = "Sean"
            new_last_name = "Gibson"
            new_image_url = ""
            data = {
                "first-name": new_first_name,
                "last-name": new_last_name,
                "image-url": new_image_url
            }
            test_user = User.query.filter_by(
                first_name=self.first_names[0]
            ).one()
            user_id = test_user.id
            resp = client.post(f"/users/{user_id}/edit", data=data, \
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{new_first_name} {new_last_name}", html)