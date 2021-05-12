from sqlalchemy import Column, Integer, String, DateTime
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import Base


class Members(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    name = Column(String(20, 'utf8mb4_unicode_ci'))
    # email = Column(String(50, 'utf8mb4_unicode_ci'))
    # phone = Column(String(20, 'utf8mb4_unicode_ci'))
    age = Column(String(20, 'utf8mb4_unicode_ci'))
    create_datetime = Column(DateTime, default=datetime.utcnow())
    delete_datetime = Column(DateTime)
    image_file = Column(String(255, 'utf8mb4_unicode_ci'))

    def __init__(self, name, age, create_datetime, delete_datetime, image_file):
        self.name = name
        self.age = age
        self.create_datetime = create_datetime
        self.delete_datetime = delete_datetime
        self.image_file = image_file

    def __repr__(self):
        return "<Member('%s','%s''%s')>" % (self.name, self.email, self.phone)


# db = SQLAlchemy()


# class Members(db.Model):
#     """ table name : members
#         table info
#     - id : index id
#     - name
#     - start: start datetime
#     - end: end datetime """

#     __tablename__ = 'members'

#     id = db.Column(db.Integer, primary_key=True,
#                    nullable=False, autoincrement=True)
#     name = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
#     email = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
#     phone = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
#     create_datetime = db.Column(db.DateTime, default=datetime.utcnow())
#     delete_datetime = db.Column(db.DateTime, default=datetime.utcnow())
#     image_file = db.Column(db.String(255, 'utf8mb4_unicode_ci'))

#     def __init__(self, name, email, phone, create_datetime, delete_datetime, image_file):
#         self.name = name
#         self.email = email
#         self.phone = phone
#         self.create_datetime = create_datetime
#         self.delete_datetime = delete_datetime
#         self.image_file = image_file

#     def __repr__(self):
#         return "<Member('%s','%s''%s')>" % (self.name, self.email, self.phone)
