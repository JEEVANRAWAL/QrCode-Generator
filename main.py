from flask import Flask, jsonify, request, url_for
import qrcode
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/get-user/<user_id>')
def getUser(user_id):
    users={
        "id": user_id,
        "name":"jeevan rawal",
        "country":"nepal"
    }

    extraData= request.args.get("email-address")
    if extraData:
        users["extra-data"]= extraData

    return jsonify(users), 200

@app.route('/create-user', methods=['POST'])
def createUser():
    data= request.get_json()

    if data:
        return jsonify("This is the response",data), 201
    return "no data found!"

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
        timestamp= datetime.now().strftime("%Y%m%d%H%M%S")
        # filename= "qr_"+ timestamp + ".png"
        filename= f"qr_{timestamp}.png"


        # Save QR code
        file_path = os.path.join(directory, filename)
        myQrCode.save(file_path)
        
        # Generate the URL
        qr_url = url_for('static', filename=f'qrcode/{filename}', _external=True)
        
        return qr_url
    
    return "No data found! Must have data to generate QR Code"

if __name__ == "__main__":
    app.run(debug=True)