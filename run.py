from app import app
from config import Config

# Use Config class to access ENVs
HOST = Config.HOST
PORT = Config.PORT

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)