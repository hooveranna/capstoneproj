# import os
# import tempfile
#
# import pytest
#
# from flask_testing import TestCase
# from flask_app import app, db
# from flask_app import User
#
# #from flask.ext.testing import current_user
# from flask import request
#
# # class MyTest(TestCase):
# #
# #     def create_app(self):
# #         app = flask_app(__name__)
# #         app.config['TESTING'] = True
# #         return app
#
# from flask import url_for, request
# import flask_app
#
# class BaseTestCase(TestCase):
#     """A base test case."""
#
#     def create_app(self):
#         #app.config.from_object('config.TestConfig')
#         return app
#
#     def setUp(self):
#         db.create_all()
#         db.session.add(User(username = "admin", email = "ad@min.com", password ="admin"))
#         # db.session.add(
#         #     BlogPost("Test post", "This is a test. Only a test.", "admin"))
#         db.session.commit()
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#
#
# class TestUser(BaseTestCase):
#
#     # Ensure user can register
#     def test_user_registeration(self):
#         with self.client:
#             response = self.client.post('register/', data=dict(
#                 username='Michael', email='michael@realpython.com',
#                 password='python', confirm='python'
#             ), follow_redirects=True)
#             # self.assertTrue(current_user.username == "Michael")
#             # self.assertTrue(current_user.is_active())
#             # user = User.query.filter_by(email='michael@realpython.com').first()
#
#     # # Ensure errors are thrown during an incorrect user registration
#     # def test_incorrect_user_registeration(self):
#     #    # with self.client:
#     #     response = self.client.post('register/', data=dict(
#     #             username='Michael', email='michael',
#     #             password='python', confirm='python'
#     #         ), follow_redirects=True)
#     #     self.assertIn(b'Invalid email address.', response.data)
#     #     self.assertIn(b'/register/', request.url)
#
#     # def test_home(self):
#     #     r = self.client.get('/')
#     #     r = self.client.post('/',
#     #                         {'kk', 'Those summer nights seem long ago, And so is the girl you used to call. '},
#     #                         follow_redirects=True)
#     #     self.assertEqual(r.status_code, 200)