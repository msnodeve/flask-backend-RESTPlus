"""
    app init
"""

from flask import Flask

def create_app() -> (Flask):
    """ create_app() 함수를 호출해 앱을 초기화 """
    app = Flask(__name__)
    app.app_context().push()

    @app.route("/")
    def index():
        """ / url index """
        return "<h1>Hello World ! <br> This is index page</h1>"
    
    return app