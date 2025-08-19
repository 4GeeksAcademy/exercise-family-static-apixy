"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# === Endpoints ===

# GET all members
@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(jackson_family.get_all_members()), 200

# GET single member by id
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404
    return jsonify(member), 200

# POST create member
@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json(silent=True) or {}
    if "first_name" not in body or "age" not in body:
        return jsonify({"msg": "first_name and age are required"}), 400
    try:
        age = int(body["age"])
        if age <= 0:
            raise ValueError()
    except Exception:
        return jsonify({"msg": "age must be an integer > 0"}), 400
    lucky = body.get("lucky_numbers", [])
    if not isinstance(lucky, list):
        return jsonify({"msg": "lucky_numbers must be a list"}), 400
    new_member = jackson_family.add_member({
        "id": body.get("id"),
        "first_name": body["first_name"],
        "last_name": body.get("last_name", jackson_family.last_name),
        "age": age,
        "lucky_numbers": lucky,
    })
    return jsonify(new_member), 201

# DELETE member by id
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if not jackson_family.delete_member(member_id):
        return jsonify({"msg": "Member not found"}), 404
    return jsonify({"done": True}), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
