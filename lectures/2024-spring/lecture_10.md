# Лекция 20.04
## Filters and Interceptors. Spring Security. Authentication and authorization

## Filters and Interceptors (Фильтры и интерсепторы)

Фильтры и интерсепторы в Spring MVC играют ключевую роль в управлении запросами и ответами, обеспечивая гибкость и 
контроль над процессом обработки запросов.

Прежде, чем говорить о фильтрах и интерсепторах, нужно разобраться, как обрабатываются запросы в Spring

### Как запросы попадают в Controller?

В Spring Java запросы попадают в контроллер через цепочку обработчиков, начиная с DispatcherServlet. DispatcherServlet 
является центральным компонентом Spring MVC, который отвечает за обработку входящих HTTP-запросов. DispatcherServlet 
в Spring MVC - это центральный сервлет, который обрабатывает входящие HTTP-запросы и направляет их к 
соответствующему контроллеру для дальнейшей обработки. 

Он играет ключевую роль в архитектуре Spring MVC, выполняя следующие функции:
- Анализ запроса: DispatcherServlet анализирует URL запроса, параметры запроса и заголовки, чтобы определить, какой контроллер должен обработать запрос.
- Преобразование параметров: DispatcherServlet преобразует параметры запроса в объекты Java, используя механизмы привязки данных.
- Вызов метода контроллера: На основе анализа запроса DispatcherServlet вызывает соответствующий метод контроллера, передавая ему преобразованные параметры.
- Обработка ответа: После выполнения логики в контроллере, DispatcherServlet преобразует ответ от контроллера в подходящий формат (например, HTML, JSON) и отправляет его обратно клиенту.

DispatcherServlet позволяет разработчикам легко создавать и настраивать веб-приложения на Java, используя Spring MVC, 
обеспечивая гибкость и контроль над обработкой запросов и ответов.

![](https://www.baeldung.com/wp-content/uploads/2021/05/filters_vs_interceptors-1536x573.jpg)

### Что такое фильтры и интерсепторы? В чем отличие?

**Фильтры в Spring MVC** работают на уровне Java Servlet и могут выполнять широкий спектр задач, таких как сжатие данных, 
аутентификация, преобразование кодировки и т.д. Они применяются до того, как запрос достигнет контроллера, и могут 
модифицировать запрос или ответ перед их передачей дальше по цепочке обработки. Фильтры настраиваются через конфигурацию 
web.xml или аннотацию @WebFilter.

**Интерсепторы в Spring MVC**, напротив, тесно интегрированы с фреймворком Spring и предназначены для выполнения действий 
до и после обработки контроллера. Они позволяют реализовать логику, которая должна выполняться независимо от конкретного
контроллера, например, проверку авторизации или логирование. Интерсепторы настраиваются через конфигурацию MVC или 
использование HandlerInterceptor.

Оба инструмента имеют свои преимущества и недостатки, и выбор между ними зависит от конкретных требований проекта. 
Фильтры лучше подходят для выполнения операций, не связанных напрямую с обработкой запросов контроллерами, в то время 
как интерсепторы обеспечивают более тонкую настройку процессов внутри Spring MVC.

### Как создать фильтр

Чтобы создать фильтр в Spring, вам необходимо выполнить следующие шаги:
1. Реализовать интерфейс `javax.servlet.Filter` или `jakarta.servlet.Filter` (для Spring Boot 3 и выше).
2. Переопределить метод `doFilter()` для реализации логики фильтрации.

Пример создания простого фильтра, который выводит сообщение при каждом запросе%

```java
@Component
public class LoggingFilter implements Filter {

    private static final Logger logger = LogManager.getLogger(LogFilter.class);

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        logger.info("Hello from: " + request.getLocalAddr());
        chain.doFilter(request, response);
    }

}
```

В этом примере класс `LoggingFilter` реализует интерфейс `Filter`, переопределяя метод `doFilter()`. Внутри метода 
`doFilter()` мы выводим сообщение в лог, а затем вызываем `chain.doFilter()`, чтобы передать запрос дальше по цепочке 
фильтров.

Чтобы зарегистрировать фильтр в контексте Spring, можно использовать аннотацию `@Component`, которая автоматически 
регистрирует компонент в контексте Spring.

### Как создать интерсептор

Чтобы создать интерсептор в Spring, вам нужно выполнить следующие шаги:

1.Реализовать интерфейс `org.springframework.web.servlet.HandlerInterceptor`.
2.Переопределить методы `preHandle`, `postHandle` и `afterCompletion` для реализации логики интерсептора.

Пример создания простого интерсептора, который выводит сообщение при каждом запросе:

```java
public class LoggingInterceptor implements HandlerInterceptor {

    private Logger logger = LoggerFactory.getLogger(LogInterceptor.class);

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) 
      throws Exception {
        logger.info("preHandle");
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) 
      throws Exception {
        logger.info("postHandle");
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) 
      throws Exception {
        logger.info("afterCompletion");
        // после обработчика, уже не можем поменять респонс
    }

}
```

В этом примере класс `LoggingInterceptor` реализует интерфейс `HandlerInterceptor`, переопределяя методы `preHandle`, 
`postHandle` и `afterCompletion`. Внутри метода `preHandle` мы выводим сообщение в лог, а затем возвращаем `true`, 
чтобы разрешить дальнейшую обработку запроса. 

Методы `postHandle` и `afterCompletion` могут использоваться для дополнительной логики после обработки запроса.
Методы postHandle и afterCompletion в Spring MVC Interceptors выполняют разные задачи и вызываются в разное время 
в процессе обработки запроса:
- postHandle - вызывается после того, как метод-обработчик контроллера завершил свою работу, но до того, как 
DispatcherServlet начнет обрабатывать результат. Этот метод используется для добавления информации в объект 
ModelAndView, который будет передан представлению. Например, здесь можно добавить дополнительные атрибуты модели или 
изменить содержимое объекта ModelAndView.
- afterCompletion - вызывается после того, как представление было полностью отрисовано и ответ был отправлен клиенту.
Этот метод используется для выполнения операций, связанных с завершением обработки запроса, таких как логирование, 
очистка ресурсов и т.д. Здесь уже нельзя изменить результат обработки запроса, так как он был отправлен клиенту.

Таким образом, основное отличие между этими двумя методами заключается в том, что postHandle дает возможность модифицировать результат обработки запроса до его отправки клиенту, в то время как afterCompletion позволяет выполнить операции после завершения обработки запроса и отправки ответа клиенту.

Чтобы зарегистрировать интерсептор в контексте Spring, можно использовать аннотацию `@Component`, которая автоматически 
регистрирует компонент в контексте Spring.

### Как выбрать что использовать?

Лучше использовать фильтры для:
- Authentication
- Logging and auditing
- Image and data compression
- Any functionality we want to be decoupled from Spring MVC

Лучше использовать интерспеторы для:
- Handling cross-cutting concerns such as application logging
- Detailed authorization checks
- Manipulating the Spring context or model

[Статейка про фильтры и интерсепторы](https://www.baeldung.com/spring-mvc-handlerinterceptor-vs-filter)

## Аутентификация и авторизация

**Аутентификация** — это процесс подтверждения личности пользователя. Представьте, что вы хотите зайти в свой аккаунт 
на сайте, и вам нужно ввести логин и пароль. Когда вы вводите правильные данные, сайт подтверждает, что вы — это вы, 
и разрешает вам продолжить работу. Это и есть аутентификация.

**Авторизация** — это процесс предоставления пользователю прав доступа к определённым ресурсам или действиям на сайте. 
Например, после успешной аутентификации вы можете получить доступ к личным настройкам своего профиля, опубликовать 
пост в блоге или отредактировать статью. Эти действия требуют авторизации.

Существует несколько основных способов аутентификации, каждый из которых имеет свои преимущества и недостатки:

- **Парольная аутентификация** - это классический способ аутентификации, основанный на вводе пользователем логина и 
пароля. Этот метод прост в реализации, но имеет низкую степень безопасности, так как пароли могут быть украдены или 
взломаны.
- **Двухфакторная аутентификация (2FA)** - это метод, который требует от пользователя предоставить два фактора 
аутентификации: что-то, что вы знаете (пароль), и что-то, что у вас есть (например, токен или код, отправленный на 
мобильное устройство). Это значительно повышает уровень безопасности, поскольку злоумышленнику необходимо получить 
доступ к обоим факторам одновременно.
- **Биометрическая аутентификация** - это метод, который использует уникальные биологические характеристики пользователя,
такие как отпечаток пальца, сканирование радужной оболочки глаза или распознавание голоса, для аутентификации. 
Преимущества включают высокую степень безопасности и удобство использования.
- **Аутентификация по сертификатам** - этот метод использует цифровые сертификаты для подтверждения личности 
пользователя. Сертификат содержит открытый ключ пользователя, который может быть проверен сервером. Преимущества 
включают высокий уровень безопасности и возможность шифрования данных.
- **Аутентификация по токенам** - этот метод использует токены (физические или виртуальные) для аутентификации. 
Токены могут содержать уникальный код или ключ, который пользователь должен предоставить для аутентификации. 
Преимущества включают удобство использования и возможность удалённой аутентификации.

### JWT-аутентификация
JSON Web Token (JWT) - это формат токена, который используется для аутентификации и обмена информацией между сторонами. 
JWT состоит из трех частей: заголовка (header), нагрузки (payload) и подписи (signature). Заголовок содержит информацию 
о типе токена и алгоритме шифрования, полезная нагрузка содержит данные о пользователе или другие полезные данные, 
а подпись используется для проверки подлинности токена.

JWT-аутентификация позволяет безопасно передавать информацию о пользователе между клиентом и сервером без необходимости 
постоянного обращения к базе данных для проверки подлинности. Это упрощает процесс аутентификации и уменьшает нагрузку 
на сервер.

Представьте, что вы студент, который хочет войти в здание университета. Обычно, чтобы попасть внутрь, вам нужно 
предъявить студенческий билет охраннику на входе. Это подтверждает вашу личность и даёт вам право 
находиться в университете.
Примерно так же работает JWT-аутентификация. Только вместо студенческого билета используется специальный токен — JWT. 
Этот токен содержит информацию о пользователе, например, его имя, роль (студент) и дату рождения. Когда пользователь хочет получить доступ к какому-либо ресурсу, он отправляет JWT-токен вместе с запросом. Сервер проверяет токен, расшифровывает его и узнаёт, кто отправил запрос. Если информация в токене верна, сервер разрешает пользователю получить доступ к ресурсу.
Пример использования JWT-аутентификации в университете:
1. Студент регистрируется в системе и вводит свои данные.
2. Система создаёт JWT-токен, который содержит информацию о студенте, например, его имя, роль и дату создания токена.
3. Система отправляет JWT-токен студенту.
4. Студент сохраняет JWT-токен в своём устройстве.
5. Каждый раз, когда студент хочет получить доступ к какой-либо странице системы, он отправляет JWT-токен вместе с запросом.
6. Сервер проверяет JWT-токен, расшифровывает его и узнаёт, кто отправил запрос. Если информация в токене верна, сервер разрешает студенту получить доступ к странице.


https://struchkov.dev/blog/ru/what-is-jwt/
https://struchkov.dev/blog/ru/jwt-implementation-in-spring/

![](https://javatodev.com/content/images/wordpress/2020/11/Untitled.png)


## Как реализовать аутентификацию в Spring?

[Документация по Spring Security](https://docs.spring.io/spring-security/reference/servlet/authentication/passwords/basic.html)
[Пошаговая инструкция (почти рабочая)](https://springjava.com/spring-boot/spring-security-basic-authentication-spring-boot/)