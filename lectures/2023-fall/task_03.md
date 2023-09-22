# ДЗ 3. Комплексные числа

## Дедлайн
**Мягкий дедлайн** - 22 сентября в 21-00

**Жесткий дедлайн** - 29 сентября в 21-00

## Как сдать
Реализуйте нужные классы. Запустите у себя на компьютере тесты. Для этого откройте консоль и выполните команду
```bash
./gradlew test
```

Если тесты прошли успешно - вы увидите надпись `BUILD SUCCESSFUL` , если же вы увидите надпись `BUILD FAILED`, то найдите в сообщении в терминале название теста и посмотрите этот тест в директории `src/test/groovy/`

После этого отправьте свое решение в ветку **main**. Призовите меня (ivanetc) в комментариях, где, **пожалуйста**, **напишите** "Cдаю задачи 1, 2, 3 ... n".
Убедитесь, что тесты проходят локально.

## Комплексные числа

Настало время вспомнить алгебру! И попрактиковаться в создании классов! Давайте создадим класс **ComplexNumber**

Краткое описание класса:

Класс **ComplexNumber** представляет комплексные числа вида a + bi. Класс содержит конструктор, методы для выполнения
арифметических операций, методы для получения действительной и мнимой части числа, а также метод для вывода комплексного
числа в виде строки и метод сравнения комплексных чисел.


Класс **ComplexNumber** должен представлять комплексные числа в виде a + bi, где a и b - действительные числа.
В классе должны быть реализованы следующие методы:

1. Конструктор, который принимает два аргумента (действительную и мнимую части числа) и создает комплексное число.
2. Метод сложения комплексных чисел (**_plus_**),
3. Метод вычитания комплексных чисел (**_minus_**),
4. Метод умножения комплексных чисел (**_multiply_**)
5. Метод деления комплексных чисел (**_divide_**)

В методах 2-5 в качестве параметра принимается другое комплексное число и возвращается новое. При этом исходное
комплексное число не меняется.

6. Методы получения действительной и мнимой частей числа (**_getReal_**, **_getImaginary_**). Возвращаемое значение
   double.
7. Метод **_toString_**, который возвращает комплексное число в виде строки "a+bi".
8. Метод сравнения комплексных чисел **_compare_**. В качестве параметра принимается другое комплексное число.
   Если исходное комплексное число больше передаваемого вернем 1, если исходное число меньше передаваемого вернем -1,
   если числа равны вернем 0.