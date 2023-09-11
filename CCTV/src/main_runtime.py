import os

db_path = f'{os.getcwd()}\database\reportData.csv'

def saveData(liter,licence_plate,isSubsidi):
    # save_path = rospack.get_path("main_process")
    with open(f"database/reportData.csv",mode='a') as wr:
        wr.write(f'{licence_plate},{liter},{isSubsidi}\n')
        

def callback(data):

    parse_data = data.split(';')
    liter_request = parse_data[0]
    license_plate = parse_data[1]
    status_subsidi = parse_data[2]


    print(f'''
    PLAT NOMOR      : {license_plate}
    Liter Bensin    : {liter_request}
    Subsidi         : {status_subsidi}''')

    saveData(liter_request,license_plate,status_subsidi)

    # openRelay(liter_request)
    # print(parse_data)

def openRelay(liter_request):
    sensor_flow =0 
    if sensor_flow == liter_request:
        pass