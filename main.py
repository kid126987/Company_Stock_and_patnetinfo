
import subprocess
import sys
# 函式：檢查並安裝封包
def install_package(package):
    """
    使用 pip 安裝指定的封包。
    """
    for i in package:
      try:
         __import__(i)
         print(f"{i} 封包已安裝，繼續執行程式...")
         continue
      except:
         print(f"找不到 f'{i}' 封包，正在嘗試安裝...")
         try:
            # 使用 subprocess 呼叫 pip 來安裝封包
            subprocess.check_call([sys.executable, "-m", "pip", "install", i])
            print(f"'{i}' 封包安裝成功！")
         except subprocess.CalledProcessError as e:
            print(f"安裝 '{i}' 封包時發生錯誤：{e}")
            sys.exit(1) # 如果安裝失敗，終止程式執行


if __name__ == "__main__":
   install_package(['requests','pandas','json','pathlib','sqlalchemy','google-generativeai','gradio','datetime','pyarrow','fastparquet'])
   
   from database_setup import *
   db_path = check_and_create_database()

   from DataCraptoDB import *
   DatatoDBS = DatatoDB()

   from gradio_app import *
   demo.launch()