from app import create_app
import app.config as config

app = create_app()

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=True)