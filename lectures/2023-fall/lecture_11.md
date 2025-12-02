# Технологии программирования

[Назад на главную](/)

## Лекция 11. Введение в многопоточность в Java **

#### 1. Что такое многопоточность?

**Многопоточность** — это способность программы выполнять **несколько действий одновременно**.

Почему это полезно?

* можно ускорить выполнение задач,
* можно выполнять работу в фоне,
* программа не “замораживается” при долгой операции.

---

## 2. Процессы и потоки

Прежде чем говорить о потоках, важно разделить два понятия.

#### 2.1. Что такое процесс?

**Процесс** — это запущенная программа.
Операционная система выделяет процессу:

* собственную память,
* ресурсы (дескрипторы файлов, сокеты и др.),
* одно или несколько ядёр CPU.

Каждый процесс работает **изолированно** от других.

Когда вы запускаете Java-приложение (`java Main`), создаётся процесс JVM.

---

#### 2.2. Что такое поток?

**Поток (Thread)** — это *единица выполнения* внутри процесса.
Потоки:

* разделяют память процесса (кучу Heap),
* имеют собственный стек вызовов,
* могут выполняться параллельно.

###### Сколько потоков может быть в процессе?

Сколько угодно — ограничение только по ресурсам ОС.

Обычная JVM-программа создаёт десятки потоков автоматом:

* GC-потоки,
* JIT-потоки,
* вспомогательные.

Даже если вы не создаёте потоки вручную — они есть.

---

#### 2.3. Как Java управляет потоками?

JVM **не реализует планировщик потоков сама** → она полагается на планировщик ОС.

* ОС решает, какой поток сейчас выполняется.
* JVM лишь создаёт/завершает потоки и обрабатывает синхронизацию.

Важно: Java-поток = системный поток операционной системы.

---

#### 2.4. Простейший пример создания потока

```java
Thread t = new Thread(() -> {
    System.out.println("Hello from thread!");
});

t.start(); // запускает новый поток
System.out.println("Main thread finished");
```

---

## 3. Почему многопоточность — это сложно

Многопоточность ускоряет программу, но создаёт **новые, непривычные проблемы**.

---

## 3.1. Проблема №1: гонки данных (race condition)

Это ситуация, когда **два потока одновременно читают и изменяют общие данные**, и результат становится неправильным.

Возьмём класс Wallet:

```java
class Wallet {
    private int balance = 100;

    public void withdraw(int amount) {
        if (balance >= amount) {
            balance = balance - amount;
        }
    }

    public int getBalance() {
        return balance;
    }
}
```

Два потока снимают по 80:

```java
Wallet wallet = new Wallet();

Thread t1 = new Thread(() -> wallet.withdraw(80));
Thread t2 = new Thread(() -> wallet.withdraw(80));

t1.start();
t2.start();
```

###### Что происходит внутри (пошагово):

1. **Поток 1** читает balance: 100  
2. **Поток 2** читает balance: 100  
3. Поток 1 выполняет `balance = 20`  
4. Поток 2 выполняет `balance = -60`  

Итог: **-60** — некорректно.

---

## 3.2. Проблема №2: взаимная блокировка (deadlock)

```java
public static void transfer(Wallet from, Wallet to, int amount) {
    synchronized (from) {
        synchronized (to) {
            from.withdraw(amount);
            to.add(amount);
        }
    }
}
```

###### Как возникает deadlock?

```java
Wallet w1 = new Wallet(100);
Wallet w2 = new Wallet(100);

Thread t1 = new Thread(() -> Wallet.transfer(w1, w2, 10));
Thread t2 = new Thread(() -> Wallet.transfer(w2, w1, 20));
```

---

## 3.3. Проблема №3: проблема видимости (visibility)

```java
class Wallet {
    private boolean active = true;

    public void deactivate() {
        active = false;
    }

    public void watch() {
        while (active) { }
        System.out.println("Wallet deactivated");
    }
}
```

Исправление:

```java
private volatile boolean active = true;
```

---

## 4. Как Java решает проблемы многопоточности

#### 4.1. synchronized

```java
public synchronized void withdraw(int amount) {
    if (balance >= amount) {
        balance -= amount;
    }
}
```

---

#### 4.2. synchronized-блоки

```java
synchronized (this) {
    balance -= amount;
}
```

---

#### 4.3. volatile

Используется для гарантии видимости изменений между потоками.

---

## 5. Concurrent Collections

| Коллекция               | Для чего подходит                                |
| ----------------------- | ------------------------------------------------ |
| `ConcurrentHashMap`     | потокобезопасная Map, высокая производительность |
| `CopyOnWriteArrayList`  | редко изменяется, часто читается                 |
| `ConcurrentLinkedQueue` | неблокирующая очередь                            |

---

## 6. ExecutorService

```java
ExecutorService exec = Executors.newFixedThreadPool(4);

exec.submit(() -> {
    System.out.println("Task executed!");
});

exec.shutdown();
```

---

## 7. Что нужно запомнить

✔ Потоки выполняются параллельно и разделяют общую память  
✔ Основные проблемы: гонки данных, deadlock, visibility  
✔ Инструменты: synchronized, volatile, concurrent collections, ExecutorService

