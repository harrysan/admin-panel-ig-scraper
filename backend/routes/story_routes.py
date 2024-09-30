from flask import Blueprint, request, jsonify
from models.models import db, Story, StoryMention
from dataclasses import fields
from sqlalchemy.exc import IntegrityError

story_bp = Blueprint('story_bp', __name__)

# GET: Get all Story
@story_bp.route('/stories', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    return jsonify(stories)

# POST: Create a new Story and Mention
@story_bp.route('/stories', methods=['POST'])
def create_stories():
    data = request.json
    new_story = Story()
    story_mentions_data = data.pop('story_mention', [])
    
    # Iterate over the fields of the User dataclass and assign values dynamically
    for field in fields(Story):
        field_name = field.name
        if field_name in data:
            setattr(new_story, field_name, data[field_name])

    # Create PostTag objects from the post_tag array
    for tag in story_mentions_data:
        new_story.story_mentions.append(StoryMention(
            pk= tag['pk'],
            user_pk= tag['user_pk'],
            story_pk= tag['story_pk'],
            username= tag['username'],
            full_name= tag['full_name'],
            is_private= tag['is_private'],
            profile_pic_url= tag['profile_pic_url'],
            profile_pic_url_hd= tag['profile_pic_url_hd']
        ))
            
    try:
        db.session.add(new_story)
        db.session.commit()
        return jsonify({'message': 'Story created successfully', 'id': new_story.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Story creation failed.'}), 400

# GET: Retrieve a Post by id
@story_bp.route('/stories/<story_id>', methods=['GET'])
def get_story(story_id):
    story = Story.query.get_or_404(story_id)
    return jsonify(story)

# GET: Retrieve a Post by user Pk
@story_bp.route('/stories/by_user_pk/<pk>', methods=['GET'])
def get_stories_by_user_pk(pk):
    stories = Story.query.filter_by(user_pk=pk).all()
    return jsonify(stories)

# DELETE: Delete a Post by User pk
@story_bp.route('/stories/by_user_pk/<pk>', methods=['DELETE'])
def delete_stories_by_pk(pk):
    story = Story.query.filter_by(user_pk=pk).first_or_404()
    try:
        db.session.delete(story)
        db.session.commit()
        return jsonify({'message': 'Story deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete story', 'error': str(e)}), 400

# GET: Get all Story Mention
@story_bp.route('/story_mentions', methods=['GET'])
def get_story_mentions():
    story_mentions = StoryMention.query.all()
    return jsonify(story_mentions)

# GET: Retrieve a Story Mentions by id
@story_bp.route('/story_mentions/<story_mention_id>', methods=['GET'])
def get_story_mention(story_mention_id):
    story_mention = StoryMention.query.get_or_404(story_mention_id)
    return jsonify(story_mention)

# GET: Retrieve a Story Mention by Story ID
@story_bp.route('/story_mentions/by_story_id/<story_id>', methods=['GET'])
def get_story_mentions_by_story_id(story_id):
    story_mentions = StoryMention.query.filter_by(story_id=story_id).all()
    return jsonify(story_mentions)

# GET: Retrieve a Post Tag by user Pk
@story_bp.route('/story_mentions/user_pk/<pk>', methods=['GET'])
def get_story_mentions_by_user_pk(pk):
    story_mentions = StoryMention.query.filter_by(user_pk=pk).all()
    return jsonify(story_mentions)

# Endpoint untuk menghitung jumlah story
@story_bp.route('/api/count_stories', methods=['GET'])
def count_stories():
    try:
        story_count = Story.query.count()
        return jsonify({"story_count": story_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500