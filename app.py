from flask import Flask, render_template, redirect, url_for, session
from config import Config
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.customer_routes import customer_bp
from routes.account_routes import account_bp
from routes.transaction_routes import transaction_bp
from routes.report_routes import report_bp
from routes.main_routes import main_bp
from routes.loan_routes import loan_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(account_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(report_bp)
app.register_blueprint(loan_bp)
app.register_blueprint(main_bp)

# Root route
@app.route('/')
def home():
    if 'admin_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

# Custom 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html', error="404 Page Not Found"), 404

# Custom 500 handler
@app.errorhandler(500)
def server_error(e):
    return render_template('login.html', error="500 Internal Server Error"), 500

if __name__ == '__main__':
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)