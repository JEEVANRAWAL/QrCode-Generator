from flask import Flask, jsonify, request, url_for
import qrcode
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/generate-QrCode', methods=['POST'])
def generateQrCode():
    data = request.get_json()
    
    if data and 'data' in data:
        # Directory to save QR codes
        directory = 'static/qrcode'
        
        # Create directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create QR code
        myQrCode = qrcode.make(data['data'])

        # generating timestamp to use it to name the qr file
        # timestamp= datetime.now().strftime("%Y%m%d%H%M%S")
        # filename= "qr_"+ timestamp + ".png"
        # filename= f"qr_{timestamp}.png"
        filename= "qr.png"


        # Save QR code
        file_path = os.path.join(directory, filename)
        myQrCode.save(file_path)
        
        # Generate the URL
        qr_url = url_for('static', filename=f'qrcode/{filename}', _external=True)
        
        return jsonify({'qr_url': qr_url}), 200
    
    return "No data found! Must have data to generate QR Code"

if __name__ == "__main__":
    app.run(debug=True)