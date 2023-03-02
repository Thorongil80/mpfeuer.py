import config
import mailer
import datetime
import dbcon
from dateutil.relativedelta import *
from datetime import date

personen = dbcon.personen()
abteilungsconfig = dbcon.abteilungsconfig()

for p in dbcon.persons_fuehr():
  person = {}
  person["id"] = str(p[0])
  person["abteilung"] = str(p[1])
  person["anrede"] = str(p[2])
  person["name"] = str(p[3])
  person["vorname"] = p[4]
  person["fuehrerschein"] = p[5]
  person["geburtstag"] = p[6]
  person["pruefokdat"] = "N/A"
  person["pruefnextdat"] = "N/A"
  person["ungueltig"] = ""
  pruefokdat = dbcon.pruefokdat_fuehr(p[0])
  if isinstance(pruefokdat[0], datetime.date):
    person["pruefokdat"] = pruefokdat[0].isoformat() 
    pruefnextdat = dbcon.pruefnextdat_fuehr(person["id"], pruefokdat)
    if isinstance(pruefnextdat[0], datetime.date):
      person["pruefnextdat"] = pruefnextdat[0].isoformat()
      today = datetime.date.today()
      if pruefnextdat[0] < today :
        person["ungueltig"] = "<font color=red>ung&uuml;ltig</font>"
      else:
        if pruefnextdat[0] < today+relativedelta(months=3) :
          person["ungueltig"] = "<font color=orange>kontaktieren!</font>"
    else:
      person["pruefnextdat"] = "N/A"  
      person["ungueltig"] = "<font color=red>ung&uuml;ltig</font>"
  else :
    pruefnextdat = dbcon.pruefnextdat_fuehr(person["id"])
    if isinstance(pruefnextdat[0], datetime.date):
      person["pruefnextdat"] = pruefnextdat[0].isoformat()
      today = datetime.date.today()
      if pruefnextdat[0] < today :
        person["ungueltig"] = "<font color=red>ung&uuml;ltig</font>"
      else:
        if pruefnextdat[0] < today+relativedelta(months=3) :
          person["ungueltig"] = "<font color=orange>kontaktieren!</font>"
    else :
      person["pruefnextdat"] = "N/A"  
      person["ungueltig"] = "<font color=red>ung&uuml;ltig</font>"
  
  if abteilungsconfig[person["abteilung"]]["send_fuehr"] == "1":
    person["fuehrerschein"] = person["fuehrerschein"].replace("C1", "XX")
    person["fuehrerschein"] = person["fuehrerschein"].replace("c1", "XX")
    
    # if it is a C1 only driver, overwrite ungueltig by green "U50"
    if not "C" in person["fuehrerschein"] and "XX" in person["fuehrerschein"] :
      if person["geburtstag"] >= today+relativedelta(years=-50) :
        person["ungueltig"] = "<font color=green>U50</font>"
     # if person["geburtstag"] >= today+relativedelta(months=-3,years=-50) :
     #   person["ungueltig"] = "<font color=orange>kontaktieren! bald 50!</font>"
    if "C" in person["fuehrerschein"] or (abteilungsconfig[person["abteilung"]]["include_c1_drivers"] == "1" and "XX" in person["fuehrerschein"] ) :
      person["fuehrerschein"] = person["fuehrerschein"].replace("XX", "C1")
      personen[person["abteilung"]].append(person)
 
print("DEBUG: ================= personen dict         ================= " )
print(personen)
print("DEBUG: ================= abteilungsconfig dict ================= ")
print(abteilungsconfig)


for k in personen.keys():
  mailer.send_mail_fuehr(k, personen[k])



def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    return from_date - relativedelta(years=years)