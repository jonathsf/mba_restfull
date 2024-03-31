from flask import Flask, request, jsonify
from model.restaurant import db, Restaurant, Address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/mba_arq_serv_restfull_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
HOST = "0.0.0.0"
PORT = 4999

db.init_app(app)

@app.route('/restaurant', methods=['POST'])
def add_restaurant():

    data = request.json

    if not data or not "name" in data or not "address" in data:    
        return jsonify({'message': 'O nome e o endereço do restaurante são obrigatórios'}), 400
    
    new_address_data = data['address']
    new_address = Address(
                        streetAddress = new_address_data['streetAddress'], 
                        addressLocality = new_address_data['addressLocality'], 
                        addressRegion = new_address_data['addressRegion'],
                        addressCountry = new_address_data['addressCountry']
                        )

    new_restaurant = Restaurant(name=data['name'], 
                                address=new_address, 
                                url=data.get('url'), 
                                telephone=data.get('telephone'), 
                                menu=data.get('menu'), 
                                priceRange=data.get('priceRange')
                                )
    
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurante inserido com sucesso'}), 201

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurantes = Restaurant.query.all()
    return jsonify([restaurante.serialize() for restaurante in restaurantes])

@app.route('/restaurant/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    return jsonify(restaurant.serialize())

@app.route('/restaurant/address', methods=['GET'])
def get_restaurantx():
    
    data = request.args

    address_country_filter = Address.addressCountry == request.args.get('addressCountry') if request.args.get('addressCountry') else True
    address_locality_filter = Address.addressLocality == request.args.get('addressLocality') if request.args.get('addressLocality') else True
    address_region_filter = Address.addressRegion == request.args.get('addressRegion') if request.args.get('addressRegion') else True
    address_street_filter = Address.streetAddress == request.args.get('streetAddress') if request.args.get('streetAddress') else True

    # if data:
    restaurants = Restaurant.query.join(Address).filter(
        address_country_filter,
        address_locality_filter,
        address_region_filter,
        address_street_filter
        ).all()
    
    serialized_restaurants = [restaurant.serialize() for restaurant in restaurants]


    return jsonify({'restaurants': serialized_restaurants}), 200

@app.route('/restaurant/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    
    restaurant = Restaurant.query.get(restaurant_id)

    if not restaurant:
        return jsonify({'message': 'Restaurante não existe'}), 404

    data = request.json

    address_data = data.get('address')

    if restaurant.address:
        address = restaurant.address
    else:
        address = Address()

    address.streetAddress = address_data.get('streetAddress', address.streetAddress)
    address.addressLocality = address_data.get('addressLocality', address.addressLocality)
    address.addressRegion = address_data.get('addressRegion', address.addressRegion)
    address.addressCountry = address_data.get('addressCountry', address.addressCountry)

    restaurant.name = data.get('name', restaurant.name)
    restaurant.address = address
    restaurant.url = data.get('url', restaurant.url)
    restaurant.menu = data.get('menu', restaurant.menu)
    restaurant.telephone = data.get('telephone', restaurant.telephone)
    restaurant.price_range = data.get('priceRange', restaurant.priceRange)

    db.session.commit()

    return jsonify({'message': 'Restaurante atualizado com sucesso'}), 200


@app.route('/restaurant/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
   
    restaurant = Restaurant.query.get(id)
   
    if not restaurant:
        return jsonify({'message': 'Restaurante não existe'}), 404

    db.session.delete(restaurant)
    db.session.commit()
    
    return jsonify({'message': 'Restaurante deletado com sucesso'}), 200

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)