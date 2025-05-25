class Book:
    def __init__(self, id, name, author, publisher, type, remind, lend, borrow_time):
        self.id = id
        self.name = name
        self.author = author
        self.publisher = publisher
        self.type = type
        self.remind = int(remind)
        self.lend = int(lend)
        self.borrow_time = borrow_time
    
    def is_borrowed(self):
        return self.lend > 0
    
    def get_borrowers(self):
        """返回借阅者列表"""
        if not self.borrow_time:
            return []
            
        entries = self.borrow_time.split(',')
        return [entry.split(':')[0] for entry in entries if ':' in entry]
    
    def get_borrow_time(self, username):
        """返回指定用户的借阅时间"""
        if not self.borrow_time:
            return None
            
        entries = self.borrow_time.split(',')
        for entry in entries:
            parts = entry.split(':')
            if len(parts) >= 2 and parts[0] == username:
                return parts[1]
                
        return None

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    
    def is_admin(self):
        return self.role == "admin"