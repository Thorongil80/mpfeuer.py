# mpfeuer.py 

Leichtgewichtige Python-Skript-Sammlung, mit der regelmäßige Reports aus "MP-Feuer" per eMail ausgesandt werden können.

Im Moment verfügbar:

* G26-Check: Pro Abteilung Liste der Personen die "bei AS anzeigen" angehakt haben mit jeweils Datum der aktuellen G26-Prüfung sowie Datum einer kommenden G26-Prüfung. Achtung: nicht "gültig bis" verwenden, sondern die kommende Prüfung eintragen mit "bestanden = 0", sonst funktioniert dieser Report nicht

* Führerschein: Pro Abteilung Liste der Personen die einen Führerschein mit "C" drin haben. Dann aktuelles und künftiges Datum einer Prüfung die den Kurznamen "FUEHR" hat. Achtung: nicht "gültig bis" verwenden, sondern die kommende Prüfung eintragen mit "bestanden = 0", sonst funktioniert dieser Report nicht


Kommend (Portierung unserer bestehenden weiteren Skripte aus Perl nach Python):

* Telefonliste Report pro Abteilung
* Automatisches Einsatzanlegen mit Einsatzfax (hier: aus Einsatzfax der Leitstelle Karlsruhe)


Author: Thomas Herzog, Freiwillige Feuerwehr Ubstadt-Weiher
