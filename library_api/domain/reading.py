from library_api.domain.data_access_layer.db import db


class Reading(db.Model):
    __tablename__ = 'readings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer, nullable=True)
    impression = db.Column(db.String(2048), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)


    book_id = db.Column(db.BigInteger, db.ForeignKey('books.id'), nullable=False)

    books = db.relationship('Book', back_populates='readings')

    def __repr__(self):
        return f'<Reading {self.id!r}>'