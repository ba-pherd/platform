import os
import logging

from flask import Flask, render_template, current_app
from flask.logging import default_handler
from werkzeug.exceptions import NotFound

from .category_flash import flash_error
from .logging_formatter import AuthenticatedRequestFormatter

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '')
if KAFKA_BOOTSTRAP_SERVERS == '':
    raise Exception('Env variable KAFKA_BOOTSTRAP_SERVERS is empty')


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Loading configurations...')
    if test_config is None:
        app.config.from_prefixed_env()
        app.config.from_mapping({
            'KAFKA_BOOTSTRAP_SERVERS': KAFKA_BOOTSTRAP_SERVERS
        })
    else:
        app.config.from_mapping(test_config)

    app.logger.info('Configurations loaded')

    os.makedirs(app.instance_path, exist_ok=True)

    app.logger.info('Configuring log format...')
    configure_logging()
    app.logger.info('Log format configured')

    from .routes import patients_data_loading, mir_results_data_loading, task_runner, users, task_results
    app.register_blueprint(patients_data_loading.bp)
    app.register_blueprint(mir_results_data_loading.bp)
    app.register_blueprint(task_runner.bp)
    app.register_blueprint(task_results.bp)
    app.register_blueprint(users.bp)

    health_check_route = app.get('/health')(health_check)
    not_found_route = app.errorhandler(Exception)(error_handler)
    home_route = app.get('/')(homepage)

    return app


def health_check():
    return ('', 200)


def homepage():
    return render_template('index.html')


def error_handler(err):
    if not isinstance(err, NotFound):
        current_app.logger.error(err, exc_info=True)
        flash_error(err)

    return render_template('index.html')


def configure_logging():
    formatter = AuthenticatedRequestFormatter(
        '[%(asctime)s] %(levelname)s account=%(group)s:%(user)s in %(module)s for %(url)s: %(message)s'
    )
    default_handler.setFormatter(formatter)