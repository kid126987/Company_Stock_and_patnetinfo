import sqlite3
import os
from pathlib import Path

def check_and_create_database():
    """
    檢查是否存在資料庫，如果沒有則使用sqlite3建立，並使用test_fixed.sql建立table
    """
    # 設定資料庫路徑
    db_path = Path(__file__).parent / "stock_database.db"
    
    # 檢查資料庫是否存在
    if db_path.exists():
        print(f"資料庫已存在: {db_path}")
        return str(db_path)
    
    # 如果資料庫不存在，建立新的資料庫
    print(f"建立新資料庫: {db_path}")
    
    # 確保DBS目錄存在
    db_path.parent.mkdir(exist_ok=True)
    
    # 建立資料庫連接
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # 讀取sql檔案
        sql_file_path = Path(__file__).parent / "DataModelInfo.sql"
        
        if not sql_file_path.exists():
            print(f"錯誤: 找不到 {sql_file_path}")
            return None
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # 分割SQL語句並執行
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in sql_statements:
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"成功執行: {statement[:50]}...")
                except sqlite3.Error as e:
                    print(f"執行SQL時發生錯誤: {e}")
                    print(f"問題語句: {statement}")
        
        # 提交變更
        conn.commit()
        print("資料庫和表格建立完成！")
        
        # 顯示建立的表格
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"建立的表格: {[table[0] for table in tables]}")
        
    except Exception as e:
        print(f"建立資料庫時發生錯誤: {e}")
        conn.rollback()
        return None
    
    finally:
        conn.close()
    
    return str(db_path)

if __name__ == "__main__":
    db_path = check_and_create_database()
    if db_path:
        print(f"資料庫路徑: {db_path}")
    else:
        print("資料庫建立失敗")
