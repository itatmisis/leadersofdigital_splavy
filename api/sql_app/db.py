import sqlite3
import logging
import re
import hashlib

logging.basicConfig(level=logging.DEBUG)

class Database:
    def __init__(self, file_name: str = ':memory:'):

        self.conn = None
        self.cursor = None

        if file_name:
            self.open(file_name)

    def open(self, file_name):

        try:
            self.conn = sqlite3.connect(file_name);
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def recreate(self):
        temp_conn = sqlite3.connect(':memory:')
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute('''create table yard(
                                            id integer primary key autoincrement,
                                            position_lat float,
                                            position_lon float)''')
        temp_cursor.execute('''create table camera(
                                            id integer primary key autoincrement,
                                            yard_id integer,
                                            position_lat float,
                                            position_lon float,
                                            foreign key(yard_id) references yard(id))''')
        temp_cursor.execute('''create table parking_lot(
                                            id integer primary key autoincrement,
                                            yard_id integer,
                                            index_in_parking_lot integer,
                                            position_lat float,
                                            position_lon float,
                                            state text,
                                            type text,
                                            foreign key(yard_id) references yard(id))''')
        temp_cursor.execute('''create table points(
                                            parking_lot_id integer primary key, 
                                            a_lat float,
                                            a_lon float,
                                            b_lat float,
                                            b_lon float,
                                            c_lat float,
                                            c_lon float,
                                            d_lat float,
                                            d_lon float,
                                            foreign key(parking_lot_id) references parking_lot(id))''')
        temp_cursor.execute('''create table user(
                                            id integer primary key autoincrement,
                                            login text unique,
                                            password_hash text)''')
        temp_conn.commit()
        temp_conn.backup(self.conn)
        temp_conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get(self, table, columns: str = '*', limit=None):
        query = f"SELECT {columns} from {table}"
        self.cursor.execute(query)
        # fetch data
        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]

    def get_where(self, table: str, columns: str, where: str, limit=None):
        query = f"SELECT {columns} from {table} where {where}"
        logging.debug(query)
        self.cursor.execute(query)
        # fetch data
        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]

    def getLast(self, table, columns):
        return self.get(table, columns, limit=1)[0]

    @staticmethod
    def to_csv(data, filename="output.csv"):
        with open(filename, 'a') as file:
            file.write(",".join([str(j) for i in data for j in i]))

    def write(self, table, columns, data):
        query = f"INSERT INTO {table} ({columns}) VALUES ({data})"
        self.cursor.execute(query)

    def query(self, sql):
        self.cursor.execute(sql)

    def add_yard(self, lat: float, lon: float):
        self.write('yard', 'position_lat, position_lon', f'{lat}, {lon}')

    def add_camera(self, yard_id: int, lat: float, lon: float):
        self.write('camera', 'position_lat, position_lon, yard_id', f'{lat}, {lon}, {yard_id}')

    def add_parking_lot(self, yard_id: int, lat: float, lon: float, state: str = "Free", type_: str = "Normal"):
        lots = self.get_where("parking_lot", "*", f"yard_id = {yard_id}")
        last = 0
        for lot in lots:
            if lot[2] and last < lot[2]:
                last = lot[2]
        last += 1
        self.write('parking_lot', 'position_lat, position_lon, yard_id, state, type, index_in_parking_lot',
                   f'{lat}, {lon}, {yard_id}, "{state}", "{type_}", {last}')

    def add_points(self, parking_lot_id: int, points: list):
        self.write('points', 'parking_lot_id, a_lat, a_lon, b_lat, b_lon, c_lat, c_lon, d_lat, d_lon',
                   f'{parking_lot_id}, {", ".join(map(str, points))}')

    def add_user(self, login: str, password_hash: str):
        if re.match(r'^[A-z0-9_]{3,30}$', login):
            self.write('user', 'login, password_hash', f'"{login}", "{password_hash}"')


    def check_user_ok(self, login, password_hash):
        if re.match(r'^[A-z0-9_]{3,30}$', login):
            user = self.get_where('user', '*', 'login = "{}"'.format(login))
            if user:
                if user[0][2] == password_hash:
                    return True, None
                else:
                    return False, "Wrong password"
            else:
                return False, "No such login"
        else:
            return False, "Wrong login symbols"

    def get_parking_lot_info(self, parking_lot_id: int):
        parking_lot = self.get_where('parking_lot', '*', 'id = {}'.format(parking_lot_id))
        if parking_lot:
            return {'parking_lot_id': parking_lot[0],
                    'yard_id': parking_lot[1],
                    'index_in_parking_lot': parking_lot[2],
                    'lat': parking_lot[3],
                    'lon': parking_lot[4],
                    'state': parking_lot[5],
                    'type': parking_lot[6]}
        else:
            return False

    def get_parkings_lot_info_by_yard_id(self, yard_id: int):
        parking_lots = self.get_where('parking_lot', '*', 'yard_id = {}'.format(yard_id))
        to_return = []
        for lot in parking_lots:
            to_return.append({'parking_lot_id': lot[0],
                              'yard_id': lot[1],
                              'index_in_parking_lot': lot[2],
                              'lat': lot[3],
                              'lon': lot[4],
                              'state': lot[5],
                              'type': lot[6]})
        return to_return

    def api_yard_info(self, yard_id):
        to_return = self.get_where('yard', '*', 'id = {}'.format(yard_id))
        if to_return:
            # parking_lots = self.get_where('parking_lot', '*', 'yard_id = {}'.format(yard_id))
            logging.debug(to_return)
            # logging.debug(parking_lots)
            return True, {'yard_id': to_return[0][0], 'lat': to_return[0][1], 'lon': to_return[0][2],
                          'parking_lots': self.get_parkings_lot_info_by_yard_id(yard_id)}
        else:
            return False, "No such yard"


    def find_closes_yards(self, cur_lat: float, cur_lon: float):
        pass