# logging_extension.py

import logging
from flask import Flask 

def setup_logging(app):
    # Log to file
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)
    
    app.logger.setLevel(logging.DEBUG)

def create_app():
    app = Flask(__name__)
    setup_logging(app)
    return app