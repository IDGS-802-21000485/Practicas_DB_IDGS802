from flask import Flask, request, render_template, Response
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelomentConfig
from models import Profesores, Pizza
from datetime import datetime
from flask import redirect
ordenes = []
clientePe = ""
ordenes.clear()
datos_objetos = []
import forms
from flask import flash
from models import db
app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CSRFProtect()
cliente = []


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/index", methods=["GET", "POST"])
def index():
    profe_form = forms.UserForm(request.form)

    if request.method == 'POST' :
        profe = Profesores(nombre=profe_form.nombre.data,
                        telefono=profe_form.telefono.data,
                        sueldo=profe_form.sueldo.data,
                        tiempo = profe_form.tiempo.data,
                        materia = profe_form.materia.data)
        # Insert
        db.session.add(profe)
        db.session.commit()
    return render_template("index.html", form=profe_form)

@app.route("/ABC_profesores",  methods=("GET", "POST"))
def ABCProfe():
    profe_form = forms.UserForm(request.form)
    profesor= Profesores.query.all()
    return render_template('ABC_Profesores.html', profesor=profesor)

@app.route("/alumnos", methods=("GET", "POST"))
def alumnos():
    print('dentro de ruta 2')
    nom = ''
    apaterno = ''
    correo = ''
    alum_forms = forms.UserForm(request.form)
    if request.method == 'POST':
        nom = alum_forms.nombre.data
        apaterno = alum_forms.apaterno.data
        correo = alum_forms.email.data
        messages = 'Bienvenido {}'.format(nom)
        flash(messages)
        print("Nombre: {}".format(nom))
        print("apaterno: {}".format(apaterno))
        print("correo: {}".format(correo))
        print(alum_forms.validate())
    return render_template("alumnos.html", form=alum_forms, nom=nom, apa=apaterno, c=correo)

@app.route("/pizza", methods=["GET", "POST"])
def pizza():
    nombreL = ""
    direccionL = ""
    telL = ""
    fechaL = ""

    totales_por_nombre = {}
    total = 0
    pizBD = Pizza.query.all()
    fecha_de_hoy = str(datetime.now().date())
    for pizza in pizBD:
        if pizza.fecha == fecha_de_hoy:
            nombre = pizza.nombre
            valor = int(pizza.subTotal)
            total += valor
            if nombre in totales_por_nombre:
                totales_por_nombre[nombre] += valor
            else:
                totales_por_nombre[nombre] = valor
    datos_objetos = [{'nombre': nombre, 'total': total} for nombre, total in totales_por_nombre.items()]
    pizza_form=forms.Pizza(request.form)
    np = {}
    if request.method=='POST':
        tamanio = pizza_form.tamanio.data
        nombreL = pizza_form.nombre.data
        direccionL = pizza_form.direccion.data
        telL = pizza_form.tel.data
        tamanio = pizza_form.tamanio.data
        fechaL = str(pizza_form.fecha.data)
        tamN = 0
        
        ingredientes = quit(str(pizza_form.ingredientes.data))
        cantidad = pizza_form.cantidad.data
        if tamanio == "Chica":
            tamN = 40
        elif tamanio == "Mediana":
            tamN = 80
        else:
            tamN = 120
        subtotal = (tamN + 10) * int(cantidad)
        ordenes.append({'tamanio': tamanio, 'ingredientes': ingredientes, 'cantidad': cantidad, 'subtotal': subtotal,'nombre': nombreL, 'direccion': direccionL, 'tel': telL, 'fecha': fechaL})
        pizza_form.tamanio.data = None
        pizza_form.ingredientes.data = None
        pizza_form.cantidad.data = None
    return render_template("Pizzeria.html", Pizza = pizza_form, Ordenes = ordenes, NP = datos_objetos, Total = total, nombre = nombreL)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    posicion = int(request.args.get('id'))
    if request.method=='GET':
        ordenes.pop(posicion)
    return redirect("/pizza")

@app.route("/guardarP", methods=["GET", "POST"])
def guardarP():
    pizza_form = forms.Pizza(request.form)
    if request.method == 'POST' or "GET":
        print("De aqui")
        print(ordenes)
        for i in ordenes:
            pizza = Pizza(tamanio=i['tamanio'], ingredientes=i['ingredientes'], cantidad=i['cantidad'], subTotal=i['subtotal'], nombre=i["nombre"], direccion=i["direccion"], tel=i["tel"], fecha= i["fecha"])
            db.session.add(pizza)
            db.session.commit()
    ordenes.clear()
    return redirect("/pizza")

from datetime import datetime

@app.route("/ABC", methods=["GET", "POST"])
def abc():
    abc_form = forms.busqueda(request.form)
    f = abc_form.palabra.data
    c = (abc_form.filtro.data)
    t = 0
    if c != None:
        t = int(c)
        
    nombres_de_dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    nombres_de_meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    piz = []
    if request.method == 'POST' or "GET":
        if t == 1:
            dia_semana = nombres_de_dias.index(f.lower())
            # Filtrar las fechas que coincidan con el día de la semana
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").weekday() == dia_semana]
        elif t == 2:
            mes = nombres_de_meses.index(f.lower()) + 1  # Sumamos 1 porque los meses en Python van de 1 a 12
            # Filtrar las fechas que coincidan con el mes
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").month == mes]
        elif t == 3:
            año = int(f)
            # Filtrar las fechas que coincidan con el año
            piz = [pizza for pizza in Pizza.query.all() if datetime.strptime(pizza.fecha, "%Y-%m-%d").year == año]
        elif t == 0:
            piz = Pizza.query.all()
    res= 0
    for a in piz:
        res+= int(a.subTotal)
    return render_template("ABCVentas.html",  bus=abc_form, Pizzas=piz, t = res)



@app.route("/limp",  methods=("GET", "POST"))
def limp():
    pizza_form=forms.Pizza(request.form)
    pizza_form.tamanio.data = None
    pizza_form.ingredientes.data = None
    pizza_form.cantidad.data = None
    pizza_form.nombre.data = None
    pizza_form.direccion.data = None
    pizza_form.tel.data = None
    ordenes.clear()
    return redirect("/pizza")

def quit(cadena):
    cadena_sin_especiales = cadena.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
    return cadena_sin_especiales


if __name__ == "__main__":
#    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
