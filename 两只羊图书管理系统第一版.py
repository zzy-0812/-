import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import random
import os

class BookManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("两只羊图书管理系统")
        self.root.geometry("800x600")
        self.current_user = None
        
        # 确保数据文件存在
        self.ensure_data_file_exists()
        self.load_book_data()
        self.load_user_data()
        
        # 创建主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 存储所有页面的字典
        self.pages = {}
        
        # 存储子页面的字典（用于二级页面）
        self.sub_pages = {}
        
        # 存储当前活动的子页面
        self.current_sub_page = None
        
        # 创建所有页面
        self.create_all_pages()
        
        # 初始显示登录页面
        self.show_page("login")
    
    def ensure_data_file_exists(self):
        # 确保图书数据文件存在
        try:
            with open('book_data.txt', 'r', encoding='utf-8') as f:
                pass  # 文件存在，无需操作
        except FileNotFoundError:
            # 创建空文件
            with open('book_data.txt', 'w', encoding='utf-8') as f:
                pass
        
        # 确保用户数据文件存在
        try:
            with open('user.txt', 'r', encoding='utf-8') as f:
                pass  # 文件存在，无需操作
        except FileNotFoundError:
            # 创建初始用户文件，包含默认管理员账户
            with open('user.txt', 'w', encoding='utf-8') as f:
                f.write("admin,123,admin\n")  # 格式：用户名,密码,角色(admin/user)
    
    def load_book_data(self):
        self.book_id = []
        self.book_type = []
        self.book_name = []
        self.book_author = []
        self.book_publisher = []
        self.book_remind = []
        self.book_lend = []
        self.borrow_time = []
        
        try:
            with open('book_data.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    self.book_id.append(parts[0])
                    self.book_name.append(parts[1])
                    self.book_author.append(parts[2])
                    self.book_publisher.append(parts[3])
                    self.book_type.append(parts[4])
                    self.book_remind.append(parts[5])
                    self.book_lend.append(parts[6])
                    self.borrow_time.append(parts[7] if len(parts) > 7 else "")
        except FileNotFoundError:
            pass  # 文件不存在，使用空数据
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时发生错误: {e}")
    
    def save_book_data(self):
        try:
            with open('book_data.txt', 'w', encoding='utf-8') as f:
                for i in range(len(self.book_id)):
                    borrow_time_str = self.borrow_time[i] if self.borrow_time[i] else ""
                    f.write(f"{self.book_id[i]},{self.book_name[i]},{self.book_author[i]},{self.book_publisher[i]},{self.book_type[i]},{self.book_remind[i]},{self.book_lend[i]},{borrow_time_str}\n")
        except Exception as e:
            messagebox.showerror("错误", f"写入文件时发生错误: {e}")
    
    def load_user_data(self):
        self.users = {}  # 格式：{用户名: (密码, 角色)}
        
        try:
            with open('user.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        self.users[parts[0]] = (parts[1], parts[2])
        except FileNotFoundError:
            # 文件不存在，在ensure_data_file_exists中已创建默认管理员
            pass
        except Exception as e:
            messagebox.showerror("错误", f"读取用户文件时发生错误: {e}")
    
    def save_user_data(self):
        try:
            with open('user.txt', 'w', encoding='utf-8') as f:
                for username, (password, role) in self.users.items():
                    f.write(f"{username},{password},{role}\n")
        except Exception as e:
            messagebox.showerror("错误", f"写入用户文件时发生错误: {e}")
    
    def create_all_pages(self):
        # 创建主页面
        main_pages = [
            "login", "register", "admin_menu", "user_menu", 
            "admin_query", "user_query", "user_borrow", "admin_user"
        ]
        
        for page in main_pages:
            frame = tk.Frame(self.main_frame)
            self.pages[page] = frame
        
        # 创建子页面容器
        sub_page_container = tk.Frame(self.main_frame)
        self.pages["sub_page_container"] = sub_page_container
        
        # 创建所有子页面
        self.create_all_sub_pages()
        
        # 初始化各页面
        self.setup_login_page()
        self.setup_register_page()
        self.setup_admin_menu_page()
        self.setup_user_menu_page()
        self.setup_admin_query_page()
        self.setup_user_query_page()
        self.setup_user_borrow_page()
        self.setup_admin_user_page()
    
    def create_all_sub_pages(self):
        # 管理员子页面
        admin_sub_pages = [
            "add_book", "del_book", "modify_book", "add_existing_book",
            "search_modify_book", "modify_book_form",
            "admin_add_user", "admin_edit_user"
        ]
        
        # 用户子页面
        user_sub_pages = [
            "change_password", "user_borrow_action", "user_borrow_status",
            "select_book_to_borrow", "select_book_to_return"
        ]
        
        for page in admin_sub_pages + user_sub_pages:
            frame = tk.Frame(self.pages["sub_page_container"])
            self.sub_pages[page] = frame
    
    def show_page(self, page_name):
        # 隐藏所有主页面
        for page in self.pages.values():
            page.pack_forget()
        
        # 隐藏所有子页面
        for sub_page in self.sub_pages.values():
            sub_page.pack_forget()
        
        # 显示指定主页面
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)
        
        # 重置当前子页面
        self.current_sub_page = None
    
    def show_sub_page(self, sub_page_name, parent_page=None, **kwargs):
        # 隐藏所有子页面
        for sub_page in self.sub_pages.values():
            sub_page.pack_forget()
        
        # 显示子页面容器
        self.pages["sub_page_container"].pack(fill=tk.BOTH, expand=True)
        
        # 显示指定子页面
        self.sub_pages[sub_page_name].pack(fill=tk.BOTH, expand=True)
        
        # 保存当前子页面
        self.current_sub_page = sub_page_name
        
        # 如果提供了父页面，存储它
        if parent_page:
            self.current_parent_page = parent_page
        
        # 传递额外参数到子页面设置函数
        if hasattr(self, f"setup_{sub_page_name}_page"):
            setup_func = getattr(self, f"setup_{sub_page_name}_page")
            setup_func(**kwargs)
    
    def setup_login_page(self):
        frame = self.pages["login"]
        
        tk.Label(frame, text="两只羊图书管理系统", font=("SimHei", 24)).pack(pady=30)
        
        input_frame = tk.Frame(frame)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="用户名:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(input_frame, font=("SimHei", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="密码:", font=("SimHei", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(input_frame, show="*", font=("SimHei", 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def login():
            username = self.username_entry.get()
            password = self.password_entry.get()
            
            if username in self.users and self.users[username][0] == password:
                self.current_user = username
                if self.users[username][1] == "admin":
                    self.show_page("admin_menu")
                else:
                    self.show_page("user_menu")
            else:
                messagebox.showerror("登录失败", "用户名或密码错误！")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="登录", command=login, font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="注册", command=lambda: self.show_page("register"), font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
    
    def setup_register_page(self):
        frame = self.pages["register"]
        
        tk.Label(frame, text="用户注册", font=("SimHei", 24)).pack(pady=30)
        
        input_frame = tk.Frame(frame)
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
        
        def register():
            username = self.register_username_entry.get()
            password = self.register_password_entry.get()
            confirm = self.register_confirm_entry.get()
            
            if not username or not password:
                messagebox.showerror("注册失败", "用户名和密码不能为空！")
                return
                
            if username in self.users:
                messagebox.showerror("注册失败", "用户名已存在！")
                return
                
            if password != confirm:
                messagebox.showerror("注册失败", "两次输入的密码不一致！")
                return
                
            # 添加用户
            self.users[username] = (password, "user")  # 普通用户
            self.save_user_data()
            
            messagebox.showinfo("注册成功", "用户注册成功！请登录")
            self.show_page("login")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="注册", command=register, font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("login"), font=("SimHei", 12), width=10).pack(side=tk.LEFT, padx=10)
    
    def setup_admin_menu_page(self):
        frame = self.pages["admin_menu"]
        
        tk.Label(frame, text="图书管理系统 - 管理员菜单", font=("SimHei", 20)).pack(pady=20)
        
        options = [
            "添加图书", "删除图书", "修改图书", 
            "查询图书", "添加已有图书", "用户管理", "返回登录"
        ]
        
        for option in options:
            tk.Button(frame, text=option, command=lambda opt=option: self.admin_action(opt), 
                     font=("SimHei", 12), width=20, height=2).pack(pady=10)
    
    def admin_action(self, action):
        if action == "添加图书":
            self.show_sub_page("add_book", parent_page="admin_menu")
        elif action == "删除图书":
            self.show_sub_page("del_book", parent_page="admin_menu")
        elif action == "修改图书":
            self.show_sub_page("modify_book", parent_page="admin_menu")
        elif action == "查询图书":
            self.show_page("admin_query")
        elif action == "添加已有图书":
            self.show_sub_page("add_existing_book", parent_page="admin_menu")
        elif action == "用户管理":
            self.show_page("admin_user")
        elif action == "返回登录":
            self.current_user = None
            self.show_page("login")
    
    def setup_admin_user_page(self):
        frame = self.pages["admin_user"]
        
        tk.Label(frame, text="用户管理", font=("SimHei", 16)).pack(pady=10)
        
        # 返回按钮
        tk.Button(frame, text="返回", command=lambda: self.show_page("admin_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 创建表格
        columns = ("用户名", "角色", "操作")
        self.user_tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            if col == "操作":
                self.user_tree.column(col, width=150, anchor=tk.CENTER)
            else:
                self.user_tree.column(col, width=200, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 绑定按钮点击事件
        self.user_tree.bind("<Button-1>", self.on_user_tree_click)
        
        # 添加用户按钮
        tk.Button(frame, text="添加用户", command=lambda: self.show_sub_page("admin_add_user", parent_page="admin_user"), width=15).pack(pady=10)
        
        # 刷新用户列表
        self.refresh_user_list()
    
    def refresh_user_list(self):
        # 清空表格
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # 填充数据
        for username, (password, role) in self.users.items():
            self.user_tree.insert("", tk.END, values=(username, role, ""))
    
    def on_user_tree_click(self, event):
        region = self.user_tree.identify_region(event.x, event.y)
        if region == "cell":
            item = self.user_tree.identify_row(event.y)
            col = self.user_tree.identify_column(event.x)
            
            if col == "#3":  # 操作列
                username = self.user_tree.item(item, "values")[0]
                
                # 计算按钮位置
                x, y, width, height = self.user_tree.bbox(item, col)
                
                # 创建编辑按钮
                edit_btn = tk.Button(self.user_tree, text="修改", width=5, 
                                    command=lambda u=username: self.show_sub_page("admin_edit_user", parent_page="admin_user", username=u))
                edit_btn.place(x=x+5, y=y, width=60, height=25)
                
                # 创建删除按钮
                delete_btn = tk.Button(self.user_tree, text="删除", width=5, 
                                      command=lambda u=username: self.admin_delete_user(u))
                delete_btn.place(x=x+70, y=y, width=60, height=25)
    
    def setup_admin_add_user_page(self, **kwargs):
        frame = self.sub_pages["admin_add_user"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="添加用户", font=("SimHei", 14)).pack(pady=10)
        
        tk.Label(frame, text="用户名:", font=("SimHei", 12)).pack(pady=5)
        username_entry = tk.Entry(frame, font=("SimHei", 12))
        username_entry.pack(pady=5)
        
        tk.Label(frame, text="密码:", font=("SimHei", 12)).pack(pady=5)
        password_entry = tk.Entry(frame, show="*", font=("SimHei", 12))
        password_entry.pack(pady=5)
        
        tk.Label(frame, text="角色:", font=("SimHei", 12)).pack(pady=5)
        role_var = tk.StringVar()
        role_var.set("user")
        role_menu = ttk.Combobox(frame, textvariable=role_var, values=["user", "admin"], width=10)
        role_menu.pack(pady=5)
        
        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            
            if not username or not password:
                messagebox.showerror("错误", "用户名和密码不能为空！")
                return
                
            if username in self.users:
                messagebox.showerror("错误", "用户名已存在！")
                return
                
            self.users[username] = (password, role)
            self.save_user_data()
            
            messagebox.showinfo("成功", "用户添加成功！")
            self.show_page("admin_user")
            self.refresh_user_list()  # 刷新用户列表
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="保存", command=save_user, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_user"), width=10).pack(side=tk.LEFT, padx=10)
    
    def setup_admin_edit_user_page(self, **kwargs):
        frame = self.sub_pages["admin_edit_user"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        username = kwargs.get("username", "")
        if not username or username not in self.users:
            messagebox.showerror("错误", "用户不存在！")
            self.show_page("admin_user")
            return
        
        tk.Label(frame, text=f"编辑用户 - {username}", font=("SimHei", 14)).pack(pady=10)
        
        tk.Label(frame, text="用户名:", font=("SimHei", 12)).pack(pady=5)
        username_entry = tk.Entry(frame, font=("SimHei", 12))
        username_entry.insert(0, username)
        username_entry.config(state="readonly")  # 用户名不可修改
        username_entry.pack(pady=5)
        
        tk.Label(frame, text="新密码:", font=("SimHei", 12)).pack(pady=5)
        password_entry = tk.Entry(frame, show="*", font=("SimHei", 12))
        password_entry.pack(pady=5)
        
        tk.Label(frame, text="角色:", font=("SimHei", 12)).pack(pady=5)
        role_var = tk.StringVar()
        role_var.set(self.users[username][1])
        role_menu = ttk.Combobox(frame, textvariable=role_var, values=["user", "admin"], width=10)
        role_menu.pack(pady=5)
        
        def save_changes():
            password = password_entry.get()
            role = role_var.get()
            
            if not password:
                messagebox.showerror("错误", "密码不能为空！")
                return
                
            # 更新用户信息
            self.users[username] = (password, role)
            self.save_user_data()
            
            messagebox.showinfo("成功", "用户信息更新成功！")
            self.show_page("admin_user")
            self.refresh_user_list()  # 刷新用户列表
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="保存", command=save_changes, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_user"), width=10).pack(side=tk.LEFT, padx=10)
    
    def admin_delete_user(self, username):
        if username == "admin":
            messagebox.showerror("错误", "默认管理员账户不能删除！")
            return
            
        confirm = messagebox.askyesno("确认删除", f"确定要删除用户 '{username}' 吗？")
        
        if confirm:
            del self.users[username]
            self.save_user_data()
            messagebox.showinfo("成功", "用户删除成功！")
            self.refresh_user_list()  # 刷新用户列表
    
    def setup_add_book_page(self, **kwargs):
        frame = self.sub_pages["add_book"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="添加新书", font=("SimHei", 16)).pack(pady=10)
        
        fields = ["图书ID", "图书名称", "图书作者", "图书出版社", "总数量"]
        entries = {}
        
        for field in fields:
            frame_row = tk.Frame(frame)
            frame_row.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(frame_row, text=f"{field}:", width=10).pack(side=tk.LEFT)
            entries[field] = tk.Entry(frame_row)
            entries[field].pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 图书类型选择
        type_frame = tk.Frame(frame)
        type_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(type_frame, text="图书类型:", width=10).pack(side=tk.LEFT)
        
        type_var = tk.StringVar()
        type_combobox = ttk.Combobox(type_frame, textvariable=type_var, values=["文学", "数学", "计算机", "医学"])
        type_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        type_combobox.set("文学")
        
        def save_book():
            book_id = entries["图书ID"].get()
            if not book_id:
                messagebox.showerror("错误", "图书ID不能为空！")
                return
                
            if book_id in self.book_id:
                messagebox.showerror("错误", "图书ID已存在！")
                return
                
            book_name = entries["图书名称"].get()
            book_author = entries["图书作者"].get()
            book_publisher = entries["图书出版社"].get()
            book_type = type_var.get()
            book_remind = entries["总数量"].get()
            
            if not all([book_name, book_author, book_publisher, book_remind]):
                messagebox.showerror("错误", "所有字段都必须填写！")
                return
                
            try:
                int(book_remind)
            except ValueError:
                messagebox.showerror("错误", "总数量必须是数字！")
                return
                
            self.book_id.append(book_id)
            self.book_name.append(book_name)
            self.book_author.append(book_author)
            self.book_publisher.append(book_publisher)
            self.book_type.append(book_type)
            self.book_remind.append(book_remind)
            self.book_lend.append(book_remind)  # 初始可借数量等于总数量
            self.borrow_time.append("")  # 初始借阅时间为空
            
            self.save_book_data()
            messagebox.showinfo("成功", "图书添加成功！")
            self.show_page("admin_menu")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="保存", command=save_book, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_menu"), width=15).pack(side=tk.LEFT, padx=10)
    
    def setup_del_book_page(self, **kwargs):
        frame = self.sub_pages["del_book"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="删除图书", font=("SimHei", 16)).pack(pady=10)
        
        tk.Label(frame, text="请输入要删除的图书ID", font=("SimHei", 12)).pack(pady=10)
        
        id_entry = tk.Entry(frame)
        id_entry.pack(pady=10)
        
        def delete_book():
            book_id = id_entry.get()
            if not book_id:
                messagebox.showerror("错误", "请输入图书ID！")
                return
                
            if book_id not in self.book_id:
                messagebox.showerror("错误", "图书ID不存在！")
                return
                
            index = self.book_id.index(book_id)
            confirm = messagebox.askyesno("确认删除", f"确定要删除图书 '{self.book_name[index]}' 吗？")
            
            if confirm:
                self.book_id.pop(index)
                self.book_name.pop(index)
                self.book_author.pop(index)
                self.book_publisher.pop(index)
                self.book_type.pop(index)
                self.book_remind.pop(index)
                self.book_lend.pop(index)
                self.borrow_time.pop(index)
                
                self.save_book_data()
                messagebox.showinfo("成功", "图书删除成功！")
                self.show_page("admin_menu")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="删除", command=delete_book, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_menu"), width=15).pack(side=tk.LEFT, padx=10)
    
    def setup_modify_book_page(self, **kwargs):
        frame = self.sub_pages["modify_book"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="修改图书", font=("SimHei", 16)).pack(pady=10)
        
        tk.Label(frame, text="请输入要修改的图书ID", font=("SimHei", 12)).pack(pady=10)
        
        id_entry = tk.Entry(frame)
        id_entry.pack(pady=10)
        
        def search_book():
            book_id = id_entry.get()
            if not book_id:
                messagebox.showerror("错误", "请输入图书ID！")
                return
                
            if book_id not in self.book_id:
                messagebox.showerror("错误", "图书ID不存在！")
                return
                
            index = self.book_id.index(book_id)
            self.show_sub_page("modify_book_form", parent_page="admin_menu", index=index)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="查找", command=search_book, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_menu"), width=15).pack(side=tk.LEFT, padx=10)
    
    def setup_modify_book_form_page(self, **kwargs):
        frame = self.sub_pages["modify_book_form"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        index = kwargs.get("index", -1)
        if index < 0 or index >= len(self.book_id):
            messagebox.showerror("错误", "图书索引无效！")
            self.show_page("admin_menu")
            return
        
        tk.Label(frame, text=f"修改图书 - {self.book_name[index]}", font=("SimHei", 16)).pack(pady=10)
        
        fields = ["图书ID", "图书名称", "图书作者", "图书出版社", "总数量", "可借数量"]
        entries = {}
        
        initial_values = [
            self.book_id[index], self.book_name[index], self.book_author[index],
            self.book_publisher[index], self.book_remind[index], self.book_lend[index]
        ]
        
        for i, field in enumerate(fields):
            frame_row = tk.Frame(frame)
            frame_row.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(frame_row, text=f"{field}:", width=10).pack(side=tk.LEFT)
            entries[field] = tk.Entry(frame_row)
            entries[field].insert(0, initial_values[i])
            if field == "图书ID":  # ID不可修改
                entries[field].config(state="readonly")
            entries[field].pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 图书类型选择
        type_frame = tk.Frame(frame)
        type_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(type_frame, text="图书类型:", width=10).pack(side=tk.LEFT)
        
        type_var = tk.StringVar()
        type_combobox = ttk.Combobox(type_frame, textvariable=type_var, values=["文学", "数学", "计算机", "医学"])
        type_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        type_combobox.set(self.book_type[index])
        
        def save_changes():
            # 图书ID不可修改
            self.book_name[index] = entries["图书名称"].get()
            self.book_author[index] = entries["图书作者"].get()
            self.book_publisher[index] = entries["图书出版社"].get()
            self.book_type[index] = type_var.get()
            self.book_remind[index] = entries["总数量"].get()
            self.book_lend[index] = entries["可借数量"].get()
            
            # 验证数值字段
            try:
                int(self.book_remind[index])
                int(self.book_lend[index])
            except ValueError:
                messagebox.showerror("错误", "总数量和可借数量必须是数字！")
                return
                
            if int(self.book_lend[index]) > int(self.book_remind[index]):
                messagebox.showerror("错误", "可借数量不能大于总数量！")
                return
                
            self.save_book_data()
            messagebox.showinfo("成功", "图书信息修改成功！")
            self.show_page("admin_menu")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="保存", command=save_changes, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_menu"), width=15).pack(side=tk.LEFT, padx=10)
    
    def setup_add_existing_book_page(self, **kwargs):
        frame = self.sub_pages["add_existing_book"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="添加已有图书", font=("SimHei", 16)).pack(pady=10)
        
        tk.Label(frame, text="请输入图书编号", font=("SimHei", 12)).pack(pady=10)
        
        id_entry = tk.Entry(frame)
        id_entry.pack(pady=10)
        
        def search_book():
            book_id = id_entry.get()
            if not book_id:
                messagebox.showerror("错误", "请输入图书ID！")
                return
                
            if book_id not in self.book_id:
                messagebox.showerror("错误", "图书ID不存在！")
                return
                
            index = self.book_id.index(book_id)
            
            # 创建添加数量页面
            self.show_sub_page("add_existing_book_confirm", parent_page="admin_menu", index=index)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="查找", command=search_book, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_menu"), width=15).pack(side=tk.LEFT, padx=10)
    
    def setup_add_existing_book_confirm_page(self, **kwargs):
        frame = self.sub_pages.get("add_existing_book_confirm", self.sub_pages["add_existing_book"])
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        index = kwargs.get("index", -1)
        if index < 0 or index >= len(self.book_id):
            messagebox.showerror("错误", "图书索引无效！")
            self.show_page("admin_menu")
            return
        
        tk.Label(frame, text=f"添加 {self.book_name[index]}", font=("SimHei", 14)).pack(pady=10)
        tk.Label(frame, text=f"当前库存: {self.book_remind[index]}", font=("SimHei", 12)).pack(pady=5)
        tk.Label(frame, text="请输入要添加的数量:", font=("SimHei", 12)).pack(pady=10)
        
        add_entry = tk.Entry(frame)
        add_entry.pack(pady=10)
        
        def add_quantity():
            try:
                add_num = int(add_entry.get())
                if add_num <= 0:
                    messagebox.showerror("错误", "添加数量必须大于0！")
                    return
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字！")
                return
                
            # 更新数量
            self.book_remind[index] = str(int(self.book_remind[index]) + add_num)
            self.book_lend[index] = str(int(self.book_lend[index]) + add_num)
            
            self.save_book_data()
            messagebox.showinfo("成功", f"成功添加 {add_num} 本《{self.book_name[index]}》！")
            self.show_page("admin_menu")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="添加", command=add_quantity, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("admin_menu"), width=15).pack(side=tk.LEFT, padx=10)
    
    def setup_admin_query_page(self):
        frame = self.pages["admin_query"]
        
        tk.Label(frame, text="查询图书", font=("SimHei", 20)).pack(pady=20)
        
        # 查询条件区域
        query_frame = tk.Frame(frame)
        query_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(query_frame, text="查询字段:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        
        field = tk.StringVar()
        field.set("ID")
        
        field_menu = ttk.Combobox(query_frame, textvariable=field, values=["ID", "名称", "作者", "类型"], width=10)
        field_menu.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(query_frame, text="查询内容:", font=("SimHei", 12)).grid(row=0, column=2, padx=10, pady=10)
        
        value_entry = tk.Entry(query_frame, width=20)
        value_entry.grid(row=0, column=3, padx=10, pady=10)
        
        def search():
            # 清空表格
            for item in tree.get_children():
                tree.delete(item)
            
            search_field = field.get()
            search_value = value_entry.get().lower()
            
            if not search_value:
                messagebox.showerror("错误", "请输入查询内容！")
                return
                
            found = False
            
            for i in range(len(self.book_id)):
                if search_field == "ID" and search_value == self.book_id[i]:
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
                elif search_field == "名称" and search_value in self.book_name[i].lower():
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
                elif search_field == "作者" and search_value in self.book_author[i].lower():
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
                elif search_field == "类型" and search_value == self.book_type[i].lower():
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
            
            if not found:
                tree.insert("", tk.END, values=("未找到匹配的图书", "", "", "", "", "", "", ""))
        
        tk.Button(query_frame, text="查询", command=search, width=10).grid(row=0, column=4, padx=10, pady=10)
        
        # 返回按钮
        tk.Button(frame, text="返回", command=lambda: self.show_page("admin_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 结果区域
        result_frame = tk.Frame(frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "名称", "作者", "出版社", "类型", "总数量", "可借数量", "状态")
        tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_user_menu_page(self):
        frame = self.pages["user_menu"]
        
        tk.Label(frame, text=f"图书管理系统 - 用户菜单 ({self.current_user})", font=("SimHei", 20)).pack(pady=20)
        
        options = [
            "查询图书", "借阅/归还图书", "查阅图书借阅状态", 
            "修改密码", "返回登录"
        ]
        
        for option in options:
            tk.Button(frame, text=option, command=lambda opt=option: self.user_action(opt), 
                     font=("SimHei", 12), width=20, height=2).pack(pady=10)
    
    def user_action(self, action):
        if action == "查询图书":
            self.show_page("user_query")
        elif action == "借阅/归还图书":
            self.show_page("user_borrow")
        elif action == "查阅图书借阅状态":
            self.show_sub_page("user_borrow_status", parent_page="user_menu")
        elif action == "修改密码":
            self.show_sub_page("change_password", parent_page="user_menu")
        elif action == "返回登录":
            self.current_user = None
            self.show_page("login")
    
    def setup_user_query_page(self):
        frame = self.pages["user_query"]
        
        tk.Label(frame, text="查询图书", font=("SimHei", 20)).pack(pady=20)
        
        # 查询条件区域
        query_frame = tk.Frame(frame)
        query_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(query_frame, text="查询字段:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        
        field = tk.StringVar()
        field.set("ID")
        
        field_menu = ttk.Combobox(query_frame, textvariable=field, values=["ID", "名称", "作者", "类型"], width=10)
        field_menu.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(query_frame, text="查询内容:", font=("SimHei", 12)).grid(row=0, column=2, padx=10, pady=10)
        
        value_entry = tk.Entry(query_frame, width=20)
        value_entry.grid(row=0, column=3, padx=10, pady=10)
        
        def search():
            # 清空表格
            for item in tree.get_children():
                tree.delete(item)
            
            search_field = field.get()
            search_value = value_entry.get().lower()
            
            if not search_value:
                messagebox.showerror("错误", "请输入查询内容！")
                return
                
            found = False
            
            for i in range(len(self.book_id)):
                if search_field == "ID" and search_value == self.book_id[i]:
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
                elif search_field == "名称" and search_value in self.book_name[i].lower():
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
                elif search_field == "作者" and search_value in self.book_author[i].lower():
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
                elif search_field == "类型" and search_value == self.book_type[i].lower():
                    status = "可借阅" if int(self.book_lend[i]) > 0 else "已借出"
                    tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        self.book_publisher[i], self.book_type[i],
                        self.book_remind[i], self.book_lend[i], status
                    ))
                    found = True
            
            if not found:
                tree.insert("", tk.END, values=("未找到匹配的图书", "", "", "", "", "", "", ""))
        
        tk.Button(query_frame, text="查询", command=search, width=10).grid(row=0, column=4, padx=10, pady=10)
        
        # 返回按钮
        tk.Button(frame, text="返回", command=lambda: self.show_page("user_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 结果区域
        result_frame = tk.Frame(frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "名称", "作者", "出版社", "类型", "总数量", "可借数量", "状态")
        tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_user_borrow_page(self):
        frame = self.pages["user_borrow"]
        
        tk.Label(frame, text="借阅/归还图书", font=("SimHei", 20)).pack(pady=20)
        
        # 借阅区域
        borrow_frame = tk.LabelFrame(frame, text="借阅图书", font=("SimHei", 12))
        borrow_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(borrow_frame, text="借阅方式:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        
        borrow_by = tk.StringVar()
        borrow_by.set("ID")
        
        borrow_by_menu = ttk.Combobox(borrow_frame, textvariable=borrow_by, values=["ID", "名称", "作者"], width=10)
        borrow_by_menu.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(borrow_frame, text="借阅内容:", font=("SimHei", 12)).grid(row=0, column=2, padx=10, pady=10)
        
        borrow_entry = tk.Entry(borrow_frame, width=20)
        borrow_entry.grid(row=0, column=3, padx=10, pady=10)
        
        def borrow_book():
            method = borrow_by.get()
            value = borrow_entry.get()
            
            if not value:
                messagebox.showerror("错误", f"请输入{method}！")
                return
                
            # 查找匹配的图书
            matched_books = []
            for i in range(len(self.book_id)):
                if method == "ID" and self.book_id[i] == value:
                    matched_books.append(i)
                elif method == "名称" and value.lower() in self.book_name[i].lower():
                    matched_books.append(i)
                elif method == "作者" and value.lower() in self.book_author[i].lower():
                    matched_books.append(i)
            
            if not matched_books:
                messagebox.showerror("错误", f"未找到匹配的图书！")
                return
                
            if len(matched_books) > 1:
                # 有多本匹配的图书，让用户选择
                self.show_sub_page("select_book_to_borrow", parent_page="user_borrow", matched_books=matched_books)
            else:
                # 只有一本匹配的图书，直接借阅
                index = matched_books[0]
                
                if int(self.book_lend[index]) <= 0:
                    messagebox.showerror("错误", "该图书已全部借出！")
                    return
                
                # 获取当前日期
                today = datetime.date.today().strftime("%Y-%m-%d")
                
                # 记录借阅信息
                if not self.borrow_time[index]:
                    self.borrow_time[index] = f"{self.current_user}:{today}"
                else:
                    self.borrow_time[index] += f",{self.current_user}:{today}"
                
                # 减少可借数量
                self.book_lend[index] = str(int(self.book_lend[index]) - 1)
                
                # 保存数据
                self.save_book_data()
                
                messagebox.showinfo("成功", f"成功借阅《{self.book_name[index]}》！")
                borrow_entry.delete(0, tk.END)
                self.refresh_borrow_status()
        
        tk.Button(borrow_frame, text="借阅", command=borrow_book, width=10).grid(row=0, column=4, padx=10, pady=10)
        
        # 归还区域
        return_frame = tk.LabelFrame(frame, text="归还图书", font=("SimHei", 12))
        return_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(return_frame, text="归还方式:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        
        return_by = tk.StringVar()
        return_by.set("ID")
        
        return_by_menu = ttk.Combobox(return_frame, textvariable=return_by, values=["ID", "名称"], width=10)
        return_by_menu.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(return_frame, text="归还内容:", font=("SimHei", 12)).grid(row=0, column=2, padx=10, pady=10)
        
        return_entry = tk.Entry(return_frame, width=20)
        return_entry.grid(row=0, column=3, padx=10, pady=10)
        
        def return_book():
            method = return_by.get()
            value = return_entry.get()
            
            if not value:
                messagebox.showerror("错误", f"请输入{method}！")
                return
                
            # 查找匹配的图书
            matched_books = []
            for i in range(len(self.book_id)):
                if method == "ID" and self.book_id[i] == value:
                    matched_books.append(i)
                elif method == "名称" and value.lower() in self.book_name[i].lower():
                    matched_books.append(i)
            
            if not matched_books:
                messagebox.showerror("错误", f"未找到匹配的图书！")
                return
                
            if len(matched_books) > 1:
                # 有多本匹配的图书，让用户选择
                self.show_sub_page("select_book_to_return", parent_page="user_borrow", matched_books=matched_books)
            else:
                # 只有一本匹配的图书，直接归还
                index = matched_books[0]
                
                # 检查该用户是否借了这本书
                if not self.borrow_time[index] or f"{self.current_user}:" not in self.borrow_time[index]:
                    messagebox.showerror("错误", "你没有借阅这本书！")
                    return
                
                # 更新借阅时间
                borrow_entries = self.borrow_time[index].split(',')
                new_entries = []
                found = False
                
                for entry in borrow_entries:
                    if entry.startswith(f"{self.current_user}:") and not found:
                        found = True
                        continue
                    new_entries.append(entry)
                
                self.borrow_time[index] = ','.join(new_entries)
                
                # 增加可借数量
                self.book_lend[index] = str(int(self.book_lend[index]) + 1)
                
                # 保存数据
                self.save_book_data()
                
                messagebox.showinfo("成功", f"成功归还《{self.book_name[index]}》！")
                return_entry.delete(0, tk.END)
                self.refresh_borrow_status()
        
        tk.Button(return_frame, text="归还", command=return_book, width=10).grid(row=0, column=4, padx=10, pady=10)
        
        # 借阅状态区域
        status_frame = tk.LabelFrame(frame, text="我的借阅状态", font=("SimHei", 12))
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建表格
        columns = ("ID", "名称", "作者", "借阅日期", "应还日期")
        self.borrow_tree = ttk.Treeview(status_frame, columns=columns, show="headings")
        
        for col in columns:
            self.borrow_tree.heading(col, text=col)
            self.borrow_tree.column(col, width=120, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.borrow_tree.yview)
        self.borrow_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.borrow_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 返回按钮
        tk.Button(frame, text="返回", command=lambda: self.show_page("user_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 刷新借阅状态
        self.refresh_borrow_status()
    
    def setup_select_book_to_borrow_page(self, **kwargs):
        frame = self.sub_pages["select_book_to_borrow"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        matched_books = kwargs.get("matched_books", [])
        if not matched_books:
            messagebox.showerror("错误", "没有匹配的图书！")
            self.show_page("user_borrow")
            return
        
        tk.Label(frame, text="选择要借阅的图书", font=("SimHei", 14)).pack(pady=10)
        
        # 创建表格
        columns = ("ID", "名称", "作者", "出版社", "可借数量", "操作")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "操作":
                tree.column(col, width=100, anchor=tk.CENTER)
            else:
                tree.column(col, width=150, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 填充数据
        for i in matched_books:
            values = (
                self.book_id[i], self.book_name[i], self.book_author[i],
                self.book_publisher[i], self.book_lend[i]
            )
            item = tree.insert("", tk.END, values=values)
            
            # 如果可借数量大于0，添加借阅按钮
            if int(self.book_lend[i]) > 0:
                tree.set(item, "操作", "借阅")
        
        # 绑定按钮点击事件
        def on_tree_click(event):
            region = tree.identify_region(event.x, event.y)
            if region == "cell":
                item = tree.identify_row(event.y)
                col = tree.identify_column(event.x)
                
                if col == "#6":  # 操作列
                    index = matched_books[list(tree.get_children()).index(item)]
                    
                    # 获取当前日期
                    today = datetime.date.today().strftime("%Y-%m-%d")
                    
                    # 记录借阅信息
                    if not self.borrow_time[index]:
                        self.borrow_time[index] = f"{self.current_user}:{today}"
                    else:
                        self.borrow_time[index] += f",{self.current_user}:{today}"
                    
                    # 减少可借数量
                    self.book_lend[index] = str(int(self.book_lend[index]) - 1)
                    
                    # 保存数据
                    self.save_book_data()
                    
                    messagebox.showinfo("成功", f"成功借阅《{self.book_name[index]}》！")
                    self.show_page("user_borrow")
                    self.refresh_borrow_status()
        
        tree.bind("<Button-1>", on_tree_click)
        
        # 返回按钮
        tk.Button(frame, text="返回", command=lambda: self.show_page("user_borrow"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
    
    def setup_select_book_to_return_page(self, **kwargs):
        frame = self.sub_pages["select_book_to_return"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        matched_books = kwargs.get("matched_books", [])
        if not matched_books:
            messagebox.showerror("错误", "没有匹配的图书！")
            self.show_page("user_borrow")
            return
        
        # 过滤出当前用户借阅的图书
        user_borrowed_books = []
        for i in matched_books:
            if self.borrow_time[i] and f"{self.current_user}:" in self.borrow_time[i]:
                user_borrowed_books.append(i)
        
        if not user_borrowed_books:
            messagebox.showerror("错误", "你没有借阅这些图书！")
            self.show_page("user_borrow")
            return
        
        tk.Label(frame, text="选择要归还的图书", font=("SimHei", 14)).pack(pady=10)
        
        # 创建表格
        columns = ("ID", "名称", "作者", "出版社", "借阅日期", "操作")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "操作":
                tree.column(col, width=100, anchor=tk.CENTER)
            else:
                tree.column(col, width=150, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 填充数据
        for i in user_borrowed_books:
            borrow_entries = self.borrow_time[i].split(',')
            user_borrow_dates = []
            
            for entry in borrow_entries:
                parts = entry.split(':')
                if len(parts) >= 2 and parts[0] == self.current_user:
                    user_borrow_dates.append(parts[1])
            
            for date in user_borrow_dates:
                values = (
                    self.book_id[i], self.book_name[i], self.book_author[i],
                    self.book_publisher[i], date
                )
                item = tree.insert("", tk.END, values=values)
                tree.set(item, "操作", "归还")
        
        # 绑定按钮点击事件
        def on_tree_click(event):
            region = tree.identify_region(event.x, event.y)
            if region == "cell":
                item = tree.identify_row(event.y)
                col = tree.identify_column(event.x)
                
                if col == "#6":  # 操作列
                    values = tree.item(item, "values")
                    book_id = values[0]
                    borrow_date = values[4]
                    
                    # 找到图书索引
                    index = self.book_id.index(book_id)
                    
                    # 更新借阅时间
                    borrow_entries = self.borrow_time[index].split(',')
                    new_entries = []
                    found = False
                    
                    for entry in borrow_entries:
                        parts = entry.split(':')
                        if len(parts) >= 2 and parts[0] == self.current_user and parts[1] == borrow_date and not found:
                            found = True
                            continue
                        new_entries.append(entry)
                    
                    self.borrow_time[index] = ','.join(new_entries)
                    
                    # 增加可借数量
                    self.book_lend[index] = str(int(self.book_lend[index]) + 1)
                    
                    # 保存数据
                    self.save_book_data()
                    
                    messagebox.showinfo("成功", f"成功归还《{self.book_name[index]}》！")
                    self.show_page("user_borrow")
                    self.refresh_borrow_status()
        
        tree.bind("<Button-1>", on_tree_click)
        
        # 返回按钮
        tk.Button(frame, text="返回", command=lambda: self.show_page("user_borrow"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
    
    def refresh_borrow_status(self):
        # 清空表格
        for item in self.borrow_tree.get_children():
            self.borrow_tree.delete(item)
        
        # 填充数据
        today = datetime.date.today()
        
        for i in range(len(self.book_id)):
            if not self.borrow_time[i]:
                continue
                
            borrow_entries = self.borrow_time[i].split(',')
            
            for entry in borrow_entries:
                parts = entry.split(':')
                if len(parts) < 2:
                    continue
                    
                username, borrow_date_str = parts
                
                if username == self.current_user:
                    borrow_date = datetime.datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
                    due_date = borrow_date + datetime.timedelta(days=30)  # 假设借阅期限30天
                    
                    # 计算剩余天数
                    days_left = (due_date - today).days
                    
                    # 根据剩余天数设置不同的颜色
                    due_date_str = due_date.strftime("%Y-%m-%d")
                    
                    self.borrow_tree.insert("", tk.END, values=(
                        self.book_id[i], self.book_name[i], self.book_author[i],
                        borrow_date_str, due_date_str
                    ))
    
    def setup_user_borrow_status_page(self):
        frame = self.sub_pages["user_borrow_status"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="图书借阅状态", font=("SimHei", 16)).pack(pady=10)
        
        # 创建表格
        columns = ("ID", "名称", "作者", "借阅人", "借阅日期", "应还日期", "状态")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "状态":
                tree.column(col, width=100, anchor=tk.CENTER)
            else:
                tree.column(col, width=120, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 返回按钮
        tk.Button(frame, text="返回", command=lambda: self.show_page("user_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 填充数据
        today = datetime.date.today()
        
        for i in range(len(self.book_id)):
            book_id = self.book_id[i]
            book_name = self.book_name[i]
            book_author = self.book_author[i]
            
            if not self.borrow_time[i]:
                # 图书未被借出
                tree.insert("", tk.END, values=(
                    book_id, book_name, book_author, 
                    "", "", "", "可借阅"
                ))
            else:
                # 图书已被借出，显示所有借阅信息
                borrow_entries = self.borrow_time[i].split(',')
                
                for entry in borrow_entries:
                    parts = entry.split(':')
                    if len(parts) < 2:
                        continue
                        
                    username, borrow_date_str = parts
                    borrow_date = datetime.datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
                    due_date = borrow_date + datetime.timedelta(days=30)  # 假设借阅期限30天
                    
                    # 计算剩余天数
                    days_left = (due_date - today).days
                    
                    # 根据剩余天数设置状态
                    if days_left < 0:
                        status = f"已逾期{-days_left}天"
                    elif days_left == 0:
                        status = "今日到期"
                    else:
                        status = f"剩余{days_left}天"
                    
                    tree.insert("", tk.END, values=(
                        book_id, book_name, book_author, 
                        username, borrow_date_str, due_date.strftime("%Y-%m-%d"), status
                    ))
    
    def setup_change_password_page(self, **kwargs):
        frame = self.sub_pages["change_password"]
        
        # 清空框架
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="修改密码", font=("SimHei", 16)).pack(pady=10)
        
        tk.Label(frame, text="当前密码:", font=("SimHei", 12)).pack(pady=10)
        current_password_entry = tk.Entry(frame, show="*")
        current_password_entry.pack(pady=5)
        
        tk.Label(frame, text="新密码:", font=("SimHei", 12)).pack(pady=10)
        new_password_entry = tk.Entry(frame, show="*")
        new_password_entry.pack(pady=5)
        
        tk.Label(frame, text="确认新密码:", font=("SimHei", 12)).pack(pady=10)
        confirm_password_entry = tk.Entry(frame, show="*")
        confirm_password_entry.pack(pady=5)
        
        def change_password():
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if current_password != self.users[self.current_user][0]:
                messagebox.showerror("错误", "当前密码不正确！")
                return
                
            if not new_password:
                messagebox.showerror("错误", "新密码不能为空！")
                return
                
            if new_password != confirm_password:
                messagebox.showerror("错误", "两次输入的新密码不一致！")
                return
                
            # 更新密码
            role = self.users[self.current_user][1]
            self.users[self.current_user] = (new_password, role)
            self.save_user_data()
            
            messagebox.showinfo("成功", "密码修改成功！请重新登录")
            self.current_user = None
            self.show_page("login")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="修改", command=change_password, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="返回", command=lambda: self.show_page("user_menu"), width=15).pack(side=tk.LEFT, padx=10)

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()