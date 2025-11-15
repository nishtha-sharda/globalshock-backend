from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load your renamed coefficients
coeffs = pd.read_csv("coefficients.csv", index_col=0)

@app.route("/")
def home():
    return jsonify({"message": "Backend running with updated sector names!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    shock_type = data.get("shock_type")
    direction = data.get("direction")
    raw_pct = data.get("percentage")

    # Handle missing percentage
    try:
        pct = float(raw_pct) if raw_pct not in ["", None] else 2.0
    except:
        pct = 2.0

    if direction == "decrease":
        pct = -pct

    # Validate shock column
    if shock_type not in coeffs.columns:
        return jsonify({"error": f"Shock '{shock_type}' not found.",
                        "available_shocks": list(coeffs.columns)})

    result = {}

    # Iterate through updated sector names
    for sector in coeffs.index:
        beta = coeffs.loc[sector, shock_type]
        result[sector] = beta * pct

    return jsonify({
        "shock": shock_type,
        "direction": direction,
        "percentage_used": pct,
        "predicted_effect": result
    })


if __name__ == "__main__":
    app.run(debug=True)
