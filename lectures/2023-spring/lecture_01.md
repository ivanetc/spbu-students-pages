# Технологии программирования

[Назад к списку лекций](/lectures/2023-spring/)

## Сборка приложения Java. Клиент-серверная архитектура. Трехслойная архитектура бэкенда.

### Сборка приложения Java.

Мы привыкли собирать и запускать приложение через Idea. Но как это сделать вручную?
Необходимо скомпилировать нашу программу в байт-код, а после этого запустить его.

Компиляция — приведение исходного кода в байт-код для последующего старта программы.
(В качестве доп. инфы - [статья про байт-код](https://habr.com/ru/post/568402/))

Порядок действий:
- Разрабатываем программу в .java файле.
- Компилируем в байт-код (превращаем _.java_ классы в _.class_ файлы)
- Запускаем программу

Возьмем для примера простую одноклассовую программу:
```java

class Test {
   public static void main(String[] args) {
      System.out.println("This is our test compilation");
   }
}

```
Поместим этот код в файл Test.java. Чтобы скомпилировать нашу программу воспользуемся утилитой javac. 
Для этого в командной строке необходимо выполнить команду

```sh
javac Test.java
```
После этого мы получим файл Test.class и сможем его запустить при помощи команды:

```sh
java Test
```

### Как скомпилировать приложение из нескольких классов?
Добавим новый класс
```java
class Test {
    public static void main(String[] args) {
        Student st = new Student();
        st.name = "Petya";
        st.sayHello();
        System.out.println("This is our test compilation");
    }
}

class Student {
    public String name;
    
    public void sayHello() {
        System.out.println("Hello, this is " + name);
    }
}
```

Чтобы скомпилировать программу из нескольких классов поместим их в папку src, создадим папку bin 
для файлов .class и выполним команду:

```sh
javac -d bin ./src/*
```

Далее для запуска программы нужно выполнить команду:

```sh
java -classpath ./bin Test
```

### Можно ли сделать один исполняемый файл? 

Да, но нам потребуется манифест. Создадим файл manifest.mf
Манифест - это файл пары ключей-значений, в котором мы описываем параметры сборки приложений:

```manifest
main-class: Test
class-path: bin/
```
Поместим этот файл в root папку проекта и выполним команду:

```sh
jar -cmf manifest.mf spbu.jar  -C bin .
```

Мы получили файл _spbu.jar_. Теперь мы можем легко транспортировать нашу программу, просто скопировав
наш jar файл. Чтобы запустить его нужно выполнить команду:

```sh
java -jar spbu.jar
```

Чуть подробнее этот пример разбирается в [статье](https://javarush.com/groups/posts/2318-kompiljacija-v-java)

## Системы сборок.
Ant, Maven и Gradle.

Maven - в файлах конфигурации описываем проект и дополнительные инструменты

Структура проекта:
![](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Maven_CoC.svg/1280px-Maven_CoC.svg.png)

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>ru.javarush.testmaven</groupId>
  <artifactId>spbu_arts</artifactId>
  <version>1.0.0</version>

  <build>
     <defaultGoal>compile</defaultGoal>
     <sourceDirectory>src</sourceDirectory>
     <outputDirectory>bin</outputDirectory>
     <finalName>${project.artifactId}-${project.version}</finalName>
  </build>
</project>
```

## Gradle

```groovy
apply plugin: 'java'
apply plugin: 'application'

sourceSets {
   main {
       java {
           srcDirs 'src'
       }
   }
}
sourceSets.main.output.classesDir = file("bin")

mainClassName = "src.BoxMachine"

defaultTasks 'compileJava', 'run'
```

Система управления сборкой проектов на основе Groovy. 
Скрипты сборки Gradle - по сути скрипты Groovy

```groovy
task hello {
    doLast {
        println 'Hello!'
    }
}

task fromSpbu(dependsOn: hello) {
    doLast {
        println "I'm from spbu"
    }
}
```

Можно добавить поведение к задаче
```groovy
task helloSpbu {
    doLast {
        println 'I will be executed second!'
    }
}

helloSpbu.doFirst {
    println 'I will be executed first!'
}

helloSpbu.doLast {
    println 'I will be executed last!'
}

```

### Плагины
Плагины - бывают двух видов: скриптовые и бинарные.
Скриптовые:
```groovy

// in spbu.gradle
task fromPlugin {
    doLast {
        println "I'm from plugin"
    }
}

// in build.gradle
apply from: 'aplugin.gradle'
```

Бинарные
```groovy
plugins {
    id "org.shipkit.bintray" version "2.3.5"
}
```

### Объявление репозитория
```groovy
repositories {
    mavenCentral()
}
```

Maven Central - центральный репозиторий Maven. Ссылка [тык сюда](https://repo.maven.apache.org/maven2/)
Искать пакеты можно [туть](https://mvnrepository.com/)

### Зависимости

```groovy
dependencies {
    implementation group: 
      'org.springframework', name: 'spring-core', version: '4.3.5.RELEASE'
    implementation 'org.springframework:spring-core:4.3.5.RELEASE',
            'org.springframework:spring-aop:4.3.5.RELEASE'
    implementation(
        [group: 'org.springframework', name: 'spring-core', version: '4.3.5.RELEASE'],
        [group: 'org.springframework', name: 'spring-aop', version: '4.3.5.RELEASE']
    )
    testImplementation('org.hibernate:hibernate-core:5.2.12.Final') {
        transitive = true
    }
    runtimeOnly(group: 'org.hibernate', name: 'hibernate-core', version: '5.2.12.Final') {
        transitive = false
    }
}
```

Локальные зависимости:

```groovy
implementation files('libs/joda-time-2.2.jar', 'libs/junit-4.12.jar')
implementation fileTree(dir: 'libs', include: '*.jar')
```

Виды объявления зависимостей:
- api - зависимости будут транзитивно доступны потребителям библиотеки 
- implementation - зависимости не будут доступны потребителям
- compile - удалена начиная с gradle 7.0 
- runtime - удалена начиная с gradle 7.0 
- runtimeOnly - Здесь вы объявляете зависимости, которые требуются только во время выполнения, а не во время компиляции.
- compileOnly - Здесь вы объявляете зависимости, которые требуются во время компиляции, но не во время выполнения. Обычно это включает в себя зависимости, которые затеняются при обнаружении во время выполнения.
- testImplementation
- testCompileOnly
- testRuntimeOnly

[Дока тут](https://docs.gradle.org/current/userguide/java_library_plugin.html#sec:java_library_configurations_graph)

### Некоторые tasks из плагина java
Список всех задач смотри в доке [здесь](https://docs.gradle.org/current/userguide/java_plugin.html)
- compileJava
- jar
- test
- clean
- build


# Клиент-серверная архитектура
см доску [Miro](https://miro.com/app/board/uXjVPo9Jtww=/?share_link_id=545215110811)
