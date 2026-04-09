import sqlite3
import os

# 根據架構設計，資料庫存放在 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')

def get_db_connection():
    """建立並回傳一個 SQLite 資料庫連線，設定 row_factory 提升存取直覺性"""
    # 若資料表所屬資料夾 instance 還未建立則會自動產生
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 使回傳的行操作像 dictionary
    return conn

class TaskModel:
    """任務模型 - 包含對於任務的新刪修查 (CRUD) 所有方法"""
    
    @staticmethod
    def init_db():
        """初期若資料庫尚未有表，執行 schema.sql 來建表"""
        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema = f.read()
            with get_db_connection() as conn:
                conn.executescript(schema)
                conn.commit()

    @staticmethod
    def create(title):
        """新增一筆任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 採用參數化查詢寫入，防止 SQL 注入
            cursor.execute(
                "INSERT INTO tasks (title, status) VALUES (?, ?)", 
                (title, 0)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        """取得所有任務，最新的任務排在前面"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            return cursor.fetchall()
            
    @staticmethod
    def get_by_id(task_id):
        """利用 ID 取得單一任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()

    @staticmethod
    def update(task_id, title=None, status=None):
        """更新任務的參數
        可單獨更新 title，也可切換 status。這會一併變更 updated_at。"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 動態建立要更新的欄位
            fields = []
            params = []
            if title is not None:
                fields.append("title = ?")
                params.append(title)
            if status is not None:
                fields.append("status = ?")
                params.append(status)
                
            if not fields:
                return
                
            # 任務有更動，順便修改更新時間
            fields.append("updated_at = CURRENT_TIMESTAMP")
            
            query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
            params.append(task_id)
            
            cursor.execute(query, tuple(params))
            conn.commit()

    @staticmethod
    def delete(task_id):
        """徹底移除某項任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
