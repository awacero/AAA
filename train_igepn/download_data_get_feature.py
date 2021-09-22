 
from get_mseed_data import get_mseed_utils as gmutils
from get_mseed_data import get_mseed
import pandas as pd
from obspy import UTCDateTime 

import sys
sys.path.append("../automatic_processing")

from config import Config
from features import FeatureVector


network = "EC"
location = ""
channel = "BHZ"
mseed_client_id="ARCLINK"
mseed_server_config_file = "./server_configuration.json"
output_folder = "./mseed_data"




mseed_server_param = gmutils.read_config_file(mseed_server_config_file)
client = get_mseed.choose_service(mseed_server_param[mseed_client_id])
tags = pd.read_csv("./etiquetas_2019.csv")

config = Config("../config/general/igepn_newsettings.json")
config.readAndCheck()

output_feature_file = "./feature_igepn_2019.csv"

feature_file = open(output_feature_file,'a+')

features = FeatureVector(config, verbatim=2)

for i,t in tags.iloc[872:1000].iterrows():


    if t['SegStart'] == 60:
        t['SegStart'] = 0
        t['MinStart'] +=1

    if t['SegEnd'] == 60:
        t['SegEnd'] = 0
        t['MinEnd'] +=1

    start_time_string = "%s-%02d-%02d %02d:%02d:%02d" %(t['Year'], t['Month'],t['Day'],t['HourStart'],t['MinStart'],t['SegStart'] )
    end_time_string = "%s-%02d-%02d %02d:%02d:%02d" %(t['Year'], t['Month'],t['Day'],t['HourEnd'],t['MinEnd'],t['SegEnd'] )
    station = t['Station']
    start_time = UTCDateTime(start_time_string) 
    end_time = UTCDateTime(end_time_string)
    file_code = "%s.%s.%s.%s.%s" %(network,station,location,channel,start_time.strftime("%Y.%m.%d.%H%M%S")) 
    print(file_code)
    try:
        temp_stream=get_mseed.get_stream(mseed_client_id,client,network,station,location,channel,start_time=start_time,end_time=end_time)
        fs = temp_stream[0].stats['sampling_rate']
        features.compute(temp_stream[0].data,fs)
        features_string = ', '.join(map(str,features.featuresValues))
        row = "%s, %s , %s \n"% (file_code,t['Type'], features_string)
        feature_file.write(row)
    except Exception as e:
        print("Error in get_stream or write: %s" %str(e))        

    print(start_time,end_time)
