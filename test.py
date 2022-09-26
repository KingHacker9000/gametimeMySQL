# IMPORT MySQL Connector Class
import mysql.connector as connector
import json

class Database:

    # Connection to Database
    def __init__(self, dbname=None):
        self.conn = connector.connect(
            host='localhost',
            user="gtroot",
            passwd="admin@12",
            auth_plugin='mysql_native_password',
            database=dbname
        )

    # Execution of SQL Commands
    def execute(self, command, *args):
        try:
            # .schema Command
            if command == ".schema;":

                # return Value
                rV = {}

                # Create A Cursor
                c = self.conn.cursor(dictionary=True)
                # Execute Command
                c.execute("SHOW TABLES")

                
                # Fetch All The Tables
                rows = c.fetchall()
                
                for row in rows:
                    for key in row:
                        if key in rV: rV[key].append(row[key])
                        else: rV[key] = [row[key]]

                # Commit the Command
                self.conn.commit()

                # Print Value if its Main File
                if __name__ == '__main__':
                    print(json.dumps(rV, indent=4))

                # Return The Return Value List if it has atleast 1 element and the status of command
                return (rV if len(rV) != 0 else None), "Output Returned"


            # For SELECT Commands
            elif "SELECT" in command[0:8].upper() or "DESC" in command[0:4].upper():

                # return Value initialization
                rV = []

                # Create A Cursor
                c = self.conn.cursor(dictionary=True)
                # Execute Command
                c.execute(command, *args)

                # Fetch All the Rows
                rows = c.fetchall()

                # Append the rows to return Value as dict
                rV = rows

                # Commit the Command
                self.conn.commit()

                # Print Return Value if it is main file
                if __name__ == '__main__':
                    print(json.dumps(rV, indent=4))

                # Return the return value if it has atleast 1 element and the status
                print((rV if len(rV) != 0 else None), "Output Returned")
                return (rV if len(rV) != 0 else None), "Output Returned"
            
            else:
                c = self.conn.cursor(dictionary=True)
                c.execute(command, *args)
                self.conn.commit()
                return None, "Command Executed"
        except (connector.errors.ProgrammingError, connector.errors.Error) as e:
            print(e)

    def __del__(self):
        self.conn.close()


# If this is the main file
if __name__ == '__main__':

    db = Database(input("Enter File Name: "))
    try:
        while True:
            db.execute(input(">>> "))

    except KeyboardInterrupt:
        quit()
