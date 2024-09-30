from flask import Blueprint, request, jsonify
from models.models import db, Post, PostTag
from dataclasses import fields
from sqlalchemy.exc import IntegrityError
from flask import send_from_directory
import os

post_bp = Blueprint('post_bp', __name__)
post_tag_bp = Blueprint('post_tag_bp', __name__)

# GET: Get all Posts
@post_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify(posts)

# POST: Create a new Post and Tag
@post_bp.route('/posts', methods=['POST'])
def create_posts():
    data = request.json
    new_post = Post()
    post_tags_data = data.pop('post_tag', [])
    
    # Iterate over the fields of the User dataclass and assign values dynamically
    for field in fields(Post):
        field_name = field.name
        if field_name in data:
            setattr(new_post, field_name, data[field_name])

    # Create PostTag objects from the post_tag array
    for tag in post_tags_data:
        new_post.post_tags.append(PostTag(
            pk= tag['pk'],
            user_pk= tag['user_pk'],
            media_pk= tag['media_pk'],
            username= tag['username'],
            full_name= tag['full_name'],
            is_private= tag['is_private'],
            profile_pic_url= tag['profile_pic_url'],
            profile_pic_url_hd= tag['profile_pic_url_hd']
        ))
            
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully', 'id': new_post.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Post creation failed.'}), 400

# GET: Retrieve a Post by id
@post_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return jsonify(post)

# GET: Retrieve a Post by user Pk
@post_bp.route('/posts/by_user_pk/<pk>', methods=['GET'])
def get_posts_by_user_pk(pk):
    posts = Post.query.filter_by(user_pk=pk).all()
    return jsonify(posts)

# DELETE: Delete a Post by User pk
@post_bp.route('/posts/by_user_pk/<pk>', methods=['DELETE'])
def delete_posts_by_pk(pk):
    post = Post.query.filter_by(user_pk=pk).first_or_404()
    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete post', 'error': str(e)}), 400

# GET: Get all Posts Tag
@post_bp.route('/post_tags', methods=['GET'])
def get_post_tags():
    post_tags = PostTag.query.all()
    return jsonify(post_tags)

# GET: Retrieve a Post Tag by id
@post_bp.route('/post_tags/<post_tag_id>', methods=['GET'])
def get_post_tag(post_tag_id):
    post = Post.query.get_or_404(post_tag_id)
    return jsonify(post)

# GET: Retrieve a Post Tag by Post ID
@post_bp.route('/post_tags/by_post_id/<post_id>', methods=['GET'])
def get_post_tags_by_post_id(post_id):
    post_tags = PostTag.query.filter_by(post_id=post_id).all()
    return jsonify(post_tags)

# GET: Retrieve a Post Tag by user Pk
@post_bp.route('/post_tags/by_user_pk/<pk>', methods=['GET'])
def get_post_tags_by_user_pk(pk):
    post_tags = PostTag.query.filter_by(user_pk=pk).all()
    return jsonify(post_tags)

# GET : path image
@post_bp.route('/profile_img/<path:filename>')
def media_files_profiles(filename):
    MEDIA_FOLDER = os.path.join(os.getcwd(), 'static/profiles')
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
        
    return send_from_directory(MEDIA_FOLDER, filename)

# GET : path image
@post_bp.route('/post_img/<path:filename>')
def media_files_posts(filename):
    MEDIA_FOLDER = os.path.join(os.getcwd(), 'static/posts')
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
        
    return send_from_directory(MEDIA_FOLDER, filename)

# GET : path image
@post_bp.route('/post_tag_img/<path:filename>')
def media_files_post_tags(filename):
    MEDIA_FOLDER = os.path.join(os.getcwd(), 'static/post_tags')
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
        
    return send_from_directory(MEDIA_FOLDER, filename)

# GET : path image
@post_bp.route('/story_img/<path:filename>')
def media_files_stories(filename):
    MEDIA_FOLDER = os.path.join(os.getcwd(), 'static/stories')
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
        
    return send_from_directory(MEDIA_FOLDER, filename)

# GET : path image
@post_bp.route('/story_mention_img/<path:filename>')
def media_files_story_mentions(filename):
    MEDIA_FOLDER = os.path.join(os.getcwd(), 'static/story_mentions')
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
        
    return send_from_directory(MEDIA_FOLDER, filename)

# Endpoint untuk menghitung jumlah post
@post_bp.route('/api/count_posts', methods=['GET'])
def count_posts():
    try:
        post_count = Post.query.count()
        return jsonify({"post_count": post_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500