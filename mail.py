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
guests={}
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
    data = number+'\n'+name+'\n'+entry+'\n'+email

    # Generate QR code
    filename = f"{name}_entry.png"
    generate_qr_code(data,(entry+'_events'), filename)

    # Send email with QR code
    msg = MIMEMultipart()
    msg['From'] = "telugusamiti.iitd@gmail.com"  # Sender's email address
    msg['To'] = email
    msg['Subject'] = "ఉగాది పండుగ సంబరాలు - SAC OAT - April 10, 2024, 5.30 PM"

    # body = f"Dear {name},\n\nPlease find your QR code attached.\n\nBest regards,\nYour Name"
    body = """\
    ప్రియమైన విద్యార్థులకు,

    శ్రీ క్రోధి నామ సంవత్సర ఉగాది శుభాకాంక్షలు

    మన కళాశాలలో జరగనున్న ఉగాది పండుగ సంబరాలకు మిమ్మల్ని ఆహ్వానిస్తున్నందుకు సంతోషిస్తున్నాము. ఉగాది, తెలుగువారు అందరు జరుపుకునే అత్యంత ముఖ్యమైన పండుగలలో ఒకటి మరియు తెలుగు కాలమాన పట్టిక ప్రకారం నూతన సంవత్సర ప్రారంభాన్ని సూచిస్తుంది.

    ఈ పర్వదినమున మనము వివిధ సాంస్కృతిక కార్యక్రమాలను నిర్వహిస్తున్నాము. ఉగాది విశిష్టత, ఆచార వ్యవహారాలను వివరిస్తూ ఉగాది సంబరాలు ప్రారంభమవుతాయి. అనంతరం మన తోటి విద్యార్థులచే ఉత్తేజాన్ని, ఆహ్లాదాన్ని కలుగచేసే సంగీత, నృత్య, నాటక ప్రదర్శనలు కనువిందు చేస్తాయి. ఈ వేడుకలో భాగంగా అచ్చమైన తెలుగు సాంప్రదాయ రుచులుతో కుడిన విందుని ఏర్పాటు చేస్తున్నాము.

    ఉగాది పండుగ సంబరాలు ఏప్రిల్ 10, 2024 న SAC OAT లో నిర్వహించబడతాయి. మన సంస్కృతి, సంప్రదాయాలను పాటిస్తూ మరియు కళాశాల లోని మన తోటి తెలుగివారి అందరితో కలిసి పండుగ జరుపుకోవడానికి ఇది ఒక శుభ సందర్భం. కావున తామెల్లరు విచ్చేసి ఈ కార్యక్రమాన్ని జయప్రదం చేయవల్సినదిగా కోరుతున్నాము.

    వేదిక(venue): SAC OAT & SAC లాన్
    తేదీ & సమయం(Date & Time): 10 ఏప్రిల్ (April), 2024, సా. 5 గం. ల నుండి

    Note: Please follow the instructions given in the attached file.

    మీ కోసం ఎదురుచూస్తూ……

    ఆహ్వానించువారు
    తెలుగు సమితి, ఐఐటి ఢిల్లీ.
    """

    msg.attach(MIMEText(body, 'plain'))
    # msg.set_content(body)

    with open(filename, 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name=filename)
        msg.attach(image)
    with open('Instructions.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='Instructions.png')
        msg.attach(image)
    with open('Ugadhi Event Planner.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='Ugadhi Event Planner.png')
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