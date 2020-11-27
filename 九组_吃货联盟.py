#!/usr/bin/python3
import time
# 面向对象方式
class Order(object): #创建订单项类
    def __init__(self, id, name, num, price, date, owner, address, state): #初始化()
        self.id = id
        self.name = name
        self.num = num
        self.price = float(price)
        self.date = date
        self.owner = owner
        self.address = address
        self.state = state
class Orders(object): #创建订单类
    order_list = [] #订单项集合
    def __add__(self, id, name, num, price, date, owner, address, state): #为订单增加订单项
        self.order_list.append(Order(id, name, num, price, date, owner, address, state))
    def __init__(self): #初始化()
        order = Order("1000", "红烧肉", 1, 30, str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), "旺财", "川电机", "送餐") #获取此线程当前时间
        self.order_list.append(order)
    def __show__(self): #展示所有订单项
        print("宝宝餐厅的订单：\n订餐编号\t\t|菜名\t\t|订餐时间\t\t\t\t\t|份数\t|总价格\t\t|订餐人\t\t|地址\t\t|订单状态")
        if len(self.order_list)==0:
            print(">当前无订单<")
        for i in self.order_list:
            print("{}\t\t{}\t\t{}\t\t{}\t\t{}￥\t\t{}\t\t\t{}\t\t{}".format(i.id, i.name, i.date, int(i.num), i.price, i.owner, i.address, i.state))
    def __cancel__(self): #取消订单
        id = input("请输入订单编号：")
        index = 0
        for i in self.order_list:
            if(i.id == id):
                del self.order_list[index]
            index += 1
    def __send__(self): #完成订单
        id = input("请输入订单编号：")
        index = 0
        for i in self.order_list:
            if(i.id == id):
                i.state = "完成"
            index += 1
class Food(object):
    def __init__(self, name, price): #新增菜品()
        self.name = name
        self.price = float(price)
class Menu(object):
    menu_food = []
    def __init__(self): #初始化()
        food_init = ["红烧肉", 30, "小丸子汤", 20, "宝宝橙汁", 10]
        self.menu_food.append(Food(food_init[0], food_init[1]))
        self.menu_food.append(Food(food_init[2], food_init[3]))
        self.menu_food.append(Food(food_init[4], food_init[5]))
    def __add__(self, name, price): #新增菜品
        self.menu_food.append(Food(name, price))
    def __show__(self): #展示菜单
        for i in self.menu_food:
            print("{}\t\t{}".format(i.name, i.price))
def Judge(str):
    if str>='0' and str<='6' and len(str)==1:
        return True
def get_Price(name, num, menu): #价格计算器
    for i in menu.menu_food:
        if(i.name==name):
            return i.price*num
def Exit(*key): #统一返回函数()
    if key: #如果输入错误则在此前加上输入错误的字符串
        print(key[0], end="")
    print("输入任意键返回","。"*7)
    input()
    return
def Order_Cancel(orders): #取消订单项
    orders.__show__()
    orders.__cancel__()
    print(">订单取消成功<")
    Exit()
def Menu_Show(menu): #显示菜单
    print("宝宝餐厅的菜单")
    menu.__show__()
    Exit()
def Menu_Add(menu): #新增菜品
    name = input("请输入菜名：")
    price = input("请输入价格：")
    menu.__add__(name, price)
    print(">新增成功<")
    Exit()
def Order_Show(orders): #展示所有订单项
    orders.__show__()
    Exit()
def Order_Add(orders, menu): #增加订单项
    id = input("请输入订单编号：")
    try:
        while True:
            name = input("请输入菜名：")
            for i in menu.menu_food:
                if i.name == name:
                    break
            flag = input("无此菜品，是否增加？(y/n)")
            if flag=="y":
                price = input("请输入价格：")
                menu.__add__(name, price)
                print(">新增成功<")
                raise
            else: Exit()
    except: pass
    num = float(input("请输入份数："))
    price = get_Price(name, num, menu)
    date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    owner = input("请输入订餐人姓名：")
    address = input("请输入送餐地址：")
    state = "送餐"
    orders.__add__(id, name, num, price, date, owner, address, state)
    print(">订餐成功<")
    Exit()
def Order_Send(orders): #设置送餐
    orders.__send__()
    print(">送餐成功<")
    Exit()
def main(): #主方法,从这里开始
    menu = Menu() #创建菜单对象
    orders = Orders() #创建总订单对象
    dict = {"1": "Menu_Show(menu)", "2":"Menu_Add(menu)", "3":"Order_Show(orders)", "4":"Order_Add(orders, menu)", "5":"Order_Send(orders)", "6":"Order_Cancel(orders)", "0":"exit('谢谢使用宝宝订餐系统')"}
    while True:
        print("*"*6,"宝宝餐厅订餐系统", "*"*6, "\n1、查看菜单\n2、新增菜单\n3、查看订单\n4、订餐\n5、送餐\n6、取消订单\n0、退出系统\n请选择操作【0-6】:", end="")
        str = input()
        eval(dict[str]) if Judge(str) else Exit("输入错误，")
if __name__ == '__main__': #禁止其它文件调用该模块
    main()