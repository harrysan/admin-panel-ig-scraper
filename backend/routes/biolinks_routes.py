from flask import Blueprint, request, jsonify
from models.models import db, BioLinks
from dataclasses import fields
from sqlalchemy.exc import IntegrityError

biolinks_bp = Blueprint('biolinks_bp', __name__)

# GET: Get all BioLinks
@biolinks_bp.route('/biolinks', methods=['GET'])
def get_biolinks():
    bl = BioLinks.query.all()
    return jsonify(bl)

# POST: Create a new BioLinks
@biolinks_bp.route('/biolinks', methods=['POST'])
def create_biolinks():
    data = request.json
    new_bl = BioLinks()
    
    # Iterate over the fields of the User dataclass and assign values dynamically
    for field in fields(BioLinks):
        field_name = field.name
        if field_name in data:
            setattr(new_bl, field_name, data[field_name])
            
    try:
        db.session.add(new_bl)
        db.session.commit()
        return jsonify({'message': 'BioLinks created successfully', 'id': new_bl.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'BioLinks creation failed.'}), 400

# GET: Retrieve a BioLinks by id
@biolinks_bp.route('/biolinks/<int:biolinks_id>', methods=['GET'])
def get_biolink(biolinks_id):
    bl = BioLinks.query.get_or_404(biolinks_id)
    return jsonify(bl)
    
# GET: Retrieve a BioLinks by user Pk
@biolinks_bp.route('/biolinks/user_pk/<string:pk>', methods=['GET'])
def get_biolinks_by_user_pk(pk):
    bl = BioLinks.query.filter_by(pk_user=pk).first_or_404()
    return jsonify(bl)

# DELETE: Delete a BioLinks by id
@biolinks_bp.route('/biolinks/<int:biolinks_id>', methods=['DELETE'])
def delete_biolink(biolinks_id):
    bl = BioLinks.query.get_or_404(biolinks_id)
    db.session.delete(bl)
    db.session.commit()
    return jsonify({'message': 'BioLink deleted successfully'}), 200

# DELETE: Delete a BioLinks by User pk
@biolinks_bp.route('/biolinks/user_pk/<string:pk>', methods=['DELETE'])
def delete_user_by_pk(pk):
    bl = BioLinks.query.filter_by(pk_user=pk).first_or_404()
    db.session.delete(bl)
    db.session.commit()
    return jsonify({'message': 'BioLink deleted successfully'}), 200