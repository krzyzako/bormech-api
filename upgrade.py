"""
    Script to import data from .csv file to Model Database DJango
    To execute this script run: 
                                1) manage.py shell
                                2) exec(open('upgrade.py').read())
"""

import csv
from homolog.models import Rodzaj

CSV_PATH = 'zbiorniki.csv'      # Csv file path  


with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='\n')
    for row in spamreader:
        print("rodzaj :" +row[0] + "  Homologacja :" +row[1], row[2] , row[3])
        #Model.objects.create(... Attributes here ...)
        # get = Rodzaj.objects.get(symbol=row[0],approval=row[1])
        # print(get.symbol)
        try:
            Rodzaj.objects.create(symbol=row[0], approval=row[1], dimeter=int(row[2]), capacity=int(row[3]),height=row[4],weight=row[5],tank=row[6])
            # Rodzaj.objects.filter(symbol=row[0]).update(height=row[4],weight=row[5])
        except:
            pass