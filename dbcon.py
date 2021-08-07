import config
import datetime
import firebirdsql

def connect():
  conn = firebirdsql.connect(
    host=config.db_host,
    database=config.db_path,
    port=config.db_port,
    user=config.db_user,
    password=config.db_pass,
	charset=config.db_char
  )
  return conn

def disconnect(conn):
  conn.close

def abteilungen():
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT ABT_ID, ABT_NAME_LANG from ABT_STAMM")
  abteilungen = cur.fetchall()
  disconnect(conn)
  return abteilungen
  
def persons_g26():
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT PER_ID, ABT_NAME_LANG, PER_ANREDE, PER_NACHNAME, PER_VORNAME FROM per_stamm as p inner join abt_stamm as a on p.PER_ABT_INDEX = a.ABT_ID where per_asu_tauglich = 1 and PER_ARCHIV_DAT is null order by PER_NACHNAME, PER_VORNAME")
  persons = cur.fetchall()
  disconnect(conn)
  return persons

def persons_fuehr():
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT PER_ID, ABT_NAME_LANG, PER_ANREDE, PER_NACHNAME, PER_VORNAME, PER_FUEHRERSCHEIN FROM per_stamm as p inner join abt_stamm as a on p.PER_ABT_INDEX = a.ABT_ID where PER_FUEHRERSCHEIN is not null and PER_ARCHIV_DAT is null order by PER_NACHNAME, PER_VORNAME")
  persons = cur.fetchall()
  disconnect(conn)
  return persons

def pruefokdat_g26(personid):
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT max(PER_PRUEF_DAT) from PER_PRUEF where per_index = '" + personid + "' and per_pruef_ok = 1 and per_pruef_lang like '%G26%'");
  pruef_ok = cur.fetchall()
  disconnect(conn) 
  if pruef_ok :
    pruefokdat = pruef_ok[0]
  disconnect(conn)
  return pruefokdat

def pruefokdat_fuehr(personid):
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT max(PER_PRUEF_DAT) from PER_PRUEF where per_index = '" + personid + "' and per_pruef_ok = 1 and per_pruef_kurz = 'FUEHR'");
  pruef_ok = cur.fetchall()
  disconnect(conn) 
  if pruef_ok :
    pruefokdat = pruef_ok[0]
  disconnect(conn)
  return pruefokdat
  
def pruefnextdat_g26(personid, pruefokdat=None):
  conn = connect()
  cur = conn.cursor()
  if isinstance(pruefokdat, datetime.date) :
    cur.execute("SELECT min(PER_PRUEF_DAT) from PER_PRUEF where per_index = '" + personid + "' and per_pruef_ok = 0 and per_pruef_dat > '" + pruefokdat[0].isoformat() + "'  and per_pruef_lang like '%G26%'");
  else :
    cur.execute("SELECT min(PER_PRUEF_DAT) from PER_PRUEF where per_index = '" + personid + "' and per_pruef_ok = 0 and per_pruef_lang like '%G26%'");    
  pruef_next = cur.fetchall()
  disconnect(conn) 
  if pruef_next :
    pruefnextdat= pruef_next[0]
  disconnect(conn)
  return pruefnextdat

def pruefnextdat_fuehr(personid, pruefokdat=None):
  conn = connect()
  cur = conn.cursor()
  if isinstance(pruefokdat, datetime.date) :
    cur.execute("SELECT min(PER_PRUEF_DAT) from PER_PRUEF where per_index = '" + personid + "' and per_pruef_ok = 0 and per_pruef_dat > '" + pruefokdat[0].isoformat() + "'  and per_pruef_kurz = 'FUEHR'");
  else :
    cur.execute("SELECT min(PER_PRUEF_DAT) from PER_PRUEF where per_index = '" + personid + "' and per_pruef_ok = 0 and per_pruef_kurz = 'FUEHR'");    
  pruef_next = cur.fetchall()
  disconnect(conn) 
  if pruef_next :
    pruefnextdat= pruef_next[0]
  disconnect(conn)
  return pruefnextdat


def abteilungsconfig():
  map = {}
  abt = abteilungen()
  for a in abt:
    try:
      map[a[1]] = config.ConfigSectionMap(a[1])
    except:
      print("no config section for " + a[1])
  return map

def personen():
  map = {}
  abt = abteilungen()
  for a in abt:
    map[a[1]] = []
  return map
