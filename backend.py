<<<<<<< HEAD
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from the Chrome extension

# Proprietary Heuristic Parser (Regex Engine & Threat Matrix)
THREAT_MATRIX = {
    "urgency": {
        "pattern": r"(?i)(only \d+ left|hurry|expires in|offer ends soon|last chance)",
        "weight": 0.6
    },
    "confirmshaming": {
        "pattern": r"(?i)(no thanks, i prefer to pay full price|i don't want to save)",
        "weight": 0.8
    },
    "hidden_fees": {
        "pattern": r"(?i)(processing fee|service charge|convenience fee)[\s:]*[\$₹€]?\d+",
        "weight": 0.5
    }
}

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    url = data.get('url', 'unknown')
    
    print(f"\n[SCANNING] Payload from {url}")

    threat_score = 0.0
    detected_patterns = []

    # Evaluate text stream against custom regex pattern dictionaries
    for category, metrics in THREAT_MATRIX.items():
        if re.search(metrics["pattern"], text):
            threat_score += metrics["weight"]
            detected_patterns.append(category)

    # Cap threat score at 1.0 (100% risk)
    threat_score = min(threat_score, 1.0)

    return jsonify({
        "status": "success",
        "threat_score": threat_score,
        "flags": detected_patterns
    }), 200

if __name__ == '__main__':
=======
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from the Chrome extension

# Proprietary Heuristic Parser (Regex Engine & Threat Matrix)
THREAT_MATRIX = {
    "urgency": {
        "pattern": r"(?i)(only \d+ left|hurry|expires in|offer ends soon|last chance)",
        "weight": 0.6
    },
    "confirmshaming": {
        "pattern": r"(?i)(no thanks, i prefer to pay full price|i don't want to save)",
        "weight": 0.8
    },
    "hidden_fees": {
        "pattern": r"(?i)(processing fee|service charge|convenience fee)[\s:]*[\$₹€]?\d+",
        "weight": 0.5
    }
}

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    url = data.get('url', 'unknown')
    
    print(f"\n[SCANNING] Payload from {url}")

    threat_score = 0.0
    detected_patterns = []

    # Evaluate text stream against custom regex pattern dictionaries
    for category, metrics in THREAT_MATRIX.items():
        if re.search(metrics["pattern"], text):
            threat_score += metrics["weight"]
            detected_patterns.append(category)

    # Cap threat score at 1.0 (100% risk)
    threat_score = min(threat_score, 1.0)

    return jsonify({
        "status": "success",
        "threat_score": threat_score,
        "flags": detected_patterns
    }), 200

if __name__ == '__main__':
>>>>>>> 79d0b65c0390d5773ad652ba42c2efe4625bfd52
    app.run(host='127.0.0.1', port=5000, debug=True)