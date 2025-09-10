from flask import Flask, request, jsonify

from fake_identity import random_person, random_address, random_email, random_phone

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/identity", methods=["POST"])
def identity():
    data = request.get_json(silent=True) or {}
    country = str(data.get("country", "US")).upper()
    # format_valid: true => guarantee_nonexistent = False
    format_valid = data.get("format_valid", True)
    # accept strings like "false"
    if isinstance(format_valid, str):
        format_valid = format_valid.lower() != "false"
    guarantee_nonexistent = not bool(format_valid)

    p = random_person()
    addr = random_address(country=country, guarantee_nonexistent=guarantee_nonexistent)
    result = {
        "first_name": p["first_name"],
        "last_name": p["last_name"],
        "email": random_email(p["first_name"], p["last_name"]),
        "phone": random_phone(country),
        "address": addr,
    }
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)