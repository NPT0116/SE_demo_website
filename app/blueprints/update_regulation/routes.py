from flask import render_template, request, jsonify
from app.database import db
from app.regulation import regulation  # Ensure this is the correct import path

# Kết nối cơ sở dữ liệu

from . import update_regulation_bp


# @update_regulation_bp.route('/')
# def update_regulation():
#     return render_template('update_regulation/update_regulation.html')

@update_regulation_bp.route('/', methods=['GET'])
def update_regulation():
    terms = regulation.get_terms()
    return render_template('update_regulation/update_regulation.html', terms=terms)