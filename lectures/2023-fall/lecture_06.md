# Технологии программирования

[Назад на главную](/)

## Лекция 6. Класс Object. Класс String. Регулярные выражения.
### Содержание
1. [Класс Object](#classObject)
2. [Действия со строками](#strings)
3. [Регулярные выражения](#regulars)

## Класс Object <a name="classObject"></a> 

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

## Класс String <a name="strings"></a>
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

## Регулярные выражения

Можно тренироваться в придумывании и использовании регулярных выражений на сайте regexr.com.

Регулярное выражение — это описание множества слов, где слова это последовательности символов.
Т.е. фактически регулярное выражение описывает подмножество значений типа String.

Примеры множеств слов:
1. Все строки длины 2
2. Все строки, начинаются и заканчиваются на букву a
3. Все строки, пример, похожи на email L = {"abc@yandex.ru", "ivanetsas@gmail.ru"}
4. Что-то похожее на даты
5. именя
6. числа


Зачем. Можно
1. Проверить, соответствует ли строка регулярному выражению. Например, вы можете проверить email, введенный пользователем,
   похож ли он вообще на email.
2. Искать вхождения внутри текста. Например, искать внутри длинного текста строки, похожие на email.
3. Искать и заменять. Например, находить имена внутри текста, заменять их на ***. Это может быть нужно для анонимизации.

Пример:
1. "ss" - одно слово ss
2. "ss|aa" - либо слово ss либо aa
3. "s(s|a)" - либо слово ss либо sa
4. "(s|a)(d|f)" - либо слово sd, sf, ad, af
5. 0 | 1 | 2 | ... | 9 - 10 вариантов любой цифры
6. \d - любая цифра
7. s* - звездочка означает что может 0 и более символов
8. s+ - плюсик что может быть 1 и более символов
9. [asdf] - только одна буква из набора
10. [asdf]* - только одна буква из набора
11. [a-zA-Z] - одна любая английская буква
12. [a-z]+@[a-z]+\.[a-z]{2,3} - такой пример для email

. - любой символ
+ - один и более
* - ноль и более
    {2,3} - повторение от 2 до 3 раз
    \s - пробельный символ

// прикреплю ссылку на доку


## Регулярки в Java <a name="regulars"></a>

Есть несколько методов в классе String, которые принимают регулярные выражения в качестве аргументов

```java
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Temp {
    public static void main(String[] args) {
        boolean isMatch = "abc".matches("[a-z]+"); // true
        String replacedString = "abc123df".replaceAll("\\d", "++"); // "\\d"
        String replaceFirstString = "abc123df".replaceFirst("\\d", "++");
        String[] array = "abc_sdf_dfg".split("_"); // ["abc", "sdf", "dfg"]

        Pattern p = Pattern.compile(
                "(\\d+) КОТ(|А|ОВ)",
                Pattern.MULTILINE + Pattern.UNICODE_CHARACTER_CLASS
        );
        
        /**
         * FLAGS:
         * CASE_INSENSITIVE - игнорировать регистр
         * UNICODE_CHARACTER_CLASS - поддержка юникода
         * DOTALL - точка будет обозначать любой символ включая перевод строки (без него - любой символ кроме перевода 
         * строки)
         * MULTILINE - ^ - начало строки, $ - дополнительно обозначает конец строки
         * */

        Matcher m1 = p.matcher("42 кота"); // связываем нашу регулярку с конкретной строкой
        if (m1.matches()) {
            System.out.println("Ура мы нашли котов!");
            System.out.println("Сопоставилось:" + m1.group());
            System.out.println("Количество найденных котов:" + m1.group(1));
        }
        
        Matcher m2 = p.matcher("1 кот, 2 кота, 3 кота");
        while (m2.find()) {
            System.out.println("Найдены коты");
            System.out.println("Сопоставилось:" + m1.group());
            System.out.println("Количество найденных котов:" + m1.group(1));
        }
        
        // appendReplacement
    }
}
```
