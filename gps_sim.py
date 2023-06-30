# python .\gps_sim.py <email> gnss/data/daily/2023/brdc brdc1800.23n.gz

from ftplib import FTP_TLS
import sys
import gzip
import io

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

fp = open(filename.replace('.gz', ''), "wb")
with gzip.open(gnss_data, "rb") as f:
    bindata = f.read()
    fp.write(bindata)
fp.close()
