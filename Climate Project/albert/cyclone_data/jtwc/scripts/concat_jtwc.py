import os
import pandas as pd

## ALL COLUMN NAMES IN JTWC DATA


## HAVE TO ADD JUNK COLUMNS FOR NOTES PRESENT IN THE CSV SO PARSING DOESNT BREAK FROM TOO MANY COLUMS


def concat_jtwc_dat(basin_path, output_path):
    column_names = [
    'BASIN', 'SEASON TC NUMBER', 'TIME (YYYYMMMDDHH)', 'TECHNUM', 'TECH', 'TAU', 'LAT (1/10 degrees)', 'LON (1/10 degrees)', 
    'VMAX (kt)', 'MSLP (MB)', 'TY' , 'RAD' , 'WINDCODE' , 'RAD1' , 'RAD2' , 'RAD3' , 'RAD4' , 'RADP' , 'RRP' , 'MRD' , 'GUSTS' , 'EYE' ,
    'SUBREGION' , 'MAXSEAS' , 'INITIALS' , 'DIR' , 'SPEED' , 'STORMNAME' , 'DEPTH' , 'SEAS' ,
    'SEASCODE' , 'SEAS1' , 'SEAS2' , 'SEAS3' , 'SEAS4']

    num_junk = 0
    
    full_df = None
    for year_folder in sorted(os.listdir(basin_path)):
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
                        segment_df = pd.read_csv(datafile_path, names=column_names, header=None)
                        success = True
                    except pd.errors.ParserError:
                        num_junk += 1
                        column_names.append(f'JUNK{num_junk}')
                if full_df is None:
                    full_df = segment_df
                else:
                    full_df = pd.concat([full_df, segment_df])
    full_df.to_csv(output_path, index=False)


if __name__ == '__main__':
    # e.g. NWP_PATH = 'cyclone_data/jtwc/NWP'
    basin_path = input('Enter path of full basin data folder relative to ./albert/ folder: ')
    output_path = input('Enter path where you would like output .csv to be placed (including filename): ')
    concat_jtwc_dat(basin_path, output_path)