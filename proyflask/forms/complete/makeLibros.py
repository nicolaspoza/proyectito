import random
from faker import Faker
import csv
import pandas as pd

cantidad = 100
fake = Faker()
data = pd.read_csv('autoresylibros.csv')
nombreA = data['nombre'].tolist()
autorA =data['autor'].tolist()


def create_csv_file():

    # estado = []
    # for i in range(cantidad):
    #     Prestamo = random.choice([True, False])
    #     if Prestamo is True:
    #         Prestamo = 'Prestado'
    #     else:
    #         Prestamo = 'Aun en repisa'
    #     estado.append(Prestamo)
    with open('Libros.csv','w',newline ='') as csvfile:
        Libros = ['id','nombre','autor','prestado','id_repisa']

        writer = csv.DictWriter(csvfile, fieldnames = Libros)
        writer.writeheader()

        for i in range(cantidad):
            writer.writerow(
            {
             'id': i+1,
             'nombre':nombreA[i],
             'autor':autorA[i],
             'prestado':random.choice([True, False]),
             'id_repisa': i+1
            }

        )
if __name__ == "__main__":
    create_csv_file()
