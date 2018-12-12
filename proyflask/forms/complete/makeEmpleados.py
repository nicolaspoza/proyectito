import random
from faker import Faker
from cryptography.fernet import Fernet
import csv

cantidad = 100
fake = Faker()

def create_csv_file():
    ans = []
    for i in range(cantidad):
        r1 = str(random.randint(1,50))
        r2 = str(random.randint(101,999))
        r3 = str(random.randint(101,999))
        r4 = random.randint(0,9)
        if r4 is 1:
            r4 = 'k'
            rut = r1 + '.' + r2 + '.' + r3 + '-' + r4
        else:
            rut = r1 + '.' + r2 + '.' + r3 + '-' + str(r4)
        ans.append(rut)
    with open('Empleados.csv','w',newline ='') as csvfile:
        Empleados = ['rut','nombre','password']

        writer = csv.DictWriter(csvfile, fieldnames = Empleados)
        writer.writeheader()

        for i in range(cantidad):
            writer.writerow(
            {
             'rut': ans[i],
             'nombre':fake.name(),
             'password':Fernet.generate_key()
            }
        )

if __name__ == "__main__":
    create_csv_file()
