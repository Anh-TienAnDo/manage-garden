import pymysql.cursors
from datetime import datetime 

class ConnectionDB:
    def __init__(self):
        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='anh1710gdt',
                             database='garden',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        
    def get_connection(self):
        return self.connection
    
    def close_connection(self):
        self.connection.close()

    def save(self):
        self.connection.commit()

    def insert_lichsuhanhdong(self, table, data):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = f"INSERT INTO `{table}` (`mai_che`, `quat_mat`, `may_tuoi_nuoc`, `den_chieu_sang`, `created_at`, `manhdat_id`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (data.get('mai_che'), data.get('quat_mat'), data.get('may_tuoi_nuoc'), data.get('den_chieu_sang'), datetime.now(), data.get('manhdat_id')))
            self.save()
    
    def insert_lichsucambien(self, table, data):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = f"INSERT INTO `{table}` (`nhiet_do`, `do_am`, `do_am_dat`, `anh_sang`, `created_at`, `manhdat_id`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (data.get('nhiet_do'), data.get('do_am'), data.get('do_am_dat'), data.get('anh_sang'), datetime.now(), data.get('manhdat_id')))
            self.save()

    def select(self, table, id):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `{table}` WHERE `id`=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return result
        
    def select_by_manhdat(self, table, land_id):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `{table}` WHERE `id`=%s"
            cursor.execute(sql, (land_id,))
            result = cursor.fetchone()
            return result
        
    def select_by_dieukhienmanhdat(self, table, land_id):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `{table}` WHERE `manhdat_id`=%s"
            cursor.execute(sql, (land_id,))
            result = cursor.fetchone()
            return result
        
    def select_lichsuhanhdong_by_manhdat_id(self, table, land_id):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `{table}` WHERE `manhdat_id`=%s ORDER BY `created_at` DESC LIMIT 1"
            cursor.execute(sql, (land_id,))
            result = cursor.fetchall()
            return result
    
    def select_all(self, table):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `{table}` Limit 1"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        
d=ConnectionDB()
# hanhdong_data = {
#     'mai_che': 1,
#     'quat_mat': 1,
#     'may_tuoi_nuoc': 1,
#     'den_chieu_sang': 1,
#     'manhdat_id': 1,
# }
# d.insert_lichsuhanhdong('lichsu_lichsuhanhdong', hanhdong_data)  
# print(d.select_all('lichsu_lichsuhanhdong')) 
# cambien_data = {
#     'nhiet_do': 30,
#     'do_am': 50,
#     'do_am_dat': 60,
#     'anh_sang': 1000,
#     'manhdat_id': 1,
# }
# d.insert_lichsucambien('lichsu_lichsucambien', cambien_data)
# print(d.select_all('lichsu_lichsucambien'))
print(d.select_all('manhdat_manhdat'))


