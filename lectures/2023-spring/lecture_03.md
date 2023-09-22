# Технологии программирования

[Назад к списку лекций](/lectures/2023-spring/)

## Базы данных. Реляционные базы данных. SQL. Работа с sql-базами данных из приложений на java.

## Базы данных
- Реляционные базы данных (PostgreSQL, MySQL, T-SQL)
- Не реляционные базы данных NoSQL:
- - Key-Value storage (Redis, Memcached, Amazon DynamoDB)
Единицей являются пары ключ-значения. По сути словарь. Быстро ищет индексы. 
Часто используется для кэша
- - Документоориентированные БД (MongoDb). 
Единицей являются документы (XML, JSON или BSON)
- - Столбцовые БД (Apache HBase, Apache Cassandra, Clickhouse) 
![](https://habrastorage.org/r/w1560/webt/t-/s7/ww/t-s7ww_5p0w8rxhmmvzz78q4kc0.jpeg)
Большой объем данных, быстрая скорость обработки запросов, гибкость данных. 
Используются для аналитики.
- - Графовая БД (Neo4j, OrientDB)

## Реляционная база данных
Основные понятия в реляционной теории:
- Отношения (Таблица)
- Кортежи (Строки)
- Атрибуты (Столбцы)

Правильное название понятий - без скобок. Но в работе чаще всего используются
более простые понятия (те, что я указал в скобках).

Пример ~~таблички~~ отношения в реляционной базе данных
![](https://habrastorage.org/r/w1560/webt/ye/js/3v/yejs3vthzyvavd1vpawh8o9brc4.jpeg)

Реляционная база данных – это коллекция таблиц, организованная согласно реляционной 
модели. Каждая ячейка этих таблиц имеет соответствующее формальное описание.

![](https://habrastorage.org/r/w1560/webt/vo/vm/ow/vovmowmobsgv-r4jxb7kydisk4w.jpeg)

Любой элемент можем идентифировать при помощи первичного ключа (primary key). Первичный ключ -
колонка, на которую накладывается ограничение на уникальность, по которой можно
однозначно идентифицировать объект в базе данных.

Foreign Key - колонка которую определяем, как связь с другой таблицей

## PostgreSQL
Распространенная реляционная база данных. 
Есть консольный клиент psql.

```sh
psql postgres #(для выхода из интерфейса используйте \q)
```

Основные команды:
- `\list` или `\l` - список баз данных
- `\du` - список пользователей
- `create database <db name>;` - создание базы данных
- `create user <user name>;` - создание юзика
-  `\password <user name>` - задать юзику пароль
- `GRANT ALL on <db name>.* TO '<user name>';` - дать права юзику на на бд
- `drop <db name>; drop <user name>` - удалить базу или юзика
- `\h` - справка по командам
- `\c` - подключиться к базе данных
- `\dt public.*` - список таблиц в схеме public

## Язык запросов SQL

Типы данных - [ссылка на доку](https://www.postgresql.org/docs/current/datatype.html)

Создать таблицу:
```postgresql
CREATE TABLE students (
    id integer PRIMARY KEY ,
    name text,
    group_number integer
);
```

Добавить в нее данные:
```postgresql
INSERT INTO students (id, name, group_number)
VALUES (1, 'Ivan Ivanov', 5), 
       (2, 'Dima Sidorov', 5), 
       (3, 'Sashs Ivanets', 5);
```

Выбрать из нее данные:
```postgresql
SELECT id, name FROM students WHERE group_number = 5;
```

Обновить данные в табличке:
```postgresql
UPDATE users SET username = 'admin' where id = 1
```

Операторы для условий:

| Оператор     | Действие                                                             |
|--------------|----------------------------------------------------------------------|
| =            | Равно                                                                |
| !=           | Не равно                                                             |
| <            | Меньше, чем                                                          |
| \>           | Больше, чем                                                          |
| <=           | Меньше или равно                                                     |
| >=           | Больше или равно                                                     |
| BETWEEN      | проверяет, находится ли значение в заданном диапазоне                |
| IN           | проверяет, содержится ли значение строки в наборе указанных значений |
| EXISTS       | проверяет, существуют ли строки при заданных условиях                |
| LIKE         | проверяет, соответствует ли значение указанной строке                |
| IS NULL      | Проверяет значения NULL                                              |
| IS NOT NULL  | Проверяет все значения, кроме NULL                                   |


Управление выводом запроса
```postgresql
SELECT COUNT(name), entree FROM dinners GROUP BY entree;
SELECT name, birthdate FROM dinners ORDER BY birthdate;
SELECT name, birthdate FROM dinners ORDER BY birthdate DESC;
```

Запрос данных из нескольких таблиц
```postgresql
SELECT tourneys.name, tourneys.size, dinners.birthdate
FROM tourneys
JOIN dinners ON tourneys.name=dinners.name;
```

## JDBC
JDBC - Java Database Connectivity

JDBC - это API для подключения и выполнения запросов к базе данных. JDBC может работать с любой базой данных,
если предоставлены надлежащие драйверы.

Чтобы подключиться к базе данных нам нужен драйвер для этой базы данных.
Его нужно добавить в зависимости и зарегистрировать.

Мы можем сделать это легко, добавив его в уже известные нам зависимости gradle, найдя нужную зависимость
в репозитории maven
Например, для [postgresql](https://mvnrepository.com/artifact/org.postgresql/postgresql):
```groovy
dependencies {
    implementation 'org.postgresql:postgresql:42.3.8'
}
```

Для подключения к базе необходимо создать соединение, указав строку подключения:

```java
public class Example {
    public static void main(String[] args) {
        Class.forName("org.postgresql.Driver");
        
        try (Connection con = DriverManager.getConnection("jdbc:postgresql://localhost:5432/myDb", "user1", "pass")) {
            // use con here
        }
    }
}
```

Для выполнения инструкций SQL необходимо создать Statement. Он бывает трех типов:
- Statement
- PreparedStatement
- CallableStatement

### Statement

```java
public class Example {
    public static void main(String[] args) {
        Class.forName("org.postgresql.Driver");

        try (Connection con = DriverManager.getConnection("jdbc:postgresql://localhost:5432/myDb", "user1", "pass")) {
            try (Statement stmt = con.createStatement()) {
                String tableSql = "CREATE TABLE IF NOT EXISTS employees"
                        + "(emp_id int PRIMARY KEY AUTO_INCREMENT, name varchar(30),"
                        + "position varchar(30), salary double)";
                int affectedLinesCount = stmt.execute(tableSql);

                String insertSql = "INSERT INTO employees(name, position, salary)"
                        + " VALUES('john', 'developer', 2000)";
                stmt.executeUpdate(insertSql); // для добавления записей используем метод executeUpdate


                String selectSql = "SELECT * FROM employees";
                // для добавления данных используем executeQuery
                try (ResultSet resultSet = stmt.executeQuery(selectSql)) {
                    Employee emp = new Employee();
                    emp.setId(resultSet.getInt("emp_id"));
                    emp.setName(resultSet.getString("name"));
                    emp.setPosition(resultSet.getString("position"));
                    emp.setSalary(resultSet.getDouble("salary"));
                    employees.add(emp);
                }
            }
        }
    }
}

```

### PreparedStatement
```java
public class Example {
    public static void main(String[] args) {
        Class.forName("org.postgresql.Driver");
        
        try (Connection con = DriverManager.getConnection("jdbc:postgresql://localhost:5432/myDb", "user1", "pass")) {
            String updatePositionSql = "UPDATE employees SET position=? WHERE emp_id=?";
            try (PreparedStatement pstmt = con.prepareStatement(updatePositionSql)) {
                pstmt.setString(1, "lead developer");
                pstmt.setInt(2, 1);

                int rowsAffected = pstmt.executeUpdate();
            }
        }
    }
}
```

## Как масштабировать приложение с реляционной базой данных?
### Репликация
![](https://toto-school.ru/800/600/https/itc-life.ru/wp-content/uploads/2017/12/Replication.png)
### Шардирование баз данных
![](https://habrastorage.org/r/w1560/webt/4q/0y/ds/4q0ydsizqds-qvfskq1cegxbkza.jpeg)
![](https://habrastorage.org/r/w1560/webt/3g/yl/ma/3gylma6_qd9qjvemx78m26ihrts.jpeg)

## Полезные ссылки

- [Базы данных: большой обзор типов и подходов. Доклад Яндекса](https://habr.com/ru/company/yandex/blog/522164/)
- [PostgreSQL Основы языка SQL](https://edu.postgrespro.ru/sql_primer.pdf)
- [Основы реляционных баз данных](https://www.internet-technologies.ru/articles/osnovy-relyacionnyh-baz-dannyh.html)
- [Статья](https://www.8host.com/blog/zaprosy-v-postgresql/) про то, как делать запросы к базе данных
- [Введение в JDBC](https://www.baeldung.com/java-jdbc)