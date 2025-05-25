import tkinter as tk
from ui.base_frame import BaseFrame
from ui.login_pages import LoginPage, RegisterPage
from ui.admin_pages import AdminMenuPage, AdminQueryPage, AdminUserPage
from ui.user_pages import UserMenuPage, UserQueryPage, UserBorrowPage
from data.data_manager import DataManager

class BookManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("两只羊图书管理系统")
        self.root.geometry("800x600")
        self.current_user = None
        
        # 初始化数据管理器
        self.data_manager = DataManager()
        self.data_manager.load_all_data()
        
        # 创建主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建所有页面
        self.pages = {
            "login": LoginPage(self.main_frame, self),
            "register": RegisterPage(self.main_frame, self),
            "admin_menu": AdminMenuPage(self.main_frame, self),
            "admin_query": AdminQueryPage(self.main_frame, self),
            "admin_user": AdminUserPage(self.main_frame, self),
            "user_menu": UserMenuPage(self.main_frame, self),
            "user_query": UserQueryPage(self.main_frame, self),
            "user_borrow": UserBorrowPage(self.main_frame, self),
        }
        
        # 初始显示登录页面
        self.show_page("login")
    
    def show_page(self, page_name):
        """显示指定页面"""
        for page in self.pages.values():
            page.hide()
        self.pages[page_name].show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()