import os
from .models import Book, User

class DataManager:
    def __init__(self):
        self.book_data = []  # 存储Book对象
        self.user_data = {}  # {username: User}
        self.data_dir = "data"
        self.book_file = os.path.join(self.data_dir, "book_data.txt")
        self.user_file = os.path.join(self.data_dir, "user.txt")
        
        # 确保数据目录存在
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_all_data(self):
        self.load_book_data()
        self.load_user_data()
    
    def load_book_data(self):
        """加载图书数据"""
        self.book_data = []
        
        try:
            if not os.path.exists(self.book_file):
                # 创建空文件
                with open(self.book_file, 'w', encoding='utf-8') as f:
                    pass
                return
                
            with open(self.book_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 8:
                        book = Book(
                            parts[0], parts[1], parts[2], parts[3],
                            parts[4], parts[5], parts[6], parts[7]
                        )
                        self.book_data.append(book)
        except Exception as e:
            print(f"Error loading book data: {e}")
    
    def save_book_data(self):
        """保存图书数据"""
        try:
            with open(self.book_file, 'w', encoding='utf-8') as f:
                for book in self.book_data:
                    f.write(f"{book.id},{book.name},{book.author},{book.publisher},"
                            f"{book.type},{book.remind},{book.lend},{book.borrow_time}\n")
        except Exception as e:
            print(f"Error saving book data: {e}")
    
    def load_user_data(self):
        """加载用户数据"""
        self.user_data = {}
        
        try:
            if not os.path.exists(self.user_file):
                # 创建默认管理员账户
                with open(self.user_file, 'w', encoding='utf-8') as f:
                    f.write("admin,123,admin\n")
            
            with open(self.user_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        user = User(parts[0], parts[1], parts[2])
                        self.user_data[parts[0]] = user
        except Exception as e:
            print(f"Error loading user data: {e}")
    
    def save_user_data(self):
        """保存用户数据"""
        try:
            with open(self.user_file, 'w', encoding='utf-8') as f:
                for username, user in self.user_data.items():
                    f.write(f"{user.username},{user.password},{user.role}\n")
        except Exception as e:
            print(f"Error saving user data: {e}")
    
    def validate_user(self, username, password):
        """验证用户登录"""
        user = self.user_data.get(username)
        return user and user.password == password
    
    def is_admin(self, username):
        """检查用户是否是管理员"""
        user = self.user_data.get(username)
        return user and user.is_admin()
    
    def user_exists(self, username):
        """检查用户是否存在"""
        return username in self.user_data
    
    def add_user(self, username, password, role="user"):
        """添加新用户"""
        if username in self.user_data:
            return False
            
        self.user_data[username] = User(username, password, role)
        self.save_user_data()
        return True
    
    def get_all_users(self):
        """获取所有用户"""
        return {username: (user.password, user.role) for username, user in self.user_data.items()}
    
    def search_books(self, field, value):
        """按字段搜索图书"""
        results = []
        value = value.lower()
        
        for book in self.book_data:
            if field == "ID" and value == book.id.lower():
                results.append(book)
            elif field == "名称" and value in book.name.lower():
                results.append(book)
            elif field == "作者" and value in book.author.lower():
                results.append(book)
            elif field == "类型" and value == book.type.lower():
                results.append(book)
                
        return results
    
    def get_book_by_id(self, book_id):
        """按ID获取图书"""
        for book in self.book_data:
            if book.id == book_id:
                return book
        return None
    
    def borrow_book(self, book_id, username):
        """借阅图书"""
        book = self.get_book_by_id(book_id)
        if not book:
            return False
            
        if book.lend <= 0:
            return False
            
        # 更新借阅信息
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        
        if not book.borrow_time:
            book.borrow_time = f"{username}:{today}"
        else:
            book.borrow_time += f",{username}:{today}"
            
        book.lend -= 1
        self.save_book_data()
        return True
    
    def return_book(self, book_id, username):
        """归还图书"""
        book = self.get_book_by_id(book_id)
        if not book:
            return False
            
        # 检查用户是否借阅了这本书
        if not book.borrow_time or f"{username}:" not in book.borrow_time:
            return False
            
        # 更新借阅信息
        entries = book.borrow_time.split(',')
        new_entries = []
        found = False
        
        for entry in entries:
            if entry.startswith(f"{username}:") and not found:
                found = True
                continue
            new_entries.append(entry)
            
        book.borrow_time = ','.join(new_entries)
        book.lend += 1
        self.save_book_data()
        return True
    
    def has_borrowed(self, book_id, username):
        """检查用户是否借阅了指定图书"""
        book = self.get_book_by_id(book_id)
        if not book or not book.borrow_time:
            return False
            
        return f"{username}:" in book.borrow_time