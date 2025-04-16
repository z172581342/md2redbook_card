from flask import Flask
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
    CORS(app)
    
    # 注册路由
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # 转换为 ASGI 应用
    asgi_app = WsgiToAsgi(app)
    return asgi_app