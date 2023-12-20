from discordwebhook import Discord
import os
import requests


def send_notification_through_discord(formated_input_date,dmv_list):
    old_day = formated_input_date.strftime("%A")
    number_of_office = len(dmv_list)
    msg_to_user = f"The date you have on hand is on {formated_input_date} {old_day}!\n I found {number_of_office} location(s) with earlier time than what you have!\n\n"

    for office in dmv_list:
        msg_to_user = msg_to_user + "------------------------"+ "\n" +office['information'] + "\n"

    discord = Discord(url="https://discord.com/api/webhooks/1185829935835791440/cSoo4VHo__d-oY_ybKcJJKMONpkiZLffcu_pfPIzY5y45qlyuAD6EYbj4ABQdN5eKtnk")
    discord.post(content=msg_to_user)
