from library_api.domain.data_access_layer.db import db


class Bookshelf(db.Model):
    __tablename__ = 'bookshelfs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)

    user_relationship = db.relationship('User', back_populates='bookshelfs')
    book_relationship = db.relationship('Book', back_populates='bookshelfs')

    def __repr__(self):
        return f'<Bookshelf {self.name!r}>'

