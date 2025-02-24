from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from App.routes.form_routes import form_bp
    app.register_blueprint(form_bp)
    
    return app 