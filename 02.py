import random
import tkinter as tk
import sqlite3

class RegisterPage:
    def __init__(self, master):
        self.master = master
        master.title("注册")
        master.geometry("400x300")  # 设置窗口大小

        self.label_username = tk.Label(master, text="用户名：", font=("Helvetica", 14))
        self.label_username.pack()

        self.entry_username = tk.Entry(master, font=("Helvetica", 14))
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="密码：", font=("Helvetica", 14))
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*", font=("Helvetica", 14))
        self.entry_password.pack()

        self.button_register = tk.Button(master, text="注册", command=self.register, font=("Helvetica", 14))
        self.button_register.pack()

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # 在这里添加注册逻辑，例如将用户名和密码保存到数据库
        conn = sqlite3.connect('users.db')  # 连接到数据库，如果数据库不存在，会自动创建
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, password TEXT)''')  # 创建一个表来存储用户信息
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))  # 插入用户信息
        conn.commit()  # 提交更改
        conn.close()  # 关闭连接

        print(f"注册成功！用户名：{username}，密码：{password}")

        # 注册成功后，关闭注册窗口并显示登录窗口
        self.master.destroy()
        root = tk.Tk()
        login_page = LoginPage(root)
        root.mainloop()

class LoginPage:
    def __init__(self, master):
        self.master = master
        master.title("登录")
        master.geometry("400x300")  # 设置窗口大小

        self.label_username = tk.Label(master, text="用户名：", font=("Helvetica", 14))
        self.label_username.pack()

        self.entry_username = tk.Entry(master, font=("Helvetica", 14))
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="密码：", font=("Helvetica", 14))
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*", font=("Helvetica", 14))
        self.entry_password.pack()

        self.button_login = tk.Button(master, text="登录", command=self.login, font=("Helvetica", 14))
        self.button_login.pack()

        self.button_register = tk.Button(master, text="注册", command=self.show_register_page, font=("Helvetica", 14))
        self.button_register.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # 在这里添加验证逻辑，例如检查用户名和密码是否正确
        conn = sqlite3.connect('users.db')  # 连接到数据库
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username =? AND password =?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            self.master.destroy()  # 关闭登录窗口
            root = tk.Tk()
            my_game = GuessNumberGame(root)
            root.mainloop()
        else:
            self.result_label.config(text="用户名或密码错误！")

    def show_register_page(self):
        self.master.destroy()
        root = tk.Tk()
        register_page = RegisterPage(root)
        root.mainloop()

class GuessNumberGame:
    def __init__(self, master):
        self.master = master
        master.title("猜数字游戏")
        master.geometry("800x600")  # 设置窗口大小

        self.number = random.randint(1, 100)
        self.attempts = 0

        # 使用字体参数来增大字体
        self.label = tk.Label(master, text="请猜一个1到100之间的数字：", font=("Helvetica", 14))
        self.label.pack()

        self.entry = tk.Entry(master, font=("Helvetica", 14))
        self.entry.pack()

        self.button = tk.Button(master, text="猜", command=self.guess, font=("Helvetica", 14))
        self.button.pack()

        self.result_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.result_label.pack()

    def guess(self):
        guess = int(self.entry.get())
        self.attempts += 1

        if guess < self.number:
            self.result_label.config(text="猜的数字太小了！")
        elif guess > self.number:
            self.result_label.config(text="猜的数字太大了！")
        else:
            self.result_label.config(text=f"恭喜你，你简直是个废物，猜对了！你一共猜了{self.attempts}次。")
            self.entry.config(state="disabled")
            self.button.config(state="disabled")

root = tk.Tk()
login_page = LoginPage(root)
root.mainloop()

