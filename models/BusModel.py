import json
from bson.objectid import ObjectId


class BusModel:
    uid = ""
    name = ''
    company = ''
    bus_number = ''
    bus_contact = ''
    bus_image = ''
    bus_image_1 = ''
    bus_image_2 = ''
    lux_type = ''
    total_seats = ''
    bus_description = ""
    amenities = ''

    def __init__(self,
                 uid,
                 name,
                 company,
                 bus_number,
                 bus_contact,
                 bus_image,
                 bus_image_1,
                 bus_image_2,
                 lux_type,
                 total_seats,
                 bus_description,
                 amenities
                 ):
        self.uid = uid
        self.name = name
        self.company = company
        self.bus_number = bus_number
        self.bus_contact = bus_contact
        self.bus_image = bus_image
        self.bus_image_1 = bus_image_1
        self.bus_image_2 = bus_image_2
        self.lux_type = lux_type
        self.total_seats = total_seats
        self.bus_description = bus_description
        self.amenities = amenities

    @staticmethod
    def get_single_bus(_id):
        from app import db

        try:
            data = db.db.Bus.find_one({
                "_id": ObjectId(_id)
            })

            bus_model = BusModel(
                JSONEncoder().encode(data["_id"]),
                data["name"],
                data["company"],
                data["bus_number"],
                data["bus_contact"],
                data["bus_image"],
                data["bus_image_1"],
                data["bus_image_2"],
                data["lux_type"],
                data["total_seats"],
                data["bus_description"],
                data["amenities"]
            )

            return {
                "message": "Success",
                "data": bus_model.__dict__
            }

        except:
            return "Error while finding Bus"

    @staticmethod
    def get_all_bus():
        from app import db

        m_all_bus = []
        data = db.db.Bus.find()

        for docs in data:
            print("This Bus: {} is Owned By Company: {}".format(
                docs["name"], docs["company"]))

            m_data = BusModel(
                JSONEncoder().encode(docs["_id"]),
                docs["name"],
                docs["company"],
                docs["bus_number"],
                docs["bus_contact"],
                docs["bus_image"],
                docs["bus_image_1"],
                docs["bus_image_2"],
                docs["lux_type"],
                docs["total_seats"],
                docs["bus_description"],
                docs["amenities"]
            )

            m_all_bus.append(m_data.__dict__)

        if len(m_all_bus) >= 1:
            return m_all_bus
        else:
            return "No Bus Data available"

    def insert(self):
        from app import db

        data = {
            "name": self.name,
            "company": self.company,
            "bus_number": self.bus_number,
            "bus_contact": self.bus_contact,
            "bus_image": self.bus_image,
            "bus_image_1": self.bus_image_1,
            "bus_image_2": self.bus_image_2,
            "lux_type": self.lux_type,
            "total_seats": self.total_seats,
            "bus_description": self.bus_description,
            "amenities": self.amenities
        }

        try:
            res = db.db.Bus.insert_one(data)
            return "Successfully Inserted"
        except:
            return "Error while adding into database"

    @staticmethod
    def delete(_id):
        from app import db
        try:
            db.db.Bus.delete_one({
                "_id": ObjectId(_id)
            })
            return "Successfully deleted Bus {}".format(_id)

        except:
            return "Error while deleted by {}".format(_id)

    def update(self):
        from app import db
        data = {
            "name": self.name,
            "company": self.company,
            "bus_number": self.bus_number,
            "bus_contact": self.bus_contact,
            "bus_image": self.bus_image,
            "bus_image_1": self.bus_image_1,
            "bus_image_2": self.bus_image_2,
            "lux_type": self.lux_type,
            "total_seats": self.total_seats,
            "bus_description": self.bus_description,
            "amenities": self.amenities
        }

        try:
            print(data)
            db.db.Bus.update_one(
                filter={
                    "_id": ObjectId(self.uid),
                },
                update={
                    "$set": data
                }
            )

            return "Successfully updated Bus: {}".format(self.uid)

        except:
            return "Error while updating Bus: {}".format(self.uid)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
