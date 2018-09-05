# -*- coding: utf-8 -*-
from Linjia import create_app
app = create_app()


@app.route('/')
def test():
    app.logger.error('sdfjlk')
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
