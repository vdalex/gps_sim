# python .\gps_sim.py <email> gnss/data/daily/2023/brdc brdc1800.23n.gz

from ftplib import FTP_TLS
import sys
import gzip
import io
from subprocess import CalledProcessError, run

DEFAULT_LOC = "40.1970,29.0602,100.0"

email = sys.argv[1]
directory = sys.argv[2]
filename = sys.argv[3]

gnss_data = io.BytesIO()

ftps = FTP_TLS(host='gdc.cddis.eosdis.nasa.gov')
ftps.login(user='anonymous', passwd=email)
ftps.prot_p()
ftps.cwd(directory)
ftps.retrbinary("RETR " + filename, gnss_data.write)

gnss_data.seek(0)

e_name = filename.replace('.gz', '')
fp = open(e_name, "wb")
with gzip.open(gnss_data, "rb") as f:
    bindata = f.read()
    fp.write(bindata)
fp.close()

# .\gps-sdr-sim.exe -e .\brdc3540.14n -l 40.1970,29.0602,100.0 -b 8 -o loc_2906.C8  -d 240 -v -T 2023/06/29,08:52:52
cmd = [
    "gps-sdr-sim.exe",
    "-e", e_name,
    "-l", DEFAULT_LOC,
    "-b", "8",
    "-o", "loc_2906.C8",
    "-d", "120"
    "-v"
]
try:
    run(cmd, capture_output=True, check=True).stdout
except CalledProcessError as e:
    raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
