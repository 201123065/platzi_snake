es una tarde de domingo, te acabas de certificar en el curso de django, y tu subconciente piensa: vaya que hoy es un buen dia para desarrollar mi primera aplicación en tiempo real!. tomas tu ordenador, ves tus apuntes y OH POR DIOS! no sabes como hacer una aplicación en realtime!. Tras trasnochar y buscar en 50 foros distintos, 80 preguntas en stackoverflow, y 6 horas en el facebook encuentras que mejor hubieras aprendido nodejs porque… you know… javascript!… no te preocupes, existe una herramienta BUENISIMA para solucionar esto, esta diseñada para entregarte acciones en vivo, y es facil de implementar, te presento, a Channels.

![](https://lh3.googleusercontent.com/PgqVxA0SgfTOBT3kaZfSikQm6GE_hx4c61srlFu7cdMQRslI8nxMxFvgfrbBTRlvqns9rOWfKQA2kQ=w2860-h2052-rw-no)


Channels es una herramienta diseñada especificamente para Django, con el objetivo de tener aplicaciones en tiempo real, pero dejemonos de palabrería, y pongamonos manos a la obra.

comenzaremos creando nuestra carpeta en el escritorio conocida como platzi_snake, ingresamos con cd platzi_snake, y generamos nuestro entorno virutal, luego ingresamos al mismo e instalamos django (pip install django)


```
~mkdir platzi_realtime
~cd platzi_realtime
~virtualenv .venv
~source .venv/bin/activate
~(.venv)

```

creamos nuestra aplicacion(django-admin.py startproject platzi_snake) e ingresamos a la misma. luego creamos nuestra aplicación snake_protocol 


```
~(.venv) django-admin.py startproject platzi_snake
~(.venv) cd platzi_snake
~(.venv) django-admin.py startapp snake_protocol

```



y listo! okno, quiza nos falta instalar ahmm… CHANNELS!!!…(y puede que pip install pathlib tambien sea necesario) 
```
~(.venv) pip install -U channels==1.1.8
~(.venv)pip install pathlib

```


**nota: la version mas reciente de channels(channels2) funciona unicamente con python3, para usar python2 debemos colocar pip install  channels==1.1.8**



y por supuesto nuestro broker(o la aplicacion que se va a encargar de realizar nuestra transaccion) como en nuestro caso: asgi_redis


```
~(.venv) pip install asgi_redis

```



una vez instalado, podemos escribir redis-server para que este se active, para saber si esta activado escribimos redis-cli ping, y nos debe responder con un PONG  
```
~(.venv) redis_cli ping
~PONG

```



primero lo primero: django no es un brujo, no sabe que vamos a utilizar channels para que funcione, por eso nos dirigimos a nuestro settings->INSTALLED_APPS y agregamos channels (y nuestra nueva app snake protocol por supuesto), tambien nuestro BASE DIR lo editamos de la siguiente manera:  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



```
 BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
.
.
.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # nuestra app sobre la que trabajaremos
    'snake_protocol',
    # nuestra hermosa herramienta channels
    'channels',

]
```
 primero recordemos como funciona django (modelo vista controlador)


![](https://heroku-blog-files.s3.amazonaws.com/posts/1473343845-django-asgi-websockets.png)


lo que haremos es agregar una capa intermedia, que reciba la petición, pero que la procese de manera asincrona, y que nos avise cuando la termine

![](https://heroku-blog-files.s3.amazonaws.com/posts/1473343845-django-wsgi.png)




ok y te podrias preguntar, ¿esto que quiere decir? pues… es bastante sencillo: para que sobrecargar nginx, si puedo procesar acciones extra en segundo plano.

bien, ahora vamos a nuestro proyecto, al cual vamos a agregar una nueva url el nuestro archivo de urls.py


```

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("snake_protocol.urls",namespace="index")),
]

```


ok pero seguramente estaras pensando: el urls no existe en snake protocol, ok tienes razon, es hora de crearlo.

```
from django.conf.urls import include, url

from .views  import juego

urlpatterns = [
	url(r'^$',juego.as_view(),name='juego'),
]

```







una vez tenemos el archivo, declaramos la url de nuestra vista:




```
from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class juego(TemplateView):
	game_template="juego.html"
	def get(self,request,*args,**kwargs):
		return render(request,self.game_template)
```





ok ahora tenemos 2 problemas: 
1: aun no hemos declarado nuetra carpeta donde se guarden los archivos estaticos
2.- tampoco donde se guarden las plantillas
3.-tampoco tenemos nuetra plantilla creada (ok, eran 3 problemas, no 2)

![](https://media.giphy.com/media/27EhcDHnlkw1O/giphy.gif)

primero resolvamos el mas sencillo: nuestra carpeta de plantillas
agregamos nuestro folder al nivel del proyecto con el nombre plantillas


ahora en nuestros settings buscamos nuestra definicion de TEMPLATES, y agregamos la siguiente instruccion en DIRS:  os.path.join(BASE_DIR,’plantillas')















```


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'plantillas')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

```


ahora resolvemos el problema de los estaticos de manera similar, creamos la carpeta al nivel del proyecto y agregamos las siguentes lineas(pueden ser al final del settings.py, no hay problema) 

```

STATIC_URL = '/estatico/'
STATIC_ROOT =os.path.join(os.path.dirname(BASE_DIR),"contenido_estatico")


STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"estatico"),
]

```















y es hora de resolver nuestro ultimo problema: crear el bendito html dentro de la capreta de plantillas con una interfaz super basica:




```
<html>
<head>
	<title>platzi goty (okno)</title>
</head>

<body>
	<img src="https://static.platzi.com/static/images/logos/platzi.3cae3cffd5ef.png" srcset="https://static.platzi.com/static/images/logos/platzi.3cae3cffd5ef.png 1x, https://static.platzi.com/static/images/logos/platzi@2x.fdf870da3a22.png 2x"  

	style="position: absolute; left: 500px; top: 150px;" heigth="" id="platzito">

</body>
</html>
```

toma en cuenta el style en la imagen, luego lo vamos a alterar, lo correcto es crear una nueva propiedad, y hacerlo en hojas de estilo, pero la pereza debe muertes, pero no tutoriales.

![](https://media.giphy.com/media/1moxLGt7YHVJvP1i2I/giphy.gif)


ok, el sitio es tan basico que lo unico que hace es mostrarnos el logo de platzi en el navegador, 
ahora, si intentamos correr nuestro proyecto sabes que pasa!…

![](http://m.memegen.com/78b1ne.jpg)


asi es! porque como dije hace un momento, django no es brujo, hay que configurar channels en nuestro settings:


```

# configuracion de CHANNELS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",  #redis como backend
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],  # busca a redis en la direccion
        },
        "ROUTING": "platzi_snake.routing.channel_routing",  # buscar el routing
    },
}
```


ahora nos podemos dar cuenta de otra peculiaridad que posee nuestro django channels, nos dice que nos falta un archivo llamdo routing: aqui es donde sucede la magia del SEGUNDO PLANO!!!..
al mismo nivel que nuestro settings, declaramos el archivo routing.py con la siguiente informacion:

```
from channels import include

channel_routing = [
	include("snake_protocol.routing.websocket_routing",path=r'^/ws_platzi'),
]

```

como nos podemos dar cuenta, sigue siendo django, es mas! es bastante sencillo confundirlo 


en el mismo nivel que este archivo, debemos crear algo que le diga a Django, hey! manda esto a segundo plano, y lo llamaremos asgi.py(asyncronous server gateway) y le decimos que vamos a utilizar django channels(‚recuerdas que redis tambien era asgi?): 

```
import os

from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "platzi_snake.settings")
channel_layer = get_channel_layer()

```
 ok, le acabamos de decir a django, manda lo que entre por channels al segundo plano, pero debemos completar lo que nos indexa de nuestra url!…. ay perdon, nuestro routing…
eso por supuesto en nuestro archivo routing.py

```
from channels import route
from .consumers import *


websocket_routing = [
	route("websocket.connect", ws_add),
	route("websocket.receive", ws_message),
	route("websocket.disconnect", ws_disconnect),
]
```

  aca declaramos 3 compuertas: la de apertura, la del mensaje y la de cerrar, estas pueden variar.
ahora veamos falta aaaalgooo…. **EL CONSUMER**!!!… la vista de nuestro websocket!!!… entonces pues… lo creamos dentro de nuestra **aplicacion** (ojo que aplicacion esta en negrita, no se crea en el proyecto, bueno, si se puede, pero por orden vamos a crearlo en nuestra app)
ok, comencemos agregando las tres definiciones que corresponden, el ws_add, ws_message, ws_disconnect



```
import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("platzi_piton").add(message.reply_channel)


def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("el formato no parece json=%s", message['text'])
        return
    if data:
        reply_channel = message.reply_channel.name
    return False

def ws_disconnect(message):
    Group("platzi_piton").discard(message.reply_channel)

```



con una url, y como toda url, es necesario colocar la casilla donde se indexa:( o sea en nuestra app snake_protocol), alli creamos el archivo websocket_routing.py



















en el ws_add creamos un grupo llamado platzi_piton que es el que escucha las peticiones del websoket

en es_message es cuando ya recibio algo (lo modificaremos mas adelante)

y el ws_disconnect es para cerrar esa conexion y que ya no siga escuchando


![](http://generadordememesonline.com/media/created/6p3q52.png)

podemos utilizar nuestra vieja y confiable ./manage makemigrations, ./manage migrate


./manage runserver

lo primero que notamos en nuestra terminal sera que nuestra terminal se llena de informacion (mas de lo normal)


```
platzi_snake git:(master) ./manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
March 10, 2018 - 00:02:13
Django version 1.11.7, using settings 'platzi_snake.settings'
Starting Channels development server at http://127.0.0.1:8000/
Channel layer default (asgi_redis.core.RedisChannelLayer)
Quit the server with CONTROL-C.
2018-03-10 00:02:13,603 - INFO - worker - Listening on channels http.request, websocket.connect, websocket.disconnect, websocket.receive
2018-03-10 00:02:13,603 - INFO - worker - Listening on channels http.request, websocket.connect, websocket.disconnect, websocket.receive
2018-03-10 00:02:13,605 - INFO - worker - Listening on channels http.request, websocket.connect, websocket.disconnect, websocket.receive
2018-03-10 00:02:13,606 - INFO - worker - Listening on channels http.request, websocket.connect, websocket.disconnect, websocket.receive
2018-03-10 00:02:13,608 - INFO - server - HTTP/2 support not enabled (install the http2 and tls Twisted extras)
2018-03-10 00:02:13,609 - INFO - server - Using busy-loop synchronous mode on channel layer
2018-03-10 00:02:13,609 - INFO - server - Listening on endpoint tcp:port=8000:interface=127.0.0.1
```





y es hora de la verdad: entramos a nuestro navegador y!!!….

ok ok, ya casi vamos empezando, por lo menos channels ya esta corriendo, es un inicio… no?

es hora de jugar un poco con nuestro websocket!!!…asi que comencemos a jugar con javascript!!!…

cuando el proyecto es grande hay que colocar los estaticos en otra carpeta bla bla bla bla… pero como este es pequeño, lo haremos en el mismo html

![](http://www.dorkly.com/images/download.jpg)
   debajo del html en el area de script agregamos lo siguiente:




```
<html>
<head>
	<title>platzi goty (okno)</title>
</head>

<body>
	<img src="https://static.platzi.com/static/images/logos/platzi.3cae3cffd5ef.png" srcset="https://static.platzi.com/static/images/logos/platzi.3cae3cffd5ef.png 1x, https://static.platzi.com/static/images/logos/platzi@2x.fdf870da3a22.png 2x"  

	style="position: absolute; left: 500px; top: 150px;" heigth="" id="platzito">

<script>
	
var ws_scheme_dispatch = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_dispatch = ws_scheme_dispatch + '://' + window.location.host + '/ws_platzi';
console.log("Conectando a " + ws_path_dispatch)
dispatch_socket = new WebSocket(ws_path_dispatch);

if (dispatch_socket.readyState == WebSocket.OPEN) dispatch_socket.onopen();



document.onkeypress =  mueve_el_platzi;
function mueve_el_platzi(e){
	var x = event.which || event.keyCode;
	if (x==119||x==87){muevelo_baby("W")}
	else if(x==83||x==115){muevelo_baby("S")}
	else if(x==65||x==97){muevelo_baby("A")}
	else if(x==68||x==100){muevelo_baby("D")}
}



function muevelo_baby(letra){
	var message = {
        action: "muevelo",
        direccion: letra,
    };
    dispatch_socket.send(JSON.stringify(message));
}


</script>

</body>
</html>
```



lo que estamos haciendo a continuación es una conexion con el websock
et creado en channels, lo imprimimos con el console.log, y le decimos que escuche cuando este este abierto, para comprobar que todo bien, podemos refrescar nuestro navegador, y en las herramientas de desarrollador, podemos ver que esta sucediendo:


ahora si, ya es momento de hacer magia, primero lo primero, creas una funcion que le hable al websocket(que le envie una informacion de cualquier tipo), y que tal si esta es un keypress en cualquer parte del teclado?, en fin, es un juego, no? pues es hora de recurrir a nuestro amigo el codigo ascii… wiiii!!!…



```

document.onkeypress =  mueve_el_platzi;
function mueve_el_platzi(e){
	var x = event.which || event.keyCode;
	if (x==119||x==87){muevelo_baby("W")}
	else if(x==83||x==115){muevelo_baby("S")}
	else if(x==65||x==97){muevelo_baby("A")}
	else if(x==68||x==100){muevelo_baby("D")}
}

```



primero lo primero, nuestra funcion esta declarada para que en el momento de presionar una tecla, esta se active, ¿como va a identificar la tecla?, gracias a nuestro a migo el codigo ascii, lo convertimos a numero, y si esta esta en mayuscula o minuscula la lee, luego la envia a una funcion llamada muevelo baby que lo convierte en un paquete y lo manda por nuestro socket dispatch_socket, pero… hace algo? PORSUPUESTO QUE NO!, 


pero es hora de interactuar con channels


 ![](https://media.giphy.com/media/3o85xoSCrG5ikLgQlG/giphy.gif)

lo primero que hacemos, es ir a nuestro ws_message y agregamos las siguientes lineas:



```
import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("platzi_piton").add(message.reply_channel)


def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("el formato no parece json=%s", message['text'])
        return
    if data:
        reply_channel = message.reply_channel.name
        if data['direccion'] == "W": 
        	direccion(0,-1,reply_channel)
        if data['direccion'] == "S":
        	direccion(0,1,reply_channel)  	
        if data['direccion'] == "A":
        	direccion(-1,0,reply_channel)  	
        if data['direccion'] == "D":
        	direccion(1,0,reply_channel)  	
    return False

def ws_disconnect(message):
    Group("platzi_piton").discard(message.reply_channel)


```



le estamos preguntando a channels 

si lo que recibio fue una letra de las validas, dependiendo de la letra que envie una instrucción (+1, -1 o 0) a una funcion llamada direccion, que contiene lo siguiente(lo colocamos en una nueva funcion que le llamaremos direccion, debajo de ws_disconnect):


```

def direccion(x,y,reply_channel):
    if reply_channel is not None:
        # Channel(reply_channel).send({
        Group("platzi_piton").send({
            "text": json.dumps ({
              "EJE_X": x,
              "EJE_Y": y,
            })
        })

```


aca channels nos esta devolviendo por el canal donde lo mandamos (reply channel) el resultado que necesitamos

y con eso ya teneoms para regresar a nuestro javascript!

de manera super primitiva, declaramos variables globales


```


var EJE_X=500;
var EJE_Y=150;

dispatch_socket.onmessage = function(e) {
	var data =JSON.parse(e.data);
	EJE_X = EJE_X+parseInt(data.EJE_X)*5
	EJE_Y = EJE_Y+parseInt(data.EJE_Y)*5
	document.getElementById('platzito').style.left=EJE_X+"px";
	document.getElementById('platzito').style.top=EJE_Y+"px";
} 

```


y ahora viene un dato importante!!!… para correr de manera correcta channels necesitamos 2 terminales(al menos en maquina local), y ambas con el entorno virtual activo, en cada una corremos distinstas instrucciones: 
en una corremos el worker ( rutas de channels) y en otra corremos el servidor SIN EL WORKER, nos mostrara algo similar a esto: 

```
./manage.py runserver --noworker

```
y en la otra



```
./manage.py runworker
```





y por supuesto!, ya podemos visitar a nuestro amigo el logo de platzi para verlo como se mueve!(utilizando las teclas W, A , S , D

![](https://media.giphy.com/media/3rgXBvnbXtxwaWmhr2/giphy.gif)

haz de estar pensando: QUEE! tanto para esto, LO PUDE HABER HECHO EN JAVASCRIPT!!!!… pues… si, la veradd si :( pero hey, que te parece si subimos la apuesta? 

![](https://media.giphy.com/media/l0HlI6NdcrtkV5C7e/giphy.gif)



por ahora no hemos hecho nada que no se pueda hacer con simplemente javascript y en front-end. pero que te parece si hacemos que se pueda manipular desde otro navegador LA MISMA IMAGEN

![](https://media.giphy.com/media/xT77XWum9yH7zNkFW0/giphy.gif)



puedes imaginar un multiplayer game online, realtime chat, o algo mas que te de tu imaginacion, los cambios son pocos, pero esenciales.

![](https://media.giphy.com/media/5VKbvrjxpVJCM/giphy.gif)

primero lo primero: nos dirigimos a nuestro archivo de channels, comentamos la linea Channel(reply_channel).send({ y agregamos el grupo que habiamos creado previamente)



```

def direccion(x,y,reply_channel):
    if reply_channel is not None:
        # Channel(reply_channel).send({
        Group("platzi_piton").send({
            "text": json.dumps ({
              "EJE_X": x,
              "EJE_Y": y,
            })
        })
```






ahora, si abrimos 2 navegadores, ( o uno en incognito y el otro en navegación normal) podemos ver como este puede ser controlado desde distintos puntos

![](https://lh3.googleusercontent.com/kAVfedFyypAbl0e-lcQyhRYXVJLPizJ5saWsCZHg-BXuIgsx-1OLPizJPwGok8naAoHuWkRGTjRuAct5sz8ipbnKaSzPloN8Zbnb=w1200-h676-rw-no)

claro, ya podras tu agregar paredes, iconos peronalizados, y otras cosas, pero esto es solo un vistazo al mundo del realtime!…

![](https://media.giphy.com/media/6tHy8UAbv3zgs/giphy.gif)

si quieres saber de manera detallada como hacer realtime con channels, te dejo la documentacion 

[](https://channels.readthedocs.io/en/latest/)
[]( https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django)


y el codigo por si quieres hecharle un vistazo ;)  [](https://github.com/201123065/platzi_snake)  
pd: este es mi primer post, asi que si algo no sale bien, lo siento 
