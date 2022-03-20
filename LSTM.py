import quandl
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from datetime import datetime
quandl.ApiConfig.api_key = "ti-yR6gd8be4x4yswvy4"

# Pull Raw Data
current_month = datetime.now().strftime('%Y') + '-' + datetime.now().strftime('%m') + '-01'
# List from https://fredaccount.stlouisfed.org/public/datalist/?st=&pageID=1 make sure `RECPROUSM156N` is first in list and not duplicated
features = ["FRED/RECPROUSM156N", "FRED/ACOILBRENTEU","FRED/ACOILWTICO","FRED/AHETPI","FRED/AISRSA","FRED/AUINSA","FRED/AWHAETP","FRED/BAA10Y","FRED/BUSINV","FRED/CANTOT","FRED/CBI","FRED/CDSP","FRED/CES0500000003","FRED/CEU0500000002","FRED/CEU0500000003","FRED/CEU0500000008","FRED/CHNTOT","FRED/CIVPART","FRED/CNP16OV","FRED/COMPNFB","FRED/COMPRNFB","FRED/COMREPUSQ159N","FRED/CPIAUCNS","FRED/CPIAUCSL","FRED/DCOILBRENTEU","FRED/DCOILWTICO","FRED/DDDM01USA156NWDB","FRED/DED1","FRED/DED3","FRED/DED6","FRED/DEXBZUS","FRED/DEXCAUS","FRED/DEXCHUS","FRED/DEXJPUS","FRED/DEXKOUS","FRED/DEXMXUS","FRED/DEXNOUS","FRED/DEXSDUS","FRED/DEXSFUS","FRED/DEXSIUS","FRED/DEXSZUS","FRED/DEXUSAL","FRED/DEXUSEU","FRED/DEXUSNZ","FRED/DEXUSUK","FRED/DGORDER","FRED/DGS10","FRED/DSPIC96","FRED/DSWP1","FRED/DSWP10","FRED/DSWP2","FRED/DSWP3","FRED/DSWP30","FRED/DSWP4","FRED/DSWP5","FRED/DSWP7","FRED/DTWEXB","FRED/DTWEXM","FRED/ECIWAG","FRED/ECOMNSA","FRED/ECOMSA","FRED/EECTOT","FRED/EMRATIO","FRED/ETOTALUSQ176N","FRED/EVACANTUSQ176N","FRED/FEDFUNDS","FRED/FRNTOT","FRED/FYFSGDA188S","FRED/GASREGCOVM","FRED/GASREGCOVW","FRED/GASREGM","FRED/GASREGW","FRED/GCT1501US","FRED/GCT1502US","FRED/GCT1503US","FRED/GERTOT","FRED/GOLDAMGBD228NLBM","FRED/GOLDPMGBD228NLBM","FRED/HCOMPBS","FRED/HDTGPDUSQ163N","FRED/HOABS","FRED/HOANBS","FRED/HOUST","FRED/HPIPONM226N","FRED/HPIPONM226S","FRED/IC4WSA","FRED/INDPRO","FRED/INTDSRUSM193N","FRED/IPBUSEQ","FRED/IPDBS","FRED/IPMAN","FRED/IPMAT","FRED/IPMINE","FRED/IR","FRED/IR10010","FRED/IREXPET","FRED/ISRATIO","FRED/JCXFE","FRED/JPNTOT","FRED/JTS1000HIL","FRED/JTS1000HIR","FRED/JTSHIL","FRED/JTSHIR","FRED/JTSJOL","FRED/JTSJOR","FRED/JTSLDL","FRED/JTSLDR","FRED/JTSQUL","FRED/JTSQUR","FRED/JTSTSL","FRED/JTSTSR","FRED/JTU1000HIL","FRED/JTU1000HIR","FRED/JTUHIL","FRED/JTUHIR","FRED/JTUJOL","FRED/JTUJOR","FRED/JTULDL","FRED/JTULDR","FRED/JTUQUL","FRED/JTUQUR","FRED/JTUTSL","FRED/JTUTSR","FRED/LNS12032194","FRED/LNS12032196","FRED/LNS14027660","FRED/LNS15000000","FRED/LNU05026642","FRED/M12MTVUSM227NFWA","FRED/M2V","FRED/MCOILBRENTEU","FRED/MCOILWTICO","FRED/MCUMFN","FRED/MEHOINUSA646N","FRED/MEHOINUSA672N","FRED/MFGOPH","FRED/MFGPROD","FRED/MNFCTRIRNSA","FRED/MNFCTRIRSA","FRED/MNFCTRMPCSMNSA","FRED/MNFCTRMPCSMSA","FRED/MNFCTRSMNSA","FRED/MNFCTRSMSA","FRED/MYAGM2USM052N","FRED/MYAGM2USM052S","FRED/NAPM","FRED/NAPMBI","FRED/NAPMCI","FRED/NAPMEI","FRED/NAPMEXI","FRED/NAPMII","FRED/NAPMIMP","FRED/NAPMNOI","FRED/NAPMPI","FRED/NAPMPRI","FRED/NAPMSDI","FRED/NILFWJN","FRED/NILFWJNN","FRED/NMFBAI","FRED/NMFBI","FRED/NMFEI","FRED/NMFEXI","FRED/NMFIMI","FRED/NMFINI","FRED/NMFINSI","FRED/NMFNOI","FRED/NMFPI","FRED/NMFSDI","FRED/NROU","FRED/NROUST","FRED/OPHMFG","FRED/OPHNFB","FRED/OPHPBS","FRED/OUTBS","FRED/OUTMS","FRED/OUTNFB","FRED/PAYEMS","FRED/PAYNSA","FRED/PCE","FRED/PCEPI","FRED/PCEPILFE","FRED/PCETRIM12M159SFRBDAL","FRED/PCETRIM1M158SFRBDAL","FRED/PNRESCON","FRED/PNRESCONS","FRED/POP","FRED/POPTHM","FRED/PPIACO","FRED/PRRESCON","FRED/PRRESCONS","FRED/PRS30006013", "FRED/PRS30006023","FRED/PRS84006013","FRED/PRS84006023","FRED/PRS84006163","FRED/PRS84006173","FRED/PRS85006023","FRED/PRS85006163","FRED/PRS85006173","FRED/RCPHBS","FRED/RETAILIMSA","FRED/RETAILIRSA","FRED/RETAILMPCSMNSA","FRED/RETAILMPCSMSA","FRED/RETAILSMNSA","FRED/RETAILSMSA","FRED/RHORUSQ156N","FRED/RIFLPCFANNM","FRED/RPI","FRED/RRSFS","FRED/RSAFS","FRED/RSAFSNA","FRED/RSAHORUSQ156S","FRED/RSEAS","FRED/RSFSXMV","FRED/RSNSR","FRED/RSXFS","FRED/T10Y2Y","FRED/T10Y3M","FRED/T10YFF","FRED/T10YIEM","FRED/T5YIEM","FRED/T5YIFR","FRED/TB3SMFFM","FRED/TCU","FRED/TDSP","FRED/TEDRATE","FRED/TLCOMCON","FRED/TLCOMCONS","FRED/TLNRESCON","FRED/TLNRESCONS","FRED/TLPBLCON","FRED/TLPBLCONS","FRED/TLPRVCON","FRED/TLPRVCONS","FRED/TLRESCON","FRED/TLRESCONS","FRED/TOTBUSIMNSA","FRED/TOTBUSIRNSA","FRED/TOTBUSMPCIMNSA","FRED/TOTBUSMPCIMSA","FRED/TOTBUSMPCSMNSA","FRED/TOTBUSMPCSMSA","FRED/TOTBUSSMNSA","FRED/TOTBUSSMSA","FRED/TOTDTEUSQ163N","FRED/TRFVOLUSM227NFWA","FRED/TTLCON","FRED/TTLCONS","FRED/U4RATE","FRED/U4RATENSA","FRED/U6RATE","FRED/U6RATENSA","FRED/UEMPMED","FRED/UKTOT","FRED/ULCBS","FRED/ULCMFG","FRED/ULCNFB","FRED/UNRATE","FRED/USAGDPDEFAISMEI","FRED/USAGDPDEFQISMEI","FRED/USAGFCFADSMEI","FRED/USAGFCFQDSMEI","FRED/USAGFCFQDSNAQ","FRED/USARECDM","FRED/USARGDPC","FRED/USASACRAISMEI","FRED/USASACRMISMEI","FRED/USASACRQISMEI","FRED/USPRIV","FRED/USRECD","FRED/USRECDM","FRED/USSLIND","FRED/USSTHPI","FRED/WCOILBRENTEU","FRED/WCOILWTICO","FRED/WHLSLRIRNSA","FRED/WHLSLRIRSA"]
dataframe = quandl.get(features, start_date="1970-01-01", end_date=current_month, collapse="monthly")

# Save to Machine For Quick Reuse
# pd.to_pickle(dataframe, 'data/dataframe.dat')

# Load Raw Data From Local Drive
# dataframe = pd.read_pickle('data/dataframe.dat')

# Interpolate Data
dataframe = dataframe.interpolate(method='time', limit_direction='both')

# Normalize Dataset
min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(dataframe)
dataframe = pd.DataFrame(np_scaled, columns = dataframe.columns)
dataset = dataframe.values

# Split Data Into Training and Test
split = 440
train = dataset[:split, :]
test = dataset[split:, :]
all_X = dataset[:, 1:]
all_Y = dataset[:, 0]

# Split Data Into Inputs and Output
train_X, train_Y = train[:, 1:], train[:, 0]
test_X, test_Y = test[:, 1:], test[:, 0]

# Reshape Input to be 3D [Samples, Timesteps, Features]
train_X = train_X.reshape(train_X.shape[0], 1, train_X.shape[1])
test_X = test_X.reshape(test_X.shape[0], 1, test_X.shape[1])

# Build Model
multi_step_model = tf.keras.models.Sequential()
multi_step_model.add(tf.keras.layers.LSTM(20, input_shape=(train_X.shape[1], train_X.shape[2])))
multi_step_model.add(tf.keras.layers.Dense(1))
multi_step_model.compile(loss='mae', optimizer='adam')

# Train Model
multi_step_model.fit(train_X, train_Y, epochs=30, batch_size=12, validation_data=(test_X, test_Y), verbose=2, shuffle=False)

# Make Test Prediction
prediction_Y = multi_step_model.predict(test_X)
plt.plot(test_Y, label='actual')
plt.plot(prediction_Y, label='predicted')
plt.legend()
plt.show()

# Make Future Prediction (Need to Use "Windowing" to Prepare Data First)
all_X = all_X.reshape(all_X.shape[0], 1, all_X.shape[1])
prediction_Y = multi_step_model.predict(all_X)
plt.plot(prediction_Y, label='predicted')
plt.legend()
plt.show()