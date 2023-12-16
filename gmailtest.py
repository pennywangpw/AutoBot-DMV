import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server_str = "smtp.gmail.com"
port = 465  # email port to use SSL
sender_email = "pennypython2023@gmail.com"
receiver_email= "pennypython2023@gmail.com"
password = input("Please enter your password: ")



def send_email(formated_input_date,dmv_list):
    old_day = formated_input_date.strftime("%A")
    number_of_office = len(dmv_list)
    msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

    for office in dmv_list:
        msg_to_user = msg_to_user + "------------------------"+ "\n" +office['information'] + "\n"

    msg = MIMEMultipart()
    msg["Subject"] = "DMV Update"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    txt = f"{msg_to_user}"
    body = MIMEText(txt, "plain")

    msg.attach(body)


    with smtplib.SMTP_SSL(smtp_server_str, port) as smtp_server:
        smtp_server.login(sender_email, password)
        smtp_server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
            )
    return "Email has been sent successfuly!"




## method 2
# import smtplib, ssl

# port = 465  # For SSL
# password = input("Type your password and press enter: ")

# # Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("pennypython2023@gmail.com", password)
