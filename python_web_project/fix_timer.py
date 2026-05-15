with open('e:/办公练习/Html/Q文件/python_web_project/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找完整的定时器函数定义
start_idx = content.find('def start_status_cleanup_timer():')
if start_idx != -1:
    print('找到了定时器函数定义')
    
    # 替换整个函数定义
    old_func = '''def start_status_cleanup_timer():
    \"\"\"启动定期清理过期用户状态的定时器\"\"\"
    def timer_loop():
        while True:
            try:
                cleanup_expired_user_statuses()
                time.sleep(60)  # 每1分钟清理一次
            except Exception as e:
                print(f\"清理用户状态时出错: {e}\")
                time.sleep(60)  # 出错后继续等待1分钟再试

    # 启动清理线程
    cleanup_thread = threading.Thread(target=timer_loop, daemon=True)
    cleanup_thread.start()'''

    new_func = '''def start_status_cleanup_timer():
    \"\"\"启动定期清理过期用户状态的定时器\"\"\"
    def timer_loop():
        import time  # 在函数内部导入time模块以确保可用
        while True:
            try:
                cleanup_expired_user_statuses()
                time.sleep(60)  # 每1分钟清理一次
            except Exception as e:
                print(f\"清理用户状态时出错: {e}\")
                time.sleep(60)  # 出错后继续等待1分钟再试

    # 启动清理线程
    cleanup_thread = threading.Thread(target=timer_loop, daemon=True)
    cleanup_thread.start()'''

    # 替换函数定义
    fixed_content = content.replace(old_func, new_func)
    
    with open('e:/办公练习/Html/Q文件/python_web_project/app.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print('定时器函数已修复')
else:
    print('未找到定时器函数定义')
