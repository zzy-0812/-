import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_frame import BaseFrame

class UserMenuPage(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        tk.Label(self.frame, text=f"图书管理系统 - 用户菜单 ({self.app.current_user})", font=("SimHei", 20)).pack(pady=20)
        
        options = [
            "查询图书", "借阅/归还图书", "查阅图书借阅状态", 
            "修改密码", "返回登录"
        ]
        
        for option in options:
            tk.Button(self.frame, text=option, command=lambda opt=option: self.user_action(opt), 
                     font=("SimHei", 12), width=20, height=2).pack(pady=10)
    
    def user_action(self, action):
        if action == "查询图书":
            self.app.show_page("user_query")
        elif action == "借阅/归还图书":
            self.app.show_page("user_borrow")
        elif action == "返回登录":
            self.app.current_user = None
            self.app.show_page("login")

class UserQueryPage(BaseFrame):
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
        tk.Button(self.frame, text="返回", command=lambda: self.app.show_page("user_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
        
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

class UserBorrowPage(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        tk.Label(self.frame, text="借阅/归还图书", font=("SimHei", 20)).pack(pady=20)
        
        # 借阅区域
        borrow_frame = tk.LabelFrame(self.frame, text="借阅图书", font=("SimHei", 12))
        borrow_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(borrow_frame, text="借阅方式:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        
        self.borrow_by = tk.StringVar()
        self.borrow_by.set("ID")
        
        borrow_by_menu = ttk.Combobox(borrow_frame, textvariable=self.borrow_by, values=["ID", "名称", "作者"], width=10)
        borrow_by_menu.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(borrow_frame, text="借阅内容:", font=("SimHei", 12)).grid(row=0, column=2, padx=10, pady=10)
        
        self.borrow_entry = tk.Entry(borrow_frame, width=20)
        self.borrow_entry.grid(row=0, column=3, padx=10, pady=10)
        
        tk.Button(borrow_frame, text="借阅", command=self.borrow_book, width=10).grid(row=0, column=4, padx=10, pady=10)
        
        # 归还区域
        return_frame = tk.LabelFrame(self.frame, text="归还图书", font=("SimHei", 12))
        return_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(return_frame, text="归还方式:", font=("SimHei", 12)).grid(row=0, column=0, padx=10, pady=10)
        
        self.return_by = tk.StringVar()
        self.return_by.set("ID")
        
        return_by_menu = ttk.Combobox(return_frame, textvariable=self.return_by, values=["ID", "名称"], width=10)
        return_by_menu.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(return_frame, text="归还内容:", font=("SimHei", 12)).grid(row=0, column=2, padx=10, pady=10)
        
        self.return_entry = tk.Entry(return_frame, width=20)
        self.return_entry.grid(row=0, column=3, padx=10, pady=10)
        
        tk.Button(return_frame, text="归还", command=self.return_book, width=10).grid(row=0, column=4, padx=10, pady=10)
        
        # 返回按钮
        tk.Button(self.frame, text="返回", command=lambda: self.app.show_page("user_menu"), width=10).pack(side=tk.RIGHT, padx=20, pady=10)
    
    def borrow_book(self):
        method = self.borrow_by.get()
        value = self.borrow_entry.get()
        
        if not value:
            messagebox.showerror("错误", f"请输入{method}！")
            return
            
        books = self.app.data_manager.search_books(method, value)
        
        if not books:
            messagebox.showerror("错误", f"未找到匹配的图书！")
            return
            
        if len(books) > 1:
            # 此处应跳转到选择图书子页面（需要进一步实现）
            pass
        else:
            book = books[0]
            
            if book.lend <= 0:
                messagebox.showerror("错误", "该图书已全部借出！")
                return
                
            # 借阅逻辑（需要在DataManager中实现）
            result = self.app.data_manager.borrow_book(book.id, self.app.current_user)
            
            if result:
                messagebox.showinfo("成功", f"成功借阅《{book.name}》！")
                self.borrow_entry.delete(0, tk.END)
            else:
                messagebox.showerror("错误", "借阅失败！")
    
    def return_book(self):
        method = self.return_by.get()
        value = self.return_entry.get()
        
        if not value:
            messagebox.showerror("错误", f"请输入{method}！")
            return
            
        books = self.app.data_manager.search_books(method, value)
        
        if not books:
            messagebox.showerror("错误", f"未找到匹配的图书！")
            return
            
        if len(books) > 1:
            # 此处应跳转到选择图书子页面（需要进一步实现）
            pass
        else:
            book = books[0]
            
            # 检查该用户是否借了这本书（需要在DataManager中实现）
            if not self.app.data_manager.has_borrowed(book.id, self.app.current_user):
                messagebox.showerror("错误", "你没有借阅这本书！")
                return
                
            # 归还逻辑（需要在DataManager中实现）
            result = self.app.data_manager.return_book(book.id, self.app.current_user)
            
            if result:
                messagebox.showinfo("成功", f"成功归还《{book.name}》！")
                self.return_entry.delete(0, tk.END)
            else:
                messagebox.showerror("错误", "归还失败！")