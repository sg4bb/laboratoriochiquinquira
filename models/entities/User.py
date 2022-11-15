from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import cv2

class User(UserMixin):

    def __init__(self, iduser, username, password, fullname="") -> None:
        self.id = iduser
        self.username = username
        self.password = password
        self.fullname = fullname

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password,password)

class NewUser():

    def __init__(self, iduser, username, password, fullname, email, address, genre, cellphone, profile_pic) -> None:
        self.id = iduser
        self.username = username
        self.password = generate_password_hash(password)
        self.fullname = fullname
        self.email = email
        self.address = address
        self.genre = genre
        self.cellphone = cellphone
        self.profile_pic = profile_pic

class ConsultUser():

    def __init__(self, username) -> None:
        self.username = username

class ConsultEmail():
    
    def __init__(self, email) -> None:
        self.email = email




        





