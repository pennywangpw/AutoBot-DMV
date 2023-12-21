import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# smtp_server_str = "smtp.gmail.com"
# port = 465  # email port to use SSL
# sender_email = "pennypython2023@gmail.com"
# receiver_email= "pennypython2023@gmail.com"
# password = input("Please enter your password: ")


class EmailHandler:
    def __init__(self):
        self.smtp_server_str = "smtp.gmail.com"
        self.port = 465
        self.sender_email = "pennypython2023@gmail.com"
        self.receiver_email= "pennypython2023@gmail.com"
        self.password = input("Please enter your password: ")


    def send_email(self,formated_input_date,dmv_list):
        print(f"確認調用static method的時候有沒有 {self.receiver_email}")
        old_day = formated_input_date.strftime("%A")
        number_of_office = len(dmv_list)
        msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

        for office in dmv_list:
            msg_to_user = msg_to_user + "------------------------"+ "\n" +office['information'] + "\n"

        msg = MIMEMultipart()
        msg["Subject"] = "DMV Update"
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email

        #attach text
        txt = f"{msg_to_user}"
        body = MIMEText(txt, "plain")

        msg.attach(body)

        #attach picture
        with open("./images.jpg","rb") as file:
            img = file.read()
        attach_file = MIMEApplication(img, Name ="cute.jpg")
        msg.attach(attach_file)


        with smtplib.SMTP_SSL(self.smtp_server_str, self.port) as smtp_server:
            smtp_server.login(self.sender_email, self.password)
            smtp_server.sendmail(
                self.sender_email,
                self.receiver_email,
                msg.as_string()
                )
        return "Email has been sent successfuly!"
