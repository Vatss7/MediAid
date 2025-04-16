import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

app = Flask(__name__)

# UltraMsg API Credentials
ULTRAMSG_INSTANCE_ID = os.getenv("INSTANCE_ID")  # UltraMsg instance ID
ULTRAMSG_TOKEN = os.getenv("TOKEN")  # UltraMsg API token
WHATSAPP_NUMBER = os.getenv("RECEIVER_PHONE")  # Recipient's WhatsApp number

# Function to send WhatsApp message
def send_whatsapp_alert(message):
    url = "http://api.textmebot.com/send.php?recipient=+917747010127&apikey=oXswcn3vjeoF&text=This%20is%20a%20test"
    

    response = requests.post(url)
    return response.json()  # Return the response for debugging

# API Route to trigger WhatsApp alert
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    message = data.get("message", "No message provided")

    response = send_whatsapp_message(message)
    
    return jsonify({
        "message_sent": message,
        "ultramsg_response": response,
        "status": "success" if response.get("sent") else "failed"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
