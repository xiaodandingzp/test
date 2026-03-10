import sqlite3
import os

# 数据库路径 - 使用绝对路径确保正确
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")


def init_db():
    """初始化数据库，创建用户表"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                openid TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        print(f"数据库初始化成功，路径: {DB_PATH}")
    except Exception as e:
        print(f"数据库初始化失败: {e}")


def get_user_by_openid(openid):
    """根据 openid 查找用户"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT openid, username FROM users WHERE openid = ?", (openid,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(openid, username):
    """创建新用户"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (openid, username) VALUES (?, ?)", (openid, username))
    conn.commit()
    conn.close()
