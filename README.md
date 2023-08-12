# Application to generate samples for GPS simulation using HackRF PortaPack

Application downloads navigation data in RINEX format from NASA ftp server and generates data samples for GPS simulation using HackRF PortaPack

Usage:

```bash
python gps_sim.py <email>
```

where email - registration email on https://cddis.nasa.gov

Output example:
```bash
Downloading navigation file for 010723 from gdc.cddis.eosdis.nasa.gov ...
Navigation file saved as brdc1820.23n
Generating data samples for GPS signal simulation ...
Data samples saved as loc_010723.C8
```

## What is the BRDC (and Institut für Angewandte Geodaesie) navigation file?

The file https://cddis.gsfc.nasa.gov/archive/gnss/data/daily/yyyy/ddd/yyn/brdcddd0.yyn.Z 

is the daily broadcast ephemeris file. This file is a merge of the individual site navigation files into one, non-redundant file that can be utilized by users instead of the many individual navigation files.

yyyy is the 4-digit year

ddd is the three-digit day of year and yy is the two-digit year

![image info](media/daily_brdc.png)


These files are also available in yearly subdirectories of https://cddis.nasa.gov/archive/gnss/data/daily/yyyy/brdc/.

Example: https://cddis.nasa.gov/archive/gnss/data/daily/2023/brdc/brdc1800.23n.gz

![image info](media/yearly_brdc.png)

## BRDC archive access

https://cddis.nasa.gov/Data_and_Derived_Products/CDDIS_Archive_Access.html


## Other gps/gnss data servers

https://www.unavco.org/data/gps-gnss/file-server/file-server.html

https://www.lantmateriet.se/en/geodata/gps-geodesi-och-swepos/swepos/swepos-services/post-processing/rinex-data---daily-files/

https://incors.in.gov/data.aspx



## Python RINEX parsers

https://pypi.org/project/RinexParser/

https://pypi.org/project/georinex/

## gps-sdr-sim

gps-sdr-sim.exe source code https://github.com/osqzss/gps-sdr-sim

## How to validate generated samples without hardware 

Just use gnss-sdr :) https://gnss-sdr.org/

```bash
gnss-sdr --config_file=./rec.conf
Initializing GNSS-SDR v0.0.16 ... Please wait.
Logging will be written at "/tmp"
Use gnss-sdr --log_dir=/path/to/log to change that.
RF Channels: 1
Starting a TCP/IP server of RTCM messages on port 2101
The TCP/IP server of RTCM messages is up and running. Accepting connections ...
Processing file ./loc_120823.C8, which contains 1247480000 samples (1247480000 bytes)
<skipped>
First position fix at 2023-Aug-12 00:01:54.100000 UTC is Lat = 40.197 [deg], Long = 29.0602 [deg], Height= 89.7712 [m]
Current receiver time: 2 min 14 s
Position at 2023-Aug-12 00:01:54.500000 UTC using 7 observations is Lat = 40.197006776 [deg], Long = 29.060217486 [deg], Height = 91.299 [m]
Velocity: East: 0.228 [m/s], North: -0.256 [m/s], Up = -0.307 [m/s]
Position at 2023-Aug-12 00:01:55.000000 UTC using 7 observations is Lat = 40.196991180 [deg], Long = 29.060181830 [deg], Height = 88.543 [m]
Velocity: East: -0.042 [m/s], North: 0.208 [m/s], Up = 0.061 [m/s]
Position at 2023-Aug-12 00:01:55.500000 UTC using 7 observations is Lat = 40.197015512 [deg], Long = 29.060195598 [deg], Height = 90.012 [m]
Velocity: East: 0.151 [m/s], North: -0.097 [m/s], Up = 0.535 [m/s]
Position at 2023-Aug-12 00:01:56.000000 UTC using 7 observations is Lat = 40.197001863 [deg], Long = 29.060196420 [deg], Height = 95.545 [m]
Velocity: East: 0.180 [m/s], North: -0.052 [m/s], Up = -0.447 [m/s]
Position at 2023-Aug-12 00:01:56.500000 UTC using 7 observations is Lat = 40.197007071 [deg], Long = 29.060187157 [deg], Height = 90.483 [m]
Velocity: East: -0.110 [m/s], North: 0.143 [m/s], Up = 0.787 [m/s]
<skipped>
```

Config file example for data samples file loc_120823.C8

rec.conf
```
[GNSS-SDR]

;######### GLOBAL OPTIONS ##################
GNSS-SDR.internal_fs_sps=2600000

;######### SIGNAL_SOURCE CONFIG ############
SignalSource.implementation=File_Signal_Source
SignalSource.filename=./loc_120823.C8
SignalSource.item_type=ibyte
SignalSource.sampling_frequency=2600000
SignalSource.samples=0

;######### SIGNAL_CONDITIONER CONFIG ############
SignalConditioner.implementation=Signal_Conditioner
DataTypeAdapter.implementation=Ibyte_To_Complex

;######### CHANNELS GLOBAL CONFIG ############
Channels_1C.count=10
Channels.in_acquisition=10
Channel.signal=1C

;######### ACQUISITION GLOBAL CONFIG ############
Acquisition_1C.implementation=GPS_L1_CA_PCPS_Acquisition
Acquisition_1C.item_type=gr_complex
Acquisition_1C.pfa=0.01
Acquisition_1C.doppler_max=10000
Acquisition_1C.doppler_step=250
Acquisition_1C.blocking=true

;######### TRACKING GLOBAL CONFIG ############
Tracking_1C.implementation=GPS_L1_CA_DLL_PLL_Tracking
Tracking_1C.item_type=gr_complex
Tracking_1C.pll_bw_hz=40.0;
Tracking_1C.dll_bw_hz=4.0;

;######### TELEMETRY DECODER GPS CONFIG ############
TelemetryDecoder_1C.implementation=GPS_L1_CA_Telemetry_Decoder

;######### OBSERVABLES CONFIG ############
Observables.implementation=Hybrid_Observables

;######### PVT CONFIG ############
PVT.implementation=RTKLIB_PVT
PVT.positioning_mode=Single
PVT.output_rate_ms=100
PVT.display_rate_ms=500
PVT.iono_model=Broadcast
PVT.trop_model=Saastamoinen
PVT.flag_rtcm_server=true
PVT.flag_rtcm_tty_port=false
PVT.rtcm_dump_devname=/dev/pts/1
PVT.rtcm_tcp_port=2101
PVT.rtcm_MT1019_rate_ms=5000
PVT.rtcm_MT1077_rate_ms=1000
PVT.rinex_version=2
```




