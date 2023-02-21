import csv
import datetime

path = './data/'


def pretty_dict(d, indent=4):
    """Pretty print a dictionary(cannot handle arrays of dicts)

    Args:
        d (dict): Dictionary to print
        indent (int, optional): Indentation factor. Defaults to 4.
    """
    print("{")
    for key, value in d.items():
        if isinstance(value, dict):
            print(' ' * indent + str(key) + ': ' + value)
        else:
            print(' ' * indent + str(key) + ': ' + str(value))
    print("}")


def extract_citizens(filename, file_path):
    """Imports citizens from csv file (exported from SQL table Bewohner)

    Args:
        filename (string): The filename
        file_path (string): The path to all data files in this project

    Returns:
        dict[]: Array of dictionaries
    """
    result_set = []
    with open(file_path + filename, 'r') as fd:
        reader = csv.reader(fd, delimiter=',')
        next(reader)  # skip first line
        # print(reader)
        for row in reader:
            # print(row)
            new_dict = {
                "id": row[0],
                "vorname": row[1],
                "nachname": row[2]
            }
            result_set.append(new_dict)
    return result_set


def extract_lendings(filename, file_path):
    """Imports lendings from csv file

    Args:
        filename (string): The filename
        file_path (string): The path to all data files in this project

    Returns:
        dict[]: Array of dictionaries
    """
    result_set = []
    with open(file_path + filename, 'r') as fd:
        reader = csv.reader(fd, delimiter=';', quotechar='"')
        next(reader)  # skip first line
        # print(reader)
        actId = 1
        for row in reader:
            # print("lendings: ", row)

            # parse items
            items = []
            if row[6] is not None and len(row[6]) > 0:
                items.append(row[6])

            if row[7] is not None and len(row[7]) > 0:
                items.append(row[7])

            if row[8] is not None and len(row[8]) > 0:
                items.append(row[8])

            if row[9] is not None and len(row[9]) > 0:
                items.append(row[9])

            new_dict = {
                "id": actId,
                "ausleihender": row[0],
                "ausgebender": row[1],
                "annehmender": row[2],
                "leihdatum": row[3],
                "rueckgabe_vereinbart": row[4],
                "rueckgabe_tatsaechlich": row[5],
                "notizen": row[10],
                "items": items
            }
            actId = actId + 1
            # print("dict: ", new_dict)
            result_set.append(new_dict)

    return result_set


def extract_items(filename, file_path):
    """Imports items from csv file (exported from SQL table Gegenstände)

    Args:
        filename (string): The filename
        file_path (string): The path to all data files in this project

    Returns:
        dict[]: Array of dictionaries
    """
    result_set = []
    with open(file_path + filename, 'r') as fd:
        reader = csv.reader(fd, delimiter=',')
        next(reader)  # skip first line
        for row in reader:
            new_dict = {
                "id": row[0],
                "beschreibung": row[3],
            }
            result_set.append(new_dict)
    return result_set


def format_date(date):
    """Transforms german date string to mysql date string

    Args:
        date (string): german date format

    Returns:
        string: Date in mysql date format
    """
    return datetime.datetime.strptime(date, '%d.%m.%y').strftime('%Y-%m-%d')


def ausleihschein(citizens, lendings, items):
    """Creates dictionary-arrays for lendings and lendings_items

    Args:
        citizens dict[]: Bewohner Dictionary
        lendings dict[]: Ausleihschein Dictionary
        items dict[]: Gegenstand_has_Ausleihschein Dictionary

    Returns:
        dict[]: Array of dictionaries for lendings
        dict[]: Array of dictionaries for lendings_items
    """
    lendings_import = []
    item_lendings = []
    for lending in lendings:
        new_lending = {}
        for citizen in citizens:
            # need for special converting Lt. ....
            if lending["ausgebender"].startswith("Lt."):
                parts = lending["ausgebender"].split(sep=" ")
                lending["ausgebender"] = " ".join(parts[1:]) + ", " + parts[0]

            if lending["annehmender"].startswith("Lt."):
                parts = lending["annehmender"].split(sep=" ")
                lending["annehmender"] = " ".join(parts[1:]) + ", " + parts[0]

            if lending["ausleihender"].startswith("Lt."):
                parts = lending["ausleihender"].split(sep=" ")
                lending["ausleihender"] = " ".join(parts[1:]) + ", " + parts[0]

            # general case
            if lending["ausleihender"] == (citizen["vorname"] + ' ' + citizen["nachname"]):
                new_lending["Ausleihender_id"] = citizen["id"]

            if lending["ausgebender"] == (citizen["vorname"] + ' ' + citizen["nachname"]):
                new_lending["Ausgebender_id"] = citizen["id"]

            if lending["annehmender"] == (citizen["vorname"] + ' ' + citizen["nachname"]):
                new_lending["Pruefender_id"] = citizen["id"]

        # date formatting: 1901-01-01 YYYY-MM-DD
        try:
            if lending["leihdatum"]:
                new_lending["ausleihe_datum"] = format_date(
                    lending["leihdatum"])
            if lending["rueckgabe_vereinbart"]:
                new_lending["vereinbarte_rueckgabe"] = format_date(
                    lending["leihdatum"])
            if lending["rueckgabe_tatsaechlich"]:
                new_lending["tatsaechliche_rueckgabe"] = format_date(
                    lending["leihdatum"])

        # parse errors für Daten abfangen
        except ValueError as err:
            print(err)
            print(lending["leihdatum"], lending["rueckgabe_vereinbart"],
                  lending["rueckgabe_tatsaechlich"],)
            # raise

        # notizen
        if lending["notizen"]:
            new_lending["notizen"] = lending["notizen"]

        new_lending["id"] = lending["id"]

        # Ausgeliehene Gegenstände
        for lended_item in lending["items"]:
           # print("lended items for lending ",
            #      lending["id"], lended_item)
            new_item_lending = {}
            new_item_lending["lending_id"] = lending["id"]
            for item in items:
                # print(item)
                # search in items for the id...
                if (item["beschreibung"] == lended_item):
                    # prevent from reusing a foreign key of item twice in same lending
                    # first filter item_lendings for item_lendings with same lending_id
                    filtered_item_ids = list(filter(
                        lambda il: il["lending_id"] == lending["id"], item_lendings))
                   # print("AARRRR", filtered_item_ids)

                    # second map only ids to a new array
                    already_imported_item_ids = list(map(
                        lambda il: il["item_id"], filtered_item_ids))
                    # print("already imp", already_imported_item_ids)

                    # hashtag referential integrity!!
                    # check if item id has already been used in this lending
                    # if not used, use it! if used just ignore this item and
                    # try to find another match
                    if item["id"] not in already_imported_item_ids:
                        new_item_lending["item_id"] = item["id"]
                        break
                    # else:
                        # print("oh nooooohhhhhh")

            # Check if all the item_lending have been properly imported
            # properly imported if a item_id and a lending_id is given in dictionary
            if "lending_id" not in new_item_lending or "item_id" not in new_item_lending:
                print(new_item_lending, " seems to be not properly imported")
                print(lending)

            item_lendings.append(new_item_lending)

        lendings_import.append(new_lending)

    return lendings_import, item_lendings


def create_lendings_sql(lendings):
    """Generates SQL-Code for Ausleihschein table

    Args:
        lendings (dict[]): Array of lendings

    Returns:
        string: sql code
    """
    statements = []
    for l in lendings:
        # print(l)
        s = 'INSERT INTO Ausleihschein (id, Ausleihender_id, Ausgebender_id, Pruefender_id, ' \
            + 'ausleihe_datum, vereinbarte_rueckgabe, tatsaechliche_rueckgabe, ' \
            + 'notizen) VALUES ({}, {}, {}, {}, "{}", "{}","{}", "{}");'.format(
                l["id"], l["Ausleihender_id"], l["Ausgebender_id"], l["Pruefender_id"], l["ausleihe_datum"], l["vereinbarte_rueckgabe"], l["tatsaechliche_rueckgabe"], l["notizen"] if "notizen" in l else '')
        statements.append(s)
    return statements


def create_lendings_items_sql(lendings_items):
    """Generates SQL-Code for Gegenstand_has_Ausleihschein table

    Args:
        lendings_items (dict[]): Array of lendings_items

    Returns:
        string: sql code
    """
    statements = []

    for l in lendings_items:
        s = 'INSERT INTO Gegenstand_has_Ausleihschein (Gegenstand_id, Ausleihschein_id) VALUES ({}, {});'.format(
            l["item_id"], l["lending_id"])
        statements.append(s)
    return statements


print('los gehts')
# Bewohner (citizens) und Gegenstände (Items) sind bereits in der Datenbank angelegt worden
# und als csv-Datei exportiert (um Ausleihe und Gegenstand_Has_Ausleihe zu befüllen)
imported_citizens = extract_citizens('Bewohner.csv', path)
imported_lendings = extract_lendings('Ausleihen.csv', path)
imported_items = extract_items('Gegenstand.csv', path)

lendings, lendings_items = ausleihschein(
    imported_citizens, imported_lendings, imported_items)
# for item in imported_items:
#    pretty_dict(item)

# for lending in lendings:
#    pretty_dict(lending)

# for item_lending in lendings_items:
#    pretty_dict(item_lending)

lendings_sql = create_lendings_sql(lendings)

# for l in lendings_sql:
#    print(l)

lending_items_sql = create_lendings_items_sql(lendings_items)

with open(path + 'sql_code.txt', 'a') as f:
    for l in lendings_sql:
        f.write(f"{l}\n")
    for l in lending_items_sql:
        f.write(f"{l}\n")

print('ende')
