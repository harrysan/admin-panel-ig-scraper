import unittest
from flask_testing import TestCase
from app import app, db
from models.models import User, Post, Story
from faker import Faker

fake = Faker()

class TestUserModel(TestCase):
    def create_app(self):
        app.config.from_object('config.Config')
        return app

    # def setUp(self):
    #     db.create_all()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def test_create_user(self):
        username = fake.first_name()
        full_name = fake.name()
        bio = fake.catch_phrase()
        
        response = self.client.post('/users', json={
            'username': username,
            'full_name': full_name,
            'bio': bio
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.json['message'])

        user = User.query.filter_by(username=username).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.full_name, full_name)
        
    def test_create_post(self):
        username = fake.first_name()
        full_name = fake.name()
        bio = fake.catch_phrase()
        
        # First, create a user
        self.client.post('/users', json={
            'username': username,
            'full_name': full_name,
            'bio': bio
        })
        user = User.query.filter_by(username=username).first()

        content = fake.sentence(nb_words=5)
        
        # Test post creation
        response = self.client.post('/posts', json={
            'user_id': user.id,
            'content': content,
            'tags': ['test', 'post']
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Post created successfully', response.json['message'])

        post = Post.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, content)
        self.assertEqual(len(post.tags), 2)
        self.assertEqual(post.tags[0].tag, 'test')
        
    def test_create_story(self):
        username = fake.first_name()
        full_name = fake.name()
        bio = fake.catch_phrase()
        
        # First, create a user
        self.client.post('/users', json={
            'username': username,
            'full_name': full_name,
            'bio': bio
        })
        user = User.query.filter_by(username=username).first()
        
        content = fake.sentence(nb_words=5)

        # Test story creation
        response = self.client.post('/stories', json={
            'user_id': user.id,
            'content': content,
            'mentions': ['mention1', 'mention2']
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Story created successfully', response.json['message'])

        story = Story.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(story)
        self.assertEqual(story.content, content)
        self.assertEqual(len(story.mentions), 2)
        self.assertEqual(story.mentions[0].mention, 'mention1')

if __name__ == '__main__':
    unittest.main()
