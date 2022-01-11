import config
import dbcon

abteilungsconfig = dbcon.abteilungsconfig()

for p in dbcon.dateien_stettfeld():
  print(p)