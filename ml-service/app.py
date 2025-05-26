from flask import Flask, request, jsonify
import time
import random
from sklearn.linear_model import LogisticRegression
import numpy as np
from prometheus_client import start_http_server, Histogram, Counter, Gauge

# Prometheus metrics
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Latency of requests')
INFERENCE_LATENCY = Histogram('inference_latency_seconds', 'Latency of model inference')
ERROR_COUNTER = Counter('errors_total', 'Total number of errors')
RPM_COUNTER = Counter('requests_per_minute', 'Requests per minute')
MODEL_TYPE_GAUGE = Gauge('model_type', 'Type of model in use', ['type'])
GENDER_GAUGE = Gauge('gender_distribution', 'Gender distribution', ['gender'])

app = Flask(__name__)
start_http_server(8000)

# Супер простая моделька
X = np.array([[1], [2], [3]])
y = np.array([0, 0, 1])
model = LogisticRegression()
model.fit(X, y)

model_type = "logistic_regression"

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(latency)
    RPM_COUNTER.inc()
    return response

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        gender = data.get("gender", "unknown")
        GENDER_GAUGE.labels(gender=gender).inc()

        x = float(data.get("x", 0))
        time.sleep(random.uniform(0.001, 0.01))  # эмуляция инференса
        pred = model.predict([[x]])[0]
        proba = model.predict_proba([[x]])[0][int(pred)]

        INFERENCE_LATENCY.observe(time.time() - request.start_time)
        MODEL_TYPE_GAUGE.labels(type=model_type).set(1)

        return jsonify({"prediction": int(pred), "probability": float(proba)})
    except Exception as e:
        ERROR_COUNTER.inc()
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return jsonify({"status": "ML Service is running", "available_endpoint": "/predict"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
