# data-import-example-python

In diesem Repository könnt ihr ein Beispielprogramm in Python zum Datenimport von Comma separated values zu unserer Datenbank finden. Der Code ist nicht perfekt und kann nicht alle möglichen Fehler abfangen, aber kann euch hoffentlich einen Einblick geben, wie das Erfassen von Daten auch anders gehen kann, als sie händisch in phpMyAdmin zu erfassen ;-)

# Ausgangslage

Wir haben die Kundendatenbank geplant und das Modell bereits mit der MySQL-Workbench erstellt. Die Gegenstände und Mitarbeiter/Bewohner sind bereits erfasst. Die Tabellen `Ausleihschein` und `Gegenstand_has_Ausleischein` sind noch zu befüllen. Der Kunde hat uns eine Excel-Tabelle mit den entsprechenden Daten zur Verfügung gestellt.

![alt text](https://github.com/shufflebyte/data-import-example-python/blob/master/misc/musterl%C3%B6sung.png?raw=true)
Abb 1: Unser Datenmodell

# Vorgehen

## Spalten den Tabellen unseres Modells zuordnen

![alt text](https://github.com/shufflebyte/data-import-example-python/blob/master/misc/daten.jpeg?raw=true)

<img src="https://github.com/shufflebyte/data-import-example-python/blob/master/misc/daten.jpeg?raw=true" width="350" title="hover text">
