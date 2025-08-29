if __name__ == "__main__":
   from sidepro.database_setup import *
   db_path = check_and_create_database()

   from sidepro.DataCraptoDB import *
   DatatoDBS = DatatoDB()

   from sidepro.gradio_app import *
   demo.launch()