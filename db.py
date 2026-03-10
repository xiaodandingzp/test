import sqlite3
import os

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def init_db():
    """初始化数据库，创建用户表"""
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
