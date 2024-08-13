from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import (
    Categoria,
    Unidad,
    Producto,
    Cliente,
    Tipo,
    CabeceraVenta,
    DetalleVenta,
    Parametros,
)
from django.db.models import Q
from .forms import (
    CategoriaForm,
    UnidadForm,
    ProductoForm,
    ClienteForm,
    TipoForm,
    CabeceraVentaForm,
    DetalleVentaForm,
    ParametrosForm,
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.


def generar_pdf(request, venta_id):
    try:
        # Obtener los datos de la venta
        venta = CabeceraVenta.objects.get(id=venta_id)
        detalles = DetalleVenta.objects.filter(idCabeceraVenta=venta)

        # Cargar la plantilla HTML
        template_path = "ventas/venta_pdf.html"
        context = {
            "venta": venta,
            "detalles": detalles,
        }
        template = get_template(template_path)
        html = template.render(context)

        # Crear una respuesta HTTP con el tipo de contenido PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"inline; filename=venta_{venta_id}.pdf"

        # Renderizar HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse("Error al generar el PDF")

        return response

    except CabeceraVenta.DoesNotExist:
        return HttpResponse("Venta no encontrada", status=404)


def acceder(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=password)

            if usuario is not None:
                login(request, usuario)
                return redirect("menu")

    form = AuthenticationForm()
    return render(request, "index.html", {"form": form})


def homePage(request):
    context = {}
    return render(request, "menu.html", context)


def listarcategoria(request):
    queryset = request.GET.get("buscar")

    if queryset:
        categorias = Categoria.objects.filter(
            Q(descripcion__icontains=queryset), estado=True
        ).distinct()
    else:
        categorias = Categoria.objects.filter(estado=True)

    context = {"categoria": categorias}
    return render(request, "listarCategoria.html", context)


from django.shortcuts import render, redirect
from .forms import CategoriaForm


def agregarcategoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarcategoria")
    else:
        form = CategoriaForm()

    context = {"form": form}
    return render(request, "categoria/agregar.html", context)


def editarcategoria(request, id):
    categoria = Categoria.objects.get(id=id)

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("listarcategoria")
    else:
        form = CategoriaForm(instance=categoria)

    context = {"form": form}
    return render(request, "categoria/editar.html", context)


def eliminarcategoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.estado = False
    categoria.save()
    return redirect("listarcategoria")


from django.shortcuts import render, redirect
from .forms import UnidadForm


def listarunidad(request):
    queryset = request.GET.get("buscar")

    if queryset:
        unidades = Unidad.objects.filter(
            Q(descripcion__icontains=queryset), estado=True
        ).distinct()
    else:
        unidades = Unidad.objects.filter(estado=True)

    context = {"unidad": unidades}
    return render(request, "listarUnidades.html", context)


def agregarunidad(request):
    if request.method == "POST":
        form = UnidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarunidad")
    else:
        form = UnidadForm()

    context = {"form": form}
    return render(request, "unidades/agregar.html", context)


def editarunidad(request, id):
    unidad = Unidad.objects.get(id=id)

    if request.method == "POST":
        form = UnidadForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect("listarunidad")
    else:
        form = UnidadForm(instance=unidad)

    context = {"form": form}
    return render(request, "unidades/editar.html", context)


def eliminarunidad(request, id):
    unidad = Unidad.objects.get(id=id)
    unidad.delete()
    return redirect("listarunidad")


def listarproducto(request):
    queryset = request.GET.get("buscar")
    producto = Producto.objects.filter(estado=True)
    if queryset:
        producto = Producto.objects.filter(
            Q(descripcion__icontains=queryset)
            | Q(idUnidad__descripcion__icontains=queryset)
            | Q(idCategoria__descripcion__icontains=queryset),
            estado=True,
        ).distinct()

    context = {"producto": producto}
    return render(request, "listarProductos.html", context)


def agregarproducto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarproducto")
    else:
        form = ProductoForm()

    context = {"form": form}
    return render(request, "producto/agregar.html", context)


def editarproducto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("listarproducto")
    else:
        form = ProductoForm(instance=producto)

    context = {"form": form}
    return render(request, "producto/editar.html", context)


def eliminarproducto(request, id):
    producto = Producto.objects.get(id=id)
    producto.estado = False
    producto.save()
    return redirect("listarproducto")


def listarcliente(request):
    queryset = request.GET.get("buscar")
    cliente = Cliente.objects.filter(estado=True)
    if queryset:
        cliente = Cliente.objects.filter(
            Q(nombres__icontains=queryset)
            | Q(email__icontains=queryset)
            | Q(direccion__icontains=queryset)
            | Q(rucDni__icontains=queryset),
            estado=True,
        ).distinct()

    context = {"cliente": cliente}
    return render(request, "listarClientes.html", context)


def agregarcliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarcliente")
    else:
        form = ClienteForm()

    context = {"form": form}
    return render(request, "cliente/agregar.html", context)


def editarcliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("listarcliente")
    else:
        form = ClienteForm(instance=cliente)

    context = {"form": form}
    return render(request, "cliente/editar.html", context)


def eliminarcliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.estado = False
    cliente.save()
    return redirect("listarcliente")


def registrarventa(request):
    if request.method == "POST":
        fecha_venta = request.POST.get("fecha_venta")
        tipo_documento_id = request.POST.get("tipo_documento")
        parametro_id = request.POST.get("parametro")
        cliente_id = request.POST.get("cliente")

        try:
            parametro = Parametros.objects.get(pk=parametro_id)
            nro_doc = (
                f"{parametro.serie}-{parametro.nroDoc}"  # Concatenar serie y nroDoc
            )
        except Parametros.DoesNotExist:
            messages.error(request, "Parámetro no encontrado.")
            return redirect("registrarventa")

        sub_total = float(request.POST.get("subtotal", 0))
        igv = float(request.POST.get("igv", 0))
        total = float(request.POST.get("total", 0))

        # Crear la CabeceraVenta
        cabecera_venta = CabeceraVenta(
            fechaVenta=fecha_venta,
            idParametros=parametro,
            idTipo_id=tipo_documento_id,
            idCliente_id=cliente_id,
            nroDoc=nro_doc,
            subTotal=sub_total,
            igv=igv,
            total=total,
            estado=True,
        )
        cabecera_venta.save()

        # Obtener los datos del carrito
        productos = request.POST.getlist("producto_id")
        cantidades = request.POST.getlist("cantidad")

        for producto_id, cantidad in zip(productos, cantidades):
            if producto_id:
                try:
                    producto = Producto.objects.get(pk=producto_id)
                    cantidad = int(cantidad)
                    precio = producto.precio
                    total_precio = precio * cantidad

                    detalle_venta = DetalleVenta(
                        idCabeceraVenta=cabecera_venta,
                        idProducto=producto,
                        precio=precio,
                        cantidad=cantidad,
                    )
                    detalle_venta.save()

                    producto.stock -= cantidad
                    producto.save()

                except Producto.DoesNotExist:
                    messages.error(
                        request, f"Producto con ID {producto_id} no encontrado."
                    )
                    return redirect("registrarventa")

        messages.success(request, "Venta registrada exitosamente.")
        return redirect("listarventas")

    # Si la solicitud es GET, cargar el formulario
    clientes = Cliente.objects.filter(estado=True)
    productos = Producto.objects.filter(estado=True)
    tipos = Tipo.objects.all()
    parametros = Parametros.objects.all()

    context = {
        "clientes": clientes,
        "productos": productos,
        "tipos": tipos,
        "parametros": parametros,
    }

    return render(request, "ventas/registrar_venta.html", context)


def clienteinfo(request):
    cliente_id = request.GET.get("cliente_id")
    cliente = Cliente.objects.filter(id=cliente_id).first()
    if cliente:
        data = {"rucDni": cliente.rucDni, "direccion": cliente.direccion}
        return JsonResponse(data)
    return JsonResponse({"error": "Cliente no encontrado"}, status=404)


def productoinfo(request):
    producto_id = request.GET.get("producto_id")
    producto = Producto.objects.filter(id=producto_id).first()
    if producto:
        data = {"unidad": producto.idUnidad.descripcion, "precio": producto.precio}
        return JsonResponse(data)
    return JsonResponse({"error": "Producto no encontrado"}, status=404)


def listarventas(request):
    ventas = CabeceraVenta.objects.all().order_by("id")
    detalles = DetalleVenta.objects.all()
    return render(
        request,
        "ventas/listar_venta.html",
        {
            "ventas": ventas,
            "detalles": detalles,
        },
    )


from django.http import JsonResponse
import requests


def consultar_documento(request, document_type, document_number):
    if document_type == "dni":
        url = f"https://apiperu.dev/api/dni/{document_number}"
    else:  # document_type == 'ruc'
        url = f"https://apiperu.dev/api/ruc/{document_number}"

    token = "c36358c49922c564f035d4dc2ff3492fbcfd31ee561866960f75b79f7d645d7d"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        if document_type == "dni":
            return JsonResponse(
                {
                    "nombre_completo": data.get("data", {}).get("nombre_completo", ""),
                    "direccion": data.get("data", {}).get("direccion", ""),
                }
            )
        else:
            return JsonResponse(
                {
                    "nombre_completo": data.get("data", {}).get(
                        "nombre_o_razon_social", ""
                    ),
                    "direccion": data.get("data", {}).get("direccion_completa", ""),
                }
            )
    else:
        return JsonResponse({"error": "No se pudo obtener la información"}, status=400)
