import os
from flask import Flask
from extensions import db, login_manager

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'school.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access the administration area.'
    from models import Admin
    from routes.admin import admin_bp
    from routes.public import public_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Admin, int(user_id))
    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == '__main__':
    print('=' * 55)
    print(' SCHOOL WEBSITE SERVER')
    print('=' * 55)
    print(' Local:   http://127.0.0.1:5000')
    print(' Admin:   http://127.0.0.1:5000/admin/login')
    print(' Network: http://192.168.18.12:5000')
    print('=' * 55)
    app.run(host='0.0.0.0', port=5000, debug=False)
