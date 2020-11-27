#!/usr/bin/python3
import time
import pymysql
# 吃货联盟订餐系统Mysql版, 需要提前创建数据库[restaurant], 修改登录信息在[96]行
# 完善和新增了更多内容
class Order(object): #创建订单项类
    def __init__(self, id, name, num, price, date, owner, address, state): #初始化()
        self.id = id
        self.name = name
        self.num = num
        self.price = price
        self.date = date
        self.owner = owner
        self.address = address
        self.state = state
class Orders(object): #创建订单类
    order_list = [] #订单项集合
    def __add__(self, id, name, num, price, date, owner, address, state, cursor): #为订单增加订单项
        self.order_list.append(Order(id, name, num, price, date, owner, address, state))
        data = [id, name, num, price, date, owner, address, state]
        sql = 'INSERT INTO ORDERS(id, name, num, price, date, owner, address, state)VALUES{}'.format(tuple(data))
        cursor.execute(sql)
    def __init__(self, cursor): #初始化()
        data = ["1000", "红烧肉", 1.0, 30.0, str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), "旺财", "川电机", "送餐"]
        order = Order(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        self.order_list.append(order)
        sql = """CREATE TABLE ORDERS(
                        ID CHAR(20) NOT NULL,
                        NAME CHAR(20),
                        NUM FLOAT,
                        PRICE FLOAT,
                        DATE CHAR(20),
                        OWNER CHAR(20),
                        ADDRESS CHAR(20),
                        STATE CHAR(20)
                        )
                        """
        sql1 = 'insert into ORDERS(id, name, num, price, date, owner, address, state)VALUES{}'.format(tuple(data))
        cursor.execute("DROP TABLE IF EXISTS ORDERS")
        cursor.execute(sql)
        cursor.execute(sql1)
    def __show__(self): #展示所有订单项
        print("宝宝餐厅的订单：\n订餐编号\t\t|菜名\t\t|订餐时间\t\t\t\t\t|份数\t|总价格\t\t|订餐人\t\t|地址\t\t|订单状态")
        if len(self.order_list)==0:
            print(">当前无订单<")
        else:
            for i in self.order_list:
                print("{}\t\t{}\t\t{}\t\t{}\t\t{}￥\t\t{}\t\t\t{}\t\t{}".format(i.id, i.name, i.date, int(i.num), i.price, i.owner, i.address, i.state))
    def __cancel__(self, cursor): #取消订单
        id = input("请输入订单编号：")
        index = 0
        for i in self.order_list:
            if(i.id == id):
                del self.order_list[index]
                sql = "DELETE FROM ORDERS WHERE ID=%s"
                cursor.execute(sql, i.id)
            index += 1
    def __send__(self, cursor): #完成订单
        id = input("请输入订单编号：")
        index = 0
        for i in self.order_list:
            if(i.id == id):
                i.state = "完成"
                sql = "UPDATE ORDERS SET STATE=%s WHERE ID=%s"
                cursor.execute(sql, ['完成', i.id])
            index += 1
class Food(object):
    def __init__(self, name, price): #初始化()
        self.name = name
        self.price = float(price)
class Menu(object):
    menu_food = []
    def __init__(self, cursor, db): #初始化()
        food_name = ["红烧肉", "小丸子汤", "宝宝橙汁"]
        food_price = [30, 20, 10]
        self.menu_food.append(Food(food_name[0], food_price[0]))
        self.menu_food.append(Food(food_name[1], food_price[1]))
        self.menu_food.append(Food(food_name[2], food_price[2]))
        data=((food_name[i], food_price[i]) for i in range(0,len(food_name)))
        sql = """CREATE TABLE MENU(
                NAME CHAR(20) NOT NULL,
                PRICE FLOAT)
                """
        sql1 = 'insert into menu values(%s,%s)'
        cursor.execute("DROP TABLE IF EXISTS MENU")
        cursor.execute(sql)
        cursor.executemany(sql1, data)
    def __add__(self, name, price, cursor): #新增菜品
        self.menu_food.append(Food(name, price))
        sql = "insert into menu(name, price)VALUES{}".format(tuple([name, price]))
        cursor.execute(sql)
    def __show__(self): #展示菜单
        for i in self.menu_food:
            print("{}\t\t{}".format(i.name, i.price))
def database_connect():
    db = pymysql.connect("localhost", "root", "123456", "restaurant", charset='utf8', autocommit =True) # 打开数据库连接
    cursor = db.cursor() # 使用 cursor() 方法创建一个游标对象 cursor
    print(">数据库已连接<")
    return cursor, db
def get_Price(name, num, menu): #价格计算器
    for i in menu.menu_food:
        if(i.name==name):
            return i.price*num
def Judgement(str):
    if('0'<=str and str<='6' and len(str)==1):
        return True
    return False
def Exit(): #统一返回函数()
    print("输入任意键返回","。"*7)
    input()
    return
def Order_Cancel(orders, cursor): #取消订单项
    orders.__show__()
    orders.__cancel__(cursor)
    print(">订单取消成功<")
    Exit()
def Menu_Show(menu): #显示菜单
    print("*"*6, "宝宝餐厅的菜单", "*"*6)
    menu.__show__()
    Exit()
def Menu_Add(menu, cursor): #新增菜品
    name = input("请输入菜名：")
    price = input("请输入价格：")
    menu.__add__(name, price, cursor)
    print(">新增成功<")
    Exit()
def Order_Show(orders): #展示所有订单项
    orders.__show__()
    Exit()
def Order_Add(orders, menu, cursor): #增加订单项
    id = input("请输入订单编号：")
    try:
        while True:
            name = input("请输入菜名：")
            for i in menu.menu_food:
                if(i.name == name):
                    raise
            flag = input("无此菜品，是否增加？(y/n)")
            if flag=="y":
                price = input("请输入价格：")
                menu.__add__(name, price, cursor)
                print(">新增成功<")
                raise
            else:
                Exit()
    except: pass
    num = float(input("请输入份数："))
    price = get_Price(name, num, menu)
    date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    owner = input("请输入订餐人姓名：")
    address = input("请输入送餐地址：")
    state = "送餐"
    orders.__add__(id, name, num, price, date, owner, address, state, cursor)
    print(">订餐成功<")
    Exit()
def Order_Send(orders, cursor): #设置送餐
    orders.__show__()
    orders.__send__(cursor)
    print(">送餐成功<")
    Exit()
def main(): #主方法
    cursor, db = database_connect() #游标对象
    menu = Menu(cursor, db) #创建菜单对象
    orders = Orders(cursor) #创建订单对象
    dict = {"1": "Menu_Show(menu)", "2":"Menu_Add(menu, cursor)", "3":"Order_Show(orders)", "4":"Order_Add(orders, menu, cursor)", "5":"Order_Send(orders, cursor)", "6":"Order_Cancel(orders, cursor)", "0":"exit('>谢谢使用宝宝订餐系统<')"}
    while True:
        print("*"*6,"宝宝餐厅订餐系统", "*"*6, "\n1、查看菜单\n2、新增菜单\n3、查看订单\n4、订餐\n5、送餐\n6、取消订单\n0、退出系统\n请选择操作【0-6】:", end="")
        jud_num = input()
        if Judgement(jud_num):
            eval(dict[jud_num]) #eval()函数字符串转执行操作
        else:
            print("请输入0-6的数字")
            Exit()
if __name__ == '__main__': #禁止其它文件调用该模块
    main()