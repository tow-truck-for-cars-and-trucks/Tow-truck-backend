import os
import csv
import chardet
from django.core.management.base import BaseCommand
from tow_truck.settings import BASE_DIR
from towin.models import Tariff, CarType, Order, PriceOrder, Feedback, TowTruck
from django.contrib.auth import get_user_model

User = get_user_model()
path = os.path.join(BASE_DIR)


class Command(BaseCommand):
    help = 'Load data from csv_file'

    def handle(self, *args, **options):
        with open(
            f'{path}/data/tariffs.csv',
            'rb',
        ) as csv_file:
            raw_data = csv_file.read()
            file_encoding = chardet.detect(raw_data)['encoding']
            decoded_data = raw_data.decode(file_encoding)
            rows = csv.reader(
                decoded_data.splitlines(True),
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                doublequote=False,
            )
            data = [Tariff(
                name=row[0],
                description=row[1],
                price=row[2]
            ) for row in rows]
            Tariff.objects.bulk_create(data)

        with open(
            f'{path}/data/cartypes.csv',
            'rb',
        ) as csv_file:
            raw_data = csv_file.read()
            file_encoding = chardet.detect(raw_data)['encoding']
            decoded_data = raw_data.decode(file_encoding)
            rows = csv.reader(
                decoded_data.splitlines(True),
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                doublequote=False,
            )
            data = [CarType(
                car_type=row[0],
                price=row[1]
            ) for row in rows]
            CarType.objects.bulk_create(data)

        with open(
            f'{path}/data/towtrucks.csv',
            'rb',
        ) as csv_file:
            raw_data = csv_file.read()
            file_encoding = chardet.detect(raw_data)['encoding']
            decoded_data = raw_data.decode(file_encoding)
            rows = csv.reader(
                decoded_data.splitlines(True),
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                doublequote=False,
            )
            data = [TowTruck(
                is_active=row[0],
                driver=row[1],
                model_car=row[2],
                license_plates=row[3]
            ) for row in rows]
            TowTruck.objects.bulk_create(data)

        with open(
            f'{path}/data/users.csv',
            'rb',
        ) as csv_file:
            raw_data = csv_file.read()
            file_encoding = chardet.detect(raw_data)['encoding']
            decoded_data = raw_data.decode(file_encoding)
            rows = csv.reader(
                decoded_data.splitlines(True),
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                doublequote=False,
            )
            data = [User(
                username=row[0],
                phone=row[1],
                email=row[2],
                first_name=row[3],
                last_name=row[4],
                role=row[5],
            ) for row in rows]
            User.objects.bulk_create(data)

        with open(
            f'{path}/data/orders.csv',
            'rb',
        ) as csv_file:
            raw_data = csv_file.read()
            file_encoding = chardet.detect(raw_data)['encoding']
            decoded_data = raw_data.decode(file_encoding)
            rows = csv.reader(
                decoded_data.splitlines(True),
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                doublequote=False,
            )
            data = [Order(
                client=User.objects.get(username=row[0]),
                address_from=row[1],
                address_to=row[2],
                addition=row[3],
                delay=row[4],
                tow_truck=TowTruck.objects.get(pk=row[5]),
            ) for row in rows]
            Order.objects.bulk_create(data)

        with open(
            f'{path}/data/priceorder.csv',
            'rb',
        ) as csv_file:
            raw_data = csv_file.read()
            file_encoding = chardet.detect(raw_data)['encoding']
            decoded_data = raw_data.decode(file_encoding)
            rows = csv.reader(
                decoded_data.splitlines(True),
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                doublequote=False,
            )

            # Через bulk_create не хочет подсчитывать итоговую цену заказа.
            # по возможности нужно разобраться почему так происходит :///

            for row in rows:
                PriceOrder.objects.create(
                    tariff=Tariff.objects.get(pk=row[0]),
                    car_type=CarType.objects.get(pk=row[1]),
                    wheel_lock=int(row[2]),
                    towin=row[3],
                    order=Order.objects.get(pk=row[4]),
                )

        with open(
            f'{path}/data/feedback.csv',
            'rb',
        ) as csv_file:
            raw_data = csv_file.read()
            file_encoding = chardet.detect(raw_data)['encoding']
            decoded_data = raw_data.decode(file_encoding)
            rows = csv.reader(
                decoded_data.splitlines(True),
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                doublequote=False,
            )
            data = [Feedback(
                score=row[0],
                comment=row[1],
                order=Order.objects.get(pk=row[2]),
            ) for row in rows]
            Feedback.objects.bulk_create(data)

            return 'Тестовые данные успешно импортированы.'
