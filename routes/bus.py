from flask_restful import Resource, reqparse
from models.BusModel import BusModel
import json


class Bus(Resource):
    def get(self):
        buses = BusModel.get_all_bus()

        return {
            "message": "Success",
            "bus": json.loads(json.dumps(buses))
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "company",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "bus_number",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "bus_contact",
            type=int,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "total_seats",
            type=int,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "lux_type",
            type=int,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "image_url",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "image_url-1",
            type=str,
            required=False
        ),
        parser.add_argument(
            "image_url-2",
            type=str,
            required=False
        ),
        parser.add_argument(
            "bus_description",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "amenities",
            type=dict,
            location="json",
            required=True,
            help="Required Field"
        )

        data = parser.parse_args()
        bus_model = BusModel(
            0,
            data["name"],
            data["company"],
            data["bus_number"],
            data["bus_contact"],
            data["image_url"],
            data["image_url-1"],
            data["image_url-2"],
            data["lux_type"],
            data["total_seats"],
            data["bus_description"],
            data["amenities"]
        )

        result = bus_model.insert()

        return {
            "result": result
        }

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "_id",
            type=str,
            required=True,
            help="Required Field"
        )
        data = parser.parse_args()
        uid = data["_id"]

        result = BusModel.delete(uid)

        return {
            "message": result
        }

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "_id",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "name",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "company",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "bus_number",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "bus_contact",
            type=int,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "total_seats",
            type=int,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "lux_type",
            type=int,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "image_url",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "image_url-1",
            type=str,
            required=False
        ),
        parser.add_argument(
            "image_url-2",
            type=str,
            required=False
        ),
        parser.add_argument(
            "bus_description",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "amenities",
            # type=object,
            required=True,
            help="Required Field"
        )

        data = parser.parse_args()
        bus_model = BusModel(
            data["_id"],
            data["name"],
            data["company"],
            data["bus_number"],
            data["bus_contact"],
            data["image_url"],
            data["image_url-1"],
            data["image_url-2"],
            data["lux_type"],
            data["total_seats"],
            data["bus_description"],
            data["amenities"]
        )

        result = bus_model.update()

        return {
            "message": result
        }

    def put(self):
        # Get Single Bus
        parser = reqparse.RequestParser()
        parser.add_argument(
            "_id",
            required=True,
            type=str,
            help="Required Field"
        )

        data = parser.parse_args()

        result = BusModel.get_single_bus(data["_id"])

        return {
            "result": result
        }
