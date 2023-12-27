from library_api.domain.data_access_layer.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
    password_salt = db.Column(db.String(64), unique=True,  nullable=False)

    bookshelfs = db.relationship('Bookshelf', back_populates='users')
    books = db.relationship('Book', back_populates='users')

    def __repr__(self):
        return f'<User {self.login!r}>'

