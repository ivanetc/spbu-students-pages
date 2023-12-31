# Технологии программирования

[Назад к списку лекций](/lectures/2022-fall/)

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


## Регулярки в Java

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

