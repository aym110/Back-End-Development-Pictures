from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data)
    return {"message":"No data found"}
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture.get("id") == id:
                return jsonify(picture),200
    return {"message":"No data found"},404       



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    request_data = request.get_json()
    newId = request_data.get("id")
    if newId is not None:
        for picture in data:
            if picture.get("id") == newId:
                return {"Message": f"picture with id {picture['id']} already present"},302
        data.append(request_data)
        return jsonify(request_data),201
    else:
        return {"message":"error"},404

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    request_data = request.get_json()
    for picture in data:
        if picture.get("id") == id:
           picture.update(request_data)
    return {"message": "picture not found"},404
            
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture.get("id") == id:
            data.remove(picture)
            return "",204
    return {"message": "picture not found"},404
            
