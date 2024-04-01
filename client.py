#importa de bibliotecas externas
from flask import Flask, request, render_template, redirect
#importa de classes e métodos do model
from model.restaurant import db
import requests

#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/mba_arq_serv_restfull_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
HOST = "0.0.0.0"
PORT = 5000

db.init_app(app)

#endpoint inicial
@app.route('/')
def index():
    return render_template('index.html')

#endpoint de cadastro
@app.route('/inserir' , methods=['GET', 'POST'])
def inserir():  
   msg = ""
   if request.method == 'POST':
        #pega os dados do corpo da requisição
        nome = request.form['name']
        endereco = {
            'streetAddress': request.form['streetAddress'],
            'addressLocality': request.form['addressLocality'],
            'addressRegion': request.form['addressRegion'],
            'addressCountry': request.form['addressCountry']
        }
        url = request.form.get('url', '') 
        menu = request.form.get('menu', '')
        telefone = request.form.get('telephone', '')
        faixa_preco = request.form.get('priceRange', '')
        #cria um novo restaurante
        novo_restaurante = {
            'name': nome,
            'address': endereco,
            'url': url,
            'menu': menu,
            'telephone': telefone,
            'priceRange': faixa_preco
        }

        #envia o novo restaurante para o endpoint do server
        response = requests.post("http://localhost:4999/restaurant", json=novo_restaurante)

        if response.status_code == 201:
            msg = "Restaurante inserido com sucesso"        
   
   return render_template('insert_restaurant.html', msg = msg)

#endpoint de edição
@app.route('/editar/', defaults={'restaurant_id': None}, methods=['GET','PUT','POST'])
@app.route('/editar/<restaurant_id>', methods=['GET','PUT', 'POST'])
def atualizar(restaurant_id):
   
    #acessa o endpoint do server passando o ID para localizar o restaurante
    response = requests.get("http://localhost:4999/restaurant/{}".format(restaurant_id))
    restaurant = response.json()   
    
    if request.method == 'POST':    
        
        #pega os dados do corpo da requisição
        nome = request.form['name']
        endereco = {
            'streetAddress': request.form['streetAddress'],
            'addressLocality': request.form['addressLocality'],
            'addressRegion': request.form['addressRegion'],
            'addressCountry': request.form['addressCountry']
        }
        url = request.form.get('url', '') 
        menu = request.form.get('menu', '')
        telefone = request.form.get('telephone', '')
        faixa_preco = request.form.get('priceRange', '')
        
        #atualiza os dados do restaurante
        atualizar_restaurante = {
            'name': nome,
            'address': endereco,
            'url': url,
            'menu': menu,
            'telephone': telefone,
            'priceRange': faixa_preco
        }

        response = requests.put("http://localhost:4999/restaurant/{}".format(restaurant_id), json=atualizar_restaurante)
        
        if response.status_code == 200:            
            return redirect('/listar')
    
    return render_template('update_restaurant.html', restaurant = restaurant)

#endpoint de listagem
@app.route('/listar')
def listar():   
    #acessa o endpoint do server para listar todos os restaurantes
    response = requests.get("http://localhost:4999/restaurants")    
    restaurants = response.json()
    return render_template('list_restaurants.html', restaurants=restaurants)

#endpoint de busca
@app.route('/buscar/', methods=['GET'])
def buscar_restaurante():
    #pega os dados do corpo da requisição
    addressLocality = request.args.get('addressLocality')
    addressRegion = request.args.get('addressRegion')
    addressCountry = request.args.get('addressCountry')
    streetAddress = request.args.get('streetAddress')
    
    #filtros
    parametros = {
            'addressLocality': addressLocality,
            'addressRegion': addressRegion,
            'addressCountry': addressCountry,
            'streetAddress': streetAddress
        }    
    
    #acessa o endpoint do server para buscar os restaurantes
    response = requests.get('http://localhost:4999/restaurants/address', params=parametros)    

    return render_template('find_restaurants_by_fields.html',data = response.json())


#endpoint de exclusão
@app.route('/excluir/', defaults={'restaurant_id': None})
@app.route('/excluir/<restaurant_id>')
def excluir(restaurant_id):
    #acessa o endpoint do server passando o ID para excluir o restaurante
    response = requests.delete("http://localhost:4999/restaurant/{}".format(restaurant_id))

    if response == 200:
        status = "Excluido com sucesso"
    else:
        status = "Erro ao excluir"

    return redirect('/listar')

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)