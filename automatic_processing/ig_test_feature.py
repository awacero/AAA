
from obspy import read

from config import Config
from features import FeatureVector

data_mseed=read("../train_igepn/20190904052127_EC_GYGU_HNZ_BP4_0.1_40.mseed")
data = data_mseed[0].data
# Change if you want your screen to keep quiet
# 0 = quiet
# 1 = in between
# 2 = detailed information
verbatim = 2

# Init project with configuration file
# config = Config('../config/general/newsettings_20.json', verbatim=verbatim)  #Fish
#config = Config('../config/general/test_igepn.json', verbatim=verbatim)  #Merapi
config = Config("../config/general/igepn_newsettings.json")
config.readAndCheck()


# Feature extraction for each data
features = FeatureVector(config, verbatim=verbatim)

features.compute(data,100)
for i,f in enumerate(features.featuresValues):
    print(i,f)
            
            
