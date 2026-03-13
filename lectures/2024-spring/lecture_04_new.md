# Технологии программирования

[Главная](/) / Работа с sql-базами данных из приложений на java. Миграции баз данных.

## Лекция 5: JDBC, пулеры соединений и миграции БД
### Сквозной пример: Система управления сотрудниками

### Содержание
1. [Клиент-серверное взаимодействие с PSQL. Фазы взаимодействия](#p1)
2. [Драйвер JDBC](#p2)
3. [Протоколы взаимодействия](#p3)
4. [Пулы соединений. HikariPool](#p4)
5. [Прокси пулеры соединений](#p5)
6. [Транзакции (через JDBC)](#p6)
7. [Миграции БД. Flyway и Liquibase](#p7)

Для демонстрации всех концепций мы будем использовать пример системы управления сотрудниками компании. Создадим простую таблицу:

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE DEFAULT CURRENT_DATE
);
```

### Диаграмма архитектуры приложения:
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Java App      │ →  │   JDBC Driver   │ →  │   PostgreSQL    │
│                 │    │                 │    │   Database      │
│ - Connection    │    │ - Protocol      │    │ - Tables        │
│ - Statements    │    │ - Parsing       │    │ - Transactions  │
│ - Transactions  │    │ - Optimization  │    │ - Indexes       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 1. Клиент-серверное взаимодействие с PSQL. Фазы взаимодействия <a name="p1"></a>

### Архитектура взаимодействия

```
┌─────────────┐    TCP/IP    ┌─────────────┐
│   Клиент    │ ←──────────→ │   Сервер    │
│  (Java App) │              │  (PostgreSQL)│
└─────────────┘              └─────────────┘
```

### Диаграмма фаз взаимодействия:
```
┌─────────────────────────────────────────────────────────┐
│                    Фазы взаимодействия                  │
├─────────────────────────────────────────────────────────┤
│ 1. Установка соединения                                 │
│    - TCP handshake                                      │
│    - Аутентификация                                     │
├─────────────────────────────────────────────────────────┤
│ 2. Подготовка запроса                                   │
│    - Парсинг SQL                                        │
│    - Планирование выполнения                            │
├─────────────────────────────────────────────────────────┤
│ 3. Выполнение запроса                                   │
│    - Обработка данных                                   │
│    - Применение изменений                               │
├─────────────────────────────────────────────────────────┤
│ 4. Получение результата                                 │
│    - Передача данных клиенту                            │
│    - Форматирование ответа                              │
├─────────────────────────────────────────────────────────┤
│ 5. Завершение                                           │
│    - Закрытие соединения                                │
│    - Освобождение ресурсов                              │
└─────────────────────────────────────────────────────────┘
```

### Фазы взаимодействия:

1. **Установка соединения** - TCP handshake и аутентификация
2. **Подготовка запроса** - парсинг и планирование
3. **Выполнение запроса** - обработка данных
4. **Получение результата** - передача данных клиенту
5. **Завершение** - закрытие соединения

## 2. Драйвер JDBC <a name="p2"></a>

JDBC (Java Database Connectivity) - стандартный API для работы с базами данных в Java.

### Основные компоненты:

```java
import java.sql.*;

public class JdbcExample {
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/company";
        String user = "postgres";
        String password = "password";
        
        try (Connection conn = DriverManager.getConnection(url, user, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM employees")) {
            
            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("id"));
                System.out.println("Name: " + rs.getString("first_name"));
                System.out.println("Email: " + rs.getString("email"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

### Ключевые интерфейсы JDBC:

- `Connection` - управление соединением
- `Statement` - выполнение SQL запросов
- `PreparedStatement` - параметризованные запросы
- `ResultSet` - работа с результатами запроса

## 3. Протоколы взаимодействия <a name="p3"></a>

### Simple Query Protocol

Простой протокол для выполнения одного запроса. При использовании этого протокола SQL-запрос передается в виде обычной текстовой строки. Сервер выполняет разбор (парсинг) запроса, планирует его выполнение и затем выполняет. Этот протокол подходит для однократных запросов, но не обеспечивает оптимальной производительности при многократном выполнении одних и тех же запросов с разными параметрами.

```java
// Пример использования Simple Query
try (Statement stmt = conn.createStatement()) {
    boolean hasResult = stmt.execute("SELECT * FROM employees");
    if (hasResult) {
        ResultSet rs = stmt.getResultSet();
        // обработка результатов
    }
}
```

### Extended Query Protocol

Расширенный протокол для параметризованных запросов. В отличие от Simple Query, этот протокол разделяет этапы подготовки запроса и его выполнения. Запрос с параметрами подготавливается один раз, а затем может многократно выполняться с разными значениями параметров. Это обеспечивает лучшую производительность и безопасность за счет предотвращения SQL-инъекций.

```java
// Пример использования PreparedStatement (Extended Query)
String sql = "INSERT INTO employees (first_name, last_name, email, department, salary) VALUES (?, ?, ?, ?, ?)";
try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setString(1, "Иван");
    pstmt.setString(2, "Петров");
    pstmt.setString(3, "ivan.petrov@company.com");
    pstmt.setString(4, "IT");
    pstmt.setBigDecimal(5, new BigDecimal("50000.00"));
    
    int rowsAffected = pstmt.executeUpdate();
    System.out.println("Добавлено записей: " + rowsAffected);
}
```

## 4. Пулы соединений. HikariPool <a name="p4"></a>

### Проблема создания соединений на каждый запрос:

При высокой нагрузке на приложение создание нового соединения с базой данных для каждого запроса становится серьезной проблемой производительности. Установка соединения - это дорогостоящая операция, требующая времени на TCP handshake, аутентификацию и инициализацию сессии. Кроме того, при большом количестве одновременных запросов может возникнуть ситуация, когда база данных исчерпает лимит соединений, что приведет к отказу в обслуживании.

```java
// НЕПРАВИЛЬНО - создание соединения для каждого запроса
public Employee getEmployee(int id) {
    Connection conn = DriverManager.getConnection(url, user, password);
    // ... выполнение запроса
    conn.close(); // Дорогая операция!
}
```

### Решение - пул соединений с HikariCP:

Пул соединений решает эту проблему, создавая заранее определенное количество соединений и повторно используя их для обработки запросов. Когда приложение нуждается в соединении с БД, оно берет уже готовое соединение из пула, использует его, а затем возвращает обратно в пул вместо закрытия. Это значительно уменьшает накладные расходы на создание/закрытие соединений и позволяет эффективно управлять ресурсами.

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

public class ConnectionPoolExample {
    private static HikariDataSource dataSource;
    
    static {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/company");
        config.setUsername("postgres");
        config.setPassword("password");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(30000);
        config.setIdleTimeout(600000);
        config.setMaxLifetime(1800000);
        
        dataSource = new HikariDataSource(config);
    }
    
    public static Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
    
    public static void exampleUsage() {
        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM employees WHERE id = ?")) {
            
            pstmt.setInt(1, 1);
            ResultSet rs = pstmt.executeQuery();
            
            if (rs.next()) {
                System.out.println("Найден сотрудник: " + rs.getString("first_name"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

## 5. Прокси пулеры соединений <a name="p5"></a>

### Архитектура с прокси:

Прокси пулеры соединений, такие как PgBouncer, представляют собой отдельные компоненты, которые размещаются между приложением и базой данных. Они управляют пулом соединений на уровне прокси, что позволяет нескольким приложениям использовать общий пул соединений. Это особенно полезно в средах с множеством микросервисов, где каждый сервис может иметь свои собственные пулы соединений, что в совокупности может привести к исчерпанию лимита соединений на стороне базы данных.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Приложение │ →  │   Прокси    │ →  │   База      │
│             │    │  (PgBouncer)│    │  Данных     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Сравнение пулов соединений:
```
┌─────────────────────────────────────────────────────────┐
│              Сравнение подходов к пулингу               │
├─────────────────┬─────────────────┬─────────────────────┤
│   Подход       │   Преимущества   │   Недостатки        │
├─────────────────┼─────────────────┼─────────────────────┤
│  HikariCP      │ - Высокая        │ - Только на уровне  │
│  (приложение)  │   производит-ть  │   приложения        │
│                 │ - Гибкая        │                     │
│                 │   настройка     │                     │
├─────────────────┼─────────────────┼─────────────────────┤
│  PgBouncer     │ - Общий для      │ - Дополнительный    │
│  (прокси)      │   всех приложений│   компонент         │
│                 │ - Экономия      │ - Сложность         │
│                 │   соединений    │   настройки         │
├─────────────────┼─────────────────┼─────────────────────┤
│  Комбинированный│ - Максимальная  │ - Максимальная      │
│                 │   эффективность │   сложность         │
│                 │ - Масштабируемость│                   │
└─────────────────┴─────────────────┴─────────────────────┘
```

### Конфигурация PgBouncer:

Основные параметры конфигурации PgBouncer включают режим пулинга (session, transaction, statement), максимальное количество клиентских соединений и размер пула соединений с базой данных. Режим transaction наиболее эффективен для приложений, которые не используют временные таблицы или блокировки на уровне сессии.

```ini
[databases]
company = host=localhost port=5432 dbname=company

[pgbouncer]
pool_mode = transaction
max_client_conn = 100
default_pool_size = 20
```

## 6. Транзакции (через JDBC) <a name="p6"></a>

### Базовые транзакции:

```java
public class TransactionExample {
    public static void transferSalary(int fromEmployeeId, int toEmployeeId, BigDecimal amount) {
        Connection conn = null;
        try {
            conn = ConnectionPoolExample.getConnection();
            conn.setAutoCommit(false); // Отключаем авто-коммит
            
            // Снимаем деньги с первого сотрудника
            String deductSql = "UPDATE employees SET salary = salary - ? WHERE id = ?";
            try (PreparedStatement deductStmt = conn.prepareStatement(deductSql)) {
                deductStmt.setBigDecimal(1, amount);
                deductStmt.setInt(2, fromEmployeeId);
                int rowsUpdated = deductStmt.executeUpdate();
                
                if (rowsUpdated == 0) {
                    throw new SQLException("Сотрудник не найден");
                }
            }
            
            // Добавляем деньги второму сотруднику
            String addSql = "UPDATE employees SET salary = salary + ? WHERE id = ?";
            try (PreparedStatement addStmt = conn.prepareStatement(addSql)) {
                addStmt.setBigDecimal(1, amount);
                addStmt.setInt(2, toEmployeeId);
                int rowsUpdated = addStmt.executeUpdate();
                
                if (rowsUpdated == 0) {
                    throw new SQLException("Сотрудник не найден");
                }
            }
            
            conn.commit(); // Коммитим транзакцию
            System.out.println("Транзакция выполнена успешно");
            
        } catch (SQLException e) {
            if (conn != null) {
                try {
                    conn.rollback(); // Откатываем при ошибке
                    System.out.println("Транзакция откачена");
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
            e.printStackTrace();
        } finally {
            if (conn != null) {
                try {
                    conn.setAutoCommit(true); // Восстанавливаем авто-коммит
                    conn.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```

### Уровни изоляции:

```java
// Установка уровня изоляции
conn.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);

// Доступные уровни:
// TRANSACTION_READ_UNCOMMITTED
// TRANSACTION_READ_COMMITTED (по умолчанию в PostgreSQL)
// TRANSACTION_REPEATABLE_READ
// TRANSACTION_SERIALIZABLE
```

### Диаграмма транзакции:
```
┌─────────────────────────────────────────────────────────┐
│                    Транзакция                           │
├─────────────────────────────────────────────────────────┤
│ 1. Начало транзакции                                    │
│    conn.setAutoCommit(false);                           │
├─────────────────────────────────────────────────────────┤
│ 2. Выполнение операций                                  │
│    - UPDATE employees SET salary = salary - ?           │
│    - UPDATE employees SET salary = salary + ?           │
├─────────────────────────────────────────────────────────┤
│ 3. Проверка успешности                                  │
│    if (rowsUpdated == 0) throw SQLException             │
├─────────────────────────────────────────────────────────┤
│ 4. Коммит или откат                                     │
│    conn.commit(); // Успешно                            │
│    conn.rollback(); // При ошибке                       │
└─────────────────────────────────────────────────────────┘
```

## 7. Миграции БД. Flyway и Liquibase <a name="p7"></a>

### Проблема управления схемой БД:

При разработке приложений, работающих с базами данных, возникает необходимость управления изменениями схемы БД. Без специальных инструментов легко столкнуться с проблемами:
- Разные версии схемы в разных средах (разработка, тестирование, продакшн)
- Отсутствие истории изменений и их документирования
- Сложность отката изменений при возникновении проблем
- Необходимость ручного применения изменений на разных средах

### Flyway - простой подход:

Flyway решает эти проблемы, предоставляя инструмент для управления миграциями БД. Миграции представляют собой SQL-скрипты с определенным именованием (V1__Create_employees_table.sql), которые применяются в строгом порядке. Flyway отслеживает, какие миграции уже применены, и автоматически применяет новые. Это обеспечивает согласованность схемы БД во всех средах и предоставляет возможность автоматического развертывания.

```sql
-- V1__Create_employees_table.sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE DEFAULT CURRENT_DATE
);

-- V2__Add_phone_column.sql
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

-- V3__Create_departments_table.sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    manager_id INTEGER REFERENCES employees(id)
);
```

### Использование Flyway в Java:

```java
import org.flywaydb.core.Flyway;

public class FlywayMigration {
    public static void main(String[] args) {
        Flyway flyway = Flyway.configure()
            .dataSource("jdbc:postgresql://localhost:5432/company", "postgres", "password")
            .locations("classpath:db/migration")
            .load();
        
        flyway.migrate(); // Применяем миграции
    }
}
```

### Liquibase - более гибкий подход:

Liquibase предоставляет более гибкий подход к миграциям, позволяя описывать изменения схемы БД в различных форматах: XML, YAML, JSON или SQL. В отличие от Flyway, Liquibase использует независимое от СУБД описание изменений, что позволяет использовать одни и те же миграции для разных СУБД. Кроме того, Liquibase предоставляет встроенные механизмы для отката изменений, что упрощает восстановление предыдущего состояния БД при необходимости.

```xml
<!-- db.changelog-master.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">
    
    <changeSet id="1" author="developer">
        <createTable tableName="employees">
            <column name="id" type="SERIAL">
                <constraints primaryKey="true"/>
            </column>
            <column name="first_name" type="VARCHAR(50)">
                <constraints nullable="false"/>
            </column>
            <column name="last_name" type="VARCHAR(50)">
                <constraints nullable="false"/>
            </column>
            <column name="email" type="VARCHAR(100)">
                <constraints nullable="false" unique="true"/>
            </column>
            <column name="department" type="VARCHAR(50)"/>
            <column name="salary" type="DECIMAL(10,2)"/>
            <column name="hire_date" type="DATE" defaultValueComputed="CURRENT_DATE"/>
        </createTable>
    </changeSet>
    
    <changeSet id="2" author="developer">
        <addColumn tableName="employees">
            <column name="phone" type="VARCHAR(20)"/>
        </addColumn>
    </changeSet>
</databaseChangeLog>
```

### Пример миграции на XML в Liquibase

Добавим новую таблицу `departments` и связь с `employees`:

```xml
<!-- db.changelog-003-add-departments.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">
    
    <changeSet id="003-1" author="developer">
        <createTable tableName="departments">
            <column name="id" type="SERIAL">
                <constraints primaryKey="true"/>
            </column>
            <column name="name" type="VARCHAR(50)">
                <constraints nullable="false" unique="true"/>
            </column>
            <column name="budget" type="DECIMAL(15,2)" defaultValue="0.00"/>
            <column name="created_at" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP"/>
        </createTable>
        
        <addColumn tableName="employees">
            <column name="department_id" type="INTEGER"/>
        </addColumn>
        
        <addForeignKeyConstraint 
            baseTableName="employees"
            baseColumnNames="department_id"
            constraintName="fk_employee_department"
            referencedTableName="departments"
            referencedColumnNames="id"/>
    </changeSet>
    
    <changeSet id="003-2" author="developer">
        <sql>
            INSERT INTO departments (name, budget) VALUES 
            ('IT', 1000000.00),
            ('HR', 500000.00),
            ('Finance', 800000.00);
        </sql>
        
        <update tableName="employees">
            <column name="department_id" value="1"/>
            <where>department = 'IT'</where>
        </update>
        
        <update tableName="employees">
            <column name="department_id" value="2"/>
            <where>department = 'HR'</where>
        </update>
        
        <update tableName="employees">
            <column name="department_id" value="3"/>
            <where>department = 'Finance'</where>
        </update>
    </changeSet>
    
    <changeSet id="003-3" author="developer">
        <dropColumn tableName="employees" columnName="department"/>
    </changeSet>
</databaseChangeLog>
```

### Использование Liquibase в Java:

```java
import liquibase.Liquibase;
import liquibase.database.Database;
import liquibase.database.DatabaseFactory;
import liquibase.database.jvm.JdbcConnection;
import liquibase.resource.ClassLoaderResourceAccessor;

public class LiquibaseMigration {
    public static void main(String[] args) {
        try (Connection conn = ConnectionPoolExample.getConnection()) {
            Database database = DatabaseFactory.getInstance()
                .findCorrectDatabaseImplementation(new JdbcConnection(conn));
            
            Liquibase liquibase = new Liquibase(
                "db/changelog/db.changelog-master.xml",
                new ClassLoaderResourceAccessor(),
                database
            );
            
            liquibase.update(); // Применяем все изменения
            System.out.println("Миграции успешно применены");
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Сравнение инструментов миграции:
```
┌─────────────────────────────────────────────────────────┐
│              Сравнение Flyway и Liquibase               │
├─────────────────┬─────────────────┬─────────────────────┤
│   Характеристика│     Flyway      │     Liquibase       │
├─────────────────┼─────────────────┼─────────────────────┤
│   Формат        │ SQL файлы       │ XML, YAML, JSON     │
│                 │                 │ SQL                 │
├─────────────────┼─────────────────┼─────────────────────┤
│   Сложность     │ Простой         │ Более гибкий        │
├─────────────────┼─────────────────┼─────────────────────┤
│   Откат         │ Требует         │ Поддержка           │
│   изменений     │ ручного SQL     │ автоматического     │
│                 │                 │ отката              │
├─────────────────┼─────────────────┼─────────────────────┤
│   Интеграция    │ Легкая          │ Более сложная       │
├─────────────────┼─────────────────┼─────────────────────┤
│   Рекомендация  │ Для простых     │ Для сложных         │
│                 │ проектов        │ enterprise проектов │
└─────────────────┴─────────────────┴─────────────────────┘
```

## Заключение

В этой лекции мы рассмотрели:

1. **Клиент-серверное взаимодействие** с PostgreSQL и фазы работы
2. **JDBC драйвер** - стандартный API для работы с БД в Java
3. **Протоколы запросов** - Simple и Extended Query
4. **Пулы соединений** - эффективное управление соединениями с HikariCP
5. **Прокси пулеры** - дополнительный уровень оптимизации
6. **Транзакции** - обеспечение целостности данных
7. **Миграции БД** - управление схемой с помощью Flyway и Liquibase

Правильное использование этих инструментов позволяет создавать надежные и масштабируемые приложения, работающие с базами данных.

## Практические рекомендации

1. Всегда используйте пулы соединений в продакшн-приложениях
2. Предпочитайте `PreparedStatement` вместо `Statement` для безопасности
3. Управляйте транзакциями явно для обеспечения целостности данных
4. Используйте миграции для управления схемой БД
5. Настройте мониторинг пула соединений и производительности БД