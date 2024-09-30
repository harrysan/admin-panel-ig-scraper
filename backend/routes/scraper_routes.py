from flask import Blueprint, request, jsonify
from models.models import db
from dataclasses import fields
from sqlalchemy.exc import IntegrityError
import time
import logging
import src.scraping as src_scrap
import json

scraper_bp = Blueprint('scraper_bp', __name__)
logger = logging.getLogger()

# GET: Get all Story
@scraper_bp.route('/scrap', methods=['POST'])
def scrap():
    start_time = time.time()
    
    try:
        # Main Process
        target = request.json
        src_scrap.processScrap(target['username'])
        
        seconds = time.time() - start_time
        response = {"status":200, "response":"Success Scraping. Time Taken : "+time.strftime("%H:%M:%S",time.gmtime(seconds))}
        logger.info(response)
        
        return json.dumps(response)
    except Exception as e:
        response = {"status":500, "response":'Error Scraping. Failed to process: ' + str(e)}
        logger.error(response)
        
        return json.dumps(response)

