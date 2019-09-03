import connexion
from flask_cors import CORS

if __name__ == '__main__':
    capp = connexion.FlaskApp(__name__, specification_dir='specs/')
    capp.add_api('blog.yaml', arguments={'title': 'Hello World Example'})
    CORS(capp.app)
    capp.run(host='0.0.0.0', debug=True, port=9090)