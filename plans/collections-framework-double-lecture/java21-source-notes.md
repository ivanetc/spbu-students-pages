# Java 21: нормативный API и детали реализации для плана

Дата доступа: 13 ноября 2026. Эти заметки фиксируют опоры для будущего конспекта; заявления о внутреннем устройстве нужно сверять с исходниками именно JDK 21 при написании.

## Карта и контракты

- [Collections Framework Overview](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/doc-files/coll-overview.html) и [Outline](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/doc-files/coll-reference.html): семейства интерфейсов и типичные реализации. `Map` входит во framework, но отделён от `Collection`.
- [SequencedCollection](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/SequencedCollection.html) и [руководство Oracle](https://docs.oracle.com/en/java/javase/21/core/creating-sequenced-collections-sets-and-maps.html): новые интерфейсы присутствуют уже в Java 21; карта лекции 6 их упрощённо опускает. Не следует представлять `List extends Collection` как непосредственное наследование в Java 21: между ними `SequencedCollection`.

## Реализации и границы асимптотики

- [ArrayList API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayList.html): `get`, `set`, `size`, получение итератора — O(1); `add(E)` амортизированно O(1); вставка/удаление по индексу и линейный поиск — O(n). Политика роста capacity не специфицирована, хотя исходники OpenJDK имеют конкретную формулу. При объяснении амортизации использовать геометрический рост как модель, отделяя его от API-обещания.
- [LinkedList API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedList.html): двусвязный список; индексная операция проходит от ближнего конца. Из этого следует O(min(i, n-i)) для достижения позиции; добавление/удаление на концах O(1), работа через уже имеющийся узел или позицию итератора O(1) после достижения. Сравнивать полную стоимость операции, а не только перестановку ссылок.
- [HashMap API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html): `get`/`put` в ожидаемом O(1) при хорошей дисперсии хешей; rehash при пороге capacity × load factor; итерация по представлениям O(capacity + size); плохие хеши портят оценку. Не обещать worst-case O(1). `get(k) == null` неоднозначен при разрешённых null values; нужен `containsKey`.
- [HashSet API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashSet.html): реализован поверх `HashMap`; те же условия O(1) для `add`/`remove`/`contains`; обход O(capacity + size). Никакого гарантированного порядка обхода.
- [ArrayDeque API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html): динамический массив для `Deque`; большинство операций амортизированно O(1), поиск/удаление по значению/`iterator.remove()` O(n). Это важная пятая реализация для практического выбора очереди и стека, но её внутренности можно дать кратко после четырёх запрошенных классов.
- [OpenJDK 21 ArrayDeque source](https://github.com/openjdk/jdk21u/blob/master/src/java.base/share/classes/java/util/ArrayDeque.java): `head` — индекс первого элемента, `tail` — индекс следующего добавления в конец; индексы переходят с конца массива на `0`. В трассировке `[B,C,пусто,A]`, `head=3`, `tail=2` вызов `offerLast(D)` временно заполняет индекс `2` и делает `tail=head=3`; `grow(1)` при длине `4` создаёт массив длины `10`, переносит `A` с `3` на `9`, оставляет `B,C,D` на местах и устанавливает `head=9`, `tail=3`. Это точная деталь OpenJDK 21 для данного примера, не обещание API и не универсальный коэффициент роста.
- [Map API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Map.html): `keySet()`, `values()`, `entrySet()` возвращают представления, связанные с отображением; это не независимые копии. Удаление через поддерживаемый iterator такого представления меняет `Map`.
- [OpenJDK 21 HashMap source](https://github.com/openjdk/jdk21u/blob/master/src/java.base/share/classes/java/util/HashMap.java): `Node` содержит hash, key, value, next; bucket может стать деревом при пороге 8 элементов и ёмкости таблицы от 64. Это детали реализации OpenJDK 21, не контракт `Map` и не универсальная гарантия O(log n) для всякого ключа.

## Педагогические следствия

- Таблица сложности должна различать позиционный доступ, поиск значения, операцию на конце, операцию после поиска места, амортизированную вставку и полный обход.
- Для хеширования нужны не только buckets и коллизии, но также `equals`/`hashCode`, стабильность ключа, загрузка и перехеширование; упоминание tree bins — как деталь OpenJDK 21, без ложного вывода о гарантированном O(log n) для любого объекта и любой операции.
- У `HashSet` внутренности логично выводить из уже разобранного `HashMap`, не повторяя всю схему.
