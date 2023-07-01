# python .\gps_sim.py <email>

from ftplib import FTP_TLS
import sys
import gzip
import io
from subprocess import CalledProcessError, run
from datetime import datetime, timezone

HOST_NAME = "gdc.cddis.eosdis.nasa.gov"
DEFAULT_LOC = "40.1970,29.0602,100.0"

# Generate directory and file names based on current date and time
dt_now = datetime.now(timezone.utc)
day_of_year = dt_now.strftime("%j")
year = dt_now.strftime("%y")
date = dt_now.strftime("%d%m%y")

ftp_directory = f"gnss/data/daily/20{year}/brdc"
ftp_filename = f"brdc{day_of_year}0.{year}n.gz"
nav_filename = ftp_filename.replace('.gz', '')
samples_filename = f"loc_{date}.C8"

email = sys.argv[1]
# directory = sys.argv[2]
# filename = sys.argv[3]

nav_data = io.BytesIO()

print(f"Downloading navigation file for {date} from {HOST_NAME} ...")

ftps = FTP_TLS(host=HOST_NAME)
ftps.login(user='anonymous', passwd=email)
ftps.prot_p()
ftps.cwd(ftp_directory)
ftps.retrbinary("RETR " + ftp_filename, nav_data.write)

nav_data.seek(0)


fp = open(nav_filename, "wb")
with gzip.open(nav_data, "rb") as f:
    bindata = f.read()
    fp.write(bindata)
fp.close()

print(f"Navigation file saved as {nav_filename}")

print("Generating data samples for GPS signal simulation ...")

# .\gps-sdr-sim.exe -e .\brdc3540.14n -l 40.1970,29.0602,100.0 -b 8 -o loc_2906.C8  -d 240 -v -T 2023/06/29,08:52:52
cmd = [
    "gps-sdr-sim.exe",
    "-e", nav_filename,
    "-l", DEFAULT_LOC,
    "-b", "8",
    "-o", samples_filename,
    "-d", "120"
]
try:
    run(cmd, capture_output=True, check=True).stdout
    print(f"Data samples saved as {samples_filename}")
except CalledProcessError as e:
    raise RuntimeError(
        f"Failed to generate gps data: {e.stderr.decode()}") from e
