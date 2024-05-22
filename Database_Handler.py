import psycopg2
import psycopg2.extras

class DatabaseHandler:
    def __init__(self):
        #set up db- credentials
        self.hostname ="127.0.0.1"
        self.database = "dmv_bot"
        self.username = "postgres"
        self.pwd = "postgres"
        self.port_id = 5432
        self.conn = None
        self.cur = None

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(
                host = self.hostname,
                dbname = self.database,
                user = self.username,
                password = self.pwd,
                port = self.port_id
            )
            self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

            #clean up db to drop the table 
            self.cur.execute('DROP TABLE IF EXISTS record')
            self.cur.execute('DROP TABLE IF EXISTS member')


            #create table- member
            create_member_script = '''CREATE TABLE IF NOT EXISTS member(
                                id bigint UNIQUE,
                                name varchar(30) NOT NULL,
                                email varchar(80) NOT NULL UNIQUE)'''

            create_record_script = '''CREATE TABLE IF NOT EXISTS record(
                                member_id int PRIMARY KEY,
                                input_date date NOT NULL,
                                input_zipcode int NOT NULL,
                                mile int,
                                FOREIGN KEY (member_id) REFERENCES member (id) ON DELETE CASCADE)'''

            self.cur.execute(create_member_script)
            self.cur.execute(create_record_script)

            self.conn.commit()
            print("it's connecting to the database.....")

        except Exception as error:
            print(error)

        # finally:
        #     if self.cur is not None:
        #         self.cur.close()
        #     if self.conn is not None:
        #         self.conn.close()

    def insert_user_data(self,email,name):
        try:
            #insert data in table
            insert_script = 'INSERT INTO member (id,name,email) VALUES(%s,%s,%s)'
            insert_values=[(1,name,email),(2,'Neil','neil@sporton.com')]
            for val in insert_values:
                self.cur.execute(insert_script,val)
                self.conn.commit()
            print("insert successfully!!", email , name)
        except Exception as error:
            print("insert_user_data error: ",error)

