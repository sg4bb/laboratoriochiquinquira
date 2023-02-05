from models.ModelUser import ModelUser
from flask_mysqldb import MySQL

datacorreouser = ModelUser.consultenvio(db, '6', '3')
print(datacorreouser)