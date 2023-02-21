# data-import-example-python

In diesem Repository könnt ihr ein Beispielprogramm in Python zum Datenimport von Comma separated values zu unserer Datenbank finden. Der Code ist nicht perfekt und kann nicht alle möglichen Fehler abfangen, aber euch hoffentlich einen Einblick geben, wie das Erfassen von Daten auch anders gehen kann, als sie händisch in phpMyAdmin zu erfassen ;-)

# Ausgangslage

Wir haben die Kundendatenbank geplant und das Modell bereits mit der MySQL-Workbench erstellt. Die **Gegenstände und Mitarbeiter/Bewohner sind bereits in der DB erfasst**. Die Tabellen `Ausleihschein` und `Gegenstand_has_Ausleischein` sind noch zu befüllen. Der Kunde hat uns eine Excel-Tabelle mit den entsprechenden Daten zur Verfügung gestellt.

# Vorgehen

## Spalten den Tabellen unseres Modells zuordnen

Zunächst müssen wir uns im Klaren darüber werden, welche Spalten in welche Tabelle gehören. Die `Ausleihen.xlsx` können wir in die Tabellen `Ausleihschein` und `Gegenstand_has_Ausleihschein` aufteilen.

Die Fremdschlüssel für die Felder `Ausleihender_id`, `Ausgebender_id`, `Pruefender_id` finden wir in der Tabelle `Bewohner` (Da die Mitarbeiter-Tabelle nur die ID der Bewohnertabelle enthält, schauen wir direkt in die Bewohner-Tabelle hinein).

Die Gegenstand ids (gelb) erhalten wir aus der Tabelle `Gegenstand`.
![alt text](https://github.com/shufflebyte/data-import-example-python/blob/master/misc/daten.jpeg?raw=true)

Der Teilauschnitt unseres Modells ist in der folgenden Abbildung zu sehen. Alle anderen Tabellen sind für diesen Import unerheblich.

![alt text](https://github.com/shufflebyte/data-import-example-python/blob/master/misc/modell_ausschnitt.jpeg?raw=true)

## Daten beschaffen

- Die Daten für die `Ausleihen` exportieren wir mit Excel in eine CSV-Datei
- Die Daten für die `Bewohner` erhalten wir als CSV-Export aus PHPMyAdmin
- Die Daten für die `Gegenstände` erhalten wir ebenfalls als CSV-EXport aus PHPMyAdmin

_Hinweis_: Die Excel-CSV hat keine Gänsefüßchen, die CSV-Dateien aus PHPMyAdmin schon... muss man beim Verarbeiten ggf. drauf achten

## Python Code schreiben

_TLDR: Die Pyhton-File liest die Daten der Tabellen ein und baut daraus [Dictionaries](https://www.w3schools.com/python/python_dictionaries.asp). Die Daten für die Tabelle Ausleihschein wird zuerst befüllt. Wir übernehmen hier die Zuteilung der IDs, weil wir diese für die Befüllung der Tabelle Gegenstand_has_Ausleihe benötigen. Am Ende der File wird eine File mit SQL-Code erzeugt, welche wir direkt über PHPMyAdmin oder das Terminal zur Ausführung bringen können. _

### Selbst ausprobieren

1. `sql_code.txt` Datei löschen oder leeren.
2. `main.py` ausführen
3. Falls Tabellen zuvor schon einmal befüllt waren, `TRUNCATE` anwenden und Auto Increment-Value von `Ausleihschein` auf 1 zurücksetzen.

```sql
TRUNCATE [TABLE] table_name;
```

4. SQL-Statements aus `sql_code.txt` kopieren und in PHPMyAdmin ausfüren.

### Tipps

- Niemals den Code auf dem Echtsystem testen
- Code überhaupt erstmal testen
- Die Ergebnisse gründlich auf Plausibilität prüfen, bevor man es auf dem Echtsystem laufen lässt
- Im Code schon die Daten checken
  - Haben die Dicts alle Keys, die ich erwartet habe?
  - Habe ich so viele Dicts raus, wie ich Zeilen habe?
  - Habe ich ausversehen auch die Überschriften mit importiert?
  - Sind Felder nicht existent, leer oder falsch befüllt?
  - Habe ich die Daten entsprechend konvertiert?

Viel Spaß bei eigenen Projekten.
