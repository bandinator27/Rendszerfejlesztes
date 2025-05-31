import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def load_private_key():
        path = os.path.abspath(os.path.dirname(__file__))
        key_path = os.path.join(path, "app/secrets", "private-key.pem")
        with open(key_path, 'r') as f:
            return f.read()
    
    SECRET_KEY = load_private_key()