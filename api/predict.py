import pickle
import os
from http.server import BaseHTTPRequestHandler
import json

# Load model and vectorizer once (cold start)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self._send_response(200, {"message": "Spam Detector API is running. Use POST with {'text': '...'}"})

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            text = data.get("text", "").strip()
            if not text:
                self._send_response(400, {"error": "Field 'text' is required and cannot be empty."})
                return

            # Vectorize and predict
            features = vectorizer.transform([text])
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0].tolist()
            class_labels = list(model.classes_)

            result = {
                "text": text,
                "prediction": str(prediction),
                "is_spam": bool(prediction == "spam" or prediction == 1),
                "confidence": {
                    str(label): round(prob, 4)
                    for label, prob in zip(class_labels, probabilities)
                }
            }
            self._send_response(200, result)

        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON body."})
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))