# Технологии программирования

[Назад к списку лекций](/lectures/2023-spring/)

## Аннотации и аспектно-ориентированное программирование. Lombok. Record. Работа с JSON.

## Аннотации в java

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

## Аспектно-ориентированное программирование (АОП)

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

## Библиотека Lombok в Java

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

## Record

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

## Работа с JSON.
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

https://habr.com/ru/company/otus/blog/687004/


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

