import json,os
from src.core.exceptions import UnableToSaveException




def read_json(db_file_name):
        try:
            file_path = os.path.join("src", "database", db_file_name)
            with open(file_path,"r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError as e:
            raise FileNotFoundError("Data Not Found")
    

def write_json(db_file_name,data):
    try:
        file_path = os.path.join("src", "database", db_file_name)
        #need to append
        with open(file_path,"w") as file:
            json.dump(data,file,indent=4)
        return True

    except Exception as e:
            print(f"An unexpected error occured: {e}")
