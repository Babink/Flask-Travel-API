import json
from bson.objectid import ObjectId
from models.BusModel import BusModel
from models.BusModel import JSONEncoder


class ReservationModel:
    uid = ''
    user_id = ""
    bus_id = ""
    total_booked = ""
    seats_number = ""
    departure_date = ""

    def __init__(self, uid, user_id, bus_id, total_booked, seats_number, departure_date):
        self.uid = uid
        self.user_id = user_id
        self.bus_id = bus_id
        self.total_booked = total_booked
        self.seats_number = seats_number
        self.departure_date = departure_date

    def addReservation(self):
        from app import db
        print("Total Seats Booked: {} for User: {} at Time: {}".format(
            self.total_booked, self.user_id, self.departure_date))
        single_bus = BusModel.get_single_bus(self.bus_id)
        single_bus = single_bus["data"]
        bus_model = BusModel(json.loads(single_bus["uid"]),
                             single_bus["name"],
                             single_bus["company"],
                             single_bus["bus_number"],
                             single_bus["bus_contact"],
                             single_bus["bus_image"],
                             single_bus["bus_image_1"],
                             single_bus["bus_image_2"],
                             single_bus["lux_type"],
                             single_bus["total_seats"] - self.total_booked,
                             single_bus["bus_description"],
                             single_bus["amenities"]
                             )

        try:
            data = {
                "user_id": self.user_id,
                "bus_id": self.bus_id,
                "total_booked": self.total_booked,
                "seats_number": self.seats_number,
                "departure_date": self.departure_date
            }

            print(data)
            bus_model.update()
            db.db.Reservation.insert_one(data)

            return "Successfully Reserved Seats: {} of Bus: {} for Date: {}".format(self.total_booked, bus_model.name, self.departure_date)

        except:
            return "Error While Reserving Ticket"

    @staticmethod
    def get_all_reservation():
        from app import db
        all_reservation = []

        try:
            data = db.db.Reservation.find()

            for docs in data:
                reservation_model = ReservationModel(
                    JSONEncoder().encode(docs["_id"]),
                    docs["user_id"],
                    docs["bus_id"],
                    docs["total_booked"],
                    docs["seats_number"],
                    docs["departure_date"]
                )

                all_reservation.append(reservation_model.__dict__)

            return all_reservation

        except:
            return "Error while Getting All reservation"

    @staticmethod
    def find_by_user_and_bus_id(user_id, bus_id):
        from app import db

        try:
            result = db.db.Reservation.find_one({
                "user_id": user_id,
                "bus_id": bus_id
            })

            reservation_id = JSONEncoder().encode(result["_id"])

            return {
                "message": "Successfully getted Reservation Id",
                "id": reservation_id
            }
        except:
            return "Error while accessing Reservation Id"

    @staticmethod
    def delete_reservation(uid):
        from app import db

        try:
            db.db.Reservation.delete_one({
                "_id": ObjectId(uid)
            })

            return "Successfully deleted Reservation"

        except:
            return "Error while deleting reservation"

    def update_reservation(self):
        from app import db

        data = {
            "user_id": self.user_id,
            "bus_id": self.bus_id,
            "total_booked": self.total_booked,
            "seats_number": self.seats_number,
            "departure_date": self.departure_date
        }

        try:
            db.db.Reservation.update_one({
                "_id": ObjectId(self.uid)
            },  {
                "$set": data
            })

            return "Successfully Updated Reservation for: {}".format(data["departure_date"])

        except:
            return "Error while updating Reservation"
