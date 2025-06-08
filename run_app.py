from config import Config
from app import create_app

if __name__ == "__main__":
    create_app(config_class=Config).run("localhost", 5000, debug = True)

# debug = True for easy reload