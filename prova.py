from flask import Flask, render_template, request, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/func_api'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Clientes(db.Model):
    __tablename__ = "cliente"

    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    razao_social = db.Column(db.String)
    cnpj = db.Column(db.Integer)
    data_inclusao = db.Column(db.Integer)

    def __init__(self, codigo, nome, razao_social, cnpj, data_inclusao):
        self.codigo = codigo
        self.nome = nome
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.data_inclusao = data_inclusao

    def __repr__(self):
        return ('Cliente{}'.format(self.nome))


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

@app.route('/add_cliente', methods=['GET', 'POST',])
def add_cliente():
    
    if request.method == 'POST':
        formulario = request.form
        cliente = Clientes(codigo=formulario['codigo'], nome=formulario['nome'], razao_social=formulario['razao_social'], cnpj=formulario['cnpj'], data_inclusao=formulario['data_inclusao'])

        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('get_cliente'))
         
    return render_template('add.html')


@app.route('/get_cliente', methods=["GET",])
def get_cliente():
    lista_clientes = Clientes.query.all()
    return render_template('get.html', lista_clientes=lista_clientes)

@app.route('/update_cliente', methods=['GET', 'POST'])
def update_cliente():
    if request.method == 'POST':
        nome_form = request.form['nome']
        cliente = Clientes.query.filter_by(nome=nome_form).first()
        return redirect(url_for('alterar_dados', cliente_nome=cliente.nome))   
    return render_template('update.html')

@app.route('/alterar_dados/<cliente_nome>', methods=['GET','PUT', 'POST'])
def alterar_dados(cliente_nome):
    cliente = Clientes.query.filter_by(nome=cliente_nome).first()
    if request.method =='POST':
        formulario = request.form
        cliente = Clientes(codigo=formulario['codigo'], nome=formulario['nome'], razao_social=formulario['razao_social'], cnpj=formulario['cnpj'], data_inclusao=formulario['data_inclusao'])
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('get_cliente'))
        
    return render_template('alterar.html', cliente=cliente)

@app.route('/delete_cliente', methods=['GET', 'DELETE', 'POST'])
def delete_cliente():
    
    if request.method == 'POST':
        nome_form = request.form['nome']
        cliente = Clientes.query.filter_by(nome=nome_form).first()
        db.session.delete(cliente)
        db.session.commit()
        return redirect(url_for('get_cliente'))
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)

