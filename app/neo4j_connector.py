from typing import Optional


from neo4j import GraphDatabase, Driver


class Neo4jConnection:
    '''Класс Neo4jConnector представляет собой простой класс, который облегчает подключение к базе данных
    Neo4j с использованием официальной библиотеки neo4j для Python.
    Он содержит методы для установления соединения с базой данных и закрытия соединения после использования.'''

    def __init__(self, uri: str, user: str, password: str) -> None:
        '''Конструктор класса __init__ принимает три параметра:
        uri: URL базы данных Neo4j,
        user: имя пользователя для аутентификации
        password: пароль для аутентификации.
        При создании объекта класса устанавливается соединение с базой данных Neo4j.'''
        self._uri = uri
        self._user = user
        self._password = password
        self._driver: Optional[Driver] = None

    def close(self) -> None:
        '''Метод close() закрывает открытое соединение с базой данных Neo4j, если таковое имеется.
        Рекомендуется вызывать этот метод после завершения всех операций с базой данных для освобождения ресурсов.'''
        if self._driver is not None:
            self._driver.close()

    def connect(self) -> Driver:
        '''Метод connect() создает драйвер для подключения к базе данных Neo4j с использованием URI,
        имени пользователя и пароля, переданных в конструкторе.
        Возвращает созданный драйвер.'''
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        return self._driver