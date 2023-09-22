# Технологии программирования

[Назад к списку лекций](/lectures/2022-fall/)

## Streams API. Lambda-выражения. Работа с файлами

### Streams API и Lambda-выражения
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


### Работа с файлами

// Java IO us NIO
// IO (old)

```java
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class FilesExample {

    public static void examples2() {
        // Как считать данные из файла. Java IO InputStream
        try (FileInputStream fin = new FileInputStream("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources1\\temp1")) {
            int i = -1;
            while ((i=fin.read())!= -1) {
                System.out.print((char) i);
            }

        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }


        // как записать в файл
        try (FileOutputStream fos = new FileOutputStream("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources1\\temp3")) {

            String result = "Hello world";
            byte[] buffer = result.getBytes();
            fos.write(buffer, 0, buffer.length);

        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }

    }

    public static void fileExamples() throws IOException {
        File temp1 = new File("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources\\temp1");
        File dir = new File("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources");

        // Переберем все в файлы в директории, распечатаем их имена и создадим рядом новую директорию
        if (dir.isDirectory()) {
            for (File file : dir.listFiles()) {
                System.out.println(file.getName());
                boolean isCreated = dir.mkdir();

            }
        }

        // переименуем директорию
        dir.renameTo(new File("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources1"));
        
        // создадим новый файлик
        File newFile = new File("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources1\\temp3");
        newFile.createNewFile();
    }
}
``` 

Пример работы с файлами через Scanner и PrintStream

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.Scanner; // аналогично import в Python

public class FileReadWriteExamples {

    // Дописываем throws Exception в заголовок всех методов,
    // которые работают с файлами
    public static void main(String[] args) throws Exception {
        readFileExample(); // прочитай пример файла

        //еще возможности по чтению. Вспомогательный класс `Files`
//        Files.readAllBytes() - прочитать как массив byte
//        Files.readString() - прочитать как строку весь файл
//        Files.readAllLines() - прочитать все строки

        writeFileExample();

        //Files.writeString() - записать строку как один файл с этой строкой
    }

    private static void writeFileExample() throws Exception {
        // запись в файлы будет похожа на печать на экран

        //try это аналог with в python, т.е. при выходе из try будет вызвано outFile.close()
        //PrintStream - это тип, который имеет System.out
        //Т.е. outFile может ровно то же, что и System.out
        try (PrintStream outFile = new PrintStream(new FileOutputStream("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources1\\temp3"))) {
            outFile.println("Hello");
            outFile.print("печать без перевода строки");
            outFile.flush(); // сброс данных в файл, но после закрытия файла это происходит автоматически
        }
    }

    // Дописываем throws Exception в заголовок всех методов,
    // которые работают с файлами
    private static void readFileExample() throws Exception {
        //заводим переменную типа Path для хранения пути к файлу
//        Path txt = Path.of("texts-examples/read-write-example.txt");

        Scanner newScanner = new Scanner(System.in);
        newScanner.nextInt();

        try (Scanner in = new Scanner(new FileInputStream("C:\\Users\\st055259\\IdeaProjects\\lectures\\resources1\\temp3"))) {
            String line1 = in.nextLine(); // прочитать строку nextLine()
            String line2 = in.nextLine(); // прочитать следующую строку
            String word3 = in.next(); // прочитать следующее слово
            System.out.println(line1);
            System.out.println(line2);
            System.out.println(word3);

            int x = in.nextInt();
            System.out.println(x);
            //int y = in.nextInt(); //ошибка, там уже не число

            if (in.hasNextInt()) {
                int y = in.nextInt();
                System.out.println("прочитали число " + y);
            } else {
                System.out.println("в файле дальше не число");
            }

            while (in.hasNext()) {
                String word = in.next();
                System.out.println("Прочитано слово " + word);
            }
        }
    }
}

```