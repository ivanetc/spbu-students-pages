# Технологии программирования

[Назад к списку лекций](/lectures/2022-fall/)

## Класс Object, класс String

## Класс Object
Этот класс — корень иерархии наследования. Любой класс, который вы заводите, 
либо наследуется от указанного вами класса: `class A extends B`, либо наследуется 
от `Object: class A` эквивалентна `class A extends Object`. Получается, что любой 
класс напрямую или косвенно наследует `Object`.

```java

class A  {
    
}

class B extends A {
    
}

class C extends B {
    
}

class Example {
    public static void main(String[] args) {
        Object a = new A();
        Object b = new B();
        Object c = new C();
        // todo Object <- A <- B <- C.
    }
}


```

Зачем? Во-первых, получается, что всё является объектом (кроме значений базовых 
типов (8 шт), например, int).

```java
// example
class Temp {
    public static void main(String[] args) {
        Object a = new int[5];
        Object s = "";
        Object sb = new StringBuilder();
    }
}
```

Второе, зачем нужен Object. В этом классе определён ряд методов, получается, 
что эти методы есть у абсолютно всех объектов. 
- equals()
- toString()
- hashCode()

### toString

можно переопределить, чтобы приводить наш объект к строке для наших нужд

```java
class Student {
    String name;
    String surname;
    int id;
    double middleMark;
    
    @Override
    public String toString() {
        return name + " " + surname;
    }
}

class Temp {
    public static void main(String[] args) {
        // todo print all students list
        Student st = new Student();
        st.name = "Alexander";
        st.surname = "Ivanets";
        System.out.println(st);
        // Alexander Ivanets
    }
}
```

### equals

```java
import java.rmi.StubNotFoundException;

class Test {
    public static void main(String[] args) {
        // Поговорим про ==
        // == проверяет ссылки на объекты
        Student st = new Student("Ivanets", "Alexander", 1);
        Student st1 = new Student("Ivanets", "Alexander", 1);

        // если мы попытаемся сравнить 2 таких объекта через ==
        var a = st == st1; // false

        st.equals(s1); // ? мы не знаем как java по-дефолту их сравнивает
    }


}

class Student {
    String name;
    String surname;
    int id;
    double middleMark;

    @Override
    public String toString() {
        return name + " " + surname;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        
        if (obj == null) {
            return false;
        }
        
        if (!(obj instanceof Student)) {
            return false;
        }
        
        Student other = (Student) obj;
        return this.id == other.id;
    }
}
```

Требования к функции:
- Рефлексивность (если на вход в equals мы получаем тот же самый объект -> true)
- Симметричность (a.equals(b) == b.equals(a))
- Транзитивность (a.equals(b) and b.equals(c) --> a.equals(c))
- Постоянность // что если мы n раз вызовем equals она даст одинаковый результат (многопоточность. отсутствие
завязок на время, состояния системы)
- Неравенство с null // b = null -> a.equals(b) == false

### hashCode
У каждого объекта есть функция hashCode которая возвращает некий int которое мы генерируем по данным объекта
```java
class Point {
    public int x;
    public int y;
    public String description;
    
    @Override
    public int hashCode() {
        return 29 * x + 31 * y + description.hashCode(); // new Point(1,2) , new Point(2,1)
    }
}
```

Требования к функции:
- Если два объекта равны (т.е. метод equals() возвращает true), у них должен 
быть одинаковый хэш-код.
- Если метод hashCode() вызывается несколько раз на одном и том же объекте, 
каждый раз он должен возвращать одно и то же число.
- Правило 1 не работает в обратную сторону. Одинаковый хэш-код может быть у 
двух разных объектов.

// hashCode следует генерить из тех же полей, которые мы используем в equals

### Полезные ссылки
[Статья про object на javarush](https://javarush.ru/groups/posts/2179-metodih-equals--hashcode-praktika-ispoljhzovanija)

## Класс String
Строки в java иммутабельны (нельзя изменить).

Для строк можно использовать специальную область памяти, называемую "пул строк". 
Благодаря которой две разные переменные типа String с одинаковым значением будут 
указывать на одну и ту же область памяти. 

Java String Pool - это специальная область памяти, в которой JVM хранит строки. 
Поскольку строки неизменяемы в Java, JVM оптимизирует объем памяти, выделенный 
для них, сохраняя только одну копию каждой строки в пуле. 

Пример:

```java
class Test {
    public static void main(String[] args) {
        String a = "abc";
        String b = "abc";

        a == b // так лучше не делать никогда -> equals
        String a = "array: ";

        for (int i = 0; i < 10_000_000; i++) {
            a += i + ", ";
        }

        // В таких моментах мы очень не аккуратно используем память
        // Для того, чтобы "менять" строку, но не расходовать память таким образом
        // существует StringBuilder

        StringBuilder sb = new StringBuilder();
        sb.append("array: ");

        for (int i = 0; i < 10_000_000; i++) {
            sb.append(i).append(", ");
        }
        String result = sb.toString();
        System.out.println(result);
        
        // Если вы конкатенируете строки один - два раза - то это может быть
        // дешевле чем создать StringBuilder
        "Solution x = " + x;
    }
}

```

### Действия со строками
```java
class Test {
    public static void main(String[] args) {
        String a = "asdf";
        int aLength = a.length(); // длинна строки
        
        String url = "https://yandex.ru/mail";
        if (url.startsWith("https://yandex.ru")) {
            // todo smth
            System.out.println("its yandex");
        }
        // url.endsWith() - аналогично с окончанием строки
        
        String domain = url.substring(8); // как слайсы в питоне
        char firstChar = domain.charAt(0);
        char[] array = domain.toCharArray();
        
        x = 1;
        x2 = 3;
        String solutionString = String.format("Solution x=%d and x2=%d", x, x2);
        solutionString = "Solution x=%d and x2=%d".formatted(x, x2);
    }
}
```
- length()
- startsWith()
- substring
- charAt
- String.format() and .formatted()

String format - обозначения:
| Обозначение   | Тип данных                         |
| ------------- | -------------                      |
| %s            | String                             |
| %d            | целое число: int, long, …          |
| %f            | вещественное число: float, double  |
| %b            | boolean                            |
| %c            | char                               |
| %t            | Date                               |
| %%            | Символ %                           |


### Сравнение строк, метод equals

Сравнивать строки нужно через equals
```java
class Test {
    public static void main(String[] args) {
        String a = "abc";
        String b = "aabc".substring(1);
        
        a == b // false
        a.equals(b); // true
        
    }
}
```
