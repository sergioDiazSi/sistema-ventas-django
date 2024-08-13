from django import forms
from .models import Categoria, Unidad, Producto, Cliente, Tipo, Parametros, CabeceraVenta, DetalleVenta

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion', 'estado']
        widgets = {
            'estado': forms.CheckboxInput(),
        }

class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['descripcion', 'estado']
        widgets = {
            'estado': forms.CheckboxInput(),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['idUnidad', 'idCategoria', 'descripcion', 'estado', 'stock', 'precio']
        widgets = {
            'estado': forms.CheckboxInput(),
        }

class ClienteForm(forms.ModelForm):
    DOCUMENT_TYPE_CHOICES = [
        ('dni', 'DNI'),
        ('ruc', 'RUC'),
    ]

    document_type = forms.ChoiceField(choices=DOCUMENT_TYPE_CHOICES, label='Tipo de Documento')
    rucDni = forms.CharField(max_length=12, label='RUC o DNI', required=True)
    nombres = forms.CharField(label='Nombres', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    direccion = forms.CharField(label='Dirección', required=False, widget=forms.TextInput())

    class Meta:
        model = Cliente
        fields = ['document_type', 'rucDni', 'nombres', 'email', 'direccion', 'estado']
        widgets = {
            'estado': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rucDni'].widget.attrs.update({
            'placeholder': 'Ingrese su número de documento',
        })

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['descripcion']

class ParametrosForm(forms.ModelForm):
    class Meta:
        model = Parametros
        fields = ['nroDoc', 'serie']

class CabeceraVentaForm(forms.ModelForm):
    class Meta:
        model = CabeceraVenta
        fields = ['fechaVenta', 'idParametros', 'idTipo', 'idCliente', 'nroDoc', 'subTotal', 'igv', 'total', 'estado']
        widgets = {
            'fechaVenta': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.CheckboxInput(),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['idCabeceraVenta', 'idProducto', 'precio', 'cantidad']
