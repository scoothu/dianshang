import mysql.connector
from mysql.connector import Error
from utils.config import ConfigManager


class Database:
    def __init__(self):
        config = ConfigManager().get_database_config()
        self.host = config.get('host')
        self.port = config.get('port')
        self.user = config.get('user')
        self.password = config.get('password')
        self.database = config.get('database')
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Query execution error: {e}")
            return None

    def execute_update(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Update execution error: {e}")
            self.connection.rollback()
            return 0

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        result = self.execute_query(query, (username,))
        return result[0] if result else None

    def get_product_by_id(self, product_id):
        query = "SELECT * FROM products WHERE id = %s"
        result = self.execute_query(query, (product_id,))
        return result[0] if result else None

    def get_order_by_id(self, order_id):
        query = "SELECT * FROM orders WHERE id = %s"
        result = self.execute_query(query, (order_id,))
        return result[0] if result else None

    def insert_test_user(self, username, password, email):
        query = """
        INSERT INTO users (username, password, email, created_at)
        VALUES (%s, %s, %s, NOW())
        """
        return self.execute_update(query, (username, password, email))

    def insert_test_product(self, name, price, stock, category):
        query = """
        INSERT INTO products (name, price, stock, category, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        """
        return self.execute_update(query, (name, price, stock, category))

    def insert_test_order(self, user_id, product_id, quantity, status):
        query = """
        INSERT INTO orders (user_id, product_id, quantity, status, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        """
        return self.execute_update(query, (user_id, product_id, quantity, status))

    def delete_test_user(self, username):
        query = "DELETE FROM users WHERE username = %s"
        return self.execute_update(query, (username,))

    def delete_test_product(self, name):
        query = "DELETE FROM products WHERE name = %s"
        return self.execute_update(query, (name,))

    def delete_test_order(self, order_id):
        query = "DELETE FROM orders WHERE id = %s"
        return self.execute_update(query, (order_id,))