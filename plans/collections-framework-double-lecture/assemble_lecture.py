"""Assemble lecture 7 from reviewed sections and finished diagrams."""

from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
work = root / "plans/collections-framework-double-lecture"
part1 = (work / "parts/01-framework-and-use.md").read_text()
part2 = (work / "parts/02-implementation-and-cost.md").read_text()

img = "../../resources/lectures/2026-fall/collections-internals/"
diagrams1 = [
    f"![Четыре задачи к университетским данным: повторные записи, уникальные группы, поиск по ID и порядок обработки заявок]({img}framework-roles.png)",
    f"[![Иерархия интерфейсов Java 21 с методами и соответствующими классами; Vector, Stack и Hashtable отмечены как старые реализации]({img}framework-hierarchy.png)]({img}framework-hierarchy.svg)",
    f"![List с повторной ссылкой на Ивана; после удаления первой позиции индексы Анны и Ивана меняются]({img}list-semantics.png)",
    f"![Map связывает ключи ID 1 и ID 2 с карточками студентов Ивана и Анны]({img}map-key-value.png)",
    f"![Map.put для существующего ключа 2 заменяет Анну на Ивана, число ключей остаётся равным двум]({img}map-put.png)",
    f"![FIFO очередь: вход справа, выход слева; LIFO стек: добавление и извлечение с одного конца]({img}queue-fifo-lifo.png)",
    f"![Коллекция с контрактом Iterable возвращает Iterator; курсор находится перед следующим элементом последовательности]({img}iterable-iterator.png)",
    f"![Итератор проходит список по одному элементу, а entrySet даёт связанное с Map представление пар]({img}iterator-map-view.png)",
]
diagrams2 = [
    f"![Три учебные модели роста числа шагов: постоянная для get(i), линейная для contains(x) и квадратичная для n поисков]({img}asymptotic-growth.png)",
    f"![ArrayList: три занятые ячейки из шести, прямой доступ к индексу и сдвиг ссылок при вставке]({img}arraylist-operations.png)",
    "",
    f"![LinkedList: три двусвязных узла и ссылки first и last; индекс требует переходов по узлам]({img}linkedlist-nodes.png)",
    f"![HashMap: два разных ключа попали в одну корзину; поиск проверяет записи до равного ключа]({img}hashmap-lookup.png)",
    f"![Учебный пример расширения HashMap с четырёх до восьми корзин: ключи 1 и 5 расходятся]({img}hashmap-resize.png)",
    f"![HashSet хранит элемент как ключ внутреннего HashMap со служебным значением]({img}hashset-map.png)",
    f"![Три состояния ArrayDeque в OpenJDK 21: A, B, C расположены через границу массива из четырёх ячеек; добавление D заполняет его и вызывает расширение до десяти ячеек с переносом A]({img}arraydeque-ring.png)",
]


def insert_diagrams(text, replacements):
    matches = list(re.finditer(r"<!-- DIAGRAM:.*? -->", text, re.S))
    assert len(matches) == len(replacements), (len(matches), len(replacements))
    it = iter(replacements)
    return re.sub(r"<!-- DIAGRAM:.*? -->", lambda _: next(it), text, flags=re.S)


part1 = insert_diagrams(part1, diagrams1)
part2 = insert_diagrams(part2, diagrams2)
part1 = part1.replace("../../lectures/autumn/lecture_06.md", "/lectures/autumn/lecture_06.html")
part1 = part1.replace("../../lectures/autumn/lecture_04.md", "/lectures/autumn/lecture_04.html")
part2 = part2.replace("../../../../lectures/autumn/lecture_04.md", "/lectures/autumn/lecture_04.html")

part1 = part1.replace("## Часть I.", '<a id="part1"></a>\n\n## Часть I.', 1)
part2 = part2.replace("## Часть II.", '<a id="part2"></a>\n\n## Часть II.', 1)
part2 = part2.replace("### Сравним полную цену операции", '<a id="complexity"></a>\n\n### Сравним полную цену операции', 1)

header = """# Лекция 7. Java Collections Framework: выбор, устройство и сложность

[Главная](/)

**Два занятия по 80 минут · Java 21.** Продолжение [лекции 6](/lectures/autumn/lecture_06.html) после раздела про `record`.

### Содержание

1. [Часть I. Как выбрать коллекцию и работать с ней](#part1)
2. [Часть II. Что хранится внутри и откуда берётся стоимость](#part2)
3. [Сводная таблица стоимости операций](#complexity)
4. [Дополнительное чтение](#reading)

"""
reading = """

<a id="reading"></a>

## Дополнительное чтение

- [Oracle: Collections Framework в Java 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/doc-files/coll-overview.html) — официальная карта интерфейсов и реализаций.
- [Oracle: `ArrayList`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayList.html), [`LinkedList`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedList.html), [`HashMap`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html), [`HashSet`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashSet.html), [`ArrayDeque`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html) — контракты и оговорки о стоимости.
- [Cornell CS 2110: хеширование](https://www.cs.cornell.edu/courses/cs2110/2025fa/lectures/lec20/) и [обход структур](https://www.cs.cornell.edu/courses/cs2110/2025fa/lectures/lec14/) — упражнения для закрепления.

**Самопроверка:** объясните, почему `add(0, e)` у `ArrayList` и `add(i, e)` у `LinkedList` в середине оба могут стоить `O(n)`, но по разным причинам. Что должно быть верно о ключах и распределении хешей, чтобы поиск в `HashMap` был ожидаемо `O(1)`?
"""

text = header + part1.rstrip() + "\n\n" + part2.rstrip() + reading
text = re.sub(r"\n{3,}", "\n\n", text)
(root / "lectures/autumn/lecture_07.md").write_text(text)
