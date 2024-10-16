import csv
import random

fields = ['car_id', 'brand', 'model', 'year', 'price']
brands = ['Toyota', 'Ford', 'BMW', 'Audi', 'Honda']
models = ['ModelX', 'Sedan', 'SUV', 'Hatchback', 'Coupe']

with open('car_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(fields)  # Заголовок
    for i in range(10000000):  # 10 миллионов строк
        brand = random.choice(brands)
        model = random.choice(models)
        year = random.randint(1990, 2023)
        price = random.uniform(5000, 50000)
        writer.writerow([i, brand, model, year, price])
