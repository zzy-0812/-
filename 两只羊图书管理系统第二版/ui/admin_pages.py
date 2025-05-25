import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_frame import BaseFrame

class AdminMenuPage(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        tk.Label(self.frame, text="图书管理系统 - 管理员菜单", font=("SimHei", 20)).pack(pady=20)
        
        options = [
            "添加图书", "删除图书", "修改图书", 
            "查询图书", "添加已有图书", "用户管理", "返回登录"
        ]
        
        for option in options:
            tk.Button(self.frame, text=option, command=lambda opt=option: self.admin_action(opt), 
                     font=("SimHei", 12), width=20, height=2).pack(pady=10)
    
    def admin_action(self, action):
        if action == "添加图书":
            # 此处应跳转到添加图书子页面（需要进一步实现）
            pass
        elif action == "查询图书":
            self.app.show_page("admin_query")
        elif action == "用户管理":
            self.app.show_page("admin_user")
        elif action == "返回登录":
            self.app.current_user = None
            self.app.show_page("login")

class AdminQueryPage(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        tk.Label(self.frame, text="查询图书", font=("SimHei", 20)).pack(pady=20)
        
        # 查询条件区域
        query_frame = tk.Frame(self.frame)
        query_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(query_frame, text="查询字段:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        
        self.field = tk.StringVar()
        self.field.set("ID")
        
        field_menu = ttk.Combobox(query_frame, textvariable=self.field, values=["ID", "名称", "作者", "类型"], width=10)
        field_menu.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(query_frame, text="查询内容:", font=("SimHei", 12)).grid(row=0, column=2, padx=10, pady=10)
        
        self.value_entry = tk.Entry(query_frame, width=20)
        self.value_entry.grid(row=0, column=3, padx=10, pady=10)
        
        tk.Button(query_frame, text="查询", command=self.search, width=10).grid(row=0, column=4, padx=10, pady=10)
        
        # 返回按钮
        tk.Button(self.frame, text="返回", command=lambda: self.app.show_page("admin_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 结果区域
        result_frame = tk.Frame(self.frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建表格
        columns = ("ID", "名称", "作者", "出版社", "类型", "总数量", "可借数量", "状态")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def search(self):
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_field = self.field.get()
        search_value = self.value_entry.get().lower()
        
        if not search_value:
            messagebox.showerror("错误", "请输入查询内容！")
            return
            
        books = self.app.data_manager.search_books(search_field, search_value)
        
        if not books:
            self.tree.insert("", tk.END, values=("未找到匹配的图书", "", "", "", "", "", "", ""))
            return
            
        for book in books:
            status = "可借阅" if book.lend > 0 else "已借出"
            self.tree.insert("", tk.END, values=(
                book.id, book.name, book.author, book.publisher,
                book.type, book.remind, book.lend, status
            ))

class AdminUserPage(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        tk.Label(self.frame, text="用户管理", font=("SimHei", 16)).pack(pady=10)
        
        # 返回按钮
        tk.Button(self.frame, text="返回", command=lambda: self.app.show_page("admin_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # 创建表格
        columns = ("用户名", "角色", "操作")
        self.user_tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            if col == "操作":
                self.user_tree.column(col, width=150, anchor=tk.CENTER)
            else:
                self.user_tree.column(col, width=200, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 添加用户按钮
        tk.Button(self.frame, text="添加用户", width=15).pack(pady=10)
        
        # 刷新用户列表
        self.refresh_user_list()
    
    def refresh_user_list(self):
        # 清空表格
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
            
        users = self.app.data_manager.get_all_users()
        
        for username, (password, role) in users.items():
            self.user_tree.insert("", tk.END, values=(username, role, ""))