import os
import pandas as pd

## ALL COLUMN NAMES IN JTWC DATA
from common import COLUMN_NAMES

## HAVE TO ADD JUNK COLUMNS FOR NOTES PRESENT IN THE CSV SO PARSING DOESNT BREAK FROM TOO MANY COLUMS


def concat_jtwc_dat(basin_path, output_path):
    column_names = COLUMN_NAMES
    num_junk = 0
    
    full_df = None
    for year_folder in sorted(os.listdir(basin_path)):
        season_str = str(year_folder).replace("bsh", "").replace("bwp", "")
        full_folder_path = os.path.join(basin_path,  year_folder)
        for data_segment_name in sorted(os.listdir(full_folder_path)):
            datafile_path = os.path.join(full_folder_path, data_segment_name)
            print(datafile_path)
            if os.path.isfile(datafile_path):
                # extensions differ between .txt and .dat but CSV formatting is maintained
                # prevent infinite loops
                success = False
                while num_junk < 100 and not success:
                    try:
                        segment_df = pd.read_csv(datafile_path, names=column_names, header=None, engine='python')
                        segment_df['Season'] = season_str
                        success = True
                    except pd.errors.ParserError as parserError:
                        with open('parseLog.log', 'a') as f:
                            f.write("PARSE ERROR:" + str(parserError) + "\n")
                            f.flush()
                        num_junk += 1
                        column_names = column_names + [f'JUNK{num_junk}']
                else:
                    if full_df is None:
                        full_df = segment_df
                    else:
                        full_df = pd.concat([full_df, segment_df], axis=0, ignore_index=True)
    full_df.to_csv(output_path, index=False)


if __name__ == '__main__':
    # e.g. NWP_PATH = 'cyclone_data/jtwc/NWP'
    basin_path = input('Enter path of full basin data folder relative to ./albert/ folder: ')
    output_path = input('Enter path where you would like output .csv to be placed (including filename): ')
    concat_jtwc_dat(basin_path, output_path)