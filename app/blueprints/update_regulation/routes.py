from flask import render_template, request, jsonify
from app.database import db


# Kết nối cơ sở dữ liệu

from . import update_regulation_bp


@update_regulation_bp.route('/')
def update_regulation():
    return render_template('update_regulation/update_regulation.html')
