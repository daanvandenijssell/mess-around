from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Beleggingsfondsen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    rate = db.Column(db.Integer, nullable=False)

    # def __repr__(self):
    #     return f"Fonds (naam: {name}, rate: {rate})"


# db.create_all()

beleggingsfonds_put_args = reqparse.RequestParser()
beleggingsfonds_put_args.add_argument(
    "name", type=str, help="Naam van het fonds ontbreekt", required=True
)
beleggingsfonds_put_args.add_argument(
    "rate", type=int, help="Score van het fonds ontbreekt", required=True
)

beleggingsfonds_patch_args = reqparse.RequestParser()
beleggingsfonds_patch_args.add_argument(
    "name", type=str, help="Naam van het fonds ontbreekt"
)
beleggingsfonds_patch_args.add_argument(
    "rate", type=int, help="Score van het fonds ontbreekt"
)

resource_fields = {"id": fields.Integer, "name": fields.String, "rate": fields.Integer}


class Beleggingsfonds(Resource):
    @marshal_with(resource_fields)
    def get(self, fonds_id):
        result = Beleggingsfondsen.query.fidlter_by(id=fonds_id).first()
        if not result:
            abort(404, message="Geen beleggingsfonds gevonden")
        return result

    @marshal_with(resource_fields)
    def put(self, fonds_id):
        args = beleggingsfonds_put_args.parse_args()
        result = Beleggingsfondsen.query.filter_by(id=fonds_id).first()
        if result:
            abort(409, message="Fonds bestaat al...")

        beleggingsfonds = Beleggingsfondsen(
            id=fonds_id, name=args["name"], rate=args["rate"]
        )
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

if __name__ == "__main__":
    app.run(debug=True)
