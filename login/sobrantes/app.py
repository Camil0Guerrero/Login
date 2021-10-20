from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)
import os
import sqlite3
from sqlite3 import Error

app=Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/validation", methods=["GET","POST"])
def validation():
  if request.method=="POST":
    email = request.form["email"]
    password = request.form["pass"]

    with sqlite3.connect("usuarios.db") as con :
      cur = con.cursor()
      cur.execute("SELECT * FROM Usuarios WHERE correo =? AND contrasena =?", [email, password])
      if cur.fetchone():
        return "login successfully"
      return "incorrect information"
  return "es esto"
        
@app.route("/register", methods=["GET","POST"])
def registrer():
  if request.method == "POST":
    name = request.form["nombre"]
    lname = request.form["apellido"]
    correo = request.form["correo"]
    password = request.form["contra"]

    try:
      with sqlite3.connect("usuarios.db") as con:
        cur = con.cursor() 
        cur.execute("INSERT INTO Usuarios (nombre, apellido, correo, contrasena) VALUES(?,?,?,?)",
        (name,lname,correo,password)) 
        con.commit() 
        return "Guardado con exito"
      
    except sqlite3.IntegrityError:
      flash("Este correo ya esta registrado en otra cuenta, inicia sesion o registrate con otro")
    
    except Error:
      print(Error)

  return "ha ocurrido un error, reinicie o inente mas tarde"
    

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/contacto")
def registro():
    return "proximamente ..."


if __name__=='__main__':
    app.run(debug=True)