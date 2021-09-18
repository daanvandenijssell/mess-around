import sys

# print(sys.executable)
# print(sys.version)

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Helloworld(Resource):
    def get(self, name):
        return {"Data": name}


api.add_resource(Helloworld, "/Helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
