import traceback
from flask import Flask, request
from flask_cors import CORS
from com.taxicoop.service.DBHelper import Database,UserModel



app = Flask(__name__)
CORS(app)

service = UserModel()

mandatory_new_user_request_fields = {'_id', 'name', "email", 'contact_info'}


# Get all users
@app.route("/api/users/v1", methods=["GET"])
def get_all_Users():
    return service.get_all_Users()

# Get Specific user by UserID
@app.route("/api/users/v1/<string:email>", methods=["GET"])
def get_specific_User(email):
    return service.find_by_username(email)

# add a new User
@app.route("/api/users/v1/register", methods=["POST"])
def register_User(name, email, contact_info):
    data = request.json

    if not mandatory_new_user_request_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_new_user_request_fields)
    else:
        try:

            service.insert_user(name, email, contact_info)
            return "Successfully registered the user"
        except Exception as e:
            traceback.print_exc()
            return "Failed to register User. Error {}".format(e.__cause__)




# Please review this part of the code.. for DB
# listening on port 8085.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)