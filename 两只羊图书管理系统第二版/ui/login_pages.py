import tkinter as tk
from tkinter import messagebox
from ui.base_frame import BaseFrame

class LoginPage(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        # 登录界面组件
        tk.Label(self.frame, text="两只羊图书管理系统", font=("SimHei", 24)).pack(pady=30)
        
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="用户名:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(input_frame, font=("SimHei", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="密码:", font=("SimHei", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(input_frame, show="*", font=("SimHei", 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="登录", command=self.login, font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="注册", command=lambda: self.app.show_page("register"), font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("登录失败", "用户名和密码不能为空！")
            return
            
        if self.app.data_manager.validate_user(username, password):
            self.app.current_user = username
            if self.app.data_manager.is_admin(username):
                self.app.show_page("admin_menu")
            else:
                self.app.show_page("user_menu")
        else:
            messagebox.showerror("登录失败", "用户名或密码错误！")

class RegisterPage(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        # 注册界面组件
        tk.Label(self.frame, text="用户注册", font=("SimHei", 24)).pack(pady=30)
        
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="用户名:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.register_username_entry = tk.Entry(input_frame, font=("SimHei", 12))
        self.register_username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="密码:", font=("SimHei", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.register_password_entry = tk.Entry(input_frame, show="*", font=("SimHei", 12))
        self.register_password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="确认密码:", font=("SimHei", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.register_confirm_entry = tk.Entry(input_frame, show="*", font=("SimHei", 12))
        self.register_confirm_entry.grid(row=2, column=1, padx=10, pady=10)
        
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="注册", command=self.register, font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.app.show_page("login"), font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
    
    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm = self.register_confirm_entry.get()
        
        if not username or not password:
            messagebox.showerror("注册失败", "用户名和密码不能为空！")
            return
            
        if self.app.data_manager.user_exists(username):
            messagebox.showerror("注册失败", "用户名已存在！")
            return
            
        if password != confirm:
            messagebox.showerror("注册失败", "两次输入的密码不一致！")
            return
            
        # 添加用户
        self.app.data_manager.add_user(username, password, "user")
        messagebox.showinfo("注册成功", "用户注册成功！请登录")
        self.app.show_page("login")