import pymysql

class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host='<hostname>.rds.amazonaws.com',
            port=int(3306),
            user="<user>",
            passwd="<password>",
            db='db_2'
        )
        self.cursor = self.conn.cursor()


    def get_all_data(self):
        self.cursor.execute('select * from tasks')
        data = self.cursor.fetchall()
        return data

    def push_data(self, name):
        sql = "INSERT INTO tasks (name) VALUES (%s)"
        val = name
        self.cursor.execute(sql, val)
        self.conn.commit()

        #Get the last entered id and name
        self.cursor.execute('SELECT * FROM tasks WHERE id=(SELECT max(id) FROM tasks)')
        data = self.cursor.fetchall()[0]
        return data

    def set_task_done(self, id):
        sql = "UPDATE tasks SET done=TRUE where id={}".format(id)
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_task(self, id):
        sql = "DELETE FROM tasks WHERE id={} ".format(id)
        self.cursor.execute(sql)
        self.conn.commit()





if __name__ == '__main__':
    Database().get_last_value()

        

# cursor = conn.cursor()
# cursor.execute("CREATE TABLE tasks (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), done BOOL default FALSE )")
#
# cursor.execute('SHOW TABLES')
# print(list(cursor))
#
#
#
#
# sql = "INSERT INTO tasks (name) VALUES (%s)"
# val = ("Git and Github")
# cursor.execute(sql, val)
#
# conn.commit()
#
# print(cursor.rowcount, "record inserted.")
#
#
#



# conn = pymysql.connect(
#     host='localhost',
#     port=int(3306),
#     user="root",
#     passwd="12345678",
#     db="database-2"
#     # db="SalesDB",
#     # charset='utf8mb4'
# )