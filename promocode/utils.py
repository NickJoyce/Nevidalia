import pandas as pd
from .models import Promocode
from datetime import date
import traceback
from database.sql_queries import delete_last_rows
from django.contrib import messages
from project.settings.base import BASE_DIR


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
                                      status=change_status_to_bool(row.Статус))
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

