from wtforms import Form
from wtforms import DateField,StringField, TextAreaField, SelectField, RadioField, EmailField, IntegerField, SelectMultipleField
from wtforms import validators
from wtforms import widgets

class UserForm(Form):
    id = IntegerField('id', [validators.number_range(min=1, max=20, message='valor no valido')])
    nombre = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])
    telefono = StringField("Telefono",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")])
    tiempo = StringField("Tiempo",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=1, max=10, message="Ingresa nombre valido")
    ])

    materia = StringField("Materia",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=1, max=50, message="Ingresa nombre valido")
    ])
    
    sueldo = IntegerField('Sueldo', [
        validators.number_range(min=1, max=1000, message="Valor no valido")
    ])

class Pizza(Form):
    tamanio = RadioField('Tamaño', choices=[('Chica', 'Chica $40'), ('Mediana','Mediana $80'), ('Grande','Grande $120')])
    ingredientes = SelectMultipleField('Ingredientes', choices=[("Jamon", "Jamon $10"), ("Piña", "Piña $10"), ("Champiñones", "Champiñones $10")],
                                                                widget=widgets.ListWidget(prefix_label=False),
                                                                option_widget=widgets.CheckboxInput())
    cantidad = IntegerField('cantidad', [
        validators.number_range(min=1, max=1000, message="Valor no valido")
    ])
    subTotal = IntegerField('SubTotal', [
        validators.number_range(min=1, max=1000, message="Valor no valido")
    ])
    nombre = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])
    direccion = StringField("Direccion",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])
    tel = StringField("Telefono",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])
    fecha = DateField("Fecha",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")
    ])

class busqueda(Form):
    palabra = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")])
    fecha = DateField("Fecha",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message="Ingresa nombre valido")])
    filtro = RadioField('Filtro', choices=[("1", 'Dia'), ("2",'Mes'), ("3",'Año')])