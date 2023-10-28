# Технологии программирования

[Назад на главную](/)

## Лекция 8. Collections. Streams API. Lambda-выражения.

### Содержание
1. [Collections](#collections)
2. [Streams API](#streams)
3. [Lambda-выражения](#lambda)

## Collections <a name="collections"></a>

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

## Streams API <a name="streams"></a> 

// используем лямбды в сортировках

```java

public class Temp {
    public static void main(String[] args) {
        // Запись без Streams API
        List<Integer> list = new ArrayList<>();
        list.add(1);
        list.add(2);
        list.add(5);
        list.add(6);
        list.add(7);

        List<Integer> newList = new ArrayList<>();
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i) % 2 == 0 && newList.size() <= 3) {
                newList.add(list.get(i) + 1);
            }
        }

        // Тоже самое с Streams API
        int[] array = IntStream.of(1, 2, 5, 6, 7) // id пользователей
                .filter(id -> id % 2 == 0)
                .map(Math::abs)   // здесь по идее должны были написать .map(x -> Math.abs(x)), но когда
                                  // у функции один параметр - можем просто указать ссылку на метод
                .limit(3)
                .toArray();
        
        // Можем фильтровать содержимое списка и находить, например первый элемент
        Optional<Integer> opt = list.stream()
                .filter(i -> i < 0)
                .findFirst();

        // Удобно работать с коллекциями объектов
        List<Student> students = new ArrayList<>();
        students.add(new Student(5.0, "Ivanets AS"));
        students.add(new Student(4.5, "Dodonov NYou"));
        students.add(new Student(4.0, "Petrov AS"));
        students.add(new Student(3.8, "Ivanov AS"));

        Stream<Student> stream = students.stream();
        
        // Например, можем строить условия с полями объектов и преобразовывать поток объектов 
        // в поток строк и собирать их в список. Например, можем собрать ФИО студентов отличников для
        // формирования приказа на назначение стипендии:
        List<String> paymentFios = students.stream()
                .filter(student -> student.middleMark >= 4)
                .map(student -> student.fio)
                .collect(Collectors.toList()); // toList() - в современной джаве

        List<Student> actualStudents = new ArrayList<>();
        
        // Можем поделить студентов на две группы - отчисленных в результате сессии и нет
        Map<String, List<Student>> splitForExpulsionStudents = students.stream()
                .map(student -> new Pair<>(student.middleMark <= 2 ? "expel" : "not expel", student))
                .collect(Collectors.groupingBy(Pair::getValue0, Collectors.mapping(Pair::getValue1, Collectors.toList())));

        // Или сгруппировать студентов по средней оценке
        Map<Double, List<Student>> middleMark = students.stream()
                .collect(Collectors.groupingBy(student -> student.middleMark));
    }

    static class Student {
        int id;
        double middleMark;
        String fio;

        Student(double middleMark, String fio) {
            this.middleMark = middleMark;
            this.fio = fio;
        }
    }

}
```

## Lambda-выражения <a name="lambda"></a> 

Lambda-выражений в Java позволяют создавать анонимные функции, которые можно использовать для работы с коллекциями и 
для передачи поведения в качестве аргумента другим методам.

Лямбда-выражения - это короткие анонимные функции в Java, которые позволяют выполнять различные операции с данными.
Их можно использовать для работы с коллекциями и для передачи поведения в качестве аргумента другим методам.
Вот как это выглядит:

```java
(параметры) -> {
    операторы;
    return возвращаемое значение;
}
```
Параметры - это то, что мы передаем в нашу мини-программу, например числа или строки. Операторы - это то, что наша 
мини-программа делает с параметрами. Возвращаемое значение - это то, что возвращается после выполнения операторов.

Например, если мы хотим создать мини-программу для сложения двух чисел, мы можем написать:

```java
(число1, число2) -> число1 + число2
```

Это означает, что наша программа принимает два числа (число1 и число2) и возвращает их сумму. Мы можем использовать 
эту лямбда-функцию для сложения любых двух чисел.

В следующем выражении мы создаем функцию возведения в квадрат при помощи lambda. Функция принимает на вход число и
возвращает его квадрат.

```java
Function<Integer, Integer> pow = x -> x * x;
var result = pow.apply(5);
```

# Полезные ссылки
