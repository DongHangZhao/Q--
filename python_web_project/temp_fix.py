with open('e:/办公练习/Html/Q文件/python_web_project/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到start_status_cleanup_timer函数的位置
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'def start_status_cleanup_timer():' in line:
        start_idx = i
        break

if start_idx != -1:
    # 找到函数结束位置
    for i in range(start_idx + 1, len(lines)):
        line = lines[i]
        # 如果行不为空且缩进小于等于8（即不是函数内部的行）
        stripped = line.lstrip()
        if stripped and (line.startswith(' ') and len(line) - len(stripped) <= 4) and not stripped.startswith('#'):
            end_idx = i
            break
        if '# 启动状态清理定时器' in stripped:
            end_idx = i + 1  # 包括注释行
            break

if start_idx != -1 and end_idx != -1:
    # 替换函数部分
    new_function = [
        'def start_status_cleanup_timer():\n',
        '    """启动定期清理过期用户状态的定时器"""\n',
        '    def timer_loop():\n',
        '        import time  # 在函数内部导入time模块\n',
        '        \n',
        '        while True:\n',
        '            try:\n',
        '                cleanup_expired_user_statuses()\n',
        '                time.sleep(60)  # 每1分钟清理一次\n',
        '            except Exception as e:\n',
        '                print(f"清理用户状态时出错: {e}")\n',
        '                time.sleep(60)  # 出错后继续等待1分钟再试\n',
        '\n',
        '    # 启动清理线程\n',
        '    cleanup_thread = threading.Thread(target=timer_loop, daemon=True)\n',
        '    cleanup_thread.start()\n',
        '\n'
    ]
    
    # 重构文件内容
    final_lines = lines[:start_idx] + new_function + lines[end_idx:]
    
    with open('e:/办公练习/Html/Q文件/python_web_project/app.py', 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    
    print(f'定时器函数已替换：从第{start_idx+1}行到第{end_idx}行被替换')
else:
    print('未找到定时器函数')
