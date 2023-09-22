# Лекция 22.04
## Filters and Interceptors. Spring Security. Authentication and authorization

## Filters and Interceptors (Фильтры и интерсепторы)

Как запросы попадают в Controller?


![](https://www.baeldung.com/wp-content/uploads/2021/05/filters_vs_interceptors-1536x573.jpg)

Как создать фильтр:

```java
@Component
public class LogFilter implements Filter {

    private static final Logger logger = LogManager.getLogger(LogFilter.class);

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        logger.info("Hello from: " + request.getLocalAddr());
        chain.doFilter(request, response);
    }

}
```

Как создать интерсептор:

```java
public class LogInterceptor implements HandlerInterceptor {

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
        // после обработчика, уже не можем поменять респонс
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) 
      throws Exception {
        logger.info("afterCompletion");
    }

}
```

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

## JWT токен (JSON Web Token)

JWT состоит из трех основных частей: заголовка (header), нагрузки (payload) и подписи (signature). 
Заголовок и нагрузка формируются отдельно в формате JSON, кодируются в base64, а затем на их основе вычисляется подпись.
Закодированные части соединяются друг с другом, и на их основе вычисляется подпись, которая также становится частью 
токена.

https://struchkov.dev/blog/ru/what-is-jwt/
https://struchkov.dev/blog/ru/jwt-implementation-in-spring/

![](https://javatodev.com/content/images/wordpress/2020/11/Untitled.png)



