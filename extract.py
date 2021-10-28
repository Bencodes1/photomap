# from exif import Image
import PIL
import exifread
import os


# img_path = '/Users/benchalmers/Documents/photomap/pics/IMG_9194.TIFF'
directory = '/Users/benchalmers/Documents/photomap/pics/'


# Converts GPS coords from deg/min/sec to decimal
def decimal_coords(coords, ref):
    decimal_degrees = float(coords[0]) + float(coords[1])/60 + convert_to_float(coords[2])/3600
    if ref == 'S' or ref == 'W':
        decimal_degrees *= -1
    return decimal_degrees


# Custom float conversion since fractions in GPS data causing bugs
def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


# loop thru directory extracting relevant data for files,
# output dict of image: tuple
def files_puller():
    data_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.tiff'): # or filename.endswith('.mov')
            img_path = os.path.join(directory, filename)
            data_dict[filename] = pulling_vars(img_path)  
        else: 
            continue
    return(data_dict)


def pulling_vars(img_path):
    with open(img_path, 'rb') as src:
        # print ("Source Image:", src.name)
        tags = exifread.process_file(src)

        # These tell us N/S and E/W to determine whether decimal
        # Needs to be negative or not (arg in decimal_coords). 
        gps_longref = str(tags['GPS GPSLongitudeRef'])
        gps_latref = str(tags['GPS GPSLatitudeRef'])
        
        # Decimal latitude
        gps_lat_temp = str(tags['GPS GPSLatitude'])
        gps_lat_temp = gps_lat_temp.replace("[","")
        gps_lat_temp = gps_lat_temp.replace("]","")
        gps_lat_temp = gps_lat_temp.split(",")
        lat = decimal_coords(gps_lat_temp, gps_latref)
        
        #Decimal longitude
        gps_long_temp = str(tags['GPS GPSLongitude'])
        gps_long_temp = gps_long_temp.replace("[","")
        gps_long_temp = gps_long_temp.replace("]","")
        gps_long_temp = gps_long_temp.split(",")
        long = decimal_coords(gps_long_temp, gps_longref)

        # Elevation (meters)
        ele = convert_to_float(str(tags['GPS GPSAltitude']))

        # Date Taken
        date = str(tags['EXIF DateTimeOriginal'])
        vars_dict = {'lat':lat, 'long':long, 'ele':ele, 'date':date}
        # print(img_path)
        # print(vars_dict)
        return(vars_dict)


print(files_puller())




# Next steps: 

# 3. make it so it loops through file list and gets it from all 
#     images/files if they have exif
# 4. output from this file should be dictionary: image filename as key, tuple of GPS and alt as value 