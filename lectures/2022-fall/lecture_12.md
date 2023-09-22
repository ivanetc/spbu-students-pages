# Технологии программирования

[Назад к списку лекций](/lectures/2022-fall/)

## Исключения в Java
Исключения - это способ прерывания нормального выполнения программы.

## Какие бывают исключения
![alt text](https://fuzeservers.ru/wp-content/uploads/e/1/a/e1a7cb380cd3af059bd0a13ab85497b5.jpeg)

## try-catch

```java

import java.io.IOException;
import java.util.Scanner;
import java.util.stream.Collectors;

public class ExceptionsExample {
public static void main(String[] args) {

        // Как бросить исключение:
        throw new RuntimeException("Всегда бросаю исключение, потому что могу");

        // Что делать, если после того, как бросили исключение, мы хотим продолжить работу программы?
        // Например, если мы завели какие-нибудь данные и не успели их сохранить? Или, например, мы хотим
        // получив исключения как-то осознанно об этом сообщить пользователю?
        // Для этого заиспользуем блок try-catch-finally
        
        try {
            // В блок try помещаем код, который может бросить исключение
            // Часто таким кодом может быть запрос к внешним ресурсам - файловой системе, БД, интернету
            readFile();
            // В readFile мы получаем исключение. Значит выполнение программы будет приостановлено и
            // все, что мы напишем в блоке try ниже не будет выполнено
            
        } catch (IOException e) {
            // Здесь мы можем обработать исключение - например распечатать какие-нибудь данные из него 
            // (например e.message)
        } catch (Error e) {
            System.out.println("error catched");
        }
        
        
        Scanner in = new Scanner(System.in);
        var a = in.tokens().map(String::toLowerCase).collect(Collectors.groupingBy(x -> x, Collectors.counting()));

    }

    
    // Здесь мы должны указать в заголовке функции 'throws IOException',
    // тк IOException не является RuntimeException и значит мы должны явно указывать, что метод 
    // может бросить соответствующее исключение
    private static void readFile() throws IOException {
        throw new IOException();
    }
}
```