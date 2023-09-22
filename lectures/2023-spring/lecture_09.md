# Лекция 07.04
## Spring Framework. JPA. Hibernate

Java Persistence API (JPA) - это спецификация для сопоставления объектов 
Java с таблицами базы данных

Hibernate - это поставщик JPA. Это означает, что он предоставляет 
реализацию для спецификации JPA. Это и ORM, и поставщик для JPA.

Object-Relational Mapping (ORM), которую реализует популярная 
библиотека Hibernate. Hibernate берет на себя задачу преобразования 
данных их реляционного вида в объектный, для чтения, и из объектного 
вида в реляционный — для записи. 

Основное понятие в Spring Data — это репозиторий. Это несколько 
интерфейсов которые используют JPA Entity для взаимодействия с ней. 
Так например интерфейс

`public interface CrudRepository<T, ID extends Serializable> extends Repository<T, ID>
`
