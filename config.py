import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def load_private_key():
        path = os.path.abspath(os.path.dirname(__file__))
        key_path = os.path.join(path, "secrets", "private-key.pem")
        with open(key_path, 'r') as f:
            return f.read()

    def load_public_key():
        path = os.path.abspath(os.path.dirname(__file__))
        key_path = os.path.join(path, "secrets", "public-key.pem")
        with open(key_path, 'r') as f:
            return f.read()
    
    SECRET_KEY = load_private_key()
    PUBLIC_KEY = load_public_key()

    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static', 'images')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024