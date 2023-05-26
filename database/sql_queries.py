from django.db import connection

def delete_last_rows(n):
    """Удаляет последние n строк из таблицы"""
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM promocode_promocode 
                          WHERE id IN (SELECT id FROM promocode_promocode ORDER BY id DESC LIMIT %s)""",
                       (n,))