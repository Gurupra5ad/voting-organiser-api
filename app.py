from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
# from api_constants import mongodb_password

app = Flask(__name__)

database_name = "API"
DB_URI = "mongodb+srv://guruprasad:SCaxg0y8vQTCVXrh@cluster0.sne4s.mongodb.net/API?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

class Voter(db.Document):
    voter_id = db.IntField()
    name = db.StringField()
    age = db.IntField()

    def to_json(self):
        return {
            "voter_id":self.voter_id,
            "name":self.name,
            "age":self.age,
        }

@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    voter1 = Voter(voter_id = 1, name = "Guru", age = 20)
    voter2 = Voter(voter_id = 2, name = "Nitiessh", age = 20)
    voter1.save()
    voter2.save()
    return make_response("", 201)


@app.route('/api/voters', methods=['GET', 'POST'])
def api_voters():
    if request.method == "GET":
        voters =[]
        for voter in Voter.objects:
            voters.append(voter)
        return make_response(jsonify(voters), 200)

    elif request.method == "POST":
        voting = request.json
        voter = Voter(voter_id=voting['voter_id'], name=voting['name'], age=voting['age'])
        voter.save()
        return make_response("", 201)

@app.route('/api/voters/<voter_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_voter(voter_id):
    if request.method == "GET":
        voter_obj = Voter.objects(voter_id=voter_id).first()
        if voter_obj:
            return make_response(jsonify(voter_obj.to_json()), 200)
        else:
            return make_response("", 404)

    elif request.method == "PUT":
        voting = request.json
        voter_obj = Voter.objects(voter_id = voter_id).first()
        voter_obj.update(name=voting['name'], age=voting['age'])
        return make_response("", 204)

    elif request.method == "DELETE":
        voter_obj = Voter.objects(voter_id = voter_id).first()
        voter_obj.delete()
        return make_response("", 204)





if __name__ == '__main__':
    app.run(debug=True)


# SCaxg0y8vQTCVXrh - pass for database access
