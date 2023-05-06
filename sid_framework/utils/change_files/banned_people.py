from glob import glob
import os
import pandas as pd


def concat_files_xlsx(path):
    all_files = glob(os.path.join(path, '*.xlsx'))
    if len(all_files) > 0:
        df = pd.concat((pd.read_excel(f) for f in all_files))
    else:
        df = pd.DataFrame({'nro_reporte': pd.Series(dtype='str'),
                           'celula': pd.Series(dtype='str'),
                           'documento': pd.Series(dtype='str'),
                           'fecha_impacto': pd.Series(dtype='str')})
    return df
