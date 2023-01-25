import os
from http import HTTPStatus
from flask import Flask
from flaskr.util.utils import response_message
from config import settings
from flaskr.views import auth, blog, users, service

def create_app(test_config = 'DevelopmentConfig'):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # app.config.from_pyfile("config.py")
    if test_config == 'ProductionConfig':        
        app.config.from_object(settings.ProductionConfig)
    elif test_config == 'TestingConfig':        
        app.config.from_object(settings.TestingConfig)
    else:              
        app.config.from_object(settings.DevelopmentConfig)

    from .models import database

    database.init_database(app)


    # apply the blueprints to the app
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(service.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    app.errorhandler(HTTPStatus.NOT_FOUND)
    def handle_404(error):
        return response_message('error', str(error), HTTPStatus.NOT_FOUND)

    app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def handle_500(error):
        return response_message('error', str(error), HTTPStatus.INTERNAL_SERVER_ERROR)

    return app
