from routes.user_routes import user_bp
from routes.follower_routes import follower_bp
from routes.following_routes import following_bp
from routes.post_routes import post_bp
from routes.story_routes import story_bp
from routes.biolinks_routes import biolinks_bp
from routes.scraper_routes import scraper_bp
import logging

def register_routes(app):
    # Konfigurasi logging untuk app utama
    logging.basicConfig(level=logging.DEBUG)

    app.register_blueprint(user_bp)
    app.register_blueprint(biolinks_bp)
    app.register_blueprint(follower_bp)
    app.register_blueprint(following_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(story_bp)
    app.register_blueprint(scraper_bp)
    
    # print('List Routes')
    # for route in app.url_map.iter_rules():
    #     print('%s' % route)
