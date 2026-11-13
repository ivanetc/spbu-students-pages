## Часть I. Как выбрать коллекцию и работать с ней

### 1. Четыре вопроса к одним объектам

В [прошлой лекции](../../lectures/autumn/lecture_06.md) появились `Student` и `record UniversityGroup`. Теперь данные одни и те же, а задачи различаются:

- Иван записался на занятие дважды. Как сохранить **обе записи и их порядок**?
- Иван и Анна учатся в одной группе. Как показать **каждую группу один раз**?
- Известен ID студента. Как найти его карточку **без полного перебора**?
- Заявки приходят одна за другой. **Какую обработать следующей**?

Массив хранит элементы, но его длина фиксирована, а правила повторов и поиска придётся реализовать самим. [Java Collections Framework](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/doc-files/coll-overview.html) даёт интерфейсы (что обещано клиенту), реализации (как данные хранятся) и общие операции. Выбор начинаем с требования задачи, а не с имени класса.

<!-- DIAGRAM: четыре вопроса к университетским данным; один Student/UniversityGroup, четыре стрелки к List, Set, Map, Deque; подписи «позиция и повторы», «уникальность», «ключ → значение», «следующая заявка». Логическая схема, не устройство в памяти. -->

### 2. Почему Framework устроен как иерархия

Общие операции не нужно придумывать заново для каждого контейнера. Интерфейс **`Iterable`** задаёт обход, **`Collection`** добавляет работу с набором элементов (`size`, `contains`, `add`, `remove`). Дальше контракт уточняется под задачу:

- **`List`** добавляет позиции и операции по индексу;
- **`Set`** усиливает правило уникальности, не вводя индексов;
- **`Queue`** задаёт получение следующего элемента, **`Deque`** — операции с обоими концами;
- **`Map`** стоит отдельно: клиент ищет значение *по ключу*, а не элемент набора.

В Java 21 между некоторыми уровнями находятся `SequencedCollection`, `SequencedSet` и `SequencedMap`: они выражают определённый порядок обхода и операции с его концами. Схема показывает нужные нам связи и основные операции, но не все типы библиотеки. **Абстрактные классы** вроде `AbstractList` дают разработчику часть реализации; **конкретные классы** вроде `ArrayList` уже хранят данные. [Иерархия Java 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/doc-files/coll-reference.html), [SequencedCollection](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/SequencedCollection.html).

<!-- DIAGRAM: точная сокращённая сеть интерфейсов Java 21 и связанных с ними абстрактных и конкретных классов; Vector, Stack, Hashtable помечены legacy. Стрелки показывают выбранные связи extends и implements. -->

*Нажмите на схему, чтобы открыть её в полном размере.*

Три похожих названия:

| Имя | Что это |
| --- | --- |
| **Collections Framework** | Система контрактов, классов и алгоритмов |
| **`Collection<E>`** | Интерфейс для набора элементов; общие `size()`, `isEmpty()`, `contains(...)` |
| **`Collections`** | Служебный класс со статическими методами, например `sort(...)` |

Запись `List<Student> registrations = new ArrayList<>();` использует знакомый полиморфизм: переменная обещает операции `List`, объект реализует их через `ArrayList`. `Student` — тип элемента; примитивы в generic-аргументах заменяются обёртками, поэтому ID в `Map` имеет тип `Integer`.

**Старые классы, которые можно встретить в чужом коде:**

| Старый класс | Для обычного нового кода | Почему |
| --- | --- | --- |
| `Vector` | `ArrayList` | Старый синхронизированный список; без требования потокобезопасности Oracle рекомендует `ArrayList`. |
| `Hashtable` | `HashMap` | Старая синхронизированная таблица; без требования потокобезопасности Oracle рекомендует `HashMap`. |
| `Stack` | `Deque` с `ArrayDeque` | `Deque` даёт более полный и согласованный набор операций стека. |

Если понадобится совместное изменение коллекции из нескольких потоков, выбор будет отдельной темой; синхронизация отдельного метода старого класса сама по себе не решает все задачи конкурентного доступа. [Vector](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Vector.html), [Hashtable](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Hashtable.html), [Stack](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Stack.html).

### 3. `List`: позиция, порядок, повторы

`List` — **интерфейс для списков**: он описывает последовательность элементов и обращение по индексу. Контракт не требует уникальности: обычный `ArrayList` допускает повторы. Для изменяемого списка начните с `ArrayList`; `LinkedList` исполняет тот же контракт, но иначе платит за операции. Стоимость разберём во второй части.

| Метод | Результат |
| --- | --- |
| `add(e)` / `add(i, e)` | Добавить в конец / перед позицией `i` |
| `get(i)` / `set(i, e)` | Прочитать / заменить элемент; `set` возвращает прежний |
| `remove(i)` / `remove(e)` | Удалить позицию / первый равный элемент; возвращают элемент / `boolean` |
| `indexOf(e)` / `contains(e)` | Найти первую позицию / проверить наличие |
| `size()` / `isEmpty()` | Число элементов / пуст ли список |

Ниже и далее — **короткие фрагменты внутри `main`**. Импорты `java.util.*` и типов `university.model.*` опущены. Мы продолжаем модель прошлой лекции: `UniversityGroup` — уже знакомый `record`; для примеров считаем, что `Student` имеет конструктор `(int id, String name, UniversityGroup group)` и методы `getId()`, `getName()`, `getGroup()`. Полное объявление студента здесь не требуется. Общие исходные объекты:

```java
Student ivan = new Student(1, "Иван", new UniversityGroup("24.Б11-мм"));
Student anna = new Student(2, "Анна", new UniversityGroup("24.Б11-мм"));
```

```java
List<Student> registrations = new ArrayList<>();
registrations.add(ivan);
registrations.add(anna);
registrations.add(ivan);
System.out.println(registrations.size());       // 3
System.out.println(registrations.get(2) == ivan); // true
```

Две позиции хранят ссылки на одного Ивана; `add` не копирует объект. После `remove(0)` прежние позиции 1 и 2 получат индексы 0 и 1. В `List<Integer>` вызов `remove(1)` выбирает **индекс**, а `remove(Integer.valueOf(1))` — **значение**; это две перегрузки, а не одна операция. Контракт методов — [List API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html).

<!-- DIAGRAM: список из трёх ячеек [0 Ivan][1 Anna][2 Ivan], обе ячейки Ivan указывают на один Student; после remove(0) две ячейки [0 Anna][1 Ivan]. Подпись: «индекс — позиция, объект не копируется». -->

### 4. `Set`: логическая уникальность

`Set` — **интерфейс для множеств**: он описывает набор без равных элементов и отвечает на вопрос «есть ли уже такой элемент?». Индексов в нём нет. Равенство задаёт тип элемента. Два `UniversityGroup` с одним именем — разные объекты, но равные значения record. Для `HashSet` согласованность `equals` и `hashCode` обязательна; её смысл знаком по [лекции 4](../../lectures/autumn/lecture_04.md).

| Метод | Результат |
| --- | --- |
| `add(e)` | `true`, если множество изменилось; равный элемент повторно не добавится |
| `contains(e)` | Есть ли равный элемент |
| `remove(e)` | `true`, если равный элемент удалён |
| `size()` / `isEmpty()` | Число разных элементов / пусто ли множество |

```java
Set<UniversityGroup> groups = new HashSet<>();
System.out.println(groups.add(ivan.getGroup())); // true
System.out.println(groups.add(anna.getGroup())); // false
System.out.println(groups.size());                // 1
```

Не выводите порядок из того, как `HashSet` однажды напечатался: [он не обещает порядок обхода](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashSet.html). `LinkedHashSet` в обычном режиме поддерживает порядок добавления, `TreeSet` — порядок сравнения. У `TreeSet` сравнение определяет также, считаются ли элементы дубликатами: оно должно быть согласовано с желаемым смыслом уникальности. `UniversityGroup` как record сам по себе не имеет естественного порядка.

### 5. `Map`: поиск по ключу

`Map<K,V>` — **интерфейс для отображений**: он описывает связи **ключ → значение** и поиск значения по ключу. Ключи уникальны, значения могут повторяться. `put` с уже имеющимся ключом заменяет значение. Здесь ключ — неизменяемый `Integer` ID, значение — студент.

<!-- DIAGRAM: два ключа ID 1 и ID 2 указывают на карточки Ивана и Анны. Это логическое отображение, не схема корзин или памяти. -->

| Метод | Результат |
| --- | --- |
| `put(k, v)` | Создать или заменить связь; вернуть прежнее значение либо `null` |
| `get(k)` / `getOrDefault(k, d)` | Значение по ключу / запасное значение при отсутствии связи |
| `containsKey(k)` / `containsValue(v)` | Проверить ключ / значение; назначение и цена различаются |
| `remove(k)` | Удалить связь, вернуть прежнее значение либо `null` |
| `keySet()` / `values()` / `entrySet()` | Представления ключей / значений / пар |

```java
Map<Integer, Student> studentsById = new HashMap<>();
studentsById.put(ivan.getId(), ivan);
studentsById.put(anna.getId(), anna);
System.out.println(studentsById.get(2).getName()); // Анна
System.out.println(studentsById.put(2, ivan) == anna); // true
System.out.println(studentsById.size()); // 2: значение заменено
```

`HashMap` допускает `null` значения: поэтому `get(k) == null` **не доказывает**, что ключа нет; проверьте `containsKey(k)`. Ключу, помещённому в хеш-таблицу, нельзя менять поля, от которых зависят `equals`/`hashCode`: последующий поиск может потерять его. Для ID здесь выбран `Integer`, а не изменяемый `Student`. У `HashMap` также [нет гарантии порядка](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html). С контрактом методов можно свериться в [Map API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Map.html).

`containsKey` ищет через хеш ключа; `containsValue` проверяет значения перебором записей. Поэтому быстрый поиск по ключу не делает столь же быстрым поиск по значению.

<!-- DIAGRAM: логическая карта «1→Ivan, 2→Anna», затем put(2,Ivan) и «1→Ivan, 2→Ivan»: ключей по-прежнему два; подчеркнуть, что это НЕ схема корзин. -->

### 6. Очередь и стек: FIFO, LIFO, `Deque`

**FIFO** (*first in, first out*) — первым пришёл, первым вышел; так обрабатываем заявки. **LIFO** (*last in, first out*) — последним положили, первым взяли; так работает стек действий. `Queue` — **интерфейс для очередей**: он описывает добавление, просмотр и извлечение следующего элемента. `Deque` — интерфейс двусторонней очереди: операции на разных концах дают FIFO, на одном конце — LIFO. Для обоих сценариев подходит `ArrayDeque`.

<!-- DIAGRAM: понятная схема FIFO очереди заявок с входом справа и выходом слева, и LIFO стека действий с push/pop на одном конце. Не утверждать, что всякий Queue — FIFO. -->

Не каждая реализация `Queue` следует времени поступления: `PriorityQueue` выдаёт элемент по приоритету. Здесь нам нужна именно очередь заявок по времени.

| Задача | Методы с особым значением при неуспехе | Методы с исключением при неуспехе |
| --- | --- | --- |
| Добавить в очередь | `offer(e)` | `add(e)` |
| Взять голову | `poll()` → `null`, если пусто | `remove()` |
| Посмотреть голову | `peek()` → `null`, если пусто | `element()` |

Для `Deque` стороны называются `First` и `Last`: `offerLast(e)` добавляет в конец, `pollFirst()` берёт с начала; симметричные `offerFirst`, `pollLast`, `peekFirst`, `peekLast` работают с другим концом. `push(e)`/`pop()` делают стек на **первом** конце. В `ArrayDeque` нельзя положить `null`, потому что `poll` и `peek` используют его как признак пустоты. [Deque API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Deque.html), [ArrayDeque API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html).

```java
Deque<String> applications = new ArrayDeque<>();
applications.offerLast("Иван");
applications.offerLast("Анна");
System.out.println(applications.pollFirst()); // Иван: FIFO

Deque<String> history = new ArrayDeque<>();
history.push("Иван");
history.push("Анна");
System.out.println(history.pop()); // Анна: LIFO
```

### 7. Обход: `Iterable`, `Iterator`, представления `Map`

`Iterable<E>` — интерфейс для того, по чему можно пройти: его `iterator()` возвращает **объект обхода** `Iterator<E>`. `Collection` наследует `Iterable`, а `Iterator` помнит текущую позицию. `for-each` вызывает эти операции за нас. Сам `Map` не является `Iterable`: для пар нужен `entrySet()`.

| Интерфейс и метод | Что делает |
| --- | --- |
| `Iterable.iterator()` | Возвращает итератор для обхода элементов |
| `Iterator.hasNext()` | Проверяет, есть ли следующий элемент |
| `Iterator.next()` | Возвращает следующий элемент и продвигает курсор; при завершённом обходе выбрасывает исключение |
| `Iterator.remove()` | Удаляет последний выданный `next()` элемент, если реализация поддерживает удаление |

<!-- DIAGRAM: Iterable-коллекция создаёт Iterator через iterator(); отдельный курсор между Иваном и Анной показывает следующий элемент. Не изображать итератор как копию коллекции. -->

```java
for (Student student : registrations) {
  System.out.println(student.getName());
}

for (Map.Entry<Integer, Student> entry : studentsById.entrySet()) {
  System.out.println(entry.getKey() + ": " + entry.getValue().getName());
}
```

Второй цикл **не обещает порядка строк**, потому что `studentsById` — `HashMap`. `keySet()`, `values()` и `entrySet()` возвращают **представления**, связанные с исходной картой, а не снимки. Например, после `studentsById.remove(1)` ключ `1` исчезнет и из ранее полученного `keySet`. [Map API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Map.html).

Когда нужно удалять во время обхода, используйте поддерживаемый `Iterator.remove()` после `next()`:

```java
Iterator<Student> it = registrations.iterator();
while (it.hasNext()) {
  if (it.next().getId() == 1) it.remove();
}
```

Не изменяйте тот же список напрямую внутри `for-each`. У распространённых реализаций это может обнаружиться как `ConcurrentModificationException`, но [fail-fast — диагностика best effort](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ConcurrentModificationException.html), не способ управлять программой. Во второй части увидим, почему для `LinkedList` последовательный обход итератором существенно дешевле повторного `get(i)`.

<!-- DIAGRAM: Iterator: курсор между элементами, hasNext→next→remove последнего выданного; рядом Map→entrySet как live view. Не рисовать Iterator как копию коллекции. -->

### 8. Порядок, сортировка и изменяемость

Один интерфейс могут реализовать разные классы. Они дают похожие операции, но отличаются хранением, порядком обхода и стоимостью. Ниже — **основные доступные контракты**, а не полный список прямых `implements` каждого класса:

| Класс | Основные интерфейсы | Что это за реализация |
| --- | --- | --- |
| `ArrayList` | `List` | расширяемый массив |
| `LinkedList` | `List`, `Deque` | двусвязный список |
| `HashSet` | `Set` | хеш-множество |
| `LinkedHashSet` | `SequencedSet`, `Set` | хеш-множество; по умолчанию порядок добавления |
| `TreeSet` | `SequencedSet`, `Set` | множество в порядке сравнения |
| `HashMap` | `Map` | хеш-таблица |
| `LinkedHashMap` | `SequencedMap`, `Map` | хеш-таблица; по умолчанию порядок добавления |
| `TreeMap` | `SequencedMap`, `Map` | отображение с ключами в порядке сравнения |
| `ArrayDeque` | `Deque`, `Queue` | двусторонняя очередь на растущем кольцевом массиве |
| `PriorityQueue` | `Queue` | очередь с выбором головы по приоритету |

Старые `Vector`, `Stack` и `Hashtable` отмечены на схеме выше: `Stack` наследует `Vector` и тем самым относится к `List`, **а не к `Deque`**. Эти классы существуют в Java 21; *legacy* не означает аннотацию `@Deprecated`.

Сначала решите, какой именно порядок требуется:

| Требование | Пример выбора |
| --- | --- |
| Сохранить позиции и повторы | `ArrayList` |
| Уникальность без обещания порядка | `HashSet` |
| Уникальность с порядком добавления | `LinkedHashSet` |
| Поиск по ключу без обещания порядка | `HashMap` |
| Ключи в порядке добавления | `LinkedHashMap` |
| Элементы или ключи в порядке сравнения | `TreeSet` / `TreeMap` |

Для списка сортировка **меняет порядок того же списка**. Строки уже имеют естественный порядок (`Comparable`):

```java
List<String> names = new ArrayList<>(List.of("Иван", "Анна"));
names.sort(null);                 // естественный порядок String
System.out.println(names);       // [Анна, Иван]
```

`Comparator` задаёт другой порядок сравнения; способ записать его через лямбду обсудим на следующей лекции. У `TreeSet`/`TreeMap` порядок поддерживается при изменениях, в отличие от разовой сортировки списка. [List.sort](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html#sort(java.util.Comparator)), [Comparator API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Comparator.html).

Создание `new ArrayList<>()` даёт изменяемый список, а `List.of(...)` — список, состав которого нельзя изменить. `List.copyOf(registrations)` фиксирует **состав на момент вызова**, но не копирует самих изменяемых студентов: если у `ivan` поменяется статус, тот же объект виден в снимке. `Set.of` отклоняет равные повторные элементы, `Set.copyOf` оставляет одного из них; фабрики `of`/`copyOf` не принимают `null`. [List API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html), [Set API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Set.html).

### 9. Выбор перед разбором внутренностей

| Вопрос программы | Контракт | Реализация для примера |
| --- | --- | --- |
| Кто записан и на какой позиции? | `List<Student>` | `ArrayList` |
| Какие группы представлены? | `Set<UniversityGroup>` | `HashSet` |
| Кто соответствует ID 2? | `Map<Integer, Student>` | `HashMap` |
| Чья заявка следующая? | `Deque<String>` | `ArrayDeque` |

Все четыре решения выражают нужный **контракт**. Но почему `get(2)` у `ArrayList` и `LinkedList` стоит по-разному? И на каком условии основан быстрый поиск `HashMap`? Чтобы ответить, заглянем в представление данных и посчитаем действия каждого метода.
