# Технологии программирования

[Назад на главную](/)

## Лекция 7. Generics. Классы-обертки над примитивными типами. Optional.
### Содержание
1. [Generics](#generics)
2. [Классы-обертки над примитивными типами](#primitives)
3. [Optional](#optional)

## Generics <a name="generics"></a> 

Generic, или обобщённые типы, в Java — это механизм, который позволяет создавать классы, интерфейсы, методы и делегаты 
с параметрами, которые могут быть любого типа, а не только заранее известного. Это позволяет сделать код более 
гибким и расширяемым, поскольку его можно использовать с разными типами данных без необходимости создавать 
отдельный вариант кода для каждого типа.

Пример использования обобщенных типов (generic) в Java можно привести на примере класса Box (коробка), который может 
хранить в себе объекты разных типов:

```java
public class Box<T> {
   private T t;

   public Box(T t) {
      this.t = t;
   }

   public void doSomething() {
      // ... use t
   }
}
```

В данном случае класс Box может хранить любой тип данных, так как поле t имеет тип T. При использовании такого 
класса, нужно указать конкретный тип данных для T, например Box<Integer> box = new Box<>(5);

Также обобщенным может быть метод. Пример метода с двумя параметрами типа:

```
public static <T, U> void print(List<T> list, Function<T, U> function) {
    for (T t : list) {
        U u = function.apply(t);
        System.out.println(u);
    }
}
```


Здесь мы определили метод print с двумя параметрами типа T и U.
T используется для обозначения типа элементов в списке list, а U - для типа значения, которое возвращает функция function.
Этот метод можно вызвать следующим образом:


```
List<Integer> integerList = Arrays.asList(1, 2, 3, 4, 5);
Function<Integer, String> stringify = i -> Integer.toString(i);

print(integerList, stringify);

```

В этом примере мы используем метод для вывода на экран значений всех элементов списка integerList, после того как они 
были преобразованы функцией stringify.

### Наследование generic

Наследование Generic в Java работает обычным образом, за исключением того, что подклассы должны указывать тот же самый 
параметр типа.

Например, если у вас есть класс Box с одним параметром типа:

```java
class Box<T> {
  T value;

  public Box(T value) {
    this.value = value;
  }

  void print() {
    System.out.println(value);
  }
}
```
Вы можете создать подкласс Box, такой как BoxInt, который является Box с целым числом:

```java
class BoxInt extends Box<Integer> {
    BoxInt(Integer value) { super(value); }
}
```

### Про Generics после компиляции.

Компилятор не генерирует class-файл для каждого параметризованного типа.
Он создаёт один class-файл для дженерик-типа. В Java в скомпилированном байт-коде нет никакой информации о типе параметра.
Один байт-код для всех типов параметра.

Компилятор стирает информацию о типе, заменяя все параметры без ограничений (unbounded)
типом Object, а параметры с границами (bounded) — на эти границы.
Это называется type erasure


```java
class Box<T> {
    private T item;

    public void putItem(T item) {
        this.item = item;
    }

    public T getItem() {
        return item;
    }
    
    public T toArray(T[] arr) {
    }
}

public class Temp {
    public static void main(String[] args) {
        Box<String> box = new Box<>();
        box.putItem("");
    }
}
```

Такой наш класс после компиляции превратится в следующий:

```java
class Box {
    private Object item;

    public void putItem(Object item) {
        this.item = item;
    }

    public Object getItem() {
        return item;
    }
}

class Temp {
    public static void main(String[] args) {
        Box box = new Box();
        box.putItem((Object) "");
        String str = (String) box;
    }
}
```

Поэтому в домашке про generics в методе `toArray` не получится создать `new T[]()` -
потому что в runtime java просто не будет ничего знать о типе T

Подробнее можно прочитать в [этой статье](https://skillbox.ru/media/code/dzheneriki-v-java-dlya-tekh-kto-postarshe/#stk-1)

## Классы-обертки над примитивными типами <a name="primitives"></a> 
Классы-обёртки в Java используются для того, чтобы представлять примитивные типы данных (например, int, double, boolean) 
в виде объектов. Они нужны для того, чтобы использовать все преимущества объектно-ориентированного программирования.

Примеры классов-обёрток:

- Integer — обёртка для типа int
- Double — обёртка для типа double
- Boolean — обёртка для типа boolean
- Character — обёртка для тип char

Эти классы предоставляют дополнительные методы и возможности, которые недоступны для примитивных типов.

```java
class Example<T> {
    T value;

    Example(T value) {
        this.value = value;
    }

    void print() {
        System.out.println(value);
    }
}

class Main {
    public static void main(String[] args) {
        Example<Integer> intExample = new Example<>(new Integer(5));
        Example example = new Example(5L);
        example.print();
    }
}
```
В данном примере мы определяем класс Example, который принимает параметр типа T. Затем мы создаем два экземпляра этого 
класса, один с параметром типа Integer, а другой с параметром типа Long. Это возможно благодаря использованию 
классов-оберток для примитивов.

### Boxing и unboxing

Boxing и unboxing - это процессы в Java, которые конвертируют между примитивными типами данных и их соответствующими 
классами-оболочками. Например, int может быть конвертирован в Integer с помощью конструктора Integer, и наоборот.

Боксинг происходит, когда примитивное значение помещается в переменную-ссылку на объект. Например:

```java
int i = 42;
Integer i = i;
```

В этом случае примитивное значение 42 боксируется в объект класса Integer.
Unboxing происходит, когда вы извлекаете примитивное значение из переменной-ссылки на объект. Например:

```java
Integer i = new Integer(42);
int j = i; 
```

Здесь объект класса Integer i анбоксируется для получения примитивного значения, которое он содержит.
Boxing и unboxing могут быть полезны при работе с generic типами, так как они позволяют использовать как примитивные, 
так и ссылочные типы в одном контексте. Однако, они также имеют некоторые издержки по производительности, так как 
требуют выделения памяти для объектов и копирования данных.


## Optional <a name="optional"></a> 

Класс Optional в Java используется для работы с объектами, которые могут быть пустыми или не существующими. 
Он предоставляет набор методов для обработки таких значений, а также для проверки их наличия.

Optional используется в ситуациях, когда объект может не существовать, например, при работе с параметрами запроса или 
при получении данных из базы данных. Это позволяет избежать исключений NullPointerException и упрощает код.

Основные методы класса Optional:

- of() - создает Optional из существующего объекта;
- empty() - возвращает пустой Optional;
- ifPresent() - выполняет заданный блок кода, если Optional содержит значение;
- orElse() - возвращает результат выполнения блока кода или указанный объект, если Optional пуст;
- orElseGet() - возвращает значение из блока кода, если Optional пустой;
- isPresent() - проверяет, содержит ли Optional значение.

Пример использования Optional:

```java
public class Main {
    public static void main(String[] args) {
        // Создаем необязательный объект
        Optional<String> optional = Optional.ofNullable("Hello, World!");
        
        // Проверяем, имеет ли Optional значение
        if (optional.isPresent()) {
            System.out.println("The optional contains a value: " + optional.get());
        } else {
            System.out.println("The optional is empty.");
        }
    }
}
```

Метод ifPresent используется для выполнения блока кода если Optional содержит значение. Он принимает в качестве параметра функцию, которая принимает значение Optional и не возвращает значение. Вот пример использования ifPresent:

```java
import java.util.Optional;

public class Main {

    public static void main(String[] args) {

        String optionalValue = "Hello, World!";

        Optional.ofNullable(optionalValue)
                .ifPresent(value -> System.out.printf("The value is: %s%n", value));
    }

}
```

Этот код выводит значение optionalValue если оно не null.

Метод orElse используется для возвращения указанного объекта если Optional пустой:

```java
import java.util.*;
import java.util.function.*;

public class Example {
    
    public static void main(String args[]) {
        Optional<Integer> integerOptional = findRandomNumber();
        Integer result = integerOptional.orElse(new Integer(42));
        System.out.println(result);
    }
 
    private static Optional<Integer> findRandomNumber() {
        Random random = new Random();
        return Optional.ofNullable(random.nextInt(100));
    }
}
```

В этом примере мы используем метод _orElse_ для возвращения объекта _Integer_ с значением _42_ если _Optional_ пустой. 
Сначала мы вызываем метод _findRandomNumber_ который использует _Random_ для генерации случайного числа от 0 до 99. 
Затем мы создаем новый _Optional_ из этого случайного числа. Если число равно _null_, то создается пустой _Optional_.

Затем мы используем метод _orElse_, чтобы вернуть объект _Integer_ если _Optional_ содержит значение или вернуть новый 
объект Integer с значением 42 если Optional пуст. В конце мы выводим результат на консоль.

# Полезные ссылки

[Статья про дженерики](https://skillbox.ru/media/base/dzheneriki-v-java-dlya-samykh-malenkikh/)
