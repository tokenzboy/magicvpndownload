from flask import (Blueprint, request, jsonify, render_template, make_response)
from flask_limiter.util import get_remote_address
from utils.file_handler import download_file

frontend = Blueprint('frontend', __name__)


@frontend.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@frontend.route('/download', methods=['POST'])
def download():
    filename = request.form.get('file_name')
    url = request.form.get('download_url')
    if not (url and filename):
        return jsonify({'message': 'Illegal input fields'})
    temp_link = download_file(url, filename, get_remote_address())
    if not temp_link:
        return jsonify({'message': 'Incorrect resource'})
    return jsonify({'file_link': temp_link})


@frontend.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify(error="You have clearly exceeded %s" % e.description)
            , 429
    )