# Технологии программирования

[Главная](/) / Работа с sql-базами данных из приложений на java. Миграции баз данных.

## Работа с sql-базами данных из приложений на java. Миграции баз данных.

### Содержание
1. [JDBC](#p1)
2. [Statement](#p2)
3. [PreparedStatement](#p3)
4. [Как масштабировать приложение с реляционной базой данных?](#p4)
5. [Миграции баз данных](#p5)
## JDBC <a name="p1"></a>

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

### Statement <a name="p2"></a>

Для выполнения инструкций SQL необходимо создать Statement.
В контексте JDBC (Java Database Connectivity), Statement представляет собой интерфейс, который используется для выполнения SQL-запросов к базе данных. Это основной инструмент для взаимодействия с базой данных, позволяющий выполнять различные типы запросов, включая простые запросы SELECT, INSERT, UPDATE, DELETE, а также более сложные запросы, требующие параметров.

Существует три основных типа Statement:
- Statement: Базовый класс, предназначенный для выполнения простых SQL-запросов без параметров.
- PreparedStatement: Наследует от Statement и используется для выполнения SQL-запросов с параметрами. Позволяет
  повысить безопасность и производительность за счет предварительной компиляции запроса.
- CallableStatement: Наследует от PreparedStatement и используется для выполнения хранимых процедур и функций.

Создание объекта Statement обычно происходит после установления соединения с базой данных. Например, для создания
объекта Statement можно использовать метод Connection.createStatement().

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

### PreparedStatement <a name="p3"></a>

PreparedStatement в контексте JDBC (Java Database Connectivity) – это интерфейс, который наследуется от базового
интерфейса Statement и используется для выполнения SQL-запросов с параметрами. Это мощный инструмент, который позволяет
повысить безопасность и производительность при работе с базой данных.

Основное отличие PreparedStatement от обычного Statement заключается в том, что в первом можно использовать параметры,
которые передаются в запрос при выполнении. Это позволяет избежать SQL-инъекций, так как параметры автоматически
экранируются, и делает запросы более читаемыми и удобными в обслуживании

Для создания объекта PreparedStatement используется метод Connection.prepareStatement(String sql) или
Connection.prepareStatement(String sql, int resultSetType, int resultSetConcurrency), где sql – строка с SQL-запросом,
содержащим параметры.

После создания объекта PreparedStatement параметры задаются с помощью методов setXXX(int parameterIndex, XXX value),
где XXX – тип параметра (например, setString, setInt, setFloat и т.д.), а parameterIndex – индекс параметра в запросе.

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

## Как масштабировать приложение с реляционной базой данных? <a name="p4"></a>
Масштабирование приложения с реляционной базой данных означает увеличение его способности обрабатывать растущий объем
данных и запросов без потери производительности. Есть два основных подхода к масштабированию:
вертикальная и горизонтальная масштабируемость.

**Вертикальная масштабируемость** подразумевает увеличение мощности существующего сервера путем добавления большего
количества ресурсов, таких как процессор, память, диск. Это может быть эффективным решением для небольших и средних
приложений, но имеет свои ограничения, когда дело доходит до больших объемов данных и высокой нагрузки.

**Горизонтальная масштабируемость** достигается путем добавления дополнительных серверов для распределения нагрузки.
Это позволяет приложению обрабатывать больше запросов одновременно, делая его более устойчивым к высоким нагрузкам.
Горизонтальная масштабируемость включает в себя два основных метода: репликацию и шардирование.

### Репликация
Репликация – это процесс копирования и размещения идентичной информации на разных серверах. Существует два типа
серверов: master и slave. Master – основной сервер, в который записывается новая информация или изменяется имеющаяся,
slave служит для копирования информации с мастера и её чтения. При репликации создается большое количество копий данных,
что обеспечивает высокую доступность и отказоустойчивость системы.

![](https://toto-school.ru/800/600/https/itc-life.ru/wp-content/uploads/2017/12/Replication.png)
### Шардирование баз данных
Шардирование (или шардинг) – это метод горизонтального масштабирования, при котором данные распределяются между
различными физическими серверами. Разные части таблиц базы данных могут храниться на разных серверах. Это позволяет
эффективно обрабатывать большие объемы данных и запросы, распределяя нагрузку между несколькими серверами.

![](https://habrastorage.org/r/w1560/webt/4q/0y/ds/4q0ydsizqds-qvfskq1cegxbkza.jpeg)
![](https://habrastorage.org/r/w1560/webt/3g/yl/ma/3gylma6_qd9qjvemx78m26ihrts.jpeg)

## Миграции баз данных <a name="p5"></a>

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

### Полезные ссылки

- [Введение в JDBC](https://www.baeldung.com/java-jdbc)
- [Лекция про работу с БД из Открытого лектория Яндекса](https://www.youtube.com/live/fsVjCEdvwdg?si=RyFKoVhYMmqffUiB)
- [Liquibase site](https://www.liquibase.org/)
- [Liquibase docs](https://docs.liquibase.com/home.html)
- [Миграции баз данных с помощью Liquibase](https://tproger.ru/articles/migracii-baz-dannyh-s-pomoshhju-biblioteki-liquibase/)