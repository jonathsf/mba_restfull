from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.relationship('Address', backref='restaurant', uselist=False, cascade='all, delete')
    url = db.Column(db.String(254), nullable=True)
    menu = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(100), nullable=False)
    priceRange = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address.serialize() if self.address else None,
            'url': self.url,
            'menu': self.menu,
            'telephone': self.telephone,
            'priceRange': self.priceRange
        }

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    streetAddress = db.Column(db.String(100), nullable=False)
    addressLocality = db.Column(db.String(100), nullable=False)
    addressRegion = db.Column(db.String(100), nullable=False)
    addressCountry = db.Column(db.String(100), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def serialize(self):
        return {
            'streetAddress': self.streetAddress,
            'addressLocality': self.addressLocality,
            'addressRegion': self.addressRegion,
            'addressCountry': self.addressCountry,
            'restaurant_id': self.restaurant_id
        }