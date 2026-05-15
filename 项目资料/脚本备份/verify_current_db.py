import sqlite3

# 检查当前使用的app.db
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print('=== 当前使用的 app.db 数据库状态 ===')

# 检查用户
cursor.execute('SELECT COUNT(*) FROM users;')
user_count = cursor.fetchone()[0]
print(f'用户数: {user_count}')

# 检查消息
cursor.execute('SELECT COUNT(*) FROM messages;')
msg_count = cursor.fetchone()[0]
print(f'消息数: {msg_count}')

# 检查关注关系
cursor.execute('SELECT COUNT(*) FROM follows;')
follows_count = cursor.fetchone()[0]
print(f'关注关系数: {follows_count}')

# 检查重要用户
cursor.execute("SELECT id, username, email FROM users WHERE username IN ('FallPetal', '赵栋行001');")
important_users = cursor.fetchall()
print('重要用户:')
for user in important_users:
    print(f'  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}')

conn.close()
print('\n现在 app.db 包含了原始数据库的所有数据')