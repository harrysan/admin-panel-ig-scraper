from flask import Blueprint, request, jsonify
from models.models import db, Following
from dataclasses import fields
from sqlalchemy.exc import IntegrityError

following_bp = Blueprint('following_bp', __name__)

# GET: Get all Following
@following_bp.route('/followings', methods=['GET'])
def get_followings():
    bl = Following.query.all()
    return jsonify(bl)

# POST: Create a new Following
@following_bp.route('/followings', methods=['POST'])
def create_followers():
    data = request.json
    new_fl = Following()
    
    # Iterate over the fields of the User dataclass and assign values dynamically
    for field in fields(Following):
        field_name = field.name
        if field_name in data:
            setattr(new_fl, field_name, data[field_name])
            
    try:
        db.session.add(new_fl)
        db.session.commit()
        return jsonify({'message': 'Followings created successfully', 'id': new_fl.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Followings creation failed.'}), 400

# GET: Retrieve a followers by id
@following_bp.route('/followings/<int:followings_id>', methods=['GET'])
def get_following(followings_id):
    bl = Following.query.get_or_404(followings_id)
    return jsonify(bl)
    
# GET: Retrieve a followers by user Pk
@following_bp.route('/followings/user_pk/<string:pk>', methods=['GET'])
def get_followings_by_user_pk(pk):
    bl = Following.query.filter_by(pk_user=pk).first_or_404()
    return jsonify(bl)

# DELETE: Delete a followers by id
@following_bp.route('/followings/<int:followings_id>', methods=['DELETE'])
def delete_followings(followings_id):
    bl = Following.query.get_or_404(followings_id)
    db.session.delete(bl)
    db.session.commit()
    return jsonify({'message': 'Following deleted successfully'}), 200

# DELETE: Delete a Following by User pk
@following_bp.route('/followings/user_pk/<string:pk>', methods=['DELETE'])
def delete_following_by_pk(pk):
    bl = Following.query.filter_by(pk_user=pk).first_or_404()
    db.session.delete(bl)
    db.session.commit()
    return jsonify({'message': 'Following deleted successfully'}), 200

