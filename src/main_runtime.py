import os

db_path = f'{os.getcwd()}\database\reportData.csv'

def saveData(liter,jenis_mobil,licence_plate,isSubsidi):
    # save_path = rospack.get_path("main_process")
    with open(f"database/reportData.csv",mode='a') as wr:
        wr.write(f'{licence_plate},{liter},{isSubsidi},{jenis_mobil}\n')
        

def callback(data):

    parse_data = data.split(';')
    liter_request = parse_data[0]
    jenis_mobil = parse_data[1]
    license_plate = parse_data[2]
    status_subsidi = parse_data[3]


    print(f'''
    Jenis Mobil     : {jenis_mobil}
    PLAT NOMOR      : {license_plate}
    Liter Bensin    : {liter_request}
    Subsidi         : {status_subsidi}''')

    saveData(liter_request,jenis_mobil,license_plate,status_subsidi)

    # openRelay(liter_request)
    # print(parse_data)

def openRelay(liter_request):
    sensor_flow =0 
    if sensor_flow == liter_request:
        pass