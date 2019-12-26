import json
from bson.objectid import ObjectId
from models.BusModel import JSONEncoder
from models.BusModel import BusModel


class RouteModel:
    uid = ""
    route_from = ""
    route_to = ""
    highway = ""
    bus_id = ""

    def __init__(self, uid, route_from, route_to, highway, bus_id):
        self.uid = uid
        self.route_from = route_from
        self.route_to = route_to
        self.highway = highway
        self.bus_id = bus_id

    def add(self):
        from app import db
        # validate bus id
        data = {
            "route_from": self.route_from,
            "route_to": self.route_to,
            "highway": self.highway,
            "bus_id": ObjectId(self.bus_id)
        }

        try:
            db.db.Route.insert_one(data)

            return "Successfully Inserted Route From: {} to: {}".format(self.route_from, self.route_to)

        except:
            return "Error while Adding Route From: {} to: {}".format(self.route_from, self.route_to)

    @staticmethod
    def delete(_id):
        from app import db

        try:
            db.db.Route.delete_one({
                "_id": ObjectId(_id)
            })

            return "Successfully Deleted Id: {}".format(_id)

        except:
            return "Error while deleting Id: {}".format(_id)

    @staticmethod
    def get_all_route():
        from app import db

        all_route = []
        try:
            routes = db.db.Route.find()

            for route in routes:
                data = RouteModel(
                    JSONEncoder().encode(route["_id"]),
                    route["route_from"],
                    route["route_to"],
                    route["highway"],
                    JSONEncoder().encode((route["bus_id"]))
                )

                all_route.append(data.__dict__)

            return all_route

        except:
            return "Error while Getting all routes"

    def update(self):
        from app import db

        data = {
            "route_from": self.route_from,
            "route_to": self.route_to,
            "highway": self.highway,
            "bus_id": self.bus_id
        }

        try:
            db.db.Route.update_one({
                "_id": self.uid
            },
                {
                "$set": data
            })

            return "Successfully Updated Route From: {} To: {}".format(self.route_from, self.route_to)

        except:
            return "Error while updating Route"

    @staticmethod
    def get_route_by_name(route_from, route_to, no_of_seats):
        from app import db

        selected_routes = []
        print("From: {} , To: {}".format(route_from, route_to))

        try:
            routes = db.db.Route.find({
                "route_from": route_from,
                "route_to": route_to
            })
            # access bus from bus_id
            # then compare available seats of bus with user's required seats
            # then only add data into selected_routes

            for route in routes:
                modeled_route = RouteModel(
                    JSONEncoder().encode(route["_id"]),
                    route["route_from"],
                    route["route_to"],
                    route["highway"],
                    JSONEncoder().encode(route["bus_id"])
                )

                bus = BusModel.get_single_bus(json.loads(modeled_route.bus_id))
                # print("Total Number of Seats Available for Bus: {} is :{}".format(
                #     bus["name"], bus["total_seats"]))
                bus = bus["data"]
                print(bus["total_seats"])

                if bus["total_seats"] >= no_of_seats:
                    selected_routes.append(modeled_route.__dict__)
                else:
                    print("Seats Is not available")

            return selected_routes

        except:
            return "Error while Searching For Routes"
