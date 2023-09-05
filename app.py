from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurar a conexão com o banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jm_veiculos'

mysql = MySQL(app)

@app.route("/")
def index():
    # Consulta os veículos cadastrados no banco de dados
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM veiculos")
    veiculos = cur.fetchall()
    cur.close()
    return render_template("index.html", veiculos=veiculos)

@app.route("/adicionar")
def exibir():

  
    return render_template("adicionar.html")


@app.route("/adicionar_veiculo", methods=["POST"])
def adicionar_veiculo():
    if request.method == "POST":
        # Recebe os dados do formulário
        tipo = request.form["tipo"]
        cor = request.form["cor"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        ano = request.form["ano"]
        estado = request.form["estado"]
        km_rodados = request.form["km_rodados"]
        leilao = request.form.get("leilao", False)
        formas_pagamento = request.form.getlist("formas_pagamento")

        # Insere os dados no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO veiculos (tipo, cor, marca, modelo, ano_fabricacao, estado, km_rodados, leilao, formas_pagamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (tipo, cor, marca, modelo, ano, estado, km_rodados, leilao, ', '.join(formas_pagamento)))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for("index"))

@app.route("/excluir_veiculo/<int:veiculo_id>")
def excluir_veiculo(veiculo_id):
    # Exclui o veículo do banco de dados
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM veiculos WHERE id = %s", (veiculo_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("index"))

@app.route("/editar_veiculo/<int:veiculo_id>")
def editar_veiculo(veiculo_id):
    # Consulta as informações do veículo com base no ID
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM veiculos WHERE id = %s", (veiculo_id,))
    veiculo = cur.fetchone()
    cur.close()
    return render_template("editar_veiculo.html", veiculo=veiculo)

@app.route("/atualizar_veiculo/<int:veiculo_id>", methods=["POST"])
def atualizar_veiculo(veiculo_id):
    if request.method == "POST":
        # Recebe os dados do formulário
        tipo = request.form["tipo"]
        cor = request.form["cor"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        ano = request.form["ano"]
        estado = request.form["estado"]
        km_rodados = request.form["km_rodados"]
        leilao = 1 if request.form.get("leilao") == "on" else 0  # Converte para 1 ou 0
        formas_pagamento = request.form.getlist("formas_pagamento")

        # Atualiza os dados no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("UPDATE veiculos SET tipo=%s, cor=%s, marca=%s, modelo=%s, ano_fabricacao=%s, estado=%s, km_rodados=%s, leilao=%s, formas_pagamento=%s WHERE id=%s",
                    (tipo, cor, marca, modelo, ano, estado, km_rodados, leilao, ', '.join(formas_pagamento), veiculo_id))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
