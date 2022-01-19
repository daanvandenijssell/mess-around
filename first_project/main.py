from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# init api
api = Api(app)
# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# init db
db = SQLAlchemy(app)


class Beleggingsfondsen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    rate = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Fonds (fonds_id: {self.id}, naam: {self.name}, rate: {self.rate})"


# db.create_all()

beleggingsfonds_put_args = reqparse.RequestParser()
beleggingsfonds_put_args.add_argument("name",
                                      type=str,
                                      help="Naam van het fonds ontbreekt",
                                      required=True)
beleggingsfonds_put_args.add_argument("rate",
                                      type=int,
                                      help="Score van het fonds ontbreekt",
                                      required=True)

beleggingsfonds_patch_args = reqparse.RequestParser()
beleggingsfonds_patch_args.add_argument("name",
                                        type=str,
                                        help="Naam van het fonds ontbreekt")
beleggingsfonds_patch_args.add_argument("rate",
                                        type=int,
                                        help="Score van het fonds ontbreekt")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "rate": fields.Integer
}


class Beleggingsfonds(Resource):
    @marshal_with(resource_fields)
    def get(self, fonds_id):
        result = Beleggingsfondsen.query.filter_by(id=fonds_id)
        if not result:
            abort(404, message="Geen beleggingsfonds gevonden")
        return result

    @marshal_with(resource_fields)
    def put(self, fonds_id):
        args = beleggingsfonds_put_args.parse_args()
        result = Beleggingsfondsen.query.filter_by(id=fonds_id).first()
        if result:
            abort(409, message="Fonds bestaat al...")

        beleggingsfonds = Beleggingsfondsen(id=fonds_id,
                                            name=args["name"],
                                            rate=args["rate"])
        db.session.add(beleggingsfonds)
        db.session.commit()
        return beleggingsfonds, 201

    @marshal_with(resource_fields)
    def patch(self, fonds_id):
        args = beleggingsfonds_patch_args.parse_args()
        result = Beleggingsfondsen.query.filter_by(id=fonds_id).first()
        if not result:
            abort(404, message="Beleggingsfonds ID bestaat niet")

        if args["name"]:
            result.name = args["name"]
        if args["rate"]:
            result.rate = args["rate"]

        db.session.commit()

        return result


api.add_resource(Beleggingsfonds, "/beleggingfonds/<int:fonds_id>")


@app.route("/kots", methods=["GET"])
def full_db():
    beleggingsfondsen = db.Table("beleggingsfondsen",
                                 db.metadata,
                                 autoload=True,
                                 autoload_method=db.engine)
    return jsonify(
        {"Belleginsfondsen": db.session.query(beleggingsfondsen).all()})


@app.route("/")
@app.route("/beleggingsfonds")
def hello_chicken():
    return "Hello you Chicken...."


if __name__ == "__main__":
    app.run(debug=True)
