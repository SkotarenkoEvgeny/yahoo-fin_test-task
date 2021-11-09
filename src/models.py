from datetime import datetime

from src import db


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(5), nullable=False)

    fin_data = db.relationship(
        'FinanceData', back_populates='company',
        lazy=True
        )

    def __repr__(self):
        return f'{self.id} - {self.name}'


class FinanceData(db.Model):
    __tablename__ = 'fin_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Integer)
    open_data = db.Column(db.Float)
    high_data = db.Column(db.Float)
    low_data = db.Column(db.Float)
    close_data = db.Column(db.Float)
    adj_close_data = db.Column(db.Float)
    volume_data = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    company = db.relationship('Company', back_populates='fin_data')

    def __repr__(self):
        return f'{self.id} - ' \
               f'{datetime.utcfromtimestamp(self.date).date().isoformat()} -' \
               f' {self.volume_data}'
