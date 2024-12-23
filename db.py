from enum import StrEnum
from typing import Any

import psycopg2


class Table(StrEnum):
    WORKER = "worker"
    CLIENT = "client"
    CONTRACT = "contract"
    SET = "set"
    CAR = "car"


class Database:
    DBNAME = "car_dealership"
    USER = "dealership_user"
    PASSWORD = "1234"
    HOST = "localhost"
    PORT = 5432

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Создаём инстанс")
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def _init_connection(self):
        self.conn = psycopg2.connect(
            dbname=self.DBNAME,
            user=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
        )
        self.conn.autocommit = True
        print("Соединение установлено")

    def init_db(self):
        print("init_db")
        self._init_connection()
        self.create_tables()

    def get_connection(self):
        if self.conn.closed:
            print("Соединение закрыто. Переподключаемся к бд...")
            self._init_connection()
        return self.conn

    def execute(self, query: str, params=None) -> list[tuple[Any, ...]] | None:
        try:
            with self.get_connection().cursor() as cursor:
                if query.startswith("get_"):
                    query = "select * from " + query
                cursor.execute(query, params)
                if cursor.description:
                    return cursor.fetchall()
            return None

        except psycopg2.OperationalError as e:
            print(f"Систменая ошибка бд: {e}")
            print("Переподключаемся...")
            self._init_connection()
            return self.execute(query, params)
        except Exception as e:
            print(f"Невозможно выполнить запрос: {e}")
            raise

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("Подключение закрыто")
        else:
            print("Подключение уже закрыто")

    def create_tables(self):
        self.execute("call create_tables()")

    def drop_all(self):
        print("drop_all")
        self.execute("call drop_all()")
        self.close()

    def drop_table(self, table_name: Table = None):
        print("drop_table")
        if table_name:
            self.execute("call drop_table(%s)", (table_name,))
        else:
            self.execute("call drop_all()")

    def get_table(self, table: Table, params=None):
        cmd = f"get_{table}("
        if params:
            cmd += ",".join(["%s"] * len(params))
        cmd += ")"
        print(cmd)
        return self.execute(cmd, params)

    def add_worker(self, fullname: str):
        print("add_worker")
        fullname = fullname.strip().lower()
        self.execute("call add_worker(%s)", (fullname,))

    def delete_worker(self, fullname: str):
        print("delete_worker")
        fullname = fullname.strip().lower()
        self.execute("call delete_worker(%s)", (fullname,))

    def add_set(self, name: str, ratio: float):
        print("add_set")
        name = name.strip().lower()
        self.execute("call add_set(%s, %s)", (name, ratio))

    def delete_set(self, set_id: int):
        print("delete_set")
        self.execute("call delete_set(%s)", (set_id,))

    def add_car(
        self, car_brand: str, car_model: str, cost: int, set_id: int, num: int = 0
    ):

        print("add_car")
        car_brand = car_brand.strip().lower()
        car_model = car_model.strip().lower()
        self.execute(
            "call add_car(%s, %s, %s, %s, %s)",
            (car_brand, car_model, cost, set_id, num),
        )

    def get_car_brand(self):
        print("get_car_brand")
        return self.execute("get_car_brand()")

    def get_model_by_brand(self, car_brand: str):
        print("get_model_by_brand")
        car_brand = car_brand.strip().lower()
        return self.execute("get_model_by_brand(%s)", (car_brand,))

    def get_set_by_car(self, car_brand: str, car_model: str):
        print("get_model_by_brand")
        car_brand = car_brand.strip().lower()
        car_model = car_model.strip().lower()
        return self.execute("get_set_by_car(%s, %s)", (car_brand, car_model))

    def update_car_cost(self, car_id: int, new_cost: int):
        print("update_car_cost")
        self.execute("call update_car_cost(%s, %s)", (car_id, new_cost))

    def update_car_num(self, car_id: int, new_num: int):
        print("update_car_num")
        self.execute("call update_car_num(%s, %s)", (car_id, new_num))

    def add_contract(
        self,
        worker_id: int,
        client_name: str,
        car_brand: str,
        car_model: str,
        set_id: int,
        is_credit: bool,
    ):
        print("add_contract")
        car_brand = car_brand.strip().lower()
        car_model = car_model.strip().lower()
        client_name = client_name.strip().lower()
        self.execute(
            "call add_contract(%s, %s, %s, %s, %s, %s)",
            (worker_id, client_name, car_brand, car_model, set_id, is_credit),
        )
