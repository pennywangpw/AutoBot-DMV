import psycopg2
import psycopg2.extras


class DatabaseHandler:
    def __init__(self):
        #set up db- credentials
        DATABASE = "dmv_bot"
        USER="postgres"
        PASSWORD="postgres"
        HOST ="localhost"
