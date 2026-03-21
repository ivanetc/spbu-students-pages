[Назад к списку лекций](/lectures/2023-spring/)

## Веб-сервер на java

### Предисловие 0. Аннотации и аспектно-ориентированное программирование. Lombok. Record. Работа с JSON.

спектно-ориентированное программирование (АОП)](#p2)
3. [Библиотека Lombok в Java](#p3)
4. [Record](#p4)
5. [Работа с JSON](#p5)

## Аннотации в java <a name="p1"></a>

Аннотации в Java — это специальные конструкции, которые предоставляют дополнительную информацию для компилятора, 
инструментов разработки и во время выполнения программы. Они не влияют на выполнение кода напрямую, но могут изменять 
процесс компиляции, генерации кода или поведение приложения в runtime.

## Что такое аннотации?

Аннотации — это своего рода «метки» или «теги», которые можно применять к классам, методам, полям и другим элементам 
программы. Они начинаются с символа @ и могут содержать атрибуты, которые определяют их поведение.

Пример:

```java
@Override
public void someMethod() {
    // тело метода
}
```

Зачем нужны аннотации?
1. Упрощение разработки: аннотации помогают автоматизировать некоторые задачи, такие как генерация кода, проверка типов 
и т. д.
2. Улучшение читаемости кода: они делают код более понятным, указывая на его назначение или особенности.
3. Интеграция с инструментами разработки: многие IDE и инструменты сборки используют аннотации для предоставления 
дополнительных функций, таких как рефакторинг, анализ кода и т. п.
4. Поддержка фреймворков и библиотек: аннотации часто используются в фреймворках и библиотеках для конфигурации и 
управления поведением компонентов.

## Как написать свою аннотацию?

Для создания собственной аннотации необходимо использовать ключевое слово interface вместе с @interface. Внутри 
аннотации можно определить атрибуты, которые будут хранить дополнительную информацию.

Пример определения аннотации:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MyAnnotation {
    String value() default "default value";
    int id();
}
```

Здесь:

- `@Retention` определяет, когда аннотация будет доступна (например, RetentionPolicy.RUNTIME означает, что аннотация 
будет доступна во время выполнения). 
- `@Target` указывает, к каким элементам программы можно применять аннотацию (например, ElementType.METHOD означает, 
что аннотацию можно применять к методам).

С какими концепциями программирования связаны аннотации?
- Аспектно-ориентированное программирование (AOP): аннотации часто используются в AOP для определения точек соединения
 (join points) и аспектов, которые будут применяться к коду. 
- Метапрограммирование: аннотации позволяют реализовывать метапрограммирование, т. е. написание кода, который генерирует
или манипулирует другим кодом. 
- Инверсия управления (IoC) и Dependency Injection (DI): в контексте IoC и DI аннотации используются для конфигурации 
компонентов и управления их зависимостями. 
- Обработка аннотаций во время компиляции и выполнения: аннотации могут быть обработаны специальными инструментами 
(например, процессорами аннотаций) во время компиляции для генерации дополнительного кода или во время выполнения для изменения поведения приложения.

Аннотации в Java — это мощный инструмент для улучшения процесса разработки, повышения читаемости кода и интеграции с 
различными инструментами и фреймворками. Понимание того, как работают аннотации и как их использовать, позволяет 
разработчикам более эффективно создавать и поддерживать свои приложения.

## Аспектно-ориентированное программирование (АОП) <a name="p2"></a>

Аспектно-ориентированное программирование (АОП) — это подход к написанию программ, который позволяет выделить и отдельно
описать так называемые «поперечные concerns» или «аспекты». Это могут быть функции, которые пересекаются с основной 
логикой программы и применяются в разных её частях, например, логирование, обработка ошибок, управление транзакциями 
или безопасность.

### Как работает АОП?
В АОП используются специальные конструкции — аннотации, которые указывают, где и как должен быть применён аспект. 
Например, вы можете определить аспект для логирования и указать, что он должен применяться ко всем методам, помеченным 
определённой аннотацией.

Это позволяет:

- Улучшить модульность и структурированность кода.
- Уменьшить дублирование кода.
- Упростить поддержку и внесение изменений в программу.

### Пример

Рассмотрим простой пример, который иллюстрирует основные идеи аспектно-ориентированного программирования (АОП). 
Предположим, у нас есть программа, которая выполняет простые арифметические операции: сложение и умножение. Мы хотим 
добавить логирование времени выполнения каждой операции без изменения исходного кода этих операций.

```java
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }
}
```

```java
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
@interface LogExecutionTime {
}

public class Calculator {

    @LogExecutionTime
    public int add(int a, int b) {
        return a + b;
    }

    @LogExecutionTime
    public int multiply(int a, int b) {
        return a * b;
    }
}
```

Сам аспект мы не будем реализовывать - его можно реализовать с помощью AspectJ. AspectJ — это расширение языка Java, 
которое позволяет реализовывать аспектно-ориентированное программирование (АОП).

## Библиотека Lombok в Java <a name="p3"></a>

Библиотека Lombok — это инструмент, который упрощает разработку на Java, автоматизируя создание шаблонного кода. Она 
позволяет сократить количество строк кода и сделать его более читаемым, устраняя необходимость вручную реализовывать 
стандартные методы, такие как геттеры, сеттеры, конструкторы и т. д.

### Что такое Lombok?
Lombok — это библиотека с открытым исходным кодом, которая использует аннотации для генерации дополнительного кода во 
время компиляции. Это означает, что вместо того, чтобы писать много строк шаблонного кода, разработчики могут 
использовать аннотации Lombok, и библиотека автоматически сгенерирует необходимый код.

### Зачем нужна Lombok?
- Сокращение объёма кода: Lombok позволяет избежать написания большого количества повторяющегося кода, такого как 
геттеры, сеттеры и конструкторы. Это делает код более компактным и читаемым. 
- Повышение производительности: автоматизация создания шаблонного кода экономит время разработчиков, позволяя им 
сосредоточиться на более сложных задачах. 
- Уменьшение вероятности ошибок: поскольку Lombok генерирует код автоматически, вероятность ошибок, связанных с 
ручным написанием кода, снижается. 
- Улучшение читаемости кода: код, написанный с использованием Lombok, часто более лаконичен и понятен, что облегчает 
его чтение и поддержку.

### Примеры использования Lombok

Генерация геттеров и сеттеров без Lombok:

```java
public class Person {
    private String name;
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
```

С lombok

```java
import lombok.Getter;
import lombok.Setter;

public class Person {
    @Getter @Setter
    private String name;
    @Getter @Setter
    private int age;
}
```

### Как добавить в проект:

```groovy
plugins {
    id 'io.franzbecker.gradle-lombok' version '5.0.0'
    id 'java'
}

lombok {
    version = '1.18.26'
    sha256 = ""
}
```

### Возможности

@Getter
@Setter

```java
@Getter
@Setter
public class Author {
    private int id;
    private String name;
    @Setter(AccessLevel.PROTECTED)
    private String surname;
}

public class Author {
    private int id;
    private String name;
    private String surname;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSurname() {
        return surname;
    }

    protected void setSurname(String surname) {
        this.surname = surname;
    }
}
```

@NoArgsConstructor - создает дефолтный конструктор
@AllArgsConstructor - создает конструктор, где все поля класса - аргументы
```java
@NoArgsConstructor
@AllArgsConstructor
public class Author {
    private int id;
    private String name;
    private String surname;
    private final String birthPlace;
}

public class Author {
    private int id;
    private String name;
    private String surname;
    private final String birthPlace;

    // @NoArgsConstructor
    public Author() {}

    // @AllArgsConstructor
    public Author(int id, String name, String surname, String birthPlace) {
        this.id = id
        this.name = name
        this.surname = surname
        this.birthPlace = birthPlace
    }

    // @RequiredArgsConstructor
    public Author(String birthPlace) {
        this.birthPlace = birthPlace
    }
}
```

@ToString - создает метод ToString
```java
@ToString(includeFieldNames=true)
public class Author {
    private int id;
    private String name;
    private String surname;
}

public class Author {
    private int id;
    private String name;
    private String surname;

    @Override
    public String toString() {
        return "Author(id=" + this.id + ", name=" + this.name + ", surnname=" + this.surname + ")";
    }
}
```

```java
@Getter
@Setter
@EqualsAndHashCode
public class Author {
    private int id;
    private String name;
    private String surname;
}

public class Author {

    // геттеры и сеттеры ...

    @Override
    public int hashCode() {
        final int PRIME = 31;
        int result = 1;
        result = prime * result + id;
        result = prime * result + ((name == null) ? 0 : name.hashCode());
        result = prime * result + ((surname == null) ? 0 : surname.hashCode());
        return result;
    }

    @Override
    public boolean equals(Object o) {
        if (o == this) return true;
        if (!(o instanceof Author)) return false;
        Author other = (Author) o;
        if (!other.canEqual((Object)this)) return false;
        if (this.getId() == null ? other.getId() != null : !this.getId().equals(other.getId())) return false;
        if (this.getName() == null ? other.getName() != null : !this.getName().equals(other.getName())) return false;
        if (this.getSurname() == null ? other.getSurname() != null : !this.getSurname().equals(other.getSurname())) return false;
        return true;
    }
}
```

@Data - сокращенная аннотация сочетающая @ToString, @EqualsAndHashCode, @Getter @Setter и @RequiredArgsConstructor.

```java
@Getter
@Builder
public class Student {
    private String firstName;
    private String lastName;
    private Long studentId;
    private String email;
    private String phoneNumber;
    private String address;
    private String country;
    private int age;
}

class Temp {
    Student john = Student.builder()
            .firstName("John")
            .lastName("Doe")
            .email("john@doe.com")
            .country("England")
            .age(20)
            .build();
}
```

### Плюсы Lombok
- Упрощение кода: Lombok позволяет сократить количество строк кода, удаляя необходимость в ручном написании геттеров, 
сеттеров и других стандартных методов.
- Снижение вероятности ошибок: автоматическое создание кода уменьшает вероятность ошибок, связанных с ручным кодированием.
- Улучшение читаемости: код становится более лаконичным и понятным.
- Поддержка инструментов разработки: многие IDE и инструменты сборки поддерживают Lombok, что упрощает его интеграцию 
в рабочий процесс.

### Недостатки Lombok
- Необходимость настройки: для использования Lombok необходимо настроить среду разработки и добавить библиотеку в проект.
- Возможны проблемы с совместимостью: некоторые инструменты и фреймворки могут не поддерживать Lombok или требовать 
дополнительной настройки.
- Может быть сложно понять, что происходит «под капотом»: поскольку Lombok генерирует код автоматически, разработчикам 
может быть сложно понять, как именно работает сгенерированный код.
- Зависимость от библиотеки: использование Lombok может привести к зависимости от этой библиотеки, что может усложнить 
миграцию на другие инструменты или платформы.

### Полезные ссылки

[Статья Lombok. Полное руководство](https://habr.com/ru/company/piter/blog/676394/)

[Статья Lombok возвращает величие Java](https://habr.com/ru/post/438870/)

[Статья Lombok: хорошее и плохое применение](https://medium.com/nuances-of-programming/lombock-хорошее-и-плохое-применение-4bd9cfdc5dd5)

## Record <a name="p4"></a>

Record — это относительно новая конструкция в языке Java, которая упрощает создание неизменяемых данных 
(immutable data). Она появилась в Java 16 как часть усилий по упрощению и улучшению языка.

### Зачем нужны Record?
- Упрощение кода: Record позволяет сократить количество шаблонного кода, необходимого для создания простых данных. Это 
особенно полезно при работе с данными, которые не должны изменяться после создания. 
- Читаемость и поддерживаемость: использование Record делает код более понятным и лёгким для поддержки, так как он явно 
указывает на намерение создать неизменяемый объект. 
- Безопасность и надёжность: неизменяемые объекты (immutable objects) менее подвержены ошибкам и обеспечивают лучшую 
безопасность потоков (thread safety), что важно для многопоточных приложений.

### Когда появились Record?
Record были введены в Java 16 в марте 2021 года как часть проекта Amber, направленного на улучшение и упрощение 
языка Java.

### Как раскрываются Record после компиляции?
После компиляции Record раскрывается в обычный класс с некоторыми автоматически сгенерированными методами:

- Геттеры: для каждого поля записи генерируются геттеры, которые позволяют получать значения полей.
- Методы equals и hashCode: эти методы генерируются автоматически, что обеспечивает корректное сравнение объектов Record.
- Метод toString: также генерируется автоматически, что упрощает вывод объектов Record в строковом представлении.

Пример записи:

```java
public record Person(String name, int age) {
    // автоматически генерируются геттеры, equals, hashCode и toString
}
```

Компилятор преобразует этот код в полноценный класс с соответствующими методами, что позволяет разработчикам 
сосредоточиться на логике приложения, а не на реализации базовых функциональностей.

Пример того, как будет выглядеть класс Person, созданный с использованием record, после компиляции в обычный класс Java:

```java
import java.util.Objects;

public final class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String name() {
        return name;
    }

    public int age() {
        return age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }

    @Override
    public String toString() {
        return "Person{" + "name=" + name + ", age=" + age + '}';
    }
}
```

Наследоваться от Record в Java нельзя, поскольку Record по умолчанию является final классом. Это сделано для обеспечения 
неизменяемости и простоты использования, что является одной из ключевых особенностей Record. Запрет на наследование 
помогает предотвратить потенциальные проблемы, связанные с нарушением инвариантов и изменением состояния объекта, что 
противоречит концепции неизменяемых данных.

## Работа с JSON. <a name="p5"></a>
JSON (JavaScript Object Notation) — это формат обмена данными, который используется для хранения и передачи 
структурированной информации. Он основан на синтаксисе объектов JavaScript и представляет данные в виде текстовых 
объектов, что делает его лёгким для чтения как для человека, так и для машины. JSON широко применяется в веб-разработке 
для обмена данными между сервером и клиентом, а также между различными приложениями.

С помощью JSON можно отправлять данные с сервера на веб-страницу.
- JSON — это текстовый файл, поэтому его можно легко передавать.
- JSON не зависит от конкретного языка.

Пример:
```json
{
  "name": "yandex",
  "id": 0
}
```

JSON обладает несколькими ключевыми особенностями:
- Простота и читаемость. Формат JSON интуитивно понятен и легко читается как машинами, так и людьми благодаря своей 
простой и логичной структуре. 
- Универсальность. JSON поддерживается множеством языков программирования и платформ, что делает его универсальным 
выбором для обмена данными между различными системами. 
- Лёгкость интеграции. JSON легко интегрируется с веб-службами и API, что делает его идеальным форматом для передачи 
данных в HTTP-запросах и ответах. 
- Иерархическая структура. Данные в JSON организованы в виде иерархической структуры, которая может включать в себя 
объекты (совокупности пар «ключ-значение») и массивы (упорядоченные списки значений). Это позволяет представлять сложные данные в структурированном виде. 
- Поддержка различных типов данных. JSON поддерживает основные типы данных, такие как строки, числа, булевы значения, 
а также null, объекты и массивы. Это обеспечивает гибкость при представлении разнообразных данных. 
- Компактность. JSON использует минимальный набор символов для представления данных, что делает его компактным и 
эффективным для передачи по сети. 
- Независимость от языка программирования. Хотя JSON возник в контексте JavaScript, он не привязан к какому-либо конкретному языку программирования и может быть использован с различными технологиями.


В Java существует несколько подходов к работе с JSON:

**Парсинг JSON:**

- Используется для анализа JSON-строк и извлечения из них данных. 
- Пример библиотеки: Json Simple. 
- Подход позволяет обрабатывать JSON как набор объектов и массивов, обеспечивая доступ к данным через ключи и индексы.

**Сериализация / десериализация объектов:**
- Позволяет преобразовывать Java-объекты в JSON-формат (сериализация) и обратно (десериализация).
- Примеры библиотек: Jackson, Gson.
- Этот метод удобен для работы с данными, которые нужно сохранить или передать в формате JSON, а затем восстановить в виде объектов Java.


### Json Simple

Json Simple — это библиотека для работы с JSON в Java, которая предоставляет простой и удобный способ парсить JSON-данные, а также создавать и манипулировать JSON-объектами.

Основные возможности Json Simple:

- Чтение JSON. Библиотека позволяет считывать JSON-данные из строк, файлов или потоков и преобразовывать их в иерархическую структуру объектов Java.
- Запись JSON. С помощью Json Simple можно создавать JSON-представление Java-объектов и записывать его в строку, файл или поток.
- Манипулирование данными. Библиотека предоставляет методы для доступа к элементам JSON-структуры, их изменения, добавления и удаления.


Конечно нам потребуется зависимость в gradle-файле (maven)
```groovy
implementation 'com.googlecode.json-simple:json-simple:1.1'
```

Мы будем работать с 2-мя основным классами:
- JSONObject
- JSONArray

```java
class Temp {
    public static String buildWeatherJson() {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("name", "Yandex");
        jsonObject.put("id", "0");

        return jsonObject.toJSONString();
    }

    public static void parseCurrentWeatherJson(String resultJson) {
        try {
            // конвертируем строку с Json в JSONObject для дальнейшего его парсинга
            JSONObject companyJsonObject = (JSONObject) JSONValue.parseWithException(resultJson);

            // получаем название города, для которого смотрим погоду
            System.out.println("Название компании: " + companyJsonObject.get("name"));

            // получаем массив элементов для поля weather
            /* ... "weather": [
            {
                "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
            }
            ], ... */
            JSONArray weatherArray = (JSONArray) weatherJsonObject.get("weather");
            // достаем из массива первый элемент
            JSONObject weatherData = (JSONObject) weatherArray.get(0);

            // печатаем текущую погоду в консоль
            System.out.println("Погода на данный момент: " + weatherData.get("main"));
            // и описание к ней
            System.out.println("Более детальное описание погоды: " + weatherData.get("description"));

        } catch (org.json.simple.parser.ParseException e) {
            e.printStackTrace();
        }
    }
}
```

## Jackson

Jackson — это популярная библиотека для работы с JSON в Java, которая предоставляет мощные возможности для сериализации и десериализации объектов. Она позволяет преобразовывать Java-объекты в JSON-формат и обратно, что упрощает обмен данными между приложениями и хранение информации.

Основные возможности Jackson:

- Сериализация: преобразование Java-объектов в JSON-строки или запись их в файлы.
- Десериализация: создание Java-объектов из JSON-строк или файлов.
- Поддержка аннотаций: возможность использования аннотаций для настройки процесса сериализации и десериализации.
- Гибкость: поддержка различных конфигураций и настроек для адаптации к различным требованиям проектов.

Подключение в gradle

```groovy
implementation 'com.fasterxml.jackson.core:jackson-core:2.10.1'
implementation 'com.fasterxml.jackson.core:jackson-annotations:2.10.1'
implementation 'com.fasterxml.jackson.core:jackson-databind:2.10.1'
```


```java
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class Employee {
    private String firstName;
    private String lastName;
    private int age;
}

public class JacksonExample {
    static ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) {
        Employee employee = new Employee("Mark", "James", 20);

        try {
            String json = objectMapper.writeValueAsString(employee);
            System.out.println(json);
        } catch (JsonProcessingException e) {
            throw new RuntimeException();
        }

        try {
            Employee employee1 = objectMapper.readValue(employeeJson, Employee.class);
            System.out.println(employee.getFirstName());
            System.out.println(employee.getLastName());
            System.out.println(employee.getAge());
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}

```

Иногда документ JSON представляет собой не объект, а список объектов. Давайте посмотрим, как можно его прочитать.
```java
class Temp {
    public static void main(String[] args) {
        File file = new File("src/test/resources/employeeList.json");
        List<Employee> employeeList = objectMapper.readValue(file, new TypeReference<>(){});

        assertThat(employeeList).hasSize(2);
        assertThat(employeeList.get(0).getAge()).isEqualTo(33);
        assertThat(employeeList.get(0).getLastName()).isEqualTo("Simpson");
        assertThat(employeeList.get(0).getFirstName()).isEqualTo("Marge");
    }
}
```



У Jackson есть свои аннотации:
@JsonSetter
@JsonGetter
@JsonIgnore

@JsonAnySetter

```java
public class Car {  
    @JsonSetter("car_brand")  
    private String carBrand;  
    private Map<String, String> unrecognizedFields = new HashMap<>();  
  
    @JsonAnySetter  
    public void allSetter(String fieldName, String fieldValue) {  
        unrecognizedFields.put(fieldName, fieldValue);  
    }  
}
```

### Предисловие 1. Немного про TCP-IP
Как же нам из приложения отправить запрос на сервер, использую эти ваши интернеты?

На примере доставки подарочной плитки шоколадки:

- Мы сначала нашу подарочку плитку должны упаковать
- Потом на уровне доставочной службы перевести к вашему другу
- А потом на уровне друга - распаковать и получить исходную шоколадку

![](https://habrastorage.org/getpro/habr/upload_files/b5e/edd/d8e/b5eeddd8e6be8a445708daa312f50ef0.png)

Какие же есть протоколы? Об этом вам подробнее расскажут на _Вычислительных системах и компьютерных сетях_.
Если вкратце - есть различные протоколы, которые определяют различные действия на различных
этапов передачи данных между программами. 

Так сложилось, что есть две модели, описывающие уровни протоколов. Одна из них теоретическая – модель OSI, а другая практическая – TCP/IP.

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/aff/6cf/3b1/aff6cf3b1baf6ac4e7e030f62812669e.png)

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/b47/646/e37/b47646e37cb04594f5cfc22165dd87f8.png)

- message - генерируется на уровне приложения (может быть http запрос)
- TCP или UDP header - присоединяется на транспортном уровне (информация о портах и другая)
- IP - заголовок - межсетевой уровень (адреса компьютеров)
- _by the way - message + TCP header + IP header = пакет данных_
- Ethernet header + Ethernet footer  - канальный уровень

Таким образом работа протоколов на пути нашего сообщения идет следующим образом:
![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/b1e/c0f/8c3/b1ec0f8c34448cf37dc7c7b73852a1ff.png)

### Предисловие 2. Немного про HTTP и REST API

Протокол HTTP:
- Протокол прикладного уровня, верхнего в моделях OSI и TCP-IP
- Основа - клиент-серверная архитектура программ. Клиент формирует запрос, сервер на него формирует ответ.
- Манипулирует над ресурсом, на который указывает URI (URL и URN - частные случаи URI)

#### Запрос HTTP
Запрос HTTP состоит из следующих элементов:

![](https://rune-dollar-ae8.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F6e930812-871d-4f02-8c6f-896581871bb8%2FUntitled.png?id=8aad3a2c-adad-4f87-966e-e2cc1dbfd7a4&table=block&spaceId=dbe9c3d4-5646-48c6-ab44-d4087dd70e2f&width=1480&userId=&cache=v2)


#### Ответ HTTP

![](https://rune-dollar-ae8.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F11e6b222-3ce8-476f-a927-4c41632b0e0a%2FUntitled.png?id=9d29fcd6-ec60-4129-9c92-3770af24f426&table=block&spaceId=dbe9c3d4-5646-48c6-ab44-d4087dd70e2f&width=1480&userId=&cache=v2)


#### Методы HTTP

- get (нет тела запроса)
- post (идемпотентны)
- put
- delete

![](https://miro.medium.com/max/724/1*bqTWyL7IFU4Z4xL0y4Su6A.jpeg)

#### Коды ответов

![](https://texterra.ru/upload/img/25-11-2020/2/1.jpg)

#### Пример запроса

![](https://rune-dollar-ae8.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F12924760-9cf7-468b-816d-6d11ce557d4a%2FUntitled.png?id=1b2786c6-2c1a-4af7-87cc-b581b016c3d4&table=block&spaceId=dbe9c3d4-5646-48c6-ab44-d4087dd70e2f&width=1480&userId=&cache=v2)

### Java Servlets
![](https://rune-dollar-ae8.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Faae5ff78-9960-4de8-8d1b-18b17f654f56%2FUntitled.png?id=ae4cc8a8-1ddf-462d-9ef0-e9e8bf3ba747&table=block&spaceId=dbe9c3d4-5646-48c6-ab44-d4087dd70e2f&width=1690&userId=&cache=v2)

Веб-контейнер - программа. В веб-контейнере развернут набор сервлетов. 

После того как соединение установлено, веб-контейнер формирует 2 объекта: HttpServletReuest and HttpServletResponse.

Зависимости gradle:
```groovy
    compileOnly 'jakarta.servlet:jakarta.servlet-api:5.0.0'
```

Пример сервлета:
```java
import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/ping")
public class PingServlet extends HttpServlet {
    /**
     * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String reply = "<h1>pong</h1>";
        response.getOutputStream().write( reply.getBytes("UTF-8") );
        response.setContentType("text/html; charset=UTF-8");
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setStatus( HttpServletResponse.SC_OK );
        
        // if response will have body
        //  response.getOutputStream().write( reply.getBytes("UTF-8") );
    }
}
```

Также можем заимплементить doPost, doPut, doDelete

![](https://rune-dollar-ae8.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F9288b649-444f-4dfd-940a-67386a7210f5%2FUntitled.png?id=ea7718cc-8a39-4d3f-a0e3-7b1b9053795c&table=block&spaceId=dbe9c3d4-5646-48c6-ab44-d4087dd70e2f&width=1690&userId=&cache=v2)

Экземпляры сервлета создает веб-контейнер в рантайме.
После этого сервлет в рантайме может обрабатывать запросы. Веб-контейнер плодит по отдельному потоку на каждый запрос, 
приходящий к нему, и сервлеты соответственно эти запросы обрабатывают.


### Jetty Server

Теперь нам нужен контейнер для наших сервлетов. Наиболее распространенные веб-сервера на java - Tom Cat, Jetty и др.
На этой лекции для избежания взрыва мозга посмотрим на Jetty, тк он кажется чуть проще.

Jetty — свободный контейнер сервлетов, написанный полностью на Java.

Конечно нам потребуются зависимости в gradle:
```groovy
implementation 'org.eclipse.jetty:jetty-servlet:11.0.14'
implementation 'org.eclipse.jetty:jetty-server:11.0.14'
```

Создадим стартовый класс для нашего сервера:
```java
public class JettyServer {
    private Server server;

    public void start() throws Exception {
        int port = 8080;
        Server server = new Server(8080);
        ServletContextHandler handler = new ServletContextHandler(server, "/");
        handler.addServlet(PingServlet.class, "/ping");

        try {
            server.start();
            System.out.println("Listening port : " + port );
        } catch (Exception e) {
            System.out.println("Error.");
            e.printStackTrace();
        }
    }
}
```


## REST API

REST (Representational State Transfer) — это архитектурный стиль для построения распределённых систем, особенно веб-сервисов. REST API — это API, который следует принципам REST.

### Основные принципы REST

1. **Клиент-серверная архитектура**: Клиент и сервер разделены, что позволяет им развиваться независимо друг от друга.

2. **Отсутствие состояния (Stateless)**: Каждый запрос от клиента должен содержать всю информацию, необходимую для понимания и обработки запроса. Сервер не хранит информацию о состоянии клиента между запросами.

3. **Кэшируемость**: Ответы от сервера должны быть явно помечены как кэшируемые или нет, что позволяет улучшить производительность.

4. **Единый интерфейс**: Унифицированный интерфейс между компонентами упрощает архитектуру и позволяет каждой части развиваться независимо.

5. **Слоистая система**: Архитектура может состоять из нескольких слоёв, каждый из которых выполняет свою функцию.

6. **Код по требованию (Code on Demand)**: Сервер может расширять функциональность клиента, передавая ему исполняемый код (необязательный принцип).

### Ресурсы и URI

В REST всё является ресурсом. Каждый ресурс имеет уникальный идентификатор — URI (Uniform Resource Identifier).

Примеры URI для ресурсов:
- `/users` — коллекция пользователей
- `/users/123` — конкретный пользователь с ID 123
- `/users/123/orders` — заказы пользователя 123
- `/products/456/reviews` — отзывы о продукте 456

### HTTP методы в REST

REST использует стандартные HTTP методы для выполнения операций над ресурсами:

#### GET
- Получение ресурса или коллекции ресурсов
- **Безопасный** (не изменяет состояние сервера)
- **Идемпотентный** (множественные одинаковые запросы дают тот же результат)
- Не должен иметь тела запроса

Примеры:
```
GET /users              — получить всех пользователей
GET /users/123          — получить пользователя с ID 123
GET /users/123/orders   — получить заказы пользователя 123
```

#### POST
- Создание нового ресурса
- **Не безопасный** (изменяет состояние сервера)
- **Не идемпотентный** (множественные одинаковые запросы создадут несколько ресурсов)
- Имеет тело запроса с данными нового ресурса

Примеры:
```
POST /users
{
  "name": "Ivan",
  "email": "ivan@example.com"
}
— создать нового пользователя
```

#### PUT
- Полное обновление ресурса (замена)
- **Не безопасный** (изменяет состояние сервера)
- **Идемпотентный** (множественные одинаковые запросы дадут тот же результат)
- Имеет тело запроса с полными данными ресурса

Примеры:
```
PUT /users/123
{
  "id": 123,
  "name": "Ivan Updated",
  "email": "ivan.updated@example.com"
}
— полностью обновить пользователя 123
```

#### PATCH
- Частичное обновление ресурса
- **Не безопасный** (изменяет состояние сервера)
- **Не идемпотентный** (зависит от реализации)
- Имеет тело запроса только с изменяемыми полями

Примеры:
```
PATCH /users/123
{
  "email": "new.email@example.com"
}
— обновить только email пользователя 123
```

#### DELETE
- Удаление ресурса
- **Не безопасный** (изменяет состояние сервера)
- **Идемпотентный** (после первого удаления последующие запросы не изменят состояние)
- Обычно не имеет тела запроса

Примеры:
```
DELETE /users/123  — удалить пользователя 123
```

### Идемпотентность

**Идемпотентность** — это свойство операции, при котором многократное выполнение одной и той же операции даёт тот же результат, что и однократное выполнение.

#### Почему идемпотентность важна?

1. **Надёжность в сети**: В распределённых системах запросы могут повторяться из-за сетевых проблем, таймаутов или ошибок. Идемпотентные операции гарантируют, что повторные запросы не приведут к нежелательным побочным эффектам.

2. **Безопасность**: Предотвращает случайное дублирование операций (например, двойное списание денег с счёта).

3. **Предсказуемость**: Поведение системы становится более предсказуемым и отлаживаемым.

#### Идемпотентность HTTP методов:

| Метод | Идемпотентный | Объяснение |
|-------|---------------|------------|
| GET | ✅ Да | Множественные запросы возвращают одни и те же данные |
| POST | ❌ Нет | Каждый запрос создаёт новый ресурс |
| PUT | ✅ Да | Замена ресурса одним и тем же содержимым даёт тот же результат |
| PATCH | ❌ Нет (обычно) | Зависит от операции (например, инкремент не идемпотентен) |
| DELETE | ✅ Да | После первого удаления последующие не изменят состояние |

#### Примеры идемпотентности:

**Идемпотентная операция (PUT):**
```bash
# Первый запрос
PUT /accounts/123
{
  "balance": 1000
}
# Результат: баланс = 1000

# Второй запрос (повтор)
PUT /accounts/123
{
  "balance": 1000
}
# Результат: баланс = 1000 (тот же результат)
```

**Не идемпотентная операция (POST):**
```bash
# Первый запрос
POST /orders
{
  "userId": 123,
  "amount": 100
}
# Результат: создан заказ с ID 1

# Второй запрос (повтор)
POST /orders
{
  "userId": 123,
  "amount": 100
}
# Результат: создан заказ с ID 2 (другой результат!)
```

**Не идемпотентная операция (PATCH с инкрементом):**
```bash
# Первый запрос
PATCH /accounts/123
{
  "operation": "increment",
  "value": 100
}
# Результат: баланс = 1100 (было 1000)

# Второй запрос (повтор)
PATCH /accounts/123
{
  "operation": "increment",
  "value": 100
}
# Результат: баланс = 1200 (другой результат!)
```

### Коды ответов HTTP

REST API использует стандартные коды ответов HTTP для указания результата операции:

#### 2xx — Успешные операции
- `200 OK` — успешный запрос
- `201 Created` — ресурс успешно создан (обычно после POST)
- `204 No Content` — успешный запрос без содержимого в ответе (обычно после DELETE или PUT)

#### 4xx — Ошибки клиента
- `400 Bad Request` — некорректный запрос
- `401 Unauthorized` — требуется аутентификация
- `403 Forbidden` — нет прав доступа
- `404 Not Found` — ресурс не найден
- `409 Conflict` — конфликт с текущим состоянием ресурса
- `422 Unprocessable Entity` — синтаксически корректный запрос, но семантически ошибочный

#### 5xx — Ошибки сервера
- `500 Internal Server Error` — внутренняя ошибка сервера
- `503 Service Unavailable` — сервис временно недоступен

### Форматы данных

REST API обычно использует JSON для обмена данными:

**Пример ответа (GET /users/123):**
```json
{
  "id": 123,
  "name": "Ivan",
  "email": "ivan@example.com",
  "createdAt": "2024-01-15T10:30:00Z",
  "_links": {
    "self": "/users/123",
    "orders": "/users/123/orders"
  }
}
```

**Пример запроса (POST /users):**
```json
{
  "name": "Petr",
  "email": "petr@example.com"
}
```

### Версионирование API

Существует несколько подходов к версионированию REST API:

1. **Версия в URL:**
   ```
   /api/v1/users
   /api/v2/users
   ```

2. **Версия в заголовке:**
   ```
   Accept: application/vnd.myapi.v1+json
   ```

3. **Версия в параметрах запроса:**
   ```
   /users?version=1
   ```

### Пример полного REST API

Рассмотрим пример REST API для управления пользователями:

```
GET    /users              — получить всех пользователей
GET    /users/{id}         — получить пользователя по ID
POST   /users              — создать нового пользователя
PUT    /users/{id}         — полностью обновить пользователя
PATCH  /users/{id}         — частично обновить пользователя
DELETE /users/{id}         — удалить пользователя

GET    /users/{id}/orders  — получить заказы пользователя
POST   /users/{id}/orders  — создать заказ для пользователя
```

**Примеры запросов и ответов:**

1. Создание пользователя:
```bash
POST /users
Content-Type: application/json

{
  "name": "Anna",
  "email": "anna@example.com"
}

Ответ:
201 Created
Location: /users/456

{
  "id": 456,
  "name": "Anna",
  "email": "anna@example.com",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

2. Получение пользователя:
```bash
GET /users/456

Ответ:
200 OK

{
  "id": 456,
  "name": "Anna",
  "email": "anna@example.com",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

3. Обновление пользователя:
```bash
PUT /users/456
Content-Type: application/json

{
  "id": 456,
  "name": "Anna Updated",
  "email": "anna.updated@example.com"
}

Ответ:
200 OK

{
  "id": 456,
  "name": "Anna Updated",
  "email": "anna.updated@example.com",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T11:00:00Z"
}
```

4. Удаление пользователя:
```bash
DELETE /users/456

Ответ:
204 No Content
```

5. Ошибка при попытке получить несуществующего пользователя:
```bash
GET /users/999

Ответ:
404 Not Found

{
  "error": "User not found",
  "code": "USER_NOT_FOUND",
  "details": "User with ID 999 does not exist"
}
```

### Лучшие практики REST API

1. **Используйте существительные во множественном числе для ресурсов:**
   - ✅ `/users`, `/products`, `/orders`
   - ❌ `/user`, `/getUsers`, `/getAllUsers`

2. **Используйте правильные HTTP методы:**
   - GET для получения данных
   - POST для создания
   - PUT для полного обновления
   - PATCH для частичного обновления
   - DELETE для удаления

3. **Возвращайте правильные коды ответов:**
   - 201 для создания ресурса
   - 200/204 для успешных операций
   - 400 для ошибок клиента
   - 404 для несуществующих ресурсов
   - 500 для ошибок сервера

4. **Используйте пагинацию для больших коллекций:**
   ```
   GET /users?page=1&limit=20
   ```

5. **Поддерживайте фильтрацию, сортировку и поиск:**
   ```
   GET /users?name=Ivan&sort=createdAt:desc
   ```

6. **Включайте метаданные в ответы:**
   ```json
   {
     "data": [...],
     "meta": {
       "total": 100,
       "page": 1,
       "limit": 20
     }
   }
   ```

7. **Обеспечивайте идемпотентность там, где это возможно:**
   - Используйте PUT вместо POST для обновлений
   - Добавляйте уникальные идентификаторы для операций
   - Реализуйте механизмы обработки повторных запросов

8. **Документируйте ваш API:**
   - Используйте OpenAPI/Swagger
   - Описывайте все эндпоинты, параметры и ответы
   - Приводите примеры запросов и ответов

## Полезные ссылки

[Очень классная статья про TCP и UDP](https://habr.com/ru/post/711578/)

[Про сервлеты](https://javarush.com/groups/posts/2529-chastjh-5-servletih-pishem-prostoe-veb-prilozhenie)

[Еще про сервлеты](https://www.baeldung.com/intro-to-servlets)

[Простая веб-служба со встроенным Jetty](https://habr.com/ru/post/259067/)

[Jetty tutorial for begginers](https://examples.javacodegeeks.com/java-development/enterprise-java/jetty/jetty-tutorial-beginners/)

[Парсинг JSON с помощью Jackson](https://habr.com/ru/company/otus/blog/687004/)
