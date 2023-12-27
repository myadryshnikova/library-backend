from library_api.domain.data_access_layer.db import db


class Citation(db.Model):
    __tablename__ = 'citations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    citation_description = db.Column(db.String(2048), nullable=False)
    author = db.Column(db.String(2048), nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    book_id = db.Column(db.BigInteger, db.ForeignKey('books.id'), nullable=False)

    books = db.relationship('Book', back_populates='citations')

    def __repr__(self):
        return f'<Book {self.name!r}>'