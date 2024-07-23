import datetime
from datetime import datetime
from DMV_API_Handler import DMVAPIHandler

dmv_api_handler = DMVAPIHandler()


class DateHandler:
    def __init__(self):
        pass

    #make string to datetime formate
    def make_string_to_datetime_format(self,str):
        try:

            date_obj = datetime.strptime(str, "%Y%m%d")
            print("成功轉成datetime format:",date_obj)

        except:
            try:
                split_str = str.split("-")
                date_obj = datetime(int(split_str[0]),int(split_str[1]),int(split_str[2][:2]))
                print("成功轉成datetime format:",date_obj)
            except:
                return"there's an issue with converting string to datetime format"
        return date_obj

    #make datetime formate to string
    def make_datetime_to_string_format(self,datetime):
        date_obj = datetime.strftime("%Y%m%d")
        print("成功轉成string format:",date_obj)
        return date_obj

    # #make datetime formate
    # def make_datetime_formate(self,str):
    #     split_str = str.split("-")
    #     datetime_formate = datetime(int(split_str[0]),int(split_str[1]),int(split_str[2][:2]))
    #     return datetime_formate

    #if user input date is later than earliest date from nearby dmv locations, send channel with good news
    def find_earlier_date_than_user_input(self,formated_input_date,formated_date_from_all_list, office_obj):
        print("這裡是find earlier date function: ",formated_input_date,formated_date_from_all_list, office_obj)
        #bot finds earlier date than user_input_date
        if formated_date_from_all_list < formated_input_date:
            
            new_day = formated_date_from_all_list.strftime("%A")
            dmv_field_office_public_id = office_obj['meta']['dmv_field_office_public_id']
            datetime_str = self.make_datetime_to_string_format(formated_date_from_all_list)

            #get available time slots on earliest date in the location
            time_slots= dmv_api_handler.get_time_slot_data_api(dmv_field_office_public_id,datetime_str)
            print("回你比較早的time slots: ", time_slots)

            all_time_slots =""
            for time_slot in time_slots:
                all_time_slots = all_time_slots +"\n" + time_slot
            
            return f"here's earliest date {formated_date_from_all_list}   {new_day} at {office_obj['slug']} ,\n available time slots as followings: \n{all_time_slots}"
        else:
            return f"Sorry, I can't find earlier one at {office_obj['id']} {office_obj['slug']}"

