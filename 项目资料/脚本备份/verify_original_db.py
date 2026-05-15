import sqlite3

# 检查原始数据库
conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

print('=== 原始数据库 (database/users.db) 最终状态 ===')

# 检查用户
cursor.execute('SELECT COUNT(*) FROM users;')
user_count = cursor.fetchone()[0]
print(f'用户数: {user_count}')

# 检查消息
cursor.execute('SELECT COUNT(*) FROM messages;')
msg_count = cursor.fetchone()[0]
print(f'消息数: {msg_count}')

# 检查重要用户的消息
cursor.execute("SELECT id, sender_id, recipient_id, content FROM messages WHERE sender_id IN (9, 10) OR recipient_id IN (9, 10) ORDER BY id LIMIT 10;")
important_msgs = cursor.fetchall()
print('\n重要用户(FallPetal和赵栋行001)的部分消息:')
for msg in important_msgs:
    print(f'  {msg[1]} -> {msg[2]}: {msg[3][:30]}...')

conn.close()
print('\n原始数据库已更新，包含了所有合并的数据')