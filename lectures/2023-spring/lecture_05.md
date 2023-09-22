# Технологии программирования

[Назад к списку лекций](/lectures/2023-spring/)

## Архитектура приложения. Логгирование.

## Логирование

Самый простой пример логирования - System.err.println

Из известных решений по логированию в Java можно выделить:
- log4j
- JUL — java.util.logging
- JCL — jakarta commons logging
- Logback
- SLF4J — simple logging facade for java

Что нужно логировать?
- Начало/конец работы приложения. Нужно знать, что приложение действительно запустилось, как мы и ожидали, и 
завершилось так же ожидаемо.
- Вопросы безопасности. Здесь хорошо бы логировать попытки подбора пароля, логирование входа важных юзеров и т.д.
- Некоторые состояния приложения. Например, переход из одного состояния в другое в бизнес процессе.
- Некоторая информация для дебага, с соответственным уровнем логирования.
- Информацию для аналитики (при запуске фичи)

О чем стоит подумать?
- Избыток логгирования
- Хранение логов (kibana)
- Согласованность уровней логов
- Не писать в логи чувствительные данные!!

Уровни логов:
- OFF: никакие логи не записываются, все будут проигнорированы;

- FATAL: ошибка, после которой приложение уже не сможет работать и будет остановлено, например, JVM out of memory error;

- ERROR: уровень ошибок, когда есть проблемы, которые нужно решить. Ошибка не останавливает работу приложения в целом. 
Остальные запросы могут работать корректно;

- WARN: обозначаются логи, которые содержат предостережение. Произошло неожиданное действие, несмотря на это система 
устояла и выполнила запрос;

- INFO: лог, который записывает важные действия в приложении. Это не ошибки, это не предостережение, это ожидаемые 
действия системы;

- DEBUG: логи, необходимые для отладки приложения. Для уверенности в том, что система делает именно то, что от нее 
ожидают, или описания действия системы: “method1 начал работу”;

- TRACE: менее приоритетные логи для отладки, с наименьшим уровнем логирования;

- ALL: уровень, при котором будут записаны все логи из системы.

Log4j

Зависимость в gradle файле:
```groovy
    implementation 'org.apache.logging.log4j:log4j-api:2.20.0'
    implementation 'org.apache.logging.log4j:log4j-core:2.20.0'
```

В ресурсных файлах нам необходимо сконфигурировать работу логгера. Создадим файлик _log4j2.xml_
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="INFO">
    <Appenders>
        <File name="all_logs_file" fileName="logs/all.log">
            <PatternLayout>
                <pattern>%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1.} %L %m%n</pattern>
            </PatternLayout>
        </File>

        <File name="important_logs_file" fileName="logs/important.log">
            <Filters>
                <ThresholdFilter level="warn" onMatch="ACCEPT" onMismatch="DENY"/>
            </Filters>
            <PatternLayout>
                <pattern>%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1.} %L %m%n</pattern>
            </PatternLayout>
        </File>
    </Appenders>
    <Loggers>
        <Root level="debug">
            <AppenderRef ref="all_logs_file"/>
            <AppenderRef ref="important_logs_file"/>
        </Root>
    </Loggers>
</Configuration>
```



Давайте рассмотрим строку _ConversionPattern_:

- **%d{yyyy-MM-dd HH:mm:ss}** – выводит дату в формате 2014-01-14 23:55:57

- **%-5p** – выводит уровень лога (ERROR, DEBUG, INFO …), цифра 5 означает что всегда использовать 5 символов 
остальное дополнится пробелами, а минус (-), то что позиционирование по левой стороне.

- **%c{1}** – категория, в скобках указывается сколько уровней выдавать. Так как у нас 1 уровень то писаться будет 
только имя класса.

- **%L** – номер строки в которой произошёл вызов записи в лог.

- **%m** – сообщение, которое передали в лог.

- **%n** – переход на новую строку.


Использование:
```java
import java.util.random.RandomGenerator;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class LogExample {
    protected static final Logger logger = LogManager.getLogger(LogExample.class.getName());


    public static void main(String[] args) {
        makeOrder();
    }

    private static void makeOrder() {
        int orderId = RandomGenerator.getDefault().nextInt();
        if (orderId == 0) {
            logger.error("Cant create order");
            return;
        }
        logger.info("User made an order {}", orderId);
    }
}
```

## Архитектура приложения. Паттерны проектирования

Паттерны проектирования

- Порождающие

Эти паттерны решают проблемы обеспечения гибкости создания объектов

- Структурные

Эти паттерны решают проблемы эффективного построения связей между объектами

- Поведенческие

Эти паттерны решают проблемы эффективного взаимодействия между объектами

Книга «Design Patterns: Elements of Reusable Object-Oriented Software» Эрих Гамма, Ричард Хелм, Ральф Джонсон, 
Джон Влиссидес

### Порождающие паттерны
#### Builder
Данный паттерн позволяет создавать сложные объекты пошагово.
```java
class Temp {
    public static void main(String[] args) {
        StringBuilder stringBuilder = new StringBuilder();
        
        stringBuilder.append("1");
        stringBuilder.append("asdf");
        
        stringBuilder.toString();
    }
}
```


#### Factory Method
Создание объекта вынесено в отдельный статический метод.

```java
import java.util.Calendar;

class Temp {
    private static final Logger logger = LogManager.getLogger(LogExample.class);

    public static void main(String[] args) {
        var calendar = Calendar.getInstance();
    }
}
```

#### Singleton (*антипаттерн)
Цель — обеспечить единственный экземпляр объекта на всё приложение. Могут возникнуть проблемы с многопоточностью.
```java
class SingletonSchoolJournal {
    
    private static SingletonSchoolJournal instance = null;

    public static SingletonSchoolJournal getInstance() {
        if (instance == null) {
            instance = new SingletonSchoolJournal();
        }
        
        return instance;
    }
    
    private SingletonSchoolJournal() {
        
    }
    
    private String label;
}
```

### Структурные паттерны
Цель — построение удобных в поддержке иерархий классов и их взаимосвязей

#### Proxy (Заместитель)
Заместитель имеет тот же интерфейс, что и реальный объект, поэтому для клиента нет разницы — работать через заместителя 
или напрямую.

```java
interface NineHomeworkable{
    void suffer();
}

class HeavyObject implements NineHomeworkable {
    // очень долго создавать
    // например нам нужно подрубиться к базе данных
    
    @Override
    void suffer() {
        //
    }
}

class HeavyObjectProxy implements NineHomeworkable {
    private HeavyObject heavyObject;

    @Override
    void suffer() {
        if (heavyObject == null) {
            heavyObject = new HeavyObject();
        }
        heavyObject.suffer();
    }
}
```

Когда использовать:
- Когда нам нужна упрощенная версия сложного или тяжелого объекта.
- Когда исходный объект присутствует в другом адресном пространстве, и мы хотим представить его локально.

#### Decorator (Заместитель)
Шаблон декоратора можно использовать для придания дополнительных обязанностей объекту.
Декоратор предоставляет улучшенный интерфейс к исходному объекту.

```java
interface ITree {
    void add(String value);
}

class Tree implements ITree {
    class Node {
        Node next;
        Node prev;
        String value;
        public Node(String value) {
            this.value = value;
        }
    }

    Node first;

    void add(String newNode) {
        first = new Node(newNode);
    }
}

class ChristmasTree implements ITree {
    private Tree tree = new Tree();
    
    void add(String newNode) {
        // timer
        tree.add(newNode + " Marry Christmas");
        // sout results
    }
}
```

#### Adapter 
Шаблон адаптера используется для подключения двух несовместимых интерфейсов, 
которые в противном случае не могут быть подключены напрямую

Основные различия между шаблонами адаптера и прокси заключаются в следующем:
- Прокси предоставляет тот же интерфейс, адаптер предоставляет другой интерфейс, совместимый с его клиентом
- Используется для того, чтобы мы могли использовать имеющиеся классы без изменения исходного кода

#### Facade
Фасад скрывает сложную подсистему за простым интерфейсом. 
Он скрывает большую часть сложности и делает подсистему простой в использовании.

```java
class Engine {
    void warm() {}
    void pushKupplung() {}
    void startEngine() {}
}

class HandBremse {
    void turnOff() {}
}

class CarFacade {
    Engine engine = new Engine();
    HandBremse handBremse = new HandBremse();
    
    void start() {
        engine.warm();
        engine.startEngine();
        handBremse.turnOff();
        engine.pushKupplung();
    }
}
```

### Поведенческие шаблоны
Одна из целей - обеспечить гибкость в изменении поведения объектов

#### Strategy (Стратегия)
При помощи паттерна "Стратегия" мы можем внутри объекта хранить то, каким образом мы будем выполнять действие,
т.е. объект внутри хранит стратегию, которая может быть изменена, в том числе во время выполнения кода.

```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.stream.Collectors;

class Temp {
    public static void main(String[] args) {
        var a = new ArrayList<Integer>().stream()
                .map(i -> i++)
                .collect(Collectors.toList());

        var b = a.sort(Comparator.comparing(/*как сравнивать элементы*/));
    }
}

class Student {
    ExamPassStrategy strategy;
    
    void passExam(ExamPassStrategy strategy) {
        strategy.init();
    }
}
```

#### Command (Команда)
Различные команды можно представлять в виде разных классов. Очень похоже на паттерн "Стратегия". 
Но в "Стратегии" мы переопределяли то, как будет выполняться конкретное действие, а в "Команде" же мы переопределяем то,
какое вообще действие будет выполнено.

```java
import java.util.*;
class Main {
  public static void main(String[] args) {
    Runnable command = () -> {
      System.out.println("Command action");
    };
    Thread th = new Thread(command);
    th.start();
  }
}
```

#### Iterator (итератор)
```java
import java.util.*;
class Main {
  public static void main(String[] args) {
    List<String> data = Arrays.asList("Moscow", "Paris", "NYC");
    Iterator<String> iterator = data.iterator();
    while (iterator.hasNext()) {
      System.out.println(iterator.next());
    }
  }
}
```

## Полезные ссылки

[Логирование: что, как, где и чем?](https://javarush.com/groups/posts/2388-logirovanie-chto-kak-gde-i-chem)

[Учимся вести логирование с помощью Log4j](https://devcolibri.com/учимся-ввести-логирования-с-помощью-log4j/)

[Шаблоны проектирования "банды четырех"](https://bool.dev/blog/detail/gof-design-patterns)

[Паттерны проектирования в Java](https://javarush.com/groups/posts/2267-patternih-proektirovanija-v-java)

[Шаблоны прокси, декоратора, адаптера и моста](https://www.baeldung.com/java-structural-design-patterns)