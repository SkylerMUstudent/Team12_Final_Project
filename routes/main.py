from flask import render_template, redirect, request, url_for, session
from . import main_bp

@main_bp.route('/')
def index():
    return render_template('index.html')