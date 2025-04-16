from flask import Flask, jsonify, request
# from whatsapp_alert import send_whatsapp_alert
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

TEXTMEBOT_INSTANCE_ID = os.getenv("INSTANCE_ID")
TEXTMEBOT_TOKEN = os.getenv("TOKEN")
WHATSAPP_NUMBER = os.getenv("RECEIVER_PHONE")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!"})

def send_whatsapp_message(message, phone_number):
    url = f"http://api.textmebot.com/send.php?recipient={phone_number}&apikey={TEXTMEBOT_TOKEN}&text={message}"  
    try:
        response = requests.post(url)
        response_json = response.json()
        print("Whatsapp API Response:", response_json)
        return response_json
    except Exception as e:
        print("Whatsapp API Error:", str(e))
        return {"error": str(e)}

@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    prescription_text = data.get("prescription_text", "No prescription text provided.")
    phone_number = data.get("phone_number", "No phone number provided.")

    if not prescription_text.strip():
        return jsonify({"status": "failed", "message": "Prescription text is empty!"}), 400

    if not phone_number.strip():
        return jsonify({"status": "failed", "message": "Phone number is empty!"}), 400

    whatsapp_response = send_whatsapp_message(f"📜 Prescription Alert:\n{prescription_text}",phone_number)

    print("Whatsapp API Response:", whatsapp_response)
    return jsonify({
        "message_sent": prescription_text,
        "whatsapp_response": whatsapp_response,
        "status": "success" if whatsapp_response.get("sent") else "failed"
    })

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
