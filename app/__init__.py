from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
import base64

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__, static_folder='static')

    app.config.from_object('config.Config')

    db.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        from . import routes, models
        db.create_all()

    def generate_nonce():
        return base64.b64encode(os.urandom(16)).decode('utf-8')

    @app.before_request
    def set_nonce():
        g.nonce = generate_nonce()

    @app.after_request
    def add_headers(response):
        csp = f"default-src 'self'; script-src 'self' 'nonce-{g.nonce}'"
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = csp
        return response

    return app
