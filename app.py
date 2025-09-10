import os
from flask import Flask, jsonify, request
from flask.logging import create_logger
from fake_identity.generator import random_person, random_address, random_email, random_phone

app = Flask(__name__)
logger = create_logger(app)

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

@app.route("/", methods=["GET"])
def home():
    """API documentation and welcome message"""
    return jsonify({
        "message": "Fake Identity Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/identity": "GET - Generate complete identity (name, email, phone, address)",
            "/person": "GET - Generate person (first_name, last_name)",
            "/address": "GET - Generate address (supports ?country=US|CA|AU)",
            "/email": "GET - Generate email (supports ?first_name=X&last_name=Y)",
            "/phone": "GET - Generate phone (supports ?country=US|CA|AU)",
            "/api/*": "Same endpoints under /api/* for parity with GitHub Pages"
        },
        "parameters": {
            "country": "US (default), CA, AU",
            "format_valid": "true (default), false - for guaranteed non-existent addresses"
        }
    })

@app.route("/person", methods=["GET"])
@app.route("/api/person", methods=["GET"])
def get_person():
    """Generate a random person"""
    person = random_person()
    return jsonify(person)

@app.route("/address", methods=["GET"])
@app.route("/api/address", methods=["GET"])
def get_address():
    """Generate a random address"""
    country = request.args.get("country", "US").upper()
    format_valid = request.args.get("format_valid", "false").lower() == "true"
    
    if country not in ["US", "CA", "AU"]:
        return jsonify({"error": "Unsupported country. Use 'US', 'CA', or 'AU'."}), 400
    
    try:
        address = random_address(country=country, guarantee_nonexistent=not format_valid)
        return jsonify(address)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/email", methods=["GET"])
@app.route("/api/email", methods=["GET"])
def get_email():
    """Generate a random email"""
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    
    if not first_name or not last_name:
        person = random_person()
        first_name = first_name or person["first_name"]
        last_name = last_name or person["last_name"]
    
    email = random_email(first_name, last_name)
    return jsonify({"email": email, "first_name": first_name, "last_name": last_name})

@app.route("/phone", methods=["GET"])
@app.route("/api/phone", methods=["GET"])
def get_phone():
    """Generate a random phone number"""
    country = request.args.get("country", "US").upper()
    
    if country not in ["US", "CA", "AU"]:
        return jsonify({"error": "Unsupported country. Use 'US', 'CA', or 'AU'."}), 400
    
    phone = random_phone(country)
    return jsonify({"phone": phone, "country": country})

@app.route("/identity", methods=["GET"])
@app.route("/api/identity", methods=["GET"])
def get_identity():
    """Generate a complete random identity"""
    country = request.args.get("country", "US").upper()
    format_valid = request.args.get("format_valid", "false").lower() == "true"

    if country not in ["US", "CA", "AU"]:
        return jsonify({"error": "Unsupported country. Use 'US', 'CA', or 'AU'."}), 400

    try:
        person = random_person()
        address = random_address(country=country, guarantee_nonexistent=not format_valid)
        email = random_email(person["first_name"], person["last_name"])
        phone = random_phone(country)

        return jsonify({
            "first_name": person["first_name"],
            "last_name": person["last_name"],
            "email": email,
            "phone": phone,
            "address": address,
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found. Visit / for API documentation."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# For local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])