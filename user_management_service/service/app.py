import traceback
from flask import Flask, request
from flask_cors import CORS
from com.taxicoop.service.user_service import UserService

app = Flask(__name__)
CORS(app)

service = UserService()

mandatory_new_user_request_fields = {'name', "email", 'contact_info'}

updatable_user_fields = {'name', 'contact_info', 'status'}


# Get all users
@app.route("/api/users/v1", methods=["GET"])
def get_all_users():
    return service.get_all_Users()


# Get Specific user by UserID
@app.route("/api/users/v1/<string:email>", methods=["GET"])
def get_specific_user(email):
    return service.find_by_email(email)


# add a new User
@app.route("/api/users/v1/register", methods=["POST"])
def register_user():
    data = request.json

    if not mandatory_new_user_request_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_new_user_request_fields)
    else:
        try:
            service.insert_user(name=data['name'], email=data['email'], contact_info=data['contact_info'])
            return "Successfully registered the user"
        except Exception as e:
            traceback.print_exc()
            return "Failed to register User. Error {}".format(e.__cause__)


## Update user  data
@app.route("/api/users/v1/<string:email>", methods=["PATCH"])
def update_user(email):
    data = request.json

    payload = {'email': email}
    for key in updatable_user_fields:
        if key in data.keys():
            payload[key] = data[key]

    return service.update_user(payload)


# Please review this part of the code.. for DB
# listening on port 8085.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
