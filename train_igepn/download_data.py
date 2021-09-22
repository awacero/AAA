 
from get_mseed_data import get_mseed_utils as gmutils
from get_mseed_data import get_mseed
import pandas as pd
from obspy import UTCDateTime 

network = "EC"
location = ""
channel = "BHZ"
mseed_client_id="ARCLINK"
mseed_server_config_file = "./server_configuration.json"
output_folder = "./mseed_data"




mseed_server_param = gmutils.read_config_file(mseed_server_config_file)

client = get_mseed.choose_service(mseed_server_param[mseed_client_id])

tags = pd.read_csv("./etiquetas_2019.csv")

print(tags.head())

for i,t in tags.iloc[:10].iterrows():
    start_time_string = "%s-%02d-%02d %02d:%02d:%02d" %(t['Year'], t['Month'],t['Day'],t['HourStart'],t['MinStart'],t['SegStart'] )
    end_time_string = "%s-%02d-%02d %02d:%02d:%02d" %(t['Year'], t['Month'],t['Day'],t['HourEnd'],t['MinEnd'],t['SegEnd'] )
    station = t['Station']
    start_time = UTCDateTime(start_time_string) 
    end_time = UTCDateTime(end_time_string)
    file_code = "%s.%s.%s.%s.%s" %(network,station,location,channel,start_time.strftime("%Y.%m.%d.%H%M%S")) 
    try:
        temp_stream=get_mseed.get_stream(mseed_client_id,client,network,station,location,channel,start_time=start_time,end_time=end_time)
        temp_stream.write("%s/%s.mseed" %(output_folder,file_code))
    except:
        print("Error in get_stream or write")        

    print(start_time,end_time)
