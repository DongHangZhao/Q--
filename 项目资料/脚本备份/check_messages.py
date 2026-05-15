'''
Author: your name
Date: 2026-01-11 22:33:00
LastEditTime: 2026-01-11 22:33:00
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_messages.py
'''
'''
Author: your name
Date: 2026-01-11 13:00:01
LastEditTime: 2026-01-11 13:00:03
LastEditors: ZDH
Description: 检查数据库中的消息数据
FilePath: e:\办公练习\Html\Q文件\python_web_project\check_messages.py
'''

from app import app, db, Message, User

def check_messages():
    with app.app_context():
        print("=== 消息数据检查报告 ===")
        
        # 统计总消息数
        total_messages = Message.query.count()
        print(f"总消息数量: {total_messages}")
        
        if total_messages > 0:
            print("\n=== 最近5条消息 ===")
            # 获取最近的5条消息
            recent_messages = Message.query.order_by(Message.timestamp.desc()).limit(5).all()
            
            for i, msg in enumerate(recent_messages, 1):
                # 获取发送者和接收者用户名
                sender_name = "未知用户"
                recipient_name = "未知用户"
                
                if msg.sender:
                    sender_name = msg.sender.username
                else:
                    # 如果关联不存在，使用ID
                    sender_user = User.query.get(msg.sender_id)
                    sender_name = sender_user.username if sender_user else f"ID:{msg.sender_id}"
                
                if msg.recipient:
                    recipient_name = msg.recipient.username
                else:
                    # 如果关联不存在，使用ID
                    recipient_user = User.query.get(msg.recipient_id)
                    recipient_name = recipient_user.username if recipient_user else f"ID:{msg.recipient_id}"
                
                print(f"{i}. ID: {msg.id}")
                print(f"   发送者: {sender_name}")
                print(f"   接收者: {recipient_name}")
                print(f"   时间: {msg.timestamp}")
                print(f"   内容: {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")
                
                if msg.attachment_path:
                    print(f"   附件: {msg.attachment_path}")
                print()
            
            print("=== 消息统计 ===")
            # 按用户统计消息数量
            users = User.query.all()
            for user in users[:10]:  # 只显示前10个用户
                sent_count = Message.query.filter(Message.sender_id == user.id).count()
                received_count = Message.query.filter(Message.recipient_id == user.id).count()
                if sent_count > 0 or received_count > 0:
                    print(f"用户 {user.username}: 发送 {sent_count} 条, 接收 {received_count} 条")
        else:
            print("数据库中暂无消息记录")

if __name__ == "__main__":
    check_messages()