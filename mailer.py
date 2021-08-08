import dbcon
import config
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import html2text
import datetime


abteilungsconfig = dbcon.abteilungsconfig()


def send_mail_g26(abteilung, personen):
  if personen:
    print("DEBUG: ================= Sending..." + abteilung + "=================")
    print(personen)
	
    receiver_email = abteilungsconfig[abteilung]["to"].strip('"')
    cc_email = abteilungsconfig[abteilung]["cc"].strip('"')
    recipients = [receiver_email] + [cc_email]
    password = config.mail_pass
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Status G26 Abteilung " + abteilung + " - " + datetime.date.today().isoformat()
    message["From"] = config.mail_from
    message["To"] = receiver_email
    message["CC"] = cc_email
    
	
    html = """
    <html>
		<head>
			<style>td,th {padding:5px 10px 5px 10px;}</style>
			<meta charset='utf-8'>
		</head>
		<body>
			<H2>Liste der Atemschutzger&auml;tetr&auml;ger der Abteilung """ + abteilung + """</H2>
			Dies ist eine automatisierte monatliche Mail des Feuerwehrservers, bei Fragen bitte an Thomas Herzog wenden<br><br>
			Die Liste enth&auml;lt alle Personen der Abteilung bei denen 'bei AS anzeigen' angehakt ist.
			<br>Bitte den Haken entfernen sobald die Einsatzkraft keinen Atemschutzdienst mehr leistet.
			<br>Den Haken SETZEN damit die Einsatzkraft k&uuml;nftig in dieser automatischen Liste gef&uuml;hrt wird.<br><br>
			Die Datenpflege f&uuml;r die G26 wird vom Ordnungsamt durchgef&uuml;hrt. Fehlende Pr&uuml;fungen dort kl&auml;ren<br><br>
			G&uuml;ltige G26 = Letzte Pr&uuml;fung mit OK bestanden und kommende Pr&uuml;fung in der Zukunft ist eingetragen in MP-Feuer.<br><br>
			Personal dessen G26 nachweislich bei einer anderen Feuerwehr gef&uuml;hrt wird bitte ignorieren.<br><br>\
			<table style='text-align:left; font-family:Courier New, Courier;'>
				<tr>
					<th colspan = 2>Atemschutzger&auml;tetr&auml;ger<th>Letzte G26
					<th>N&auml;chste G26
					<th>
				</tr>"""
	
    for p in personen:
      html = html + "<tr><td colspan=2>" + p["name"] + "&nbsp;" + p["vorname"] + "<td>" + p["pruefokdat"] + "<td>" + p["pruefnextdat"] + "<td>" + p["ungueltig"] + "</tr>\n"
	
    html = html + """\
			</table>
		</body>
	</html>
	"""
	
    # Create the plain-text and HTML version of your message
    text = html2text.html2text(html)

    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config.mail_server, int(config.mail_port), context=context) as server:
        server.login(config.mail_user, config.mail_pass)
        server.sendmail(
            config.mail_from, recipients, message.as_string()
        )
		
		
def send_mail_fuehr(abteilung, personen):
  if personen:
    print("DEBUG: ================= Sending..." + abteilung + "=================")
    print(personen)
	
    receiver_email = abteilungsconfig[abteilung]["to"].strip('"')
    cc_email = abteilungsconfig[abteilung]["cc"].strip('"')
    recipients = [receiver_email] + [cc_email]
    password = config.mail_pass
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Status Fuehrerscheine Abteilung " + abteilung + " - " + datetime.date.today().isoformat()
    message["From"] = config.mail_from
    message["To"] = receiver_email
    message["CC"] = cc_email
    
	
    html = """
    <html>
		<head>
			<style>td,th {padding:5px 10px 5px 10px;}</style>
			<meta charset='utf-8'>
		</head>
		<body>
		   <H2>Liste der Kameraden mit LKW F&uuml;hrerscheinen der Abteilung""" + abteilung + """</H2>
            Dies ist eine automatisierte monatliche Mail des Feuerwehrservers, bei Fragen bitte an Thomas Herzog wenden<br><br>
            Die Liste enth&auml;lt alle Personen der Abteilung bei denen ein F&uuml;hrerschein mit 'C' in der Bezeichnung gefunden wurde.<br><br>
            Beachtet: C(E) und C1(E) m&uuml;ssen alle 5 Jahre verl&auml;ngert werden.<br>Bei C1(E) bis zum 18.01.2013 ausgestellt gilt dies erst ab dem 50. Geburtstag.<br>
            <i>C1(E) wird aufgrund Fahrzeugbestand nur bei der Abteilung Stettfeld in dieser Auswertung berücksichtigt.</i><br><br>
            Sobald der F&uuml;hrerschein gepr&uuml;ft wurde, so tragt bitte die Untersuchung/Pr&uuml;fung <b>'F&uuml;hrerschein-Ablaufcheck'</b> als <b>'bestanden'</b> und die n&auml;chste <b>entsprechend Ablaufdatum</b> in MP-Feuer ein.<br>
            L&auml;sst ein Kamerad seinen LKW-F&uuml;hrerschein verfallen, so entfernt die F&uuml;hrerscheinklasse bitte in MP-Feuer.<br><br><br> 
			<table style='text-align:left; font-family:Courier New, Courier;'>
				<tr>
					<th colspan = 2>Inhaber
					<th>F&uuml;hrerschein
					<th>Letzter Check
					<th>N&auml;chster Check
					<th>
				</tr>"""
	
    for p in personen:
      html = html + "<tr><td colspan=2>" + p["name"] + "&nbsp;" + p["vorname"] + "<td>" + p["fuehrerschein"] + "<td>" + p["pruefokdat"] + "<td>" + p["pruefnextdat"] + "<td>" + p["ungueltig"] + "</tr>\n"
	
    html = html + """\
			</table>
		</body>
	</html>
	"""
	
    # Create the plain-text and HTML version of your message
    text = html2text.html2text(html)

    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config.mail_server, int(config.mail_port), context=context) as server:
        server.login(config.mail_user, config.mail_pass)
        server.sendmail(
            config.mail_from, recipients, message.as_string()
        )
