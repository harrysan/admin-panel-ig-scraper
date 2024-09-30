from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from util.handle_error import HandleError
from util.upload_img import UploadImg
from dotenv import load_dotenv
import os
import logging
import time
import random
from models.models import db, User, Follower, Following, BioLinks, Post, PostTag, Story, StoryMention

logger = logging.getLogger()

# Load File Env
load_dotenv()
USERNAME = os.environ['namauser']
PASSWORD = os.environ['password']

# Initiate Client
cl = Client(delay_range=[1,3])
cl.handle_exception = HandleError.handle_exception

# Login User
def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    # Check if session file empty
    with open("session.json", 'rb') as file:
        if file.read(2) != '[]':
            session = cl.dump_settings("session.json")
            
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    
    
    uuids = session["uuids"]
    sessionID = uuids['client_session_id']
    return sessionID

# Get User ID
def get_user_id(usernametarget):
    user_id = cl.user_id_from_username(usernametarget)
    
    return user_id

# Get User Info
def scrap_and_insert_user_info(usernametarget, user_id):
    user = User.query.filter_by(username=usernametarget).first()
    if not user:
        user_info = cl.user_info(user_id)
        
        # Simpan gambar profil ke server dan dapatkan path-nya
        saved_profile_pic_path = UploadImg.save_picture(user_info.profile_pic_url, user_info.pk+".jpg", "profiles")
        saved_profile_pic_hd_path = UploadImg.save_picture(user_info.profile_pic_url_hd, user_info.pk+"_hd.jpg", "profiles")
        
        user = User(
            pk=user_info.pk,
            username=user_info.username, 
            full_name = user_info.full_name,
            is_private = user_info.is_private,
            profile_pic_url = saved_profile_pic_path,
            profile_pic_url_hd = saved_profile_pic_hd_path,
            is_verified = user_info.is_verified,
            media_count = user_info.media_count,
            follower_count = user_info.follower_count,
            following_count = user_info.following_count,
            biography = user_info.biography,
            external_url = user_info.external_url,
            account_type = user_info.account_type,
            is_business = user_info.is_business,
            public_email = user_info.public_email,
            contact_phone_number = user_info.contact_phone_number,
            public_phone_country_code = user_info.public_phone_country_code,
            public_phone_number = user_info.public_phone_number,
            business_contact_method = user_info.business_contact_method,
            business_category_name = user_info.business_category_name,
            category_name = user_info.category_name,
            category = user_info.category,
            address_street = user_info.address_street,
            city_id = user_info.city_id,
            city_name = user_info.city_name,
            latitude = user_info.latitude,
            longitude = user_info.longitude,
            zip = user_info.zip,
            instagram_location_id = user_info.instagram_location_id,
            interop_messaging_user_fbid = user_info.interop_messaging_user_fbid)

        if len(user_info.bio_links) > 0:
            bio = BioLinks(
                pk_user = user_info.pk,
                link_id = user_info.bio_links[0].link_id,
                url = user_info.bio_links[0].url,
                lynx_url = user_info.bio_links[0].lynx_url,
                link_type = user_info.bio_links[0].link_type,
                title = user_info.bio_links[0].title,
                is_pinned = user_info.bio_links[0].is_pinned,
                open_external_url_with_in_app_browser = user_info.bio_links[0].open_external_url_with_in_app_browser,
            )
            db.session.add(bio)

        db.session.add(user)
        db.session.commit()
        print(f"User {usernametarget} inserted into the database.")
    else:
        print(f"User {usernametarget} already exists, skipping insert.")
        
    return user

# Get User Followers
def scrap_and_insert_user_followers(usernametarget, amount):
    user = scrap_and_insert_user_info(usernametarget=usernametarget, user_id=0)
    user_pk = user.pk
    
    user_followers = cl.user_followers(user_id=user_pk,amount=amount)
    for user_id, user_followers in user_followers.items():
        if Follower.query.filter_by(pk_user=user_pk, pk=user_id).first():
            print(f"Follower {user_id} already exists for {usernametarget}, skipping insert.")
            continue
        
        follower = Follower (
            pk= user_id,
            pk_user= user_pk,
            username = user_followers.username,
            full_name = user_followers.full_name,
            profile_pic_url = user_followers.profile_pic_url,
            profile_pic_url_hd = user_followers.profile_pic_url_hd,
            is_private = user_followers.is_private,
        )
        db.session.add(follower)
    
    db.session.commit()
    print(f"Followers for {usernametarget} inserted into the database.")

# Get User Following
def scrap_and_insert_user_following(usernametarget, amount):
    user = scrap_and_insert_user_info(usernametarget=usernametarget, user_id=0)
    user_pk = user.pk
    
    user_following = cl.user_following(user_id=user_pk,amount=amount)
    for user_id, user_following in user_following.items():
        if Following.query.filter_by(pk_user=user_pk, pk=user_id).first():
            print(f"Following {user_id} already exists for {usernametarget}, skipping insert.")
            continue
        
        following = Following (
            pk= user_id,
            pk_user= user_pk,
            username = user_following.username,
            full_name = user_following.full_name,
            profile_pic_url = user_following.profile_pic_url,
            profile_pic_url_hd = user_following.profile_pic_url_hd,
            is_private = user_following.is_private,
        )
        db.session.add(following)
        
    db.session.commit()
    print(f"Following for {usernametarget} inserted into the database.")

# Get User Medias ( last 20 medias )
def scrap_and_insert_user_posts(usernametarget, user_id, amount):
    user = scrap_and_insert_user_info(usernametarget=usernametarget, user_id=user_id)
    user_pk_target = user.pk
    
    user_medias = cl.user_medias(user_id,amount)
    for user_media in user_medias:
        is_Exists = False
        is_Exists = Post.query.filter_by(id_pk=user_media.id).first()
        
        if is_Exists:
            print("Post "+user_media.pk+" already exists for "+usernametarget+", skipping insert.")
            continue
        
        # Simpan gambar posts ke server dan dapatkan path-nya
        saved_post_thumbnail_path = UploadImg.save_picture(user_media.thumbnail_url, user_media.pk+"_thumbnail.jpg", "posts")
        saved_post_video_path = UploadImg.save_picture(user_media.video_url, user_media.pk+"_video.mp4", "posts")
        
        new_post = Post (
            pk = user_media.pk,
            id_pk = user_media.id,
            code = user_media.code,
            taken_at = user_media.taken_at,
            media_type	= user_media.media_type,
            # image_versions2 = user_media.image_versions2,
            product_type = user_media.product_type,
            thumbnail_url = saved_post_thumbnail_path,
            # location_pk = user_media.location_pk,
            user_pk = user_pk_target,
            comment_count	= user_media.comment_count,
            comments_disabled = user_media.comments_disabled,
            commenting_disabled_for_viewer = user_media.commenting_disabled_for_viewer,
            like_count	= user_media.like_count,
            play_count	= user_media.play_count,
            has_liked = user_media.has_liked,
            caption_text = user_media.caption_text,
            accessibility_caption = user_media.accessibility_caption,
            video_url = saved_post_video_path,
            view_count	= user_media.view_count,
            video_duration	= user_media.video_duration,
            title = user_media.title
        )
        
        print("User Media Tags", user_media.usertags)
        for tag in user_media.usertags:
            print("Tag : ",tag)
            # Simpan gambar post tags ke server dan dapatkan path-nya
            saved_post_tag_path = UploadImg.save_picture(tag.user.profile_pic_url, tag.user.pk+".jpg", "post_tags")
            saved_post_tag_hd_path = UploadImg.save_picture(tag.user.profile_pic_url_hd, tag.user.pk+"_hd.jpg", "post_tags")
        
            new_post.post_tags.append(PostTag(
                pk = tag.user.pk,
                user_pk = user_pk_target,
                media_pk = user_media.pk,
                username = tag.user.username, 
                full_name = tag.user.full_name,
                is_private = tag.user.is_private,
                profile_pic_url = saved_post_tag_path,
                profile_pic_url_hd = saved_post_tag_hd_path,
            ))
            # db.session.add(post_tag)
            
        db.session.add(new_post)

    db.session.commit()
    print(f"Posts for {usernametarget} inserted into the database.")

# Get User Stories ( get 20 from current stories  )
def scrap_and_insert_user_stories(usernametarget, user_id, amount):
    user = scrap_and_insert_user_info(usernametarget=usernametarget, user_id=user_id)
    user_pk_target = user.pk
    
    user_stories = cl.user_stories(user_id,amount)
    for story in user_stories:
        is_Exists = Story.query.filter_by(id_pk=str(story.id)).first()
        
        if is_Exists:
            print("Story "+story.pk+" already exists for "+usernametarget+", skipping insert.")
            continue
        
        # Simpan gambar stories ke server dan dapatkan path-nya
        saved_story_thumbnail_path = UploadImg.save_picture(story.thumbnail_url, story.pk+"_thumbnail.jpg", "stories")
        saved_story_video_path = UploadImg.save_picture(story.video_url, story.pk+"_video.mp4", "stories")
        
        story_info = cl.story_info(story_pk=story.pk)
        new_story = Story(
            pk = story.pk,
            id_pk = story.id,
            code = story.code,
            taken_at = story.taken_at,
            media_type	= story.media_type,
            product_type = story.product_type,
            thumbnail_url = saved_story_thumbnail_path,
            user_pk = user_pk_target,
            video_url = saved_story_video_path,
            video_duration	= story_info.video_duration,
        )
        
        mentions = story_info.mentions
        for mention in mentions:
            # Simpan gambar post tags ke server dan dapatkan path-nya
            saved_story_mentions_path = UploadImg.save_picture(mention.user.profile_pic_url, mention.user.pk, "story_mentions")
            saved_story_mentions_hd_path = UploadImg.save_picture(mention.user.profile_pic_url_hd, mention.user.pk+"_hd", "story_mentions")
            
            new_story.story_mentions.append(StoryMention(
                pk = mention.user.pk,
                user_pk = user_pk_target,
                story_pk = story.pk,
                username = mention.user.username, 
                full_name = mention.user.full_name,
                is_private = mention.user.is_private,
                profile_pic_url = saved_story_mentions_path,
                profile_pic_url_hd = saved_story_mentions_hd_path,
            ))
            # db.session.add(story_mention)
            
        db.session.add(new_story)

    db.session.commit()
    print(f"Stories for {usernametarget} inserted into the database.")

def processScrap(username):
    # Insert to DB
    try:
        start_time = time.time()
        
        login_user()
        user_id = get_user_id(username)
        time.sleep(random.randint(10, 60))
        scrap_and_insert_user_info(usernametarget=username, user_id=user_id)
        time.sleep(random.randint(30, 60))
        scrap_and_insert_user_following(usernametarget=username, amount=0)
        time.sleep(random.randint(30, 60))
        scrap_and_insert_user_followers(usernametarget=username, amount=0)
        time.sleep(random.randint(30, 60))
        scrap_and_insert_user_posts(usernametarget=username, user_id=user_id, amount=20)
        time.sleep(random.randint(30, 60))
        scrap_and_insert_user_stories(usernametarget=username, user_id=user_id, amount=20)
        
        seconds = time.time() - start_time
        forLog = "From Src Scraping. Success. Time Taken : "+time.strftime("%H:%M:%S",time.gmtime(seconds))
        print(forLog)
    except Exception as e:
        forLog = "From Src Scraping. Failed to process: " + str(e)
        print(forLog)