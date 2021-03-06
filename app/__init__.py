import os

from flask import Flask


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # register blueprints
    from app.api.bucket.views import bucket_blueprint
    app.register_blueprint(bucket_blueprint)

    from app.api.file.views import file_blueprint
    app.register_blueprint(file_blueprint)

 
    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app