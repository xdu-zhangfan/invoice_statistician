# 说明：    发票文件必须为.pdf后缀（大小写不敏感），格式为“发票项目名称-金额.pdf”；
#           发票项目名称和金额之间必须使用小写横杠“-”进行连接；
#           发票项目名称中不能包含小写横杠“-”；
#           金额可以为小数或者整数，整数必须有至少一位，若无小数部分则不需要写小数点，有小数点的情况下小数位数至少应该有1位（也就是遵照一般阿拉伯数字命名规则）；
#           不能解析的文件名如：“射频模块-5..pdf”（有小数点但是小数位数为0位）、“射频模块-1-5.pdf”（“-1”无法作为发票项目名称解析，这样解析出来的发票项目名称将会是“射频模块”）

import os
import re
import csv
import datetime
import colorama
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from colorama import Fore

colorama.init()


def button_seldir_callback():
    path = filedialog.askdirectory()

    if path != '':
        label_dir.config(text=path)
    else:
        label_dir.config(text='您没有选择任何文件')

    return


def button_gen_callback():

    path = str(label_dir.cget("text")) + "/"
    filename = str(text_csvfname.get("1.0", "end"))[:-1]

    if path == "/":
        messagebox.askokcancel(title='提示', message='没有选择目录')
        return

    if filename == "":
        messagebox.askokcancel(title='提示', message='没有输入CSV文件的主文件名')
        return

    csv_file_name = path + filename + ".csv"
    print(csv_file_name)

    money_regular_expression = "((\d+)|(\d{1,}\.?\d{0,})).pdf"
    name_regular_expression = "^[\u4e00-\u9fa5_a-zA-Z0-9]{0,}-"

    datanames = os.listdir(path)
    main_dict = {}
    for filename in datanames:
        try:
            money_pre_res = re.search(
                money_regular_expression, filename, re.I).group(0)
            money_pre_res = money_pre_res[:-4]
            money = float(money_pre_res)

            name_pre_res = re.search(name_regular_expression, filename, re.I | re.U).group(
                0
            )
            name_pre_res = name_pre_res[:-1]

            main_dict[name_pre_res] = money
        except:
            print(Fore.RED + 'Invalid file name "' + filename + '".')
            print(
                Fore.RED
                + 'Please ensure that the format of the name of each file is "name-amount.pdf"'
            )

    print(Fore.RESET + "Total items: ", len(main_dict))

    # Check for duplicate invoice amounts
    all_money = {}
    for i in main_dict:
        if str(main_dict[i]) in all_money.keys():
            all_money[str(main_dict[i])] += 1
        else:
            all_money[str(main_dict[i])] = 1

    for i in all_money:
        if all_money[i] > 1:
            print(
                Fore.YELLOW
                + "Warning: money "
                + str(i)
                + " repeated "
                + str(all_money[i])
                + " times."
            )

    # Write .csv file
    rows = [("Item", "Money")]
    amount = 0
    for i in main_dict:
        rows.append((i, main_dict[i]))
        amount += main_dict[i]

    rows.append(("Total", str(amount)))
    rows.append(("Date", datetime.datetime.now()))

    with open(csv_file_name, "w", encoding="utf8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    messagebox.askokcancel(title='提示', message='已经创建CSV文件')
    return


window = tk.Tk()
window.title("电子发票统计器")
window.geometry('450x300')

label_dir = tk.Label(window, text="", font=('宋体', 10), padx=7, pady=7,
                     borderwidth=1, width=40, height=1, anchor='w', relief='solid')
button_seldir = tk.Button(
    window, text='Select directory', anchor='w', command=button_seldir_callback)
text_csvfname = tk.Text(window, font=('宋体', 10), padx=7, pady=7,
                        borderwidth=1, width=40, height=1, relief='solid')
button_gen = tk.Button(window, text='Generate CSV', anchor='w',
                       command=button_gen_callback)

label_dir.grid(row=0, column=0)
button_seldir.grid(row=0, column=1)
text_csvfname.grid(row=1, column=0)
button_gen.grid(row=1, column=1)


if __name__ == "__main__":
    window.mainloop()
