from flask import Blueprint, request, jsonify
from models.models import db, Follower
from dataclasses import fields
from sqlalchemy.exc import IntegrityError

follower_bp = Blueprint('follower_bp', __name__)

# GET: Get all Follower
@follower_bp.route('/followers', methods=['GET'])
def get_followers():
    bl = Follower.query.all()
    return jsonify(bl)

# POST: Create a new Follower
@follower_bp.route('/followers', methods=['POST'])
def create_followers():
    data = request.json
    new_fl = Follower()
    
    # Iterate over the fields of the User dataclass and assign values dynamically
    for field in fields(Follower):
        field_name = field.name
        if field_name in data:
            setattr(new_fl, field_name, data[field_name])
            
    try:
        db.session.add(new_fl)
        db.session.commit()
        return jsonify({'message': 'Followers created successfully', 'id': new_fl.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Followers creation failed.'}), 400

# GET: Retrieve a followers by id
@follower_bp.route('/followers/<int:followers_id>', methods=['GET'])
def get_follower(followers_id):
    bl = Follower.query.get_or_404(followers_id)
    return jsonify(bl)
    
# GET: Retrieve a followers by user Pk
@follower_bp.route('/followers/user_pk/<string:pk>', methods=['GET'])
def get_followers_by_user_pk(pk):
    bl = Follower.query.filter_by(pk_user=pk).first_or_404()
    return jsonify(bl)

# DELETE: Delete a followers by id
@follower_bp.route('/followers/<int:followers_id>', methods=['DELETE'])
def delete_followers(followers_id):
    bl = Follower.query.get_or_404(followers_id)
    db.session.delete(bl)
    db.session.commit()
    return jsonify({'message': 'Followers deleted successfully'}), 200

# DELETE: Delete a Follower by User pk
@follower_bp.route('/followers/user_pk/<string:pk>', methods=['DELETE'])
def delete_follower_by_pk(pk):
    bl = Follower.query.filter_by(pk_user=pk).first_or_404()
    db.session.delete(bl)
    db.session.commit()
    return jsonify({'message': 'Followers deleted successfully'}), 200
