from bson.objectid import ObjectId


class BlackList:
    jti = ""

    def __init__(self, jti):
        self.jti = jti

    def add_to_blacklist(self):
        from app import db
        try:
            db.db.BlackList.insert({
                "jti": self.jti
            })

            return "Successfully added to blacklist"

        except:
            return "Error while adding to blacklist"

    def filter_blacklist(self):
        from app import db
        try:
            res = db.db.BlackList.find_one({
                "jti": self.jti
            })

            return res

        except:
            return "Error while filtering black-list"
