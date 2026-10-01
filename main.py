from flask import Flask, render_template
from flasgger import Swagger
from immaculate_api import create_app

#creates a flask app to be loaded locally when running program
app = create_app()
swagger = Swagger(app)

if __name__ == "__main__":
    app.run()


# TODO FIGURE OUT WHAT PACKAGE IS MISSING FOR INTERACTIVEINTERPRETER