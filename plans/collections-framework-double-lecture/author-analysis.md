# Исследование авторских материалов

Дата проверки: 13 ноября 2026. Целевая версия новой лекции — Java 21. Здесь проверена выборка существенных утверждений о коллекциях, а не весь текст конспектов.

## Что студенты уже слышали

По сообщению преподавателя, из [`lectures/autumn/lecture_06.md`](../../lectures/autumn/lecture_06.md) изложены только разделы 1–4: разрастание модели и файлов, пакеты, `enum StudentStatus`, `record UniversityGroup`. Значит, глава о Collections Framework из этого же файла — **ещё не пройденный материал**. До неё в курсе были знакомы массивы и цикл `for-each` по массиву (`lecture_01.md`), интерфейсы и полиморфизм (`lecture_03.md`), логическое равенство и контракт `hashCode` с предварительным примером `HashSet` (`lecture_04.md`), generics и обёртки примитивов (`lecture_05.md`). Из структур данных, по уточнению преподавателя, известны массивы и O-нотация, но не устройство связного списка и хеш-таблицы.

## Реальная структура исходников

| Файл и место | Содержание | Роль в новой лекции |
| --- | --- | --- |
| `lectures/autumn/lecture_06.md`, §1–4 | Университетская модель: `Student`, `UniversityGroup`, `StudentStatus`; перенос в пакеты, `record` и смысл равенства | Уже рассказанное: краткое напоминание, продолжать ту же модель без повтора подробностей |
| Там же, §5 | Мотив от массива к Framework; интерфейс и реализация; `Collection` / `Collections`; упрощённая карта | Основа первой половины, расширить до реальной иерархии Java 21 |
| Там же, §6–9 | `List`, `Set`, `Map`, `Queue`/`Deque` на студентах, группах и заявках; `ArrayList`, `LinkedList`, `HashSet`, `LinkedHashSet`, `TreeSet`, `HashMap`, `LinkedHashMap`, `TreeMap`, `ArrayDeque` | Сохранить сценарии; глубже объяснить выбор и порядок, ввести стоимость операций |
| Там же, §10–12 и справка | `of`/`copyOf`, ограничения `null`, полный проект, таблица выбора, упражнения, `List<Integer>.remove` | Сохранить как практический слой; полный проект дозировать, не читать все файлы подряд |
| `lectures/2023-fall/lecture_08.md`, §Collections | Старый обзор реализаций короткими фрагментами | Использовать как перечень тем, но проверить факты; не переносить сторонние картинки и устаревшие утверждения |
| `lectures/autumn/lecture_04.md`, конец | `equals`, `hashCode`, коллизии и `HashSet<UniversityGroup>` | Опора для объяснения коллизий и инварианта ключа; повторить только нужный минимум |
| `lectures/autumn/lecture_05.md`, §Generics | `Box<T>`, `List<T>`, обёртки | Опора для сигнатур `List<E>`/`Map<K,V>`; не повторять теорию erasure |

## Авторская линия и педагогические находки

Основной вопрос развивается естественно: массив участников перестаёт подходить для растущего набора → контракт хранения зависит от задачи → один и тот же университетский домен требует списка записей, уникальных групп, индекса по ID и очереди заявок. Фрагменты показывают наблюдаемые результаты (`add` дубликата в `Set`, замена `put`, `poll` пустой очереди), что удобно использовать как предсказания перед запуском. Рисунки §5–10 показывают логические роли, не подменяя внутреннее устройство. Хорошо объяснены различия `Map.get` и `containsKey`, `of` и `copyOf`, поверхностного снимка и неизменяемого объекта, а также отсутствие обещания порядка у хеш-коллекций.

Резкий переход для новой задачи находится в конце §12: внутренности и асимптотика, затем итерация и сортировка обещаны *следующими отдельными занятиями*. По новому расписанию таких занятий не будет. Для готовой двойной лекции нужны новый блок об устройстве, сравнение операций с уточнением видов оценки, минимальные `Iterable`/`Iterator` и обход `Map.entrySet`, сортировка через `Comparator` на уровне применения. Нельзя просто добавить таблицу Big O к существующему обзору: студенты не знают, что такое узлы и корзины. Старый конспект §Collections не даёт объяснения хеширования и содержит ошибку про `PriorityQueue` как FIFO.

Важное ограничение времени: §1–4 шестой лекции повторять только мостиком на 2–3 минуты. §11 с четырьмя полными файлами оставить для самостоятельного чтения или раздаточного конспекта; на экране развивать один работающий пример. `WeakHashMap`, `Hashtable`, `Vector`, `Stack` из старого §Collections не нужны для решения заявленной задачи и отвлекут от основных механизмов. `ArrayDeque` нужен как практическая очередь/стек, но глубокий разбор кольцевого буфера можно оставить за пределами устных 160 минут.

## Реестр проверенных утверждений

| Место / тезис | Статус для Java 21 | Исправление или граница | Первичный источник |
| --- | --- | --- | --- |
| `lecture_06` §5: `Map` — часть Framework, но не подтип `Collection` | Верно | На схеме Java 21 отметить `SequencedCollection`, `SequencedSet`, `SequencedMap`, введённые в 21; упрощённая схема должна быть явно подписана | [Oracle JCF outline 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/doc-files/coll-reference.html), [SequencedCollection 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/SequencedCollection.html) |
| `lecture_06` §6: `ArrayList` и `LinkedList` разделяют `List`, но стоимость различна | Верно | У `ArrayList` `get/set` O(1), append амортизированно O(1), вставка/удаление со сдвигом O(n). У `LinkedList` доступ по индексу требует обхода от ближнего конца; вставка после получения узла O(1), поиск позиции O(n) | [ArrayList 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayList.html), [LinkedList 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedList.html) |
| `lecture_06` §7: `HashSet` не обещает порядок; реализован через `HashMap` | Верно | O(1) для базовых операций оговорено равномерным распределением хешей; обход имеет стоимость O(число элементов + ёмкость таблицы) | [HashSet 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashSet.html) |
| `lecture_06` §7–8: обычные `LinkedHashSet` / `LinkedHashMap` сохраняют порядок вставки, повторное добавление/`put` не перемещает запись | Верно, с оговоркой | В Java 21 есть явные методы перестановки `addFirst/addLast`, `putFirst/putLast`, а `LinkedHashMap` может быть сконструирован в режиме порядка доступов. Для обычного конструктора тезис верен | [LinkedHashSet 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedHashSet.html), [LinkedHashMap 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedHashMap.html) |
| `lecture_06` §8: `HashMap` допускает `null` ключ и значения, `get == null` не доказывает отсутствия ключа | Верно | Ввести `containsKey`; при разборе сложности оговорить качество хеша и resize. `keySet`/`values`/`entrySet` являются связанными с картой представлениями, а не независимыми копиями | [HashMap 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html), [Map 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Map.html) |
| `lecture_06` §9: `ArrayDeque` для FIFO и LIFO, `null` запрещён, `poll/peek` пустой возвращают `null` | Верно | Большинство операций амортизированно O(1), а поиск `contains/remove(Object)` O(n); `Queue` вообще не гарантирует FIFO для всех реализаций | [ArrayDeque 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html), [Queue 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Queue.html) |
| `lecture_06` §10: `List.copyOf` фиксирует состав, но не копирует изменяемые элементы; `Set.of` отклоняет повторы, а `Set.copyOf` схлопывает их | Верно | У `Set.copyOf` при равных, но разных ссылках представитель произволен. `copyOf` может повторно использовать уже неизменяемый контейнер; не обещать новый identity | [List 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html), [Set 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Set.html) |
| `lecture_08` §Queue: `PriorityQueue` — FIFO | **Неверно** | Голова — минимальный по сравнению элемент; равные приоритеты разрешаются произвольно. Это O(log n) enqueue/dequeue, O(1) peek | [PriorityQueue 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/PriorityQueue.html) |
| `lecture_08` §List: `ArrayDeque` «быстрее Stack и LinkedList» | Зависит от контекста | API называет его *likely to be faster* в ролях стека/очереди, но это не универсальная гарантия производительности | [ArrayDeque 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html) |
| Новая тема: удаление при обходе и fail-fast | Проверено для Java 21 | `Iterator.remove` удаляет последний выданный элемент; изменение контейнера иным способом во время обхода не имеет универсального результата. `ConcurrentModificationException` в общих реализациях — best effort, возможна и в одном потоке, не механизм корректности | [Iterator 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Iterator.html), [ConcurrentModificationException 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ConcurrentModificationException.html) |

## Рекомендации редактору

1. Сохранить университетскую модель и последовательность задач, заменив старую концовку §12 на реальный переход к устройству и асимптотике в той же сдвоенной лекции.
2. Сразу отделять *контракт интерфейса* от *свойств конкретной реализации OpenJDK 21*. Формулу `HashMap` O(1) не записывать без условия на распределение; tree bins не превращать в безусловное обещание O(log n) для каждого вызова.
3. Студентам, знающим только массив, показать узел двусвязного списка, массив ссылок и сдвиг, таблицу корзин, коллизию, resize и разницу между `equals` и `hashCode`. Их предыдущее знание равенства из лекции 4 позволяет не объяснять `equals` заново.
4. В первой половине включить `Iterable` → `Iterator` как механизм `for-each` и `Map.entrySet` как способ обхода, чтобы следующий блок о Stream API опирался на понятную традиционную обработку коллекций. Упомянуть безопасное удаление через итератор, не строить рассказ вокруг fail-fast исключения.
5. Показать `Comparator` и `List.sort` на одном коротком сценарии выбора порядка; деревья `TreeSet`/`TreeMap` оставить обзорно, поскольку доказательство балансировки дерева не помещается в 160 минут.
6. В справке оставить `of/copyOf`, `List<Integer>.remove`, варианты null и таблицу выбора; в устной части дать только ловушки, которые существенны для решаемого примера.

## Границы проверки

Проверены перечисленные API-утверждения по Oracle Java SE 21. Исходный `lecture_06.md` содержит ссылки на Java 26; в новом конспекте их надо заменить на 21 и отдельно сверить все новые вызовы при написании. Конкретный исходный код `HashMap` OpenJDK 21 (пороги treeify/untreeify, детали смешивания hash и формулу роста) здесь не аудирован: это отдельное исследование для разработки внутреннего раздела.
