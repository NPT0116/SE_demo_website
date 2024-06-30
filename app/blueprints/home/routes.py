from flask import render_template, request, jsonify



# Kết nối cơ sở dữ liệu

from . import home_bp

@home_bp.route('/')
def home():
    return render_template('home/home.html')


