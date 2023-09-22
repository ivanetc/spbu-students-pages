# Технологии программирования

[Назад к списку лекций](/lectures/2023-spring/)

## Индексы в PostgreSQL. Миграции баз данных.

## Индексы

Индексы в PostgreSQL — специальные объекты базы данных, предназначенные 
в основном для ускорения доступа к данным.

### Что такое индекс?

Отдельная табличка с отсортированными значениями, которые хранят ссылки на запись в основной таблице.
Можно представить себе как бинарное дерево. Нельзя создать для типов данных, предназначенных для 
хранения больших объектов: text, image или varchar(max).

![](https://doberbeatzblog.files.wordpress.com/2017/03/screen-shot-2017-05-30-at-17-00-16.png)

### Как создать индекс:
```postgresql
-- Syntax:
CREATE INDEX name ON table (column);

-- Query:
CREATE INDEX users_age_idx ON users (age);

```

![](https://doberbeatzblog.files.wordpress.com/2017/03/screen-shot-2017-05-30-at-17-00-46.png)

### Типы индексов:

![](https://doberbeatzblog.files.wordpress.com/2017/03/screen-shot-2017-05-30-at-17-01-30.png)

**Кластеризованный индекс** уже хранит данные в своих листьях. Он находится в отсортированном виде 
и создается только один на всю таблицу. Обычно на колонку id, которая является 
первичным ключом (primary key), по умолчанию создается кластеризованный индекс.

**Некластеризованный индекс** хранит в своих листьях ссылки на записи кластеризованного индекса 
или на записи из кучи, если кластеризованного индекса нет.

### Параметры создания индекса:

```postgresql
CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ]name ] ON table_name [ USING method ] ({ column | ( expression ) } [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...]) [ WHERE predicate ]
```

Уникальный индекс
```postgresql
CREATE UNIQUE INDEX users_uid_idx ON users (uid);

CREATE UNIQUE INDEX users_full_name_idx
    ON users (first_name, last_name);
```

### Индексы Postgresql
**B-Tree (Balanced Tree)**

Если не указать индекс, то B-Tree - дефолтный.

Когда использовать?
- операторы сравнения >, <, =, >=, <=, BETWEEN и IN;
- условия пустоты IS NULL и IS NOT NULL;
- операторы поиска подстроки LIKE и ~, если искомая строка закреплена 
в начале шаблона (например name LIKE 'Lisa%');

**Hash**

Hash-индексы используются только при условии равенства.
![](https://doberbeatzblog.files.wordpress.com/2017/03/screen-shot-2017-06-12-at-19-13-19.png)

```postgresql
CREATE INDEX name ON table USING hash (column);
```

**GiST (Generalized Search Tree)**

По умолчанию PostgreSQL предоставляет индексы для некоторых типов данных, таких как 
геометрические типы, сетевые адреса, диапазоны и т.д.

Полезен для типов box, circle, polygon, inet, cidr, point, tsquery

**SP-GiST (Space-Partitioned GiST)**

**GIN (Generalized Inverted Index)**

Индексы применимы к составным типам, работа с которыми осуществляется с помощью ключей. 
Это массивы, jsonb и tsvector.

**BRIN (Block Range Index)**

## Миграции баз данных

Миграция баз данных — это что-то вроде системы контроля версий для вашей схемы базы данных. 
Она позволяет разработчикам изменять структуру БД, сообщать другим участникам команды об этих изменениям
и самим быть в курсе апдейтов, а также отслеживать историю изменений.

В java-приложениях чаще всего используют инструменты
- Liquibase
- Flyway

Рассмотрим Liquibase

```groovy
dependencies {
    implementation 'org.liquibase:liquibase-core:4.10.0'
}
```

Создадим в папке с ресурсами файл с ченджсетом `src/main/resources/db/changelog/changelog.xml`
```xml
<databaseChangeLog
       xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog">
   <changeSet id="create_table_genre" author="mediaSoft">
        <!-- Прописываем создание таблицы genre&ndash;-->
       <createTable tableName="genre">
        <!--Создаем поля -->
           <column autoIncrement="true" name="genre_id" type="bigint">
               <constraints primaryKey="true" nullable="false"/>
           </column>
           <column name="genre_name" type="varchar(64)">
               <constraints nullable="false" unique="true"/>
           </column>
       </createTable>
   </changeSet>
</databaseChangeLog>
```

```xml
<changeset author="mueller@synyx.de" id="2"> 
  <sql> 
    UPDATE Person SET firstname = SUBSTRING_INDEX(name, ' ', 1); 
    UPDATE Person SET lastname = SUBSTRING_INDEX(name, ' ', -1); 
  </sql> 
  <rollback> 
    UPDATE Person SET firstname = ''; 
    UPDATE Person SET lastname = ''; 
  </rollback> 
</changeset>
```

```sh
liquibase init project --format=xml

liquibase --url=jdbc:h2:tcp://localhost:9090/mem:integration update
```

```sh
liquibase rollback --tag=myTag --changelog-file=example-changelog.xml
```

## Полезные ссылки
- [Введение в индексы](https://doberbeatzblog.wordpress.com/2017/03/13/postgresql-indexes/)
- [Суперсила индексов для оптимизации SQL-запросов](https://medium.com/nuances-of-programming/супер-сила-индексов-для-оптимизации-sql-запросов-df2549431bf8)
- [Статья на хабре про индексы](https://habr.com/ru/company/postgrespro/blog/326096/)


- [Liquibase site](https://www.liquibase.org/)
- [Liquibase docs](https://docs.liquibase.com/home.html)
- [Миграции баз данных с помощью Liquibase](https://tproger.ru/articles/migracii-baz-dannyh-s-pomoshhju-biblioteki-liquibase/)
