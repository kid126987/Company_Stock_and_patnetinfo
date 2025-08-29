if __name__ == "__main__":
   from database_setup import *
   db_path = check_and_create_database()

   from DataCraptoDB import *
   DatatoDBS = DatatoDB()

   from gradio_app import *

   demo.launch()
