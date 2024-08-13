
from django.urls import path,include 
from .views import acceder,homePage, listarcategoria, agregarcategoria,editarcategoria,eliminarcategoria, listarunidad, agregarunidad, editarunidad, eliminarunidad, listarproducto, agregarproducto, editarproducto, eliminarproducto, listarcliente, agregarcliente, editarcliente, eliminarcliente, registrarventa, listarventas,clienteinfo,productoinfo,generar_pdf,consultar_documento
from django.contrib.auth import views 
# from django.contrib.auth import views
urlpatterns = [     
    path('', acceder,name="login"),    
    path('home/',homePage ,name="home"),  
    path('listacategoria/',listarcategoria,name="listarcategoria"), 
    path('agregarcategoria/',agregarcategoria ,name="agregarcategoria"), 
    path('editarcategoria/<int:id>/',editarcategoria ,name="editarcategoria"),
    path('eliminarcategoria/<int:id>/',eliminarcategoria,name="eliminarcategoria"),
    path('listaunidades/',listarunidad,name="listarunidad"), 
    path('agregarunidad/',agregarunidad ,name="agregarunidad"), 
    path('editarunidad/<int:id>/',editarunidad ,name="editarunidad"),
    path('eliminarunidad/<int:id>/',eliminarunidad,name="eliminarunidad"),
    path('listaproducto/',listarproducto,name="listarproducto"),
    path('agregarproducto/',agregarproducto ,name="agregarproducto"),
    path('editarproducto/<int:id>/',editarproducto ,name="editarproducto"),
    path('eliminarproducto/<int:id>/',eliminarproducto ,name="eliminarproducto"),
    path('listacliente/',listarcliente,name="listarcliente"),
    path('agregarcliente/',agregarcliente ,name="agregarcliente"),
    path('editarcliente/<int:id>/',editarcliente ,name="editarcliente"),
    path('eliminarcliente/<int:id>/',eliminarcliente ,name="eliminarcliente"),
    path('listarventas/', listarventas, name='listarventas'),
    path('registrarventa/', registrarventa, name='registrarventa'),
    path('clienteinfo/', clienteinfo, name='clienteinfo'),
    path('productoinfo/', productoinfo, name='productoinfo'),
    path('generar_pdf/<int:venta_id>/', generar_pdf, name='generar_pdf'), 
    path('consultar/<str:document_type>/<str:document_number>/', consultar_documento, name='consultar_documento'),
] 


