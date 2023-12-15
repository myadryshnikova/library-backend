from library_api.domain.data_access_layer.db import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=False)
    author = db.Column(db.String(2048), nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    bookshelf_id = db.Column(db.BigInteger, db.ForeignKey('bookshelfs.id'), nullable=True)

    user_relationship = db.relationship('User', back_populates='books')
    bookshelf_relationship = db.relationship('Bookshelf', back_populates='books')

    def __repr__(self):
        return f'<Bookshelf {self.name!r}>'