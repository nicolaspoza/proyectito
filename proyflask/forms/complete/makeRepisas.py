import random
from faker import Faker
from cryptography.fernet import Fernet
import csv
import pandas as pd

cantidad = 100
fake = Faker()


def create_csv_file():
    with open('categories.csv',"rt") as csvfile:
        record = csv.reader(csvfile,delimiter = '-')
        with open('Repisas.csv','w',newline ='') as csvfile:
            Repisas = ['id','categoria']

            writer = csv.DictWriter(csvfile, fieldnames = Repisas)
            writer.writeheader()

            for index,elem in enumerate(record):
                writer.writerow(
                {
                 'id':index+1,
                 'categoria':elem[1]
                }

            )
if __name__ == "__main__":
    create_csv_file()
