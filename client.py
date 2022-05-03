import secrets

import requests
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

headers = {"Content-Type": "application/json", "Accept": "application/json"}


@app.route("/")
def index():
    response = requests.get(
        "https://api-modelos-ia.herokuapp.com/modelo", headers=headers
    )
    if response.status_code == 200:
        modelos = response.json()
        return render_template("index.html", modelos=modelos)


@app.route("/create", methods=["POST"])
def create():
    nome = request.form["nome"]
    descricao = request.form["descricao"]

    requests.post(
        "https://api-modelos-ia.herokuapp.com/modelo",
        json={"nome": nome, "descricao": descricao},
        headers=headers,
    )

    flash("Modelo adicionado com sucesso!")

    return redirect(url_for("index"))


@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        id = request.form["id"]

        nome = request.form["nome"]
        descricao = request.form["descricao"]

        link = "https://api-modelos-ia.herokuapp.com/modelo/{0}".format(id)

        requests.put(link, json={"nome": nome, "descricao": descricao}, headers=headers)

        flash("Modelo editado com sucesso!")

        return redirect(url_for("index"))
    else:
        redirect(url_for("delete"))


@app.route("/delete/<int:id>")
def delete(id):
    link = "https://api-modelos-ia.herokuapp.com/delete/{0}".format(id)

    requests.delete(link, headers=headers)

    flash("Modelo Deletado com Sucesso.")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
