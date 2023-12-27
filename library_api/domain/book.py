from library_api.domain.data_access_layer.db import db
from sqlalchemy.dialects.postgresql import JSON


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=False)
    author = db.Column(db.String(2048), nullable=False)
    description = db.Column(db.String(2048), nullable=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    bookshelf_id = db.Column(db.BigInteger, db.ForeignKey('bookshelfs.id'), nullable=True)

    deleted_at = db.Column(db.DateTime, nullable=True)
    additional_fields = db.Column(JSON, nullable=True)

    users = db.relationship('User', back_populates='books')
    bookshelfs = db.relationship('Bookshelf', back_populates='books')
    citations = db.relationship('Citation', back_populates='books')
    readings = db.relationship('Reading', back_populates='books')


    def __repr__(self):
        return f'<Book {self.id!r} {self.name!r} {self.description!r}>'

    def __getitem__(self, key):
        return getattr(self, key)
        