import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import *
import os
import json

def create_db_session():
    """Создает и возвращает сессию базы данных (внутри ф-ции также создаются таблицы, описанные в models.py)
    Запрашивает у пользователя имя пользователя, пароль и название базы данных.
    Предполагается, что база данных PostgreSQL развернута на локальном компьютере
    (localhost) и использует стандартный порт (5432).

    Returns:
        Session: Объект сессии для работы с базой данных.
    """
    user = input('Введите имя пользователя: ')
    password = input('Введите пароль: ')
    db_name = input('Введите название БД: ')
    DSN = f'postgresql://{user}:{password}@localhost:5432/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)  # Создание таблиц
    Session = sessionmaker(bind=engine)
    return Session()

def load_data(session, file_path):
    """Загружает данные из JSON-файла и добавляет их в базу данных.

    Args:
        session (Session): Объект сессии для работы с базой данных.
        file_path (str): Путь к JSON-файлу, содержащему данные.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    for model in data:
        if model['model'] == 'publisher':
            publisher = Publisher(name=model['fields']['name'],
                                  id=model['pk'])
            session.add(publisher)
        elif model['model'] == 'book':
            book = Book(title=model['fields']['title'],
                        id=model['pk'],
                        publisher_id=model['fields']['id_publisher'])
            session.add(book)
        elif model['model'] == 'shop':
            shop = Shop(name=model['fields']['name'],
                        id=model['pk'])
            session.add(shop)
        elif model['model'] == 'stock':
            stock = Stock(id=model['pk'],
                          shop_id=model['fields']['id_shop'],
                          book_id=model['fields']['id_book'],
                          count=model['fields']['count'])
            session.add(stock)
        elif model['model'] == 'sale':
            sale = Sale(id=model['pk'],
                        price=model['fields']['price'],
                        date_sale=model['fields']['date_sale'],
                        stock_id=model['fields']['id_stock'],
                        count=model['fields']['count'])
            session.add(sale)
    session.commit()

def query_books_by_publisher(session, publisher):
    """Запрашивает книги по id или имени издателя и выводит результаты.

   Args:
       session (Session): Объект сессии для работы с базой данных.
       publisher (str): id или название издателя.

   Если `publisher` является числом, выполняется поиск по id.
   Если это строка, выполняется поиск по имени. Результаты выводятся в формате:
   'Название книги | Название магазина | Цена | Дата продажи'.

   Returns:
       None
   """
    if publisher.isdigit():
        query = session.query(Book, Publisher, Stock, Shop, Sale)\
            .join(Publisher, Book.publisher_id == Publisher.id)\
            .join(Stock, Book.id == Stock.book_id)\
            .join(Shop, Stock.shop_id == Shop.id)\
            .join(Sale, Stock.id == Sale.stock_id)\
            .filter(Publisher.id == publisher)\
            .with_entities(Book.title, Shop.name, Sale.price, Sale.date_sale)
        results = query.all()
        if results:
            for title, name, price, date_sale in results:
                print(f'{title} | {name} | {price} | {date_sale}')
        else:
            print('Издатель не найден.')
    else:
        query_ids = session.query(Publisher.id)\
            .filter(Publisher.name == publisher)\
            .all()  # Получаем все id с одинаковым именем издателя

        if query_ids:
            # Извлекаем все id издателей с одинаковым именем
            publisher_ids = [id_tuple[0] for id_tuple in query_ids]

            # Выполняем запрос для каждого найденного id
            query = session.query(Book, Publisher, Stock, Shop, Sale)\
                .join(Publisher, Book.publisher_id == Publisher.id)\
                .join(Stock, Book.id == Stock.book_id)\
                .join(Shop, Stock.shop_id == Shop.id)\
                .join(Sale, Stock.id == Sale.stock_id)\
                .filter(Publisher.id.in_(publisher_ids))\
                .with_entities(Book.title, Shop.name, Sale.price, Sale.date_sale)
            results = query.all()
            for title, name, price, date_sale in results:
                print(f'{title} | {name} | {price} | {date_sale}')
        else:
            print('Издатель не найден.')

def main():
    """Основная функция программы.

    Создает сессию базы данных, загружает данные из JSON-файла, запрашивает у пользователя информацию
    об издателе и выводит соответствующие книги.

   Returns:
       None
    """
    session = create_db_session()

    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'fixtures', 'tests_data.json')
    load_data(session, file_path)

    publisher = input('Введите издателя: id или название: ')
    query_books_by_publisher(session, publisher)

if __name__ == '__main__':
    main()











