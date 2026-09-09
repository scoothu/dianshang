"""
数据库操作封装层
支持两种模式：
  - SQLite（默认，本地无需安装，数据存 ecommerce.db 文件）
  - MySQL（生产环境，通过 config.yaml 配置）
通过 config.yaml 中 database.type 字段切换
"""
import os
import sqlite3
import threading
from utils.config import ConfigManager


class Database:
    """数据库操作类，统一封装 SQLite 和 MySQL 操作"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        config = ConfigManager().get_database_config()
        self.db_type = config.get('type', 'sqlite')
        self.conn = None
        self._connect()

    def _connect(self):
        if self.db_type == 'sqlite':
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ecommerce.db')
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        else:
            try:
                import mysql.connector
                self.conn = mysql.connector.connect(
                    host=config.get('host'),
                    port=config.get('port'),
                    user=config.get('user'),
                    password=config.get('password'),
                    database=config.get('database')
                )
            except Exception as e:
                print(f"MySQL连接失败，回退到SQLite: {e}")
                self.db_type = 'sqlite'
                db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ecommerce.db')
                self.conn = sqlite3.connect(db_path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row

    def init_tables(self):
        """初始化数据库表结构"""
        cursor = self.conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                category TEXT,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                address TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()

    # ==================== 通用查询 ====================
    def query(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params or ())
        return [dict(row) for row in cursor.fetchall()]

    def update(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params or ())
        self.conn.commit()
        return cursor.lastrowid

    # ==================== 用户 ====================
    def get_user(self, username):
        return self.query("SELECT * FROM users WHERE username=?", (username,))

    def add_user(self, username, password, email, role='user'):
        return self.update(
            "INSERT INTO users (username,password,email,role) VALUES (?,?,?,?)",
            (username, password, email, role)
        )

    # ==================== 商品 ====================
    def get_all_products(self):
        return self.query("SELECT * FROM products")

    def get_product(self, product_id):
        return self.query("SELECT * FROM products WHERE id=?", (product_id,))

    def add_product(self, name, price, stock, category, description=''):
        return self.update(
            "INSERT INTO products (name,price,stock,category,description) VALUES (?,?,?,?,?)",
            (name, price, stock, category, description)
        )

    def update_product(self, product_id, name, price, stock, category, description=''):
        return self.update(
            "UPDATE products SET name=?,price=?,stock=?,category=?,description=? WHERE id=?",
            (name, price, stock, category, description, product_id)
        )

    def delete_product(self, product_id):
        return self.update("DELETE FROM products WHERE id=?", (product_id,))

    # ==================== 订单 ====================
    def get_all_orders(self):
        return self.query("SELECT * FROM orders")

    def get_order(self, order_id):
        return self.query("SELECT * FROM orders WHERE id=?", (order_id,))

    def add_order(self, user_id, product_id, quantity, address, status='pending'):
        return self.update(
            "INSERT INTO orders (user_id,product_id,quantity,address,status) VALUES (?,?,?,?,?)",
            (user_id, product_id, quantity, address, status)
        )

    def update_order_status(self, order_id, status):
        return self.update("UPDATE orders SET status=? WHERE id=?", (status, order_id))

    def cancel_order(self, order_id):
        return self.update("UPDATE orders SET status='cancelled' WHERE id=?", (order_id,))

    def close(self):
        if self.conn:
            self.conn.close()
