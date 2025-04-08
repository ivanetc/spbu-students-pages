# Технологии программирования

[Назад на главную](/)

# Конспект лекции: Фреймворк Spring

---

## **1. Введение**
### **Что такое Spring?**
- **Open-source фреймворк** для создания Java-приложений.
- Основные цели:
    - Уменьшение связанности кода (**loose coupling**).
    - Упрощение разработки через **IoC** (Inversion of Control) и **DI** (Dependency Injection).
- История: создан Родом Джонсоном в 2003 году как альтернатива EJB.

### **Преимущества Spring**
- Модульность (можно подключать только нужные компоненты).
- Интеграция с другими технологиями (Hibernate, Kafka, REST).
- Упрощение работы с БД, транзакциями, безопасностью.
- Поддержка тестирования.

---

## **2. Архитектура Spring**
### **Основные модули**
1. **Core Container**
    - **IoC-контейнер**: управление жизненным циклом объектов (бинов).
    - **DI**: внедрение зависимостей через конструктор, сеттеры или аннотации.

2. **Spring MVC**
    - Фреймворк для создания веб-приложений на основе паттерна **MVC** (Model-View-Controller).

3. **Spring Data Access**
    - Упрощение работы с базами данных (JDBC, JPA, Hibernate).
    - Spring Data JPA: автоматическая генерация репозиториев.

4. **Spring Boot**
    - Надстройка для быстрого старта проектов.
    - **Автоконфигурация**, встроенный сервер (Tomcat), стартеры.

![](https://cdn.javarush.com/images/article/15aad279-13e0-49ce-820a-094570fb5fb1/512.webp)
---

## **3. Dependency Injection (DI) и IoC**
### **Ключевые понятия**
- **Bean**: объект, управляемый Spring-контейнером.
- **IoC**: инверсия управления (контейнер создаёт и связывает объекты).
- **DI**: внедрение зависимостей (например, сервис получает репозиторий через конструктор).

### **Пример кода**
```java
@Component
public class UserService {
    private final UserRepository repository;

    @Autowired // DI через конструктор
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```


## Основные аннотации Spring и Spring Boot

---

## **4. Основные аннотации Spring**

### **4.1. Аннотации для создания бинов**
- **`@Component`**  
  Указывает, что класс является компонентом (бином), который управляется Spring-контейнером.
  ```java
  @Component
  public class UserService { ... }
  ```
- **`@Service`**  
  Специализированная версия @Component для слоя бизнес-логики (сервисов).
    ```java
    @Service
    public class PaymentService { ... }
    ```
- **`@Repository`**  
  Специализированная версия @Component для слоя доступа к данным (репозиториев).
  ```java
    @Repository
    public class UserRepository { ... }
    ``` 
- **`@Controller / @RestController`**
  - `@Controller`: для веб-контроллеров (возвращает представления).
  - `@RestController`: для REST-API (возвращает данные в формате JSON/XML).

```java
@RestController
public class UserController { ... }
```

### **4.2. Аннотации для внедрения зависимостей**

- **`@Autowired`**  
  Указывает, что зависимость должна быть внедрена автоматически.
  ```java
    @Service
    public class UserService {
        @Autowired
        private UserRepository repository;
    }
  ```
- **`@Qualifier`**  
  Указывает, какой бин должен быть внедрен.
  ```java
    @Service
    public class UserService {
        @Autowired
        @Qualifier("userRepository")
        private UserRepository repository;
    }
  ```

### **4.3. Конфигурационные аннотации**
- **`@Configuration`**  
  Помечает класс как источник конфигурации (определение бинов вручную).
  ```java
    @Configuration
    public class AppConfig {
        @Bean
        public DataSource dataSource() { ... }
    }
  ```
- **`Bean`**  
  Определяет бин вручную внутри конфигурационного класса.

## **5. Spring Boot**
### Особенности Spring Boot
1. Автоконфигурация

Spring Boot автоматически настраивает компоненты на основе зависимостей в проекте (например, подключение к БД).

2. Встроенный сервер

Запуск приложения через встроенный Tomcat, Jetty или Undertow (не требуется развёртывание WAR).

3. Стартеры (Starters)

Готовые наборы зависимостей для быстрого старта (например, spring-boot-starter-web для веб-приложений).

4. Упрощённая конфигурация

Настройки в файле application.properties/application.yml (порт, БД, логирование и др.).

### Генерация шаблона приложения
Используйте Spring Initializr:
1. Перейдите на https://start.spring.io.

1. Заполните параметры:
    1. Project: Maven/Gradle. 
   1. Language: Java. 
   1. Dependencies: Выберите нужные (например, Spring Web, Spring Data JPA, H2 Database). 
1. Сгенерируйте проект и откройте его в IDE (IntelliJ IDEA, Eclipse).

