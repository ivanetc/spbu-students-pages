"""Generate editable SVG and PNG diagrams for autumn lecture 7."""

from pathlib import Path
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderSVG, renderPDF
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "resources/lectures/2026-fall/collections-internals"
OUT.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

BG = HexColor("#fbfcfd")
WHITE = HexColor("#ffffff")
INK = HexColor("#26323d")
MUTED = HexColor("#5c6975")
LINE = HexColor("#9eabb5")
PALE = HexColor("#e8edf1")
BLUE = HexColor("#155799")
GREEN = HexColor("#159957")
BLUE_PALE = HexColor("#edf5fb")
GREEN_PALE = HexColor("#eef8f3")
SAND_PALE = HexColor("#fff8eb")
SAND = HexColor("#b8842f")


class Canvas:
    def __init__(self, width, height, title, note=None):
        self.w, self.h = width, height
        self.d = Drawing(width, height)
        self.d.add(Rect(0, 0, width, height, fillColor=BG, strokeColor=None))
        self.d.add(Rect(32, height-60, 6, 30, rx=3, ry=3, fillColor=BLUE, strokeColor=None))
        self.text(52, 51, title, 25, bold=True)
        if note:
            self.text(42, height-25, note, 17, color=MUTED)

    def text(self, x, top, value, size=20, color=INK, bold=False, anchor="start"):
        self.d.add(String(x, self.h-top, value, fontName="ArialBold" if bold else "Arial", fontSize=size, fillColor=color, textAnchor=anchor))

    def box(self, x, top, w, h, label=None, fill=WHITE, stroke=LINE, size=20, bold=False):
        self.d.add(Rect(x, self.h-top-h, w, h, rx=10, ry=10, fillColor=fill, strokeColor=stroke, strokeWidth=1.7))
        if label:
            self.text(x+w/2, top+h/2+7, label, size=size, bold=bold, anchor="middle")

    def line(self, x1, t1, x2, t2, color=LINE, width=2):
        self.d.add(Line(x1, self.h-t1, x2, self.h-t2, strokeColor=color, strokeWidth=width))

    def arrow(self, x1, t1, x2, t2, color=BLUE, width=2):
        self.line(x1,t1,x2,t2,color,width)
        import math
        angle=math.atan2(t2-t1,x2-x1)
        a=math.pi/7
        r=10
        p=[x2,self.h-t2,
           x2-r*math.cos(angle-a),self.h-(t2-r*math.sin(angle-a)),
           x2-r*math.cos(angle+a),self.h-(t2-r*math.sin(angle+a))]
        self.d.add(Polygon(p,fillColor=color,strokeColor=None))

    def save(self, name):
        svg=OUT/f"{name}.svg"
        pdf=OUT/f"{name}.pdf"
        renderSVG.drawToFile(self.d,str(svg))
        renderPDF.drawToFile(self.d,str(pdf))
        subprocess.run(["pdftoppm","-f","1","-l","1","-singlefile","-png","-r","144",str(pdf),str(OUT/name)],check=True,stdout=subprocess.DEVNULL)
        pdf.unlink()


def hierarchy():
    c=Canvas(2000,1220,"Контракты и реализации Java 21")

    def legend(x, label, fill, stroke, dashed=False):
        c.d.add(Rect(x,c.h-115,28,23,rx=5,ry=5,fillColor=fill,strokeColor=stroke,strokeWidth=2,strokeDashArray=[4,3] if dashed else None))
        c.text(x+40,111,label,18)
    legend(55,"интерфейс",BLUE_PALE,BLUE)
    legend(405,"абстрактный класс",SAND_PALE,SAND,True)
    legend(905,"конкретный класс",GREEN_PALE,GREEN)
    legend(1380,"legacy (конкретный класс)",PALE,LINE)

    def iface(x,t,w,h,name,methods,nsize=22,msize=17):
        c.box(x,t,w,h,fill=BLUE_PALE,stroke=BLUE)
        c.text(x+w/2,t+32,name,nsize,bold=True,anchor="middle")
        lines=methods if isinstance(methods,list) else [methods]
        for j,value in enumerate(lines):
            c.text(x+w/2,t+62+j*21,value,msize,color=MUTED,anchor="middle")

    def abstract(x,t,w,label,size=19):
        c.d.add(Rect(x,c.h-t-64,w,64,rx=10,ry=10,fillColor=SAND_PALE,strokeColor=SAND,strokeWidth=2,strokeDashArray=[6,4]))
        c.text(x+w/2,t+39,label,size,bold=True,anchor="middle")

    def concrete(x,t,w,label,size=18):
        c.box(x,t,w,55,label,GREEN_PALE,GREEN,size,True)

    def legacy(x,t,w,label,size=17):
        c.box(x,t,w,55,label,PALE,LINE,size,True)
        c.box(x+w-68,t-13,66,23,"legacy",WHITE,LINE,12,True)

    # Interfaces: arrows point from a superinterface to a subinterface.
    iface(850,155,300,72,"Iterable<E>","iterator()")
    iface(850,260,300,96,"Collection<E>",["size(), contains(e)","add(e), remove(e)"],msize=16)
    iface(110,405,300,90,"Set<E>",["add(e), contains(e)","нет равных элементов"],msize=16)
    iface(720,405,370,96,"SequencedCollection<E>",["getFirst(), getLast()","reversed()"],nsize=20,msize=16)
    iface(1300,405,300,80,"Queue<E>","offer(e), poll(), peek()",msize=16)
    iface(1690,260,280,96,"Map<K,V>",["get(k), put(k,v)","containsKey(k), entrySet()"],msize=16)
    iface(110,545,300,75,"SequencedSet<E>","порядок + reversed()",nsize=20,msize=16)
    iface(750,545,310,75,"List<E>","get(i), set(i,e), add(i,e)",msize=16)
    iface(1295,545,310,75,"Deque<E>","offerFirst(e), pollLast()",msize=16)
    iface(1690,405,280,80,"SequencedMap<K,V>","firstEntry(), reversed()",nsize=20,msize=16)
    c.arrow(1000,227,1000,260,BLUE)
    c.arrow(905,356,260,405,BLUE)
    c.arrow(1000,356,905,405,BLUE)
    c.arrow(1095,356,1450,405,BLUE)
    c.arrow(260,495,260,545,BLUE)
    c.arrow(815,501,395,545,BLUE)
    c.arrow(905,501,905,545,BLUE)
    c.arrow(1000,501,1370,545,BLUE)
    c.arrow(1450,485,1450,545,BLUE)
    c.arrow(1830,356,1830,405,BLUE)

    # Abstract classes are integrated into their interface branches.
    abstract(110,680,300,"AbstractSet<E>")
    abstract(750,680,310,"AbstractList<E>")
    abstract(1180,680,270,"AbstractQueue<E>")
    abstract(1460,680,210,"AbstractCollection<E>",14)
    abstract(1690,680,280,"AbstractMap<K,V>")

    # Dashed grey paths mean that a class fulfills an interface contract.
    def contract_path(points):
        for (x1,t1),(x2,t2) in zip(points,points[1:]):
            c.d.add(Line(x1,c.h-t1,x2,c.h-t2,strokeColor=LINE,strokeWidth=2.2,strokeDashArray=[6,4]))
        (x1,t1),(x2,t2)=points[-2:]
        import math
        a=math.atan2(t2-t1,x2-x1)
        r=10
        c.d.add(Polygon([x2,c.h-t2,x2-r*math.cos(a-.45),c.h-(t2-r*math.sin(a-.45)),x2-r*math.cos(a+.45),c.h-(t2-r*math.sin(a+.45))],fillColor=LINE,strokeColor=None))
    contract_path([(110,445),(75,445),(75,712),(110,712)])
    contract_path([(905,620),(905,680)])
    contract_path([(1300,445),(1155,445),(1155,712),(1180,712)])
    contract_path([(1690,308),(1670,308),(1670,712),(1690,712)])

    # Concrete descendants and the abstract class in the LinkedList branch.
    concrete(85,850,150,"HashSet")
    concrete(255,850,170,"TreeSet",17)
    concrete(85,985,200,"LinkedHashSet",17)
    c.arrow(190,744,160,850,GREEN)
    c.arrow(330,744,340,850,GREEN)
    c.arrow(160,905,160,985,GREEN)

    concrete(620,850,135,"ArrayList",17)
    abstract(770,845,175,"AbstractSequentialList",14)
    legacy(960,850,130,"Vector",17)
    concrete(770,985,175,"LinkedList",17)
    legacy(960,985,130,"Stack",17)
    c.arrow(825,744,688,850,GREEN)
    c.arrow(905,744,858,845,GREEN)
    c.arrow(1000,744,1025,850,GREEN)
    c.arrow(858,909,858,985,GREEN)
    c.arrow(1025,905,1025,985,GREEN)

    concrete(1180,850,190,"PriorityQueue",17)
    concrete(1400,850,220,"ArrayDeque",17)
    concrete(1290,985,190,"LinkedList",17)
    c.arrow(1315,744,1275,850,GREEN)
    c.arrow(1565,744,1510,850,GREEN)
    contract_path([(1605,585),(1650,585),(1650,872),(1620,872)])
    contract_path([(1295,585),(1135,585),(1135,1012),(1290,1012)])

    concrete(1685,850,135,"HashMap",16)
    concrete(1830,850,135,"TreeMap",16)
    concrete(1685,985,155,"LinkedHashMap",15)
    legacy(1845,985,125,"Hashtable",15)
    c.arrow(1790,744,1752,850,GREEN)
    c.arrow(1880,744,1897,850,GREEN)
    c.arrow(1752,905,1752,985,GREEN)
    contract_path([(1970,308),(1990,308),(1990,1012),(1970,1012)])

    c.text(60,1140,"Синие стрелки: интерфейс extends интерфейс. Зелёные: наследование классов.",17,color=MUTED)
    c.text(60,1173,"Серый пунктир: класс реализует контракт. Показаны основные связи; часть опущена. LinkedList показан дважды.",17,color=MUTED)
    c.save("framework-hierarchy")


def roles():
    c=Canvas(1240,540,"Какие задачи возникли с университетскими данными?","Вопросы сформулированы до выбора интерфейса и реализации.")
    c.box(410,115,420,62,"Студенты · группы · заявки",BLUE_PALE,BLUE,22,True)
    cards=[
        (40,"Запись на занятие",["Иван записался дважды.","Как сохранить обе записи","и их порядок?"]),
        (340,"Группы студентов",["Иван и Анна в одной группе.","Как показать каждую","группу только раз?"]),
        (640,"Поиск по ID",["Есть ID студента.","Как найти его карточку","без полного перебора?"]),
        (940,"Очередь заявок",["Заявки идут одна за другой.","Какую обработать","следующей?"]),
    ]
    for x,title,lines in cards:
        c.box(x,265,260,175,fill=GREEN_PALE,stroke=GREEN)
        c.text(x+130,306,title,19,bold=True,anchor="middle")
        for j,line in enumerate(lines):
            c.text(x+130,348+j*28,line,16,anchor="middle")
        c.arrow(620,177,x+130,265,GREEN)
    c.save("framework-roles")


def map_concept():
    c=Canvas(1100,570,"Map: ключ ведёт к значению","Здесь показаны связи, а не корзины HashMap или расположение объектов в памяти.")
    c.text(240,130,"Ключи: ID",21,bold=True,anchor="middle")
    c.text(835,130,"Значения: карточки Student",21,bold=True,anchor="middle")
    rows=[(170,"ID 1","Иван","И"),(310,"ID 2","Анна","А")]
    for top,key,name,initial in rows:
        c.box(95,top,290,95,key,BLUE_PALE,BLUE,24,True)
        c.arrow(390,top+47,600,top+47,GREEN,3)
        c.box(610,top,420,95,fill=GREEN_PALE,stroke=GREEN)
        c.d.add(Circle(660,c.h-(top+47),29,fillColor=GREEN,strokeColor=None))
        c.text(660,top+55,initial,23,color=WHITE,bold=True,anchor="middle")
        c.text(835,top+55,name,21,bold=True,anchor="middle")
    c.text(90,475,"У каждого ключа одно текущее значение; разные ключи могут ссылаться на одно значение.",19,color=MUTED)
    c.save("map-key-value")


def queue_fifo_lifo():
    c=Canvas(1100,790,"Очередь FIFO и стек LIFO","Один Deque поддерживает оба способа; поведение задают выбранные операции.")
    c.text(65,125,"FIFO · очередь заявок",23,bold=True)
    c.text(65,165,"Первым добавили → первым извлекли",18,color=MUTED)
    for i,name in enumerate(["Иван","Анна"]):
        c.box(350+i*220,215,190,78,name,BLUE_PALE,BLUE,21)
    c.arrow(335,254,90,254,GREEN,3)
    c.text(100,320,"pollFirst()",18,color=GREEN,bold=True)
    c.arrow(930,254,745,254,BLUE,3)
    c.text(810,320,"offerLast()",18,color=BLUE,bold=True)
    c.text(550,365,"голова слева · хвост справа",18,color=MUTED,anchor="middle")

    c.line(55,405,1045,405,PALE)
    c.text(65,450,"LIFO · стек действий",23,bold=True)
    c.text(65,600,"Последним положили → первым извлекли",18,color=MUTED)
    for i,name in enumerate(["Анна","Иван"]):
        c.box(445,475+i*67,220,58,name,GREEN_PALE,GREEN,20)
    c.arrow(880,500,650,500,BLUE,3)
    c.text(860,535,"push()",18,color=BLUE,bold=True)
    c.arrow(430,500,270,500,GREEN,3)
    c.text(270,535,"pop()",18,color=GREEN,bold=True)
    c.text(555,700,"push и pop работают с одним концом: верхний элемент сейчас Анна.",18,color=MUTED,anchor="middle")
    c.save("queue-fifo-lifo")


def iterable_iterator():
    c=Canvas(1100,560,"Iterable даёт Iterator для обхода","* remove() может не поддерживаться; Iterator не копирует коллекцию.")
    c.box(55,145,320,90,fill=BLUE_PALE,stroke=BLUE)
    c.text(215,180,"registrations : List<Student>",19,bold=True,anchor="middle")
    c.text(215,210,"также Iterable<Student>",17,color=MUTED,anchor="middle")
    c.arrow(380,190,510,190,BLUE,3)
    c.text(445,165,"iterator()",18,color=BLUE,bold=True,anchor="middle")
    c.box(525,145,350,90,fill=GREEN_PALE,stroke=GREEN)
    c.text(700,180,"Iterator<Student>",21,bold=True,anchor="middle")
    c.text(700,210,"hasNext() · next() · remove()*",17,color=MUTED,anchor="middle")
    c.text(110,300,"Последовательность элементов",20,bold=True)
    for i,name in enumerate(["Иван","Анна","Иван"]):
        c.box(110+i*280,330,245,75,name,BLUE_PALE,BLUE,21)
    c.arrow(372,475,372,410,GREEN,3)
    c.text(372,505,"позиция перед следующим элементом",18,color=GREEN,bold=True,anchor="middle")
    c.save("iterable-iterator")


def list_semantics():
    c=Canvas(1100,520,"List: позиция и повторная ссылка","После удаления позиции индексы меняются; объекты Student не копируются.")
    c.text(80,130,"До remove(0)",21,bold=True)
    for i,name in enumerate(["Иван","Анна","Иван"]):
        x=80+i*250
        c.box(x,165,220,80,name,BLUE_PALE,BLUE,21)
        c.text(x+110,275,f"индекс {i}",17,MUTED,anchor="middle")
    c.text(875,220,"0 и 2 →",18,color=GREEN,bold=True)
    c.text(875,250,"один Student",18,color=GREEN,bold=True)
    c.arrow(460,300,460,335,GREEN)
    c.text(80,365,"После remove(0):",21,bold=True)
    c.box(360,335,220,80,"Анна",GREEN_PALE,GREEN,21)
    c.box(610,335,220,80,"Иван",GREEN_PALE,GREEN,21)
    c.text(470,440,"индекс 0",17,MUTED,anchor="middle")
    c.text(720,440,"индекс 1",17,MUTED,anchor="middle")
    c.save("list-semantics")


def map_put():
    c=Canvas(1100,450,"Map.put: повторный ключ заменяет значение","Ключей остаётся два; Map не проверяет согласованность ID студента и ключа.")
    c.text(75,135,"До put(2, Иван)",21,bold=True)
    c.box(75,165,335,65,"1 → Иван",BLUE_PALE,BLUE)
    c.box(75,245,335,65,"2 → Анна",BLUE_PALE,BLUE)
    c.arrow(450,237,625,237,GREEN,3)
    c.text(770,135,"После",21,bold=True)
    c.box(660,165,335,65,"1 → Иван",GREEN_PALE,GREEN)
    c.box(660,245,335,65,"2 → Иван",GREEN_PALE,GREEN)
    c.text(550,370,"size() = 2; put вернул прежнюю Анну",20,color=GREEN,bold=True,anchor="middle")
    c.save("map-put")


def iterator_view():
    c=Canvas(1100,480,"Обход: курсор и представление Map","Итератор не копирует коллекцию; entrySet связан с исходной Map.")
    c.text(80,130,"Iterator над List",21,bold=True)
    for i,name in enumerate(["Иван","Анна","Иван"]):
        c.box(80+i*200,165,175,68,name,BLUE_PALE,BLUE,19)
    c.arrow(280,275,280,235,GREEN)
    c.text(280,310,"next() → Анна",18,color=GREEN,bold=True,anchor="middle")
    c.text(280,342,"remove() удалит последнюю выданную",17,color=MUTED,anchor="middle")
    c.text(825,130,"Map и её представление",21,bold=True,anchor="middle")
    c.box(690,170,260,62,"Map: 1→Иван, 2→Иван",BLUE_PALE,BLUE,18)
    c.arrow(820,232,820,275,GREEN)
    c.box(690,275,260,62,"entrySet(): пары",GREEN_PALE,GREEN,18)
    c.text(820,380,"Удаление связи видно в обоих",17,color=MUTED,anchor="middle")
    c.save("iterator-map-view")


def asymptotic_bridge():
    c=Canvas(1100,590,"Как растёт работа с коллекцией","Условное число шагов на одной шкале; это не замеры времени Java.")
    c.text(55,125,"Увеличиваем число элементов n → смотрим, сколько действий понадобится.",19,bold=True)

    x0,y0=100,520
    c.arrow(x0,y0,610,y0,LINE,2)
    c.arrow(x0,y0,x0,230,LINE,2)
    c.text(615,527,"n",18,bold=True)
    c.text(47,230,"шаги",16,color=MUTED)
    c.text(100,548,"0",15,color=MUTED,anchor="middle")
    c.text(520,548,"6",15,color=MUTED,anchor="middle")
    for func,color in [
        (lambda n:1,BLUE),
        (lambda n:n,GREEN),
        (lambda n:n*n,LINE),
    ]:
        points=[(x0+70*n,y0-7*func(n)) for n in range(0,7)]
        for (x1,t1),(x2,t2) in zip(points,points[1:]):
            c.line(x1,t1,x2,t2,color,3)
    c.text(552,496,"1",18,color=BLUE,bold=True)
    c.text(552,466,"n",18,color=GREEN,bold=True)
    c.text(552,272,"n²",18,color=MUTED,bold=True)

    examples=[
        (230,BLUE_PALE,BLUE,"O(1) · ArrayList.get(i)","модель: одна ячейка при любом n"),
        (335,GREEN_PALE,GREEN,"O(n) · ArrayList.contains(x)","худший случай: n → 2n сравнений"),
        (440,WHITE,LINE,"O(n²) · n поисков в ArrayList","худший случай: n² → 4n² сравнений"),
    ]
    for t,fill,stroke,title,note in examples:
        c.box(680,t,370,82,fill=fill,stroke=stroke)
        c.text(700,t+30,title,19,bold=True)
        c.text(700,t+62,note,17,color=MUTED)
    c.save("asymptotic-growth")


def asymptotic_bridge_detailed():
    """Preserved illustration for the archived, more mathematical lecture block."""
    c=Canvas(1100,590,"От размера коллекции к асимптотике")
    c.box(45,110,250,76,"Размер n",BLUE_PALE,BLUE,21,True)
    c.arrow(305,148,390,148,BLUE,3)
    c.box(400,110,300,76,"Действия T(n) = 3n + 5",BLUE_PALE,BLUE,19,True)
    c.arrow(710,148,795,148,GREEN,3)
    c.box(805,110,250,76,"Рост: Θ(n)",GREEN_PALE,GREEN,21,True)
    c.text(55,219,"Учебная модель линейного поиска: не точный счёт инструкций Java.",18,color=MUTED)
    x0,y0=110,525
    c.arrow(x0,y0,620,y0,LINE,2)
    c.arrow(x0,y0,x0,270,LINE,2)
    c.text(635,532,"n",18,bold=True)
    c.text(61,270,"действия",16,color=MUTED)
    for func,color in [(lambda n:3*n+5,BLUE),(lambda n:8*n,GREEN),(lambda n:n*n,LINE)]:
        points=[(x0+49*n,y0-2.45*func(n)) for n in range(1,11)]
        for (x1,t1),(x2,t2) in zip(points,points[1:]):
            c.line(x1,t1,x2,t2,color,3)
    c.text(505,428,"T(n)",17,color=BLUE,bold=True)
    c.text(535,365,"8n",17,color=GREEN,bold=True)
    c.text(525,285,"n²",17,color=MUTED,bold=True)
    c.text(159,552,"n = 1",15,color=MUTED,anchor="middle")
    c.text(600,552,"n = 10",15,color=MUTED,anchor="middle")
    c.box(685,278,365,105,fill=BLUE_PALE,stroke=BLUE)
    c.text(707,312,"Большое O: верхняя граница",19,bold=True)
    c.text(707,350,"3n + 5 ≤ 8n при n ≥ 1",19)
    c.box(685,405,365,105,fill=GREEN_PALE,stroke=GREEN)
    c.text(707,439,"Малое o: строго меньший рост",19,bold=True)
    c.text(707,477,"T(n) / n² → 0 при n → ∞",19)
    c.save("asymptotic-growth-detailed")


def arraylist():
    c=Canvas(1100,590,"ArrayList: размер, ёмкость и сдвиг","Учебная ёмкость 6; точная начальная ёмкость реализацией не обещана.")
    c.text(55,120,"До вставки: size = 3, capacity = 6",21,bold=True)
    names=["Иван","Анна","Олег","свободно","свободно","свободно"]
    for i,n in enumerate(names):
        c.box(55+i*165,150,150,72,n,BLUE_PALE if i<3 else WHITE,BLUE if i<3 else PALE,19)
        c.text(130+i*165,244,str(i),17,MUTED,anchor="middle")
    c.arrow(55+165+75,270,55+165+75,222,GREEN)
    c.text(300,300,"get(1): сразу ячейка 1 → O(1)",20,color=GREEN,bold=True)
    c.text(55,370,"add(1, Лена): сначала сдвигаем Анну и Олега вправо",20,bold=True)
    after=["Иван","Лена","Анна","Олег","свободно","свободно"]
    for i,n in enumerate(after):
        c.box(55+i*165,405,150,72,n,GREEN_PALE if i==1 else BLUE_PALE if i<4 else WHITE,GREEN if i==1 else BLUE if i<4 else PALE,19)
    c.text(55,525,"Передвинуто n − i ссылок; сами объекты Student не копируются.",19,color=MUTED)
    c.save("arraylist-operations")


def linkedlist():
    c=Canvas(1100,500,"LinkedList: узлы и поиск позиции","Узлы могут лежать в разных местах памяти; линия показывает ссылку, не соседство адресов.")
    labels=["Иван","Анна","Олег"]
    for i,x in enumerate([120,440,760]):
        c.box(x,175,220,95,fill=BLUE_PALE,stroke=BLUE)
        c.line(x+58,175,x+58,270,PALE)
        c.line(x+162,175,x+162,270,PALE)
        c.text(x+110,230,labels[i],21,bold=True,anchor="middle")
        c.text(x+28,230,"prev",14,MUTED,anchor="middle")
        c.text(x+191,230,"next",14,MUTED,anchor="middle")
    c.arrow(230,112,230,173)
    c.text(230,95,"first",17,color=BLUE,anchor="middle")
    c.arrow(870,112,870,173)
    c.text(870,95,"last",17,color=BLUE,anchor="middle")
    for a,b in [(340,440),(660,760)]:
        c.arrow(a,203,b,203,GREEN)
        c.arrow(b,248,a,248,GREEN)
    c.text(90,350,"get(i): переходы от ближайшего конца → до O(n)",21,bold=True)
    c.text(90,396,"Вставка у найденного узла: меняем несколько ссылок → O(1)",21,bold=True)
    c.text(90,442,"add(i, e) в середине: сначала ищем узел → O(n) целиком",21,color=GREEN,bold=True)
    c.save("linkedlist-nodes")


def hashmap_lookup():
    c=Canvas(1100,600,"HashMap: корзины, коллизия, проверка ключа","Игрушечная модель: index = hash mod 4. OpenJDK 21 вычисляет индекс иначе.")
    c.box(55,130,220,58,"get(5)",GREEN_PALE,GREEN,bold=True)
    c.arrow(275,159,365,159,GREEN)
    c.box(365,130,270,58,"hash → корзина 1",BLUE_PALE,BLUE)
    c.text(80,250,"Массив корзин",20,bold=True)
    for i in range(4):
        c.box(80,275+i*60,150,49,f"{i}",WHITE,LINE,19)
    c.arrow(230,359,365,359,BLUE)
    c.box(365,327,230,65,"1 → Иван",BLUE_PALE,BLUE)
    c.text(480,420,"1 ≠ 5",17,color=MUTED,anchor="middle")
    c.arrow(595,359,655,359,BLUE)
    c.box(655,327,230,65,"5 → Анна",GREEN_PALE,GREEN)
    c.text(770,430,"equals(5, 5)",18,color=GREEN,anchor="middle")
    c.text(80,530,"Коллизия: разные ключи попали в одну корзину. Поиск проверяет записи внутри неё.",19,color=MUTED)
    c.save("hashmap-lookup")


def hashmap_resize():
    c=Canvas(1100,630,"HashMap: расширение и перераспределение","Игрушечная модель: index = hash mod capacity; порог 3 при capacity 4.")
    c.text(70,120,"До: 3 записи, capacity = 4",21,bold=True)
    c.text(610,120,"После put(3): 4 записи, capacity = 8",21,bold=True)
    before={0:"—",1:"1, 5",2:"2",3:"—"}
    after={0:"—",1:"1",2:"2",3:"3",4:"—",5:"5",6:"—",7:"—"}
    for i in range(4):
        c.box(70,155+i*75,330,58,f"{i}: {before[i]}",BLUE_PALE if i in (1,2) else WHITE,BLUE if i in (1,2) else PALE,19)
    for i in range(8):
        c.box(650,145+i*48,310,38,f"{i}: {after[i]}",GREEN_PALE if i in (1,2,3,5) else WHITE,GREEN if i in (1,2,3,5) else PALE,17)
    c.arrow(405,305,625,305,GREEN,3)
    c.text(515,280,"O(m) за один resize",18,color=GREEN,bold=True,anchor="middle")
    c.text(70,570,"Ключи 1 и 5 после роста попали в разные корзины; старые записи надо перенести.",19,color=MUTED)
    c.save("hashmap-resize")


def hashset():
    c=Canvas(1100,390,"HashSet: элемент становится ключом Map","Два равных UniversityGroup дают одну запись; служебное значение не видно пользователю.")
    c.box(60,150,365,95,"Set<UniversityGroup>",BLUE_PALE,BLUE,bold=True)
    c.text(242,290,"{ «24.Б11-мм» }",20,anchor="middle")
    c.arrow(435,197,580,197,GREEN,3)
    c.box(590,125,440,145,fill=GREEN_PALE,stroke=GREEN)
    c.text(810,175,"HashMap внутри",22,bold=True,anchor="middle")
    c.text(810,220,"ключ: группа   →   значение: PRESENT",19,anchor="middle")
    c.save("hashset-map")


def arraydeque():
    c=Canvas(1100,850,"ArrayDeque: переход через край и расширение")
    c.text(55,113,"Индексы идут по кругу: 0 → 1 → 2 → 3 → 0",20,bold=True)

    def cells(values, x, top, step, width, head=None, tail=None, show_status=True):
        for i,value in enumerate(values):
            active=value!="·"
            c.box(x+i*step,top,width,58,value if active else "пусто",
                  BLUE_PALE if i==head else GREEN_PALE if active else WHITE,
                  BLUE if i==head else GREEN if active else PALE,
                  21 if active else 15,active)
            c.text(x+i*step+width/2,top+83,str(i),16,color=MUTED,anchor="middle")
        if head is not None and show_status:
            c.text(55,top+37,f"head = {head}",18,color=BLUE,bold=True)
        if tail is not None and show_status:
            c.text(55,top+66,f"tail = {tail}",18,color=GREEN,bold=True)

    c.text(55,155,"1. До добавления: порядок A → B → C",21,bold=True)
    cells(["B","C","·","A"],410,185,125,110,head=3,tail=2)
    c.text(410,293,"A стоит в ячейке 3; после неё читаем ячейку 0.",18,color=MUTED)
    c.arrow(550,307,550,340,GREEN,3)
    c.text(590,336,"offerLast(D) записывает D в ячейку 2",18,color=GREEN,bold=True)

    c.text(55,374,"2. На мгновение внутри offerLast: свободных ячеек нет",20,bold=True)
    cells(["B","C","D","A"],410,399,125,110,head=3)
    c.text(410,504,"head = tail = 3 → запускается grow",18,color=MUTED)
    c.arrow(550,518,550,549,GREEN,3)
    c.text(590,545,"новый массив и перенос ссылки на A",18,color=GREEN,bold=True)

    c.text(55,580,"3. После расширения: порядок всё ещё A → B → C → D",20,bold=True)
    cells(["B","C","D","·","·","·","·","·","·","A"],70,610,98,87,head=9,tail=3,show_status=False)
    c.text(70,725,"head = 9 (A), tail = 3 (пусто). Логический порядок сохранился.",18,color=MUTED)
    c.text(70,755,"Массив: 4 → 10 ячеек; A: индекс 3 → 9. B, C, D остались на местах.",18,color=MUTED)
    c.text(55,810,"Трассировка OpenJDK 21; точный размер массива и размещение — не контракт Deque.",17,color=MUTED)
    c.save("arraydeque-ring")


for fn in [roles,hierarchy,map_concept,queue_fifo_lifo,iterable_iterator,list_semantics,map_put,iterator_view,asymptotic_bridge,asymptotic_bridge_detailed,arraylist,linkedlist,hashmap_lookup,hashmap_resize,hashset,arraydeque]:
    fn()
