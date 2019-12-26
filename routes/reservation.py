from flask_restful import Resource, reqparse
from models.reservationModel import ReservationModel
import json


class Reservation(Resource):
    def get(self):
        reservation = ReservationModel.get_all_reservation()

        return {
            "data": json.loads(json.dumps(reservation)),
            "message": "Success"
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "user_id",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "bus_id",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "departure_date",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "seats_number",
            type=list,
            location="json",
            required=True,
            help="Required Field"
        ),

        data = parser.parse_args()
        total_booked_seats = len(data["seats_number"])

        reservation_model = ReservationModel(0,
                                             data["user_id"],
                                             data["bus_id"],
                                             total_booked_seats,
                                             data["seats_number"],
                                             data["departure_date"]
                                             )

        result = reservation_model.addReservation()

        return {
            "message": result
        }

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "user_id",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "bus_id",
            type=str,
            required=True,
            help="Required Field"
        )

        data = parser.parse_args()
        reservation_id = ReservationModel.find_by_user_and_bus_id(
            data["user_id"], data["bus_id"])
        reservation_model = ReservationModel.delete_reservation(
            json.loads(reservation_id["id"]))
        return {
            "message": reservation_model
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
            "user_id",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "bus_id",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "departure_date",
            type=str,
            required=True,
            help="Required Field"
        ),
        parser.add_argument(
            "seats_number",
            type=list,
            location="json",
            required=True,
            help="Required Field"
        ),

        data = parser.parse_args()
        total_booked_seats = len(data["seats_number"])

        reservation_model = ReservationModel(
            data["_id"],
            data["user_id"],
            data["bus_id"],
            total_booked_seats,
            data["seats_number"],
            data["departure_date"]
        )

        result = reservation_model.update_reservation()

        return {
            "message": result
        }
