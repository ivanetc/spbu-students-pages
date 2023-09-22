# Лекция 29.04
## Попытки посмотреть на фронтенд. JSP. Thymeleaf. 

## JSP
Java Server Pages — это технология Java, которая позволяет создавать динамические веб-страницы для Java приложений.

JSP позволяет разработчику:
- получать данные из веб-страницы в Java-код;
- отправлять данные из Java кода на веб-страницу;
- писать Java-код, прямо внутри html (однако злоупотреблять этим не стоит).

Необходимость знания JSP можно оценить довольно высоко по нескольким причинам:
- JSP — одна из основных Java web-технологий;
- JSP широко используется в большинстве компаний и проектов;
- JSP бесшовно интегрируется с сервлетами Java внутри контейнера сервлетов.

![](https://cdn.javarush.com/images/article/5c675f57-eee0-4fad-9fcb-642ed80552d0/800.webp)
```groovy
	implementation 'javax.servlet:jstl'
	implementation 'org.apache.tomcat.embed:tomcat-embed-jasper'
```

```html
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>

<!DOCTYPE HTML>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Person List</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/style.css"/>
  </head>
  <body>
    <h1>Person List</h1>
   
    <br/><br/>
    <div>
      <table border="1">
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
        </tr>
        <c:forEach  items="${persons}" var ="person">
        <tr>
          <td>${person.firstName}</td>
          <td>${person.lastName}</td>
        </tr>
        </c:forEach>
      </table>
    </div>
  </body>
 
</html>
```

```java
import java.util.ArrayList;
import java.util.List;

import org.o7planning.sbjsp.model.Person;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class MainController {

    private static List<Person> persons = new ArrayList<Person>();

    static {
        persons.add(new Person("Bill", "Gates"));
        persons.add(new Person("Steve", "Jobs"));
    }

    @RequestMapping(value = { "/", "/index" }, method = RequestMethod.GET)
    public String index(Model model) {

        String message = "Hello Spring Boot + JSP";

        model.addAttribute("message", message);

        return "index";
    }

    @RequestMapping(value = { "/personList" }, method = RequestMethod.GET)
    public String viewPersonList(Model model) {

        model.addAttribute("persons", persons);

        return "personList";
    }

}
```

```java
public record Person(String firstName, String lastName) {}

```

## Thymeleaf

см проект

## React

npx create-react-app my-app



## Ссылки:
[Статья на javarush](https://javarush.com/groups/posts/2655-chto-takoe-jsp-razbiraemsja-s-vozmozhnostjami-na-praktike)

[Статья на Baeldung](https://www.baeldung.com/spring-boot-jsp)
