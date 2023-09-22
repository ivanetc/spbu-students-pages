# Технологии программирования

[Назад к списку лекций](/lectures/2023-spring/)

## Lombok. Record. Работа с JSON.

## Lombok

```java
class Company {
    private String name;
    private int id;

    public Company() {

    }

    public Company(String name, int id) {
        this.id = id;
        this.name = name;
    }

    public String getName() {
        return name;
    }
}

class Company {
    private String name;
    private int id;
}
```

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

Ломбок - упрощает написание кода, генерируя за нас часть кода на этапе компиляции
Делаем при помощи аннотаций:

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


POJO - plain old java objects. простой Java-объект, не ограниченный какими-либо запретами, 
специфичными для того или иного фреймворка (за исключением спецификации самой Java, разумеется) и 
пригодный для использования в любой среде.

https://habr.com/ru/company/piter/blog/676394/
https://habr.com/ru/post/438870/
https://medium.com/nuances-of-programming/lombock-хорошее-и-плохое-применение-4bd9cfdc5dd5


## Record

```java
class Company {
    private final String name;
    private final int id;

    public Company(String name, int id) {
        this.name = name;
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public int getId() {
        return id;
    }

    @Override
    public String toString() {
        return super.toString();
    }
}

record Company(String name, int id) { }

/*
 * раскроектся в final класс, наследник от java. ... .Record, все поля приватные и final, созданы публичные
 * getter-ы
 * */
```


## Работа с JSON.
JSON — это простой формат для хранения и отправки данных на веб-страницу. 

JSON — это аббревиатура от “JavaScript Object Notation” (Обозначение Объектов JavaScript). 
С помощью JSON можно отправлять данные с сервера на веб-страницу. 
- JSON — это текстовый файл, поэтому его можно легко передавать.
- JSON не зависит от конкретного языка.

```json
{
  "name": "yandex",
  "id": 0
}

```

Особенности:
- Простой
- Имеет независимую платформу
- Легко передать
- Поддерживает расширяемость
- Наличие совместимости

Есть несколько подходов к работе с json в Java:
- Парсить json (например, используя API Json Simple)
- Сериализовать / десериализовать объекты (Jackson, gson)

### Json Simple

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

