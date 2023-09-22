# Технологии программирования

[Назад к списку лекций](/lectures/2023-spring/)

## Веб-сервер на java

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

host/insert-student - неверно
host/put-all-5-marks

url host/student/5/marks?new-mark=5
method post 

get host/student

## Полезные ссылки

[Очень классная статья про TCP и UDP](https://habr.com/ru/post/711578/)

[Про сервлеты](https://javarush.com/groups/posts/2529-chastjh-5-servletih-pishem-prostoe-veb-prilozhenie)

[Еще про сервлеты](https://www.baeldung.com/intro-to-servlets)

[Простая веб-служба со встроенным Jetty](https://habr.com/ru/post/259067/)

[Jetty tutorial for begginers](https://examples.javacodegeeks.com/java-development/enterprise-java/jetty/jetty-tutorial-beginners/)
