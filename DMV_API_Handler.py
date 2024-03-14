import requests, datetime

class DMVAPIHandler:
    def __init__(self):
        pass


    #API -san jose location available dates list
    def get_sj_date_data_api(self):
        url = "https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/516!56b48e272ba45819d81868f440fb30eb6c406b705436cf1d101d2ea2c75c/dates?services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=977125805110.5748"
        response = requests.get(url)

        data = response.json()

        return data[0]


    #API -locations available dates list
    def get_date_data_api(self,dmv_field_office_public_id):

        url = f"https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/{dmv_field_office_public_id}/dates?services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=977125805110.5748"
        response = requests.get(url)

        available_datas_data = response.json()



        earliest_available_date = available_datas_data[0]
        return earliest_available_date

    #API- find available time slot
    def get_time_slot_data_api(self,dmv_field_office_public_id,datetime):

        date = datetime.strftime("%Y-%m-%d")
        url = f"https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/{dmv_field_office_public_id}/times?date={date}&services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=867712719559.5795"

        response = requests.get(url)

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            data = None
        return data

    #API- find nearby DMV office by zipcode
    def get_dmv_office_nearby_data_api(self,zipcode):
        url = f"https://www.dmv.ca.gov/portal/wp-json/dmv/v1/field-offices?q={zipcode}"
        response = requests.get(url)
        data = response.json()
        return data

    #API- find nearby DMV office by zipcode by miles
    def get_dmv_office_nearby_within_miles_data_api(self,zipcode,miles):
        url = f"https://www.dmv.ca.gov/portal/wp-json/dmv/v1/field-offices?q={zipcode}"
        response = requests.get(url)
        data = response.json()
        dmv_office_nearby = []

        for office in data:
            if office["distance"] < miles:
                dmv_office_nearby.append(office)
        return dmv_office_nearby


    #API - get all zipcode
    def get_dmv_offices_zipcode_data_api(self):
        url = "https://www.dmv.ca.gov/portal/wp-json/dmv/v1/field-offices?q="
        response = requests.get(url)
        data = response.json()
        all_dmv_offices_zipcode = []
        for office in data:
            all_dmv_offices_zipcode.append(office["meta"]["dmv_field_office_zipcode"])
        return all_dmv_offices_zipcode
