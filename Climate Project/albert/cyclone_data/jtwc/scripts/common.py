COLUMN_NAMES = [
    'BASIN', 'SEASON TC NUMBER', 'TIME (YYYYMMMDDHH)', 'TECHNUM', 'TECH', 'TAU', 'LAT (1/10 degrees)', 'LON (1/10 degrees)', 
    'VMAX (kt)', 'MSLP (MB)', 'TY' , 'RAD' , 'WINDCODE' , 'RAD1' , 'RAD2' , 'RAD3' , 'RAD4' , 'RADP' , 'RRP' , 'MRD' , 'GUSTS' , 'EYE' ,
    'SUBREGION' , 'MAXSEAS' , 'INITIALS' , 'DIR' , 'SPEED' , 'STORMNAME' , 'DEPTH' , 'SEAS' ,
    'SEASCODE' , 'SEAS1' , 'SEAS2' , 'SEAS3' , 'SEAS4']


# Longitude Boundaries (out of 360 degrees)
# =========================

# SOUTH INDIAN
SI_MIN = 30
SI_MAX = 90

# AUSTRALIA
AUS_MIN = SI_MAX
AUS_MAX = 160

# SOUTH PACIFIC
SP_MIN = AUS_MAX
SP_MAX = 240