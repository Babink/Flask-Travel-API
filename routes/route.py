from flask_restful import Resource, reqparse
from models.RouteModel import RouteModel
import json


class Route(Resource):
    def get(self):
        route = RouteModel.get_all_route()

        return {
            "message": "Success",
            "data": json.loads(json.dumps(route))
        }

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument(
            "from",
            required=True,
            type=str,
            help="Required Field"
        ),
        parse.add_argument(
            "to",
            required=True,
            type=str,
            help="Required Field"
        ),
        parse.add_argument(
            "highway",
            required=True,
            type=str,
            help="Required Field"
        ),
        parse.add_argument(
            "bus_id",
            required=True,
            type=str,
            help="Required Field"
        )

        data = parse.parse_args()

        route_model = RouteModel(
            0,
            data["from"].lower(),
            data["to"].lower(),
            data["highway"],
            data["bus_id"]
        )

        result = route_model.add()
        return {
            "result": result
        }

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "_id",
            required=True,
            type=str,
            help="Required Field"
        )

        data = parser.parse_args()

        result = RouteModel.delete(data["_id"])
        return {
            "result": result
        }

    def patch(self):
        parse = reqparse.RequestParser()
        parse.add_argument(
            "_id",
            required=True,
            type=str,
            help="Required Field"
        ),
        parse.add_argument(
            "from",
            required=True,
            type=str,
            help="Required Field"
        ),
        parse.add_argument(
            "to",
            required=True,
            type=str,
            help="Required Field"
        ),
        parse.add_argument(
            "highway",
            required=True,
            type=str,
            help="Required Field"
        ),
        parse.add_argument(
            "bus_id",
            required=True,
            type=str,
            help="Required Field"
        )

        data = parse.parse_args()

        route_model = RouteModel(
            data["_id"],
            data["from"].lower(),
            data["to"].lower(),
            data["highway"],
            data["bus_id"]
        )

        result = route_model.update()

        return {
            "result": result
        }

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "from",
            required=True,
            type=str,
            help="Required Field"
        ),
        parser.add_argument(
            "to",
            required=True,
            type=str,
            help="Required Field"
        ),
        parser.add_argument(
            "No_of_seats",
            required=False,
            type=int,
            help="Required Field"
        )

        data = parser.parse_args()

        result = RouteModel.get_route_by_name(
            data["from"].lower(), data["to"].lower() , data["No_of_seats"])

        return {
            "result": json.loads(json.dumps(result))
        }
