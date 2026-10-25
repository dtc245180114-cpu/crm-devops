from flask import Flask, request, jsonify
import sys
import datetime

app = Flask(__name__)
alerts_history = []

@app.route('/alert', methods=['POST'])
def receive_alert():
    try:
        data = request.get_json(force=True, silent=True) or {}
    except Exception:
        data = {}
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    alerts_history.append(data)
    
    log_msg = f"[ALERT-SINK] WEBHOOK ALERT RECEIVED AT {timestamp} - status={data.get('status', 'unknown')}"
    print(log_msg, flush=True)
    return jsonify({"status": "received", "timestamp": timestamp}), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts_history), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    print("[ALERT-SINK] Starting Alert-Sink listener on 0.0.0.0:5000...", flush=True)
    app.run(host='0.0.0.0', port=5000)
