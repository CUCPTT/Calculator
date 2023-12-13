import re
import tkinter as tk
from tkinter import ttk
# 分析过程
def analyse(token):
# E -> T
# T -> M|T(/)M
# M-> K | M^K
# K -> F | K&F
# F-> G | F>>G | F<< G
# G-> H | G-H| G+H
# H -> I| H*I | H/J | H%J
# I -> J | ~J
# J-> num | (E) | sin(E) | cos(E) | tan(E) | ln(E) | sqrt(E)

    priority_map = [
    # 行元素在栈内，列元素在栈外
    #  +    -   *    /    (    )     %   ^    &    |    ~    <<   >>  sin( cos( ln( sqrt( tan( num   #
    ['>', '>', '<', '<', '<', '>', '<', '>', '>', '>', '<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# +
    ['>', '>', '<', '<', '<', '>', '<', '>', '>', '>', '<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# -
    ['>', '>', '>', '>', '<', '>', '>', '>', '>', '>', '<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# *
    ['>', '>', '>', '>', '<', '>', '>', '>', '>', '>', '<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# /
    ['<', '<', '<', '<', '<', '=', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '0'],# (
    ['>', '>', '>', '>', '0', '>', '>', '>', '>', '>', '0', '>', '>', '0', '0', '0', '0', '0', '0', '>'],# )
    ['>', '>', '>', '>', '<', '>', '>', '>', '>', '>', '<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# %
    ['<', '<', '<', '<', '<', '>', '<', '>', '<', '>', '<', '<', '<', '<', '<', '<', '<', '<', '<', '>'],# ^
    ['<', '<', '<', '<', '<', '>', '<', '>', '>', '>', '<', '<', '<', '<', '<', '<', '<', '<', '<', '>'],# &
    ['<', '<', '<', '<', '<', '>', '<', '<', '<', '>', '<', '<', '<', '<', '<', '<', '<', '<', '<', '>'],# |
    ['>', '>', '>', '>', '<', '>', '>', '>', '>', '>', '<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# ~
    ['<', '<', '<', '<', '<', '>', '<', '>', '>', '>','<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# <<
    ['<', '<', '<', '<', '<', '>', '<', '>', '>', '>','<', '>', '>', '<', '<', '<', '<', '<', '<', '>'],# >>
    ['<', '<', '<', '<', '<', '=', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<','<', '0'],# sin(
    ['<', '<', '<', '<', '<', '=', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<','<', '0'],# cos(
    ['<', '<', '<', '<', '<', '=', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<','<', '0'],# ln(
    ['<', '<', '<', '<', '<', '=', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<','<', '0'],# sqrt(
    ['<', '<', '<', '<', '<', '=', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<', '<','<', '0'],# tan(
    ['>', '>', '>', '>', '0', '>', '>', '>', '>', '>', '<', '>', '>', '0', '0', '0', '0', '0', '0', '>'],# num
    ['<', '<', '<', '<', '<', '0', '<', '<', '<', '<', '0', '<', '<', '<', '<', '<', '<', '<', '<', '=']# # 
    ]
    word_map = {'+':0, '-':1, '*':2, '/':3, '(':4, ')':5, '%':6, '^':7, '&':8, '|':9, '~':10, '<<':11, '>>':12, 'sin(':13, 'cos(':14, 'ln(':15, 'sqrt(':16, 'tan(':17, 'num':18, '#':19}
    grammar = [('E','T', ''), ('T','M', ''), ('T','T|M', '|'), ('M','K', ''), ('M','M^K', '^'), ('K','F', ''), ('K','K&F', '&'), ('F','G', ''), ('F','F>>G', '>>'), ('T','F<<G', '<<'), ('G','H', ''), ('G','G-H', '-'), ('G','G+H', '+'), ('H','I', ''), ('H','H*I', '*'), ('H','H/J', '/'), ('H','H%J', '%')
               , ('I','J', ''), ('I','~J', '~'), ('J','num', ''), ('J','(E)', '('), ('J','sin(E)', 'sin('), ('J','cos(E)', 'cos('), ('J','tan(E)', 'tan('), ('J','ln(E)', 'ln('), ('J','sqrt(E)', 'sqrt(')]
    string = ''
    for i in token:
        string += i[2]



    cnt = 0
    stack = [('#','#','#')]
    token.append(('#','#','#'))
    table_text = []
    flag = -1
    while token != []:
        # print(stack)
        # print(token)
        cnt = cnt + 1
        a = token[0]
        x = -1
        for i in range(len(stack)-1,-1,-1):
            if stack[i][0] != '':
                # print(cnt)
                # print(stack[i][2])
                x = word_map[stack[i][2]]
                break
        
        if a[0] == 'number':
            y = word_map['num']
        else:
            y = word_map[a[2]]
        
        if priority_map[x][y] == '<':
            stack_string = ''
            string = ''
            for i in stack:
                stack_string += i[2]
            for i in token:
                if i[2] != a[2]:
                    string += i[2]
            table_text.append((str(cnt), stack_string, '<', a[2], string,'移进'))
            if a[0] == 'number':
                stack.append((a[0],a[1],'num'))    
            else:
                stack.append(a)
            token.remove(a)

        elif priority_map[x][y] == '>':
            stack_string = ''
            string = ''
            for i in stack:
                stack_string += i[2]
            for i in token:
                if i[2] != a[2]:
                    string += i[2]
            table_text.append((str(cnt), stack_string, '>', a[2], string,'归约'))
            
            nowy = y
            reduce_string = ''
            for i in range(len(stack)-1,-1,-1):
                if stack[i][0] == '': 
                    reduce_string = stack[i][2] + reduce_string
                elif priority_map[word_map[stack[i][2]]][nowy] == '>':
                    reduce_string = stack[i][2] + reduce_string
                    nowy = word_map[stack[i][2]]
                else:
                    break
            
            #print('reduce',reduce_string)
            after_reduce_string = ''
            for i in grammar:
                if i[1] == reduce_string:
                    after_reduce_string = i[0]
                    break
                if len(i[1]) >= 3 and len(reduce_string) >= 3:
                    # print('i   ',i[2])
                    # print(reduce_string[1:len(reduce_string)-1])
                    # print(reduce_string[:len(reduce_string)-2])
                    if i[2] == reduce_string[1:len(reduce_string)-1] or i[2] == reduce_string[:len(reduce_string)-2]:
                        after_reduce_string = i[0]
                        break
            #print("after ",after_reduce_string)
            nowy = y
            if after_reduce_string != '':
                for i in range(len(stack)-1,-1,-1):
                    if stack[i][0] =='': 
                        stack.remove(stack[i])
                    elif priority_map[word_map[stack[i][2]]][nowy] == '>':
                        nowy = word_map[stack[i][2]] 
                        stack.remove(stack[i])
                    else:
                        stack.append(('','',after_reduce_string))
                        #print(stack)
                        break
            else:
                table_text.append(('', '', '', '', '','拒绝'))
                flag = 1
                break
        elif priority_map[x][y] == '=':
            if len(stack) == 2 and stack[1][0] == '' and len(token) == 1 and token[0][0] == '#':
                table_text.append((str(cnt), '#'+stack[1][2], '<', '#', '','接受'))
                break
            stack_string = ''
            string = ''
            for i in stack:
                stack_string += i[2]
            for i in token:
                if i[2] != a[2]:
                    string += i[2]
            table_text.append((str(cnt), stack_string, '<', a[2], string,'移进'))
            if a[0] == 'number':
                stack.append((a[0],a[1],'num'))    
            else:
                stack.append(a)
            token.remove(a)
            cnt = cnt + 1
            a = token[0]
            stack_string = ''
            string = ''
            for i in stack:
                stack_string += i[2]
            for i in token:
                if i[2] != a[2]:
                    string += i[2]
            table_text.append((str(cnt), stack_string, '>', a[2], string,'归约'))
            stack.remove(stack[len(stack)-1])
            stack.remove(stack[len(stack)-1])
            stack.remove(stack[len(stack)-1])
            stack.append(('','','E'))                        
        else:
            table_text.append(('', '', '', '', '','拒绝'))
            flag = 2
            break
        
    info = ''
    if flag == 1:
        info = "Error:Reduction failed"
    elif flag == 2:
        info = "Error:Formula doesn't follow grammar rules"

    return table_text, string, info
        


def show(table_text, string):
    root = tk.Tk()
    root.title("对输入串 "+string+" 的算符优先归约过程")
    root.iconbitmap('misc/favicon.ico') 

    # 创建标题标签
    title_label = tk.Label(root, text="对输入串 "+string+" 的算符优先归约过程", font=("Arial", 12))
    title_label.pack(pady=10)
    
    # 创建表格
    table = ttk.Treeview(root,height=20)
    table["columns"] = ("Steps", "Stack", "PriorityRelationship", "CurrentSymbol", "RemainingInputString","ShiftOrReduce")
    # 显示表格并设置垂直滚动条
    vsb = ttk.Scrollbar(root, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    table.pack(expand=True, fill="both", pady=200) # 设置表格的初始高度
    # 设置表格的位置和大小
    table.place( width=500, height=800)
    # 设置列宽
    table.column("#0", width=0, stretch=tk.NO)
    table.column("Steps", width=100)
    table.column("Stack", width=150)
    table.column("PriorityRelationship", width=100)
    table.column("CurrentSymbol", width=100)
    table.column("RemainingInputString", width=150)
    table.column("ShiftOrReduce", width=100)
    
    # 设置列标题
    table.heading("#0", text="", anchor=tk.W)
    table.heading("Steps", text="步骤")
    table.heading("Stack", text="栈")
    table.heading("PriorityRelationship", text="优先关系")
    table.heading("CurrentSymbol", text="当前符号")
    table.heading("RemainingInputString", text="剩余输入串")
    table.heading("ShiftOrReduce", text="移进或归约")
    for i in table_text:
        table.insert("", tk.END, text=i[0], values=(i[0],i[1],i[2],i[3],i[4],i[5]))
        # 显示表格
    table.pack()
    
    # 运行主循环
    root.mainloop()
    
# show(analyse([('left','function','sin('), ('left','','('),
#     ('number','integer','1'), ('operator','logical','<<'),
#     ('number','integer','2'), ('right','',')'),
#     ('operator','arithmetic','+'), ('number','integer','3'),
#     ('operator','arithmetic','*'), ('number','integer','4'),
#     ('right','',')')]))
