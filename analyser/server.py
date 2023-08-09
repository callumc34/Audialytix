from app import create_app

from asgiref.wsgi import WsgiToAsgi

app = WsgiToAsgi(create_app())
