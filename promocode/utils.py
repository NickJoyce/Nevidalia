import pandas as pd
from .models import Promocode
from datetime import date
import traceback
from database.sql_queries import delete_last_rows
from django.contrib import messages
from project.settings.base import BASE_DIR


class Customer():
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone


class OrderItem():
    def __init__(self, name: str, quantity: int, amount: int, price: int, externalid: str):
        self.name = name
        self.quantity = quantity
        self.amount = amount
        self.price = price
        self.externalid = externalid
        self.promocodes = []

    def get_promocodes_as_str(self):
        if self.promocodes:
            return ", ".join([promocode.code for promocode in self.promocodes])





class Order():
    def __init__(self, customer: Customer, park: str, order_id: str, items: [OrderItem], amount:int):
        self.customer = customer
        self.order_id = order_id
        self.amount = amount
        self.items = items
        self.park = park









def get_data_from_str(data_as_str) -> date:
    """data format: 23.05.2023"""
    return date(*reversed([int(i) for i in data_as_str.split('.')]))

def change_status_to_bool(status):
    return False if status == "Не использован" else True


def csv_file_handling(file, request):
    try:
        df = pd.read_csv(file, delimiter=';', encoding="windows-1251")
    except UnicodeDecodeError:
        messages.add_message(request, messages.ERROR, "Ошибка кодировки")
        messages.add_message(request, messages.ERROR, traceback.format_exc())
        return False

    # remove whitespace from column headers
    df.columns = df.columns.str.replace(' ', '_')

    is_ok = True
    for n, row in enumerate(df.itertuples(index=False), start=1):
        try:
            Promocode.objects.create(date_of_create=get_data_from_str(row.Дата_создания),
                                      start_date=get_data_from_str(row.Начало),
                                      end_date=get_data_from_str(row.Окончание),
                                      park=row.Парк,
                                      creator=row.Создатель,
                                      action_name=row.Название_акции,
                                      code=row.Код,
                                      status=change_status_to_bool(row.Статус),
                                      tilda_external_product_id=row.Внешний_код)
        except:
            delete_last_rows(n-1)
            messages.add_message(request, messages.ERROR, 'Данные из файла не загружены в БД')
            messages.add_message(request, messages.ERROR, f'Ошибка в строке {n+1} csv файла')
            messages.add_message(request, messages.ERROR, traceback.format_exc())
            is_ok = False
            break
    return is_ok




if __name__ == "__main__":
    file = "Промокоды_будни_Волгоград.csv"
    csv_file_handling(file)

