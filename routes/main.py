from flask import render_template, redirect, request, url_for, session
from . import main_bp

ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (username == ADMIN_CREDENTIALS['username'] and
            password == ADMIN_CREDENTIALS['password']):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_dashboard'))
        return render_template('admin_login.html', error="Invalid credentials")
    
    return render_template('admin_login.html')
