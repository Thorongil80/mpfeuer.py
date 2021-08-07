import config
import mailer
import datetime
import dbcon
from dateutil.relativedelta import *

personen = dbcon.personen()
abteilungsconfig = dbcon.abteilungsconfig()

for p in dbcon.persons_g26():
  person = {}
  person["id"] = str(p[0])
  person["abteilung"] = str(p[1])
  person["anrede"] = str(p[2])
  person["name"] = str(p[3])
  person["vorname"] = p[4]
  person["pruefokdat"] = "N/A"
  person["pruefnextdat"] = "N/A"
  person["ungueltig"] = ""
  pruefokdat = dbcon.pruefokdat_g26(p[0])
  if isinstance(pruefokdat[0], datetime.date):
    person["pruefokdat"] = pruefokdat[0].isoformat() 
    pruefnextdat = dbcon.pruefnextdat_g26(person["id"], pruefokdat)
    if isinstance(pruefnextdat[0], datetime.date):
      person["pruefnextdat"] = pruefnextdat[0].isoformat()
      today = datetime.date.today()
      if pruefnextdat[0] < today :
        person["ungueltig"] = "<font color=red>ung&uuml;ltig</font>"
      else:
        if pruefnextdat[0] < today+relativedelta(months=3) :
          person["ungueltig"] = "<font color=orange>einberufen!</font>"
  else :
    pruefnextdat = dbcon.pruefnextdat_g26(person["id"])
    if isinstance(pruefnextdat[0], datetime.date):
      person["pruefnextdat"] = pruefnextdat[0].isoformat()
      today = datetime.date.today()
      if pruefnextdat[0] < today :
        person["ungueltig"] = "<font color=red>ung&uuml;ltig</font>"
      else:
        if pruefnextdat[0] < today+relativedelta(months=3) :
          person["ungueltig"] = "<font color=orange>einberufen!</font>"
    else :
      person["pruefnextdat"] = "N/A"  
      person["ungueltig"] = "<font color=red>ung&uuml;ltig</font>"
  
  if abteilungsconfig[person["abteilung"]]["send_g26"] == "1":
    personen[person["abteilung"]].append(person)
 
print("DEBUG: ================= personen dict         ================= " )
print(personen)
print("DEBUG: ================= abteilungsconfig dict ================= ")
print(abteilungsconfig)


for k in personen.keys():
  mailer.send_mail_g26(k, personen[k])