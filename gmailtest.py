import smtplib

smtp_server_str = "smtp.gmail.com"
port = 465  # email port to use SSL
sender_email = "pennypython2023@gmail.com"
receiver_email= "pennypython2023@gmail.com"
password = input("Please enter your password: ")


def send_email(dmv_list):
    print(f"這裡傳進來的是整包dmv_obj {dmv_list}")
    msg_to_user = "~~~"

    for office in dmv_list:
        msg_to_user = msg_to_user + office['information'] + "\n" +"------------------------"+ "\n"
        # info_detail = f"Hey!!!! {office['information']}"

    print(f"家完後的msg_to_user  {msg_to_user}")

    message = """\
    Subject: Hi there

    This message is sent from Python."""
    # message = f"Subject: Hello from Bob.Hi, this is Bob. Long time no see. {msg_to_user}"

    with smtplib.SMTP_SSL(smtp_server_str, port) as smtp_server:
        smtp_server.login(sender_email, password)
        smtp_server.sendmail(
            sender_email,
            receiver_email,
            message
            # f'Subject: GOOD NEWS! we find an earlier time.\ntesting why this is not working tho....{msg_to_user}',
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
