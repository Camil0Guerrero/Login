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
from markupsafe import escape
# escape hace es no se puedan entrar funciones por medio de los formularios
# ya que los inserta como si fuera un texto mas
import os
import sqlite3
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash

codigo=[]
correos=[]
def sendemail(correo):
    import smtplib 
    import random
    numero = random.randint(99999,1000000)
    codigo.append(numero)
    try:
      server=smtplib.SMTP(host="smtp.gmail.com",port= 587)
      server.ehlo()
      server.starttls()
      server.login("keyloggerprueba30@gmail.com","prueba123456")
      mensaje = 'Subject: {}\n{}{}'.format("Codigo","El codigo es ", numero) 
      server.sendmail("keyloggerprueba30@gmail.com",correo, mensaje)
      server.quit()
      return numero      
    except:
      return "correo no enviado "
#

app=Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/validation", methods=["GET","POST"])
def validation():
  if request.method=="POST":
    email =    escape(request.form["email"])
    password = escape(request.form["pass" ])
    hashclave = generate_password_hash(password)

    with sqlite3.connect("usuarios.db") as con :
      cur = con.cursor()
      consulta = cur.execute("SELECT contrasena FROM Usuarios WHERE correo =? " , [email]).fetchone()
      if consulta != None:
        clave_hash = consulta[0]

        if check_password_hash(clave_hash, password):
          return "contraseña correcta"
        
        return "incorrect information"
  return "es esto"
        
@app.route("/register", methods=["GET","POST"])
def registrer():
  if request.method == "POST":
    name     = escape(request.form["nombre"  ])
    lname    = escape(request.form["apellido"])
    correo   = escape(request.form["correo"  ])
    password = escape(request.form["contra"  ])
    hashclave = generate_password_hash(password)
    try:
      with sqlite3.connect("usuarios.db") as con:
        cur = con.cursor() 
        cur.execute("INSERT INTO Usuarios (nombre, apellidos, correo, contrasena) VALUES(?,?,?,?)",
        [name,lname,correo,hashclave]) 
        con.commit() 
        return "Guardado con exito"
    except sqlite3.IntegrityError:
      return "este correo ya esta asociado a otro usuario, intenta con otro o inicia sesion"
      
  

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


@app.route("/reset",methods=["GET","POST"])
def reset():
    if request.method=="POST":
      email = escape(request.form["correo"])
      with sqlite3.connect("usuarios.db") as con :
        cur = con.cursor()
        consulta = cur.execute("SELECT correo FROM Usuarios WHERE correo =? " , [email]).fetchone()
        correos.append(consulta)
        if consulta:
          numero = sendemail(consulta)
          return render_template("codigo.html")

        else:
          return("Este correo no ha sido registrado, para mas informacion contactacte con el admistrador")
  

@app.route("/reset_password", methods=["POST","GET"])
def reset_password():
  return render_template("Reset_request.html")

@app.route("/validationpass", methods=["GET","POST"])
def vaidationcode():
  codig = int(escape(request.form["codigo"]))
  if codig == int(codigo[0]):
    return render_template("newpass.html")
  else:
    return"codigo incorrecto"

@app.route("/updatepass", methods=["GET","POST"])
def updatepass():
  password = escape(request.form["npassword"])
  with sqlite3.connect("usuarios.db") as con :
      cur = con.cursor()
      email= correos[0][0]
      data = cur.execute("SELECT * FROM Usuarios WHERE correo =? " , [email]).fetchall()
      consulta = cur.execute("UPDATE Usuarios set id=?, nombre = ?, apellidos=?, correo=?, contrasena=?  WHERE correo =? ", [data[0][0],data[0][1],data[0][2],data[0][3],password,email])
      con.commit()
      return "contraseña insertada"
  


if __name__=='__main__':
    app.run(debug=True)
