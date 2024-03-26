from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from sqlalchemy.exc import IntegrityError
import json 
from cryptography.fernet import Fernet, InvalidToken
fil = open('key.key', 'rb')  # Open the file as wb to read bytes
key = fil.read()  # The key will be type bytes
# import myende
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Initialize Database within Application Context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

#         new_user = User(username=username, password_hash=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         flash('Registration successful! Please login.')
#         return redirect(url_for('index'))

#     return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/scan')
def scan():
        # Open the camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Read frame from the camera
        ret, frame = cap.read()

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        try:
            # Decode QR code
            decoded_objects = decode(gray_frame)

            if decoded_objects:
                # Print the decoded information
                for obj in decoded_objects:
                    # print('Type:', obj.type)
                    # print('Data:', obj.data.decode('utf-8'))
                    # print('hello',obj.data)
                    # print('hi',mydecrypt(obj.data))
                    return render_template('scannedpage.html',data=mydecrypt(obj.data))

                # Draw a rectangle around the QR codemain_dic
                for obj in decoded_objects:
                    points = obj.polygon
                    if len(points) > 4:
                        hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                        hull = list(map(tuple, np.squeeze(hull)))
                    else:
                        hull = points
                    n = len(hull)
                    for j in range(0, n):
                        cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

                cv2.imshow('QR Code Scanner', frame)

        except Exception as e:
            print("Error:", e)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

def mydecrypt(input_data):
    # input_file = 'test.encrypted'
    # output_file = 'testout.txt'

    # with open(input_file, 'rb') as f:
    #     data = f.read()  # Read the bytes of the encrypted file
    data=input_data
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(data)
        with open("my_dict.json", "r") as file:
            read_data=json.load(file)
        # with open(output_file, 'wb') as f:
        #     f.write(decrypted)  # Write the decrypted bytes to the output file
        out_id=decrypted.decode('utf-8')
        out_data=read_data[out_id]
        if out_data!='None':
            read_data[out_id]="None"
            with open("my_dict.json", "w") as file:
                json.dump(read_data, file)
        return out_data

        # Note: You can delete input_file here if you want
    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")
# @app.route('/scan')
# def scan():
#     # Open the camera
#     cap = cv2.VideoCapture(0)

#     while True:
#         # Read frame from the camera
#         ret, frame = cap.read()

#         # Convert frame to grayscale
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         try:
#             # Decode QR code
#             decoded_objects = decode(gray_frame)

#             if decoded_objects:
#                 # Print the decoded information
#                 for obj in decoded_objects:
#                     qr_data = obj.data.decode('utf-8')
#                     print('Type:', obj.type)
#                     print('Data:', qr_data)
                    
#                     # Check if QR code has already been used
#                     qr_code = QRCode.query.filter_by(code=qr_data).first()
#                     if qr_code:
#                         if qr_code.used:
#                             print("QR code has already been used.")
#                             continue  # Skip to next QR code if already used
#                         else:
#                             # Mark QR code as used
#                             qr_code.used = True
#                             try:
#                                 db.session.commit()
#                             except IntegrityError:
#                                 db.session.rollback()
#                                 print("An error occurred while marking QR code as used.")
#                                 continue  # Skip to next QR code in case of error

#                     else:
#                         print("Invalid QR code.")
#                         continue  # Skip to next QR code if invalid

#                     return render_template('scannedpage.html', data=qr_data)

#                 # Draw a rectangle around the QR code
#                 for obj in decoded_objects:
#                     points = obj.polygon
#                     if len(points) > 4:
#                         hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
#                         hull = list(map(tuple, np.squeeze(hull)))
#                     else:
#                         hull = points
#                     n = len(hull)
#                     for j in range(0, n):
#                         cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

#                 cv2.imshow('QR Code Scanner', frame)

#         except Exception as e:
#             print("Error:", e)

#         # Exit on 'q' press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the camera and close the OpenCV window
#     cap.release()
#     cv2.destroyAllWindows()


from flask import current_app

@app.route('/get_users', methods=['GET'])
def get_users():
    with current_app.app_context():
        user_to_delete = User.query.filter_by(username='UgadiFoodTeam2').first()
    
    # # Check if the user exists before attempting to delete
    # if user_to_delete:
    #     db.session.delete(user_to_delete)
    #     db.session.commit()  # Don't forget to commit the transaction
    #     print("User deleted successfully")
    # else:
    #     print("User not found")
        
    users = User.query.all()
    
    for user in users:
        print(f"Username: {user.username}, Password Hash: {user.password_hash}")
    return "Check your terminal for user data."


if __name__ == '__main__':
    app.run(debug=True)

