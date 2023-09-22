# Лекция 01.04
## Spring Framework

Spring Framework, или просто Spring — один из самых популярных фреймворков для создания веб-приложений на Java

![](https://cdn.javarush.com/images/article/15aad279-13e0-49ce-820a-094570fb5fb1/512.webp)

Spring состоит из нескольких модулей:
- data access;
- web;
- core;
- и других.


Два важных момента:
- IoC (Inversion of Control) — инверсия управления.
- DI (Dependency Inversion, Dependency Injection)

Основные понятия в Spring-е
- Bean (бин)
- Application context (Контекст) это набор бинов

Как спринг будет знать, какие объекты создавать?

Ответ: при помощи конфигурации приложения. Есть 3 способа 
сконфигурировать приложение:
- при помощи xml файлов/конфигов;
- при помощи java-конфигов;
- автоматическая конфигурация.