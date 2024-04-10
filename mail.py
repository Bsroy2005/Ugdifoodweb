import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd
import os
import json
# import myende
df = pd.read_excel('sheet.xlsx')

from cryptography.fernet import Fernet, InvalidToken

file = open('key.key', 'rb')  # Open the file as wb to read bytes
key = file.read()  # The key will be type bytes
file.close()
with open('normal.json', 'r') as file:
    guests = json.load(file)
def myencrypt(input_data,id):
    # input_file = 'test.txt'
    # output_file = 'test.encrypted'

    # with open(input_file, 'rb') as f:
    #     data = f.read()  # Read the bytes of the input file
    guests[id]=input_data
    data=id.encode('utf-8')
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    # with open(output_file, 'wb') as f:
    #     f.write(encrypted)  # Write the encrypted bytes to the output file

    return encrypted
        

# Function to generate QR code
def generate_qr_code(data,id, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(myencrypt(data,id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
# names=df['Names'].tolist()
# mails=df['email-id'].tolist()
# entry_no=df['Entrynum'].tolist()
id=0
# Loop through each person
for index, row in df.iterrows():
    name = str(row['Names'])
    email = str(row['email-id'])
    entry= str(row['Entrynum'])
    number=str(row['Index'])
    data = 'Food_Entry'+'\n'+number+'\n'+name+'\n'+entry+'\n'+email

    # Generate QR code
    filename = f"{name}_food.png"
    generate_qr_code(data,(entry+'_food'), filename)

    # Send email with QR code
    msg = MIMEMultipart()
    msg['From'] = "telugusamiti.iitd@gmail.com"  # Sender's email address
    msg['To'] = email
    msg['Subject'] = "ఉగాది పండుగ సంబరాలు - Food QR code"

    # body = f"Dear {name},\n\nPlease find your QR code attached.\n\nBest regards,\nYour Name"
    body = """\
    Dear Students,

    Please find the attached QR code for dinner in the ugadi event. It is compulsory to show the QR code in the dining area.

    Note: There are two QR codes,
    1) for entry (already sent)
    2) for dinner (attached here)

    We are looking forward for your gracious presence on this occasion.

    Regards,
    Team Ugadi 2024.
    """

    msg.attach(MIMEText(body, 'plain'))
    # msg.set_content(body)

    with open(filename, 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name=filename)
        msg.attach(image)
    # msg.attach('Instructions.png')
    # msg.attach('Ugadhi Event Planner.png')

    smtp_server = "smtp.gmail.com"  # SMTP server address
    smtp_port = 587  # SMTP port
    smtp_username = "telugusamiti.iitd@gmail.com"  # SMTP username
    smtp_password = "milfzqucfhcyupma"  # SMTP password

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {str(e)}")
    finally:
        server.quit()
    os.remove(filename)

with open("normal.json", "w") as file:
    json.dump(guests, file)

# milf zquc fhcy upma