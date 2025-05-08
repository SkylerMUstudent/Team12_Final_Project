from flask import Flask
from config import Config
from models import db
from routes import main_bp, admin_bp, reservation_bp
from models import db, Admin

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reservation_bp)

    return app

app = create_app()

#this helps create admin table..
with app.app_context():
    db.create_all()

    Admin.query.delete()
    db.session.add_all([
        Admin(username='admin1', password='pass1'),
        Admin(username='admin2', password='pass2'),
        Admin(username='admin3', password='pass3')
    ])
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
