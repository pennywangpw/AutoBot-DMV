import datetime
from datetime import datetime
from DMV_API_Handler import DMVAPIHandler

dmv_api_handler = DMVAPIHandler()


class DateHandler:
    def __init__(self):
        pass

    #make datetime formate
    def make_datetime_formate(self,str):
        split_str = str.split("-")
        datetime_formate = datetime(int(split_str[0]),int(split_str[1]),int(split_str[2][:2]))
        return datetime_formate


    #find the earliest date and add weekday information
    def find_earlier_date_than_user_input(self,formated_input_date,formated_date_from_all_list, office_obj):
        if formated_date_from_all_list < formated_input_date:

            new_day = formated_date_from_all_list.strftime("%A")

            dmv_field_office_public_id = office_obj['meta']['dmv_field_office_public_id']
            time_slots= dmv_api_handler.get_time_slot_data_api(dmv_field_office_public_id,formated_date_from_all_list)

            print("---------------------------------------------")

            available_time_slots = []

            for time_slot in time_slots:
                available_time_slots.append(time_slot)

            time_slots_str = '\n'.join(available_time_slots)
            information = f"Id: {office_obj['id']} \n Location : {office_obj['slug']},\n Date : {formated_date_from_all_list} {new_day},\n Time slots as followings: \n{time_slots_str}"
            return information

        else:

            return f"Sorry, I can't find earlier one at {office_obj['id']} {office_obj['slug']}"
