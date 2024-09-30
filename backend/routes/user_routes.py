from flask import Blueprint, request, jsonify, current_app
from models.models import db, User
from dataclasses import fields
from sqlalchemy.exc import IntegrityError
import logging
from pathlib import Path
import os

user_bp = Blueprint('user_bp', __name__)
logger = logging.getLogger()

MEDIA_FOLDER = os.path.join(os.getcwd(), 'static')
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)

# GET: Get all User
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    logger.info("Get All User")
    # current_app.logger.info("Get All User user")
    
    print(MEDIA_FOLDER)
    
    return jsonify(users)

# POST: Create a new user
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User()
    
    # Iterate over the fields of the User dataclass and assign values dynamically
    for field in fields(User):
        field_name = field.name
        if field_name in data:
            setattr(new_user, field_name, data[field_name])
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User creation failed, username may already exist'}), 400

# POST: Bulk insert users
@user_bp.route('/users/batch', methods=['POST'])
def batch_insert_users():
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid input. Expected a list of users.'}), 400

    users = []

    for user_data in data:
        new_user = User()

        # Iterate over the fields dynamically and set values from user_data
        for field in fields(User):
            field_name = field.name
            if field_name in user_data:
                setattr(new_user, field_name, user_data[field_name])

        users.append(new_user)

    try:
        # Bulk insert users using add_all for better performance
        db.session.add_all(users)
        db.session.commit()
        return jsonify({'message': f'{len(users)} users created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to insert users', 'error': str(e)}), 400

# GET: Retrieve a user by user_id
@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user)
    
# GET: Retrieve a user by username
@user_bp.route('/users/username/<username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user)

# PUT: Update an existing user by user_id
@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    # Iterate over the fields of the User dataclass and update the values
    for field in fields(User):
        field_name = field.name
        if field_name in data:
            setattr(user, field_name, data[field_name])
    
    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully', 'user_id': user.id}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Update failed, username may already exist'}), 400

# DELETE: Delete a user by user_id
@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# DELETE: Delete a user by pk
@user_bp.route('/users/pk/<pk>', methods=['DELETE'])
def delete_user_by_pk(pk):
    user = User.query.filter_by(pk=pk).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Endpoint untuk menghitung jumlah user
@user_bp.route('/api/count_users', methods=['GET'])
def count_users():
    try:
        user_count = User.query.count()
        return jsonify({"user_count": user_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500