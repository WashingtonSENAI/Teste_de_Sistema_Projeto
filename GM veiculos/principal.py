from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    u_nome = db.Column(db.String(120), unique=False, nullable=False)
    u_email = db.Column(db.String(120), unique=True, nullable=False)
    u_telefone = db.Column(db.BigInteger, unique=False, nullable=False)


class Produtos(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    p_nome = db.Column(db.String(120), unique=True, nullable=False)
    p_preco = db.Column(db.String(120), unique=False, nullable=False)



class Quantidade(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    q_produtos_id = db.Column(db.Integer, db.ForeignKey('produtos.p_id'), nullable=False)
    q_quantidade = db.Column(db.Integer, unique=False, nullable=False)
    q_produtos = db.relationship('Produtos', backref='quantidade')

                                                                                                                                                               
with app.app_context():
     db.create_all()
     
@app.route("/adicionar")
def adicionar():
    return render_template("adicionar.html")
     
 
@app.route("/listar")
def listar():
    produtos = Produtos.query.all()  
    usuarios = Usuario.query.all()  
    return render_template('listar.html',produtos = produtos, usuarios = usuarios)


@app.route("/remover")
def remover():
    
    return render_template('remover.html')
    
 
@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    if request.method == 'POST':
        p_nome= request.form['Nome']
        p_preco = request.form['Preco']

        produto = Produtos(p_nome = p_nome, p_preco = p_preco)

        db.session.add(produto)
        db.session.commit()
        produtos = Produtos.query.all()  
        usuarios = Usuario.query.all()  
        return render_template("listar.html", produtos = produtos, usuarios = usuarios)
    
     
@app.route('/adicionar_user', methods=['POST'])
def adicionar_user():
    if request.method == 'POST':
        u_nome= request.form['Nome']
        u_email = request.form['email']
        u_telefone = request.form['telefone']
        user = Usuario(u_nome = u_nome, u_email = u_email,u_telefone = u_telefone)

        db.session.add(user)
        db.session.commit()
        produtos = Produtos.query.all()  
        usuarios = Usuario.query.all()  
        return render_template("listar.html", produtos = produtos, usuarios = usuarios)
    
    
@app.route('/buscar_e_Excluir_Produto', methods=['POST'])
def buscar_veiculoExcluir_Produto():
    if request.method == 'POST':
        produto_id = request.form['p_id']
        produto = Produtos.query.get(produto_id)

        if produto:
            
            db.session.delete(produto)
            db.session.commit() 
            
            produtos = Produtos.query.all()  
            usuarios = Usuario.query.all()
           
            return render_template('listar.html',produtos = produtos, usuarios = usuarios)
        else:
            return render_template('remover.html', naoexiste_Produto = True)




@app.route('/buscar_e_Excluir_User', methods=['POST'])
def buscar_veiculoExcluir_User():
    if request.method == 'POST':
        user_id = request.form['u_id']
        user = Usuario.query.get(user_id)

        if user:
            
            db.session.delete(user)
            db.session.commit() 
            
            produtos = Produtos.query.all()  
            usuarios = Usuario.query.all()
           
            return render_template('listar.html',produtos = produtos, usuarios = usuarios)
        else:
            return render_template('remover.html', naoexiste_User = True)





if __name__ == "__main__":
    app.run(debug=True)
