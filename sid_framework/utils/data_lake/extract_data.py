import pandas as pd
import configparser
from pathlib import Path
from impala.dbapi import connect
from impala.util import as_pandas

class HiveFetchData():

    """
    
    """

    def __init__(self, config_path) -> None:
        
        config_obj = configparser.ConfigParser()
        config_obj.read(config_path)
        self.hive_params = config_obj['hive']
        self.data_params = config_obj['data']


    def connect_hive(self):

        """
    
        """

        try:    
            self.conn = connect(
                host = self.hive_params['HOST'],
                port = int(self.hive_params['PORT']),
                auth_mechanism = 'PLAIN',
                user = self.hive_params['USER'],
                password = self.hive_params['PASSWORD'],
            )       
            print('Successful connection to Data Lake!')
        
            return self.conn
        except Exception as e:
            print(f'Failed process due to {e}')
    
    def close_connection(self):

        try:
            self.conn.close()
            print('Hive Server disconnected!')
        except Exception as e:
            print(f'Failed process due to {e}')


    def save_df_to_file(_, df: pd.DataFrame, path_to_save):

        """
        
        """

        try:
            saving_functions = {
                '.csv': df.to_csv(path_to_save, index = False),
                '.parquet': df.to_parquet(path_to_save, index = False),
                '.xlsx': df.to_excel(path_to_save, index = False),
                '.xls': df.to_excel(path_to_save, index = False)
            }

            file_extension = Path(path_to_save).suffix

            if file_extension not in saving_functions.keys():
                raise ValueError
            else:
                saving_functions[file_extension]()

        except Exception as e:
            print(f'Failed process due to {e}')


    def extract_raw_data(self, sql_script, save_file_path = None):

        """
    
        """

        try:

            self.cursor = self.conn.cursor()
            self.cursor.execute(sql_script)
            data_frame = as_pandas(self.cursor)
            
            if save_file_path:
                self.save_df_to_file(data_frame, save_file_path)
                print(f'Saved successfully on {save_file_path}!')
                
            return data_frame
        
        except Exception as e:
            print(f'Failed process due to {e}')
