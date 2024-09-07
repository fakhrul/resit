import psycopg2
import re
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse
from datetime import datetime
from psycopg2 import sql

load_dotenv(find_dotenv())


class DatabaseManager:
    def __init__(self):
        super(DatabaseManager, self).__init__()
        load_dotenv(override=True)  
        # self.database_pwd = os.getenv('DATABASE_PWD')
        # self.database_host = os.getenv('DATABASE_HOST')
        db_url = os.getenv('DATABASE_URL')
        parsed_url = urlparse(db_url)
        self.database_host = parsed_url.hostname
        self.database_pwd = parsed_url.password


        if self.database_host is None:
            self.database_host = "localhost"

    def get_camera_position_sequences(self):
        conn = None
        result = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT * FROM public.camerasequences order by sequenceno asc')

            # display the PostgreSQL database server version
            result = cur.fetchall()
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
    
    # def fun(self,s):
    #     a = re.match(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$', s)
    #     return(a)
    
    # def filter_mail(self, emails):
    #     return list(filter(self.fun, emails))


    def get_receipient_email(self):
        conn = None
        result = None
        try:
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            cur = conn.cursor()
            cur.execute('SELECT email FROM public.phones')

            # display the PostgreSQL database server version
            results = cur.fetchall()

            emails = []
            for result in results:
                if result[0] != None and result[0] != '':
                    emails.append(result[0])

            return emails
            # print(emails)
            # filtered_emails = self.filter_mail(result)
            # return filtered_emails
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result

    def get_receipient_phone(self):
        conn = None
        result = None
        try:
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            cur = conn.cursor()
            cur.execute('SELECT phoneno FROM public.phones')

            # display the PostgreSQL database server version
            results = cur.fetchall()
            phones = []
            for result in results:
                if result[0] != None and result[0] != '' :
                    phoneno = str(result[0])
                    if phoneno.isnumeric():
                        phones.append(phoneno)

            return phones
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
            
    def param_all(self):
        conn = None
        result = None
        try:
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            cur = conn.cursor()
            cur.execute('SELECT * FROM public.parameters ORDER BY id ASC LIMIT 1')
            result = cur.fetchone()
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
    
 

    def get_configuration_dropbox_app_secret(self):
        conn = None
        result = None
        try:
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT "DropboxAppSecret" FROM public.configurations ORDER BY id ASC LIMIT 1')

            # display the PostgreSQL database server version
            result = cur.fetchone()[0]
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
    
    def get_configuration_dropbox_app_key(self):
        conn = None
        result = None
        try:
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT "DropboxAppKey" FROM public.configurations ORDER BY id ASC LIMIT 1')

            # display the PostgreSQL database server version
            result = cur.fetchone()[0]
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result

    def get_configuration_location(self):
        conn = None
        result = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT "LocationName" FROM public.configurations ORDER BY id ASC LIMIT 1')

            # display the PostgreSQL database server version
            result = cur.fetchone()[0]
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result

    def get_configuration(self):
        conn = None
        result = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT * FROM public.configurations ORDER BY id ASC LIMIT 1')

            # display the PostgreSQL database server version
            result = cur.fetchone()
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
    
    def get_rtu_ip(self):
        conn = None
        result = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT "rtuipaddress" FROM public.configurations ORDER BY id ASC LIMIT 1')

            # display the PostgreSQL database server version
            result = cur.fetchone()[0]
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
    

    def get_active_snap_schedules(self):
        conn = None
        result = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT * FROM public.snapschedules where isactive = True')

            # display the PostgreSQL database server version
            result = cur.fetchall()
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("get_active_snap_schedules",error)
        finally:
            if conn is not None:
                conn.close()
        return result


    def insert_incident(self,
                        msg_datetime,
                    details,
                    imagepath):
        conn = None
        updated_rows = 0
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            sql = "INSERT INTO public.incidents(datetime, info, imagepath) VALUES(%s, %s,%s ) RETURNING id"
            cur.execute(sql,(msg_datetime, 
                             details,
                             imagepath,
                             ))
            updated_rows = cur.rowcount
            # display the PostgreSQL database server version
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows
    
    def get_binary_array(self, path):
        with open(path, "rb") as image:
            f = image.read()
            b = bytes(f).hex()
            return b
    # def insert_image(self,msg_datetime,file_path):
    #     conn = None
    #     updated_rows = 0
    #     try:
    #         # connect to the PostgreSQL server
    #         conn = psycopg2.connect(
    #                     host=self.database_host,
    #                     port=5432,
    #                     database="cropsmon",
    #                     user="postgres",
    #                     password=self.database_pwd)
            
    #         # create a cursor
    #         cur = conn.cursor()
    #         sql = "UPDATE public.incidents SET imageinbytes = decode(%s, 'hex') WHERE datetime = %s"

    #         # sql = "UPDATE INTO public.incidents(imageinbytes) VALUES(decode(%s, 'hex')) WHERE datetime = %s"
    #         cur.execute(sql,(self.get_binary_array(file_path),
    #                          msg_datetime))
    #         updated_rows = cur.rowcount
    #         # display the PostgreSQL database server version
    #         conn.commit()
    #         cur.close()
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #     finally:
    #         if conn is not None:
    #             conn.close()
    #     return updated_rows
    
    def get_movement_method(self):
        conn = None
        result = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT scanmethod FROM public.parameters ORDER BY id ASC LIMIT 1')

            # display the PostgreSQL database server version
            result = cur.fetchone()[0]
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result

    def delete_incident_by_id(self, incident_id):
        conn = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            # Execute the query to delete the incident by ID
            cur.execute(
                sql.SQL("DELETE FROM public.incidents WHERE id = %s"),
                [incident_id]
            )

            # Commit the transaction
            conn.commit()
            
            # Get the number of deleted rows
            deleted_rows = cur.rowcount
            
            # Close the cursor
            cur.close()
            
            # Check if the row was deleted
            if deleted_rows > 0:
                print(f"Incident with id {incident_id} has been deleted successfully.")
            else:
                print(f"No incident found with id {incident_id}.")
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
        finally:
            if conn is not None:
                conn.close()
    def get_oldest_incident(self):
        conn = None
        result = None
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(
                        host=self.database_host,
                        port=5432,
                        database="cropsmon",
                        user="postgres",
                        password=self.database_pwd)
            
            # create a cursor
            cur = conn.cursor()
            
            cur.execute('SELECT * FROM public.incidents ORDER BY datetime ASC LIMIT 1')

            # display the PostgreSQL database server version
            result = cur.fetchone()
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
            
    # def set_device_status_dropbox(self, status):
    #     conn = None
    #     result = None
    #     try:
    #         # connect to the PostgreSQL server
    #         conn = psycopg2.connect(
    #                     host=self.database_host,
    #                     port=5432,
    #                     database="cropsmon",
    #                     user="postgres",
    #                     password=self.database_pwd)
            
    #         # create a cursor
    #         cur = conn.cursor()

    #         # Update the 'dropbox' column in the first row of the 'devicestatus' table
    #         update_query = """
    #         UPDATE devicestatus
    #         SET dropbox = %s
    #         WHERE id = (SELECT id FROM devicestatus ORDER BY id LIMIT 1);
    #         """
    #         new_value = status # Replace this with the actual value you want to set

    #         cur.execute(update_query, (new_value,))
    #         conn.commit()
    #         cur.close()
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #     finally:
    #         if conn is not None:
    #             conn.close()
    #     return result
                            
    def set_device_status_dropbox(self, status):
        conn = None
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(
                host=self.database_host,
                port=5432,
                database="cropsmon",
                user="postgres",
                password=self.database_pwd
            )

            # Create a cursor
            cur = conn.cursor()

            # Update the 'dropbox' column and set 'dropbox_update_datetime' to the current timestamp
            update_query = """
            UPDATE devicestatus
            SET dropbox = %s, dropbox_update_datetime = %s
            WHERE id = (SELECT id FROM devicestatus ORDER BY id LIMIT 1);
            """
            current_time = datetime.now()
            cur.execute(update_query, (status, current_time))
            conn.commit()

            # Close the cursor
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
        finally:
            if conn is not None:
                conn.close()

if __name__ == "__main__":
    from datetime import datetime
    
    object = DatabaseManager()
    result = object.get_movement_method()
    print(result)

    result = object.get_camera_position_sequences()
    print(result)



    
    incidentdatetime = datetime.now()
    incidentsource = 'debug_laptop'
    incidentincidenttype = "test"
    incidentinfo = "test"
    incidentpositionx = 0
    incidentpositiony = 0
    incidentdistanceinmeter = 0
    incidentimagepath = "test"
    incidentvideopath = "test"
    incidentlongitude = 0
    incidentlatitude = 0
    incidentaltitude = 0

    incidentsection = ""
    # try:
    #     section = self._database.get_section(incident.positionx)
    #     if section is not None:
    #         incident.section = section
    # except:
    #     pass

    incidentaiversion = ""

    object.insert_incident(
                    incidentdatetime,
                    incidentsource,
                    incidentincidenttype,
                    incidentinfo,
                    incidentpositionx,
                    incidentpositiony,
                    incidentdistanceinmeter,
                    incidentimagepath,
                    incidentvideopath,
                    incidentlongitude,
                    incidentlatitude,
                    incidentaltitude,
                    incidentsection,
                    incidentaiversion

                )    
    print("DONE")