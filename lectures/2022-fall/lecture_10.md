# Технологии программирования

[Назад к списку лекций](/lectures/2022-fall/)

## Generics. Optional. Collections
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

#### Важный вывод который нужно запомнить:
По своей сути generic-класс – это обертка над классом с Object, которая
проверяет (приводит) тип во всех точках входа и выхода из generic-кода.
Тем самым проверяется корректность присваиваний и операций на
этапе компиляции

### Optional

Один из важных дженерик-классов, который мы используем - это Optional.

Цель класса - предоставить решение на уровне типа для представления необязательных значений вместо нулевых ссылок
Иными словами - это некоторая обертка над любым типом T, которая позволяет нам представить отсутствие значение
не с помощью null (нулевой ссылки), а с помощью объектов данного класса и методов данных объектов. Это позволяет
явным образом в коде отметить, что в какой-то переменной может отсутствовать значения и нужно явно учесть случай
отсутствия значения.

```java
import java.util.Optional;

class Temp {
    public static void main(String[] args) {
        Integer tempInt = null;
        Optional<Integer> a = Optional.of(tempInt); // Рассчитывает, что не передаем в него null. 
                                                    // Если передать null, то будет exception
     
        Optional<Integer> optionalInt = Optional.ofNullable(tempInt); // Можно передать null
        Optional<Integer> emptyOptional = Optional.empty(); // Сразу пустой Optional
     
        optionalInt.isEmpty(); // если null, или если мы создали пустой optional -> true
        optionalInt.isPresent();
        
        Integer value = optionalInt.get(); // если значения нет - то будет exception
                                           // поэтому мы хотим проверить, есть ли в Optional значение:
        if (optionalInt.isPresent()) {
            value = optionalInt.get();
        } else {
            value = 0;
        }
        Integer value = optionalInt.orElse(0);

        // Пример, где нам это может потребоваться. Например, при работе с базой данных.
        // Если мы пишем библиотеку, которую потом будут использовать другие разработчики (коллеги, например),
        // и какой-то метод в нашей библиотеки пытается что-нибудь достать из базы данных, то мы должны предусмотреть 
        // ситуацию, когда искомый объект отсутствует в базе. Конечно в такой ситуации мы можем просто вернуть null, 
        // но было хорошим тоном явно указать в сигнатуре метода, что мы можем ожидать в ответе отсутствие объекта:
        
        Optional<Student> optionalSt = getFromDb(1);
        
        // Для любителей c# - Optional в каком-то смысле аналог 'int?'
    }
    
    public static Optional<Student> getFromDb(int id) {
        // какой-то код который вытаскивает из бд пользователя
        // student - либо null, или Student
        return Optional.ofNullable(student);
    }
    
    
    public class Student {
        // код студента
    }
}
```



## Java Collection Framework

![alt text](https://habrastorage.org/r/w1560/files/65c/d6d/ce5/65cd6dce50e84d659152c482e5565f3c.png "Collections")

[Collection](https://docs.oracle.com/javase/8/docs/api/java/util/Collection.html)
Простые наборы элементов.

Базовый набор методов (size(), isEmpty(), add(E e) и др - см доку)

В интерфейсе уже есть дефолтные реализации.


[Map](https://docs.oracle.com/javase/8/docs/api/java/util/Map.html)

Работа с типами данных ключ - значение. В c# - аналог Dictionary, в питоне - словари.

Базовый набор методов (containsKey(Object key), get(Object key), isEmpty(), size())

### Map
![alt text](https://habrastorage.org/r/w1560/files/40a/eca/09a/40aeca09ac1c4cc7bdbd475a3c12fd95.png)

```java
import java.util.HashMap;
import java.util.Hashtable;

class Temp {
    public static void main(String[] args) {
        // Hashtable - хэш-таблица. Нельзя использовать null как value или key. 
        // Все методы помечены synchronized - поэтому есть проблемы с производительностью
        Hashtable<Integer, String> table = new Hashtable<>();
        table.put(1, "hello");
        String value = table.get(1); // hello

        // HashMap - альтернатива. Не синхронизирована. И можно использовать null
        HashMap<Integer, String> map = new HashMap<>();
        map.put(1, "good evening");
        String str = map.get(1); // good evening

        // LinkedHashMap - упорядоченная в порядке добавления элементов.

        // TreeMap - основана на красно-черных деревьях, тоже является упорядоченной. 
        // Порядок можно задавать через Comparator

        // WeakHashMap. Garbage Collector автоматически удалит элемент из коллекции 
        // при следующей сборке мусора, если на ключ этого элемента нет жёстких ссылок.


    }
}
```

### List
![alt text](https://habrastorage.org/r/w1560/files/187/da1/649/187da164972c4519b6affbc4a2c6fda1.png)

```java
import java.util.ArrayList;
import java.util.LinkedList;

class Temp {
    public static void main(String[] args) {
        // Vector - синхронизирован. Будем использовать ArrayList
        // Stack - LIFO, но лучше использовать ArrayDeque

        // ArrayList - список основан на массиве
        ArrayList<String> ourList = new ArrayList<String>();
        ourList.size();
        ourList.add("");
        ourList.remove(0);
        ourList.toArray(new String[]{});
        ourList.addAll(new ArrayList<>());

        // LinkedList - связный
    }
}
```


![alt text](https://habrastorage.org/r/w1560/files/aca/208/428/aca20842816a48628772bd23d2bb0f24.png)

```java
import java.util.HashSet;

class Temp {
    public static void main(String[] args) {
        // HashSet - Set, базирующийся на HashMap. Порядок не гарантируется. 
        HashSet<String> set = new HashSet<>();
        set.add("123");
        set.add("123");
        set.add("123");
        set.size();
        set.remove("123");

        // LinkedHashSet - базируется на LinkedHashMap

        // TreeSet - специфичный сет, можно управлять порядком элементов и использовать Comparator
    }
}
```

### Queue 
![alt text](https://habrastorage.org/r/w1560/webt/ju/m6/3h/jum63htuhoc4v-xnumg0zslptsy.png)

```java
import java.util.ArrayDeque;

class Temp {
    public static void main(String[] args) {
        // PriorityQueue - очередь FIFO, не поддерживает null, можно управлять порядком 
        // через Comparator

        // ArrayDeque - LIFO (stack), быстрее чем Stack и LinkedList
        ArrayDeque<String> stack = new ArrayDeque<>();
        stack.addFirst("123");
        stack.pollFirst(); // возвращает первый элемент и удаляет из коллекции 
    }
}
```


Более распространенные коллекции: HashMap, HashSet, ArrayList, LinkedList, ArrayDeque