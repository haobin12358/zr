# -*- coding: utf-8 -*-
import logging


from Linjia import create_app
app = create_app()


@app.route('/test')
def default_route():
    return 'hello'


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    app.run()
