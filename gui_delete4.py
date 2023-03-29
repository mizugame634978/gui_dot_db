import tkinter as tk
import tkinter.ttk as ttk
import sqlite3


# SQLiteデータベースに接続
conn = sqlite3.connect('TEST.db')
cur = conn.cursor()

global_selected_table = ""


# GUIアプリケーションの作成#############
root = tk.Tk()
root.title("guiでDB確認")
root.geometry("400x300")
#root.resizable(False, False)
root.attributes('-fullscreen',True)


root.grid_rowconfigure(0,weight=1)
root.grid_columnconfigure(0,weight=1)

frame2=ttk.Frame(root)#frame2をつかい各flameを作る
frame2.rowconfigure(0,weight=1)
frame2.columnconfigure(0,weight=1)
frame2.grid(row=0,column=0,sticky="nsew")
scan_frame=tk.Frame(frame2,background="aquamarine1")#最初に出る画面
scan_frame.grid(row=0,column=0,sticky="nsew")
#####################

def get_char(flag):#検索ボタンを押した際の関数
    char1 =  textBox1.get()
    

    if flag == 0:#ターブル名を取得してselect


        sql = "select * from "+ char1
        
        cur.execute(sql)

    elif flag == 1:#テーブル名一覧を取得
        
        cur.execute('select name from sqlite_master where type="table"')
        
    textBox1.delete(0,tk.END)
    listbox.delete(0, tk.END)
    #cur.execute('SELECT * FROM book where book_name like %?',(char1,))
    for row in cur.fetchall():
        listbox.insert('end', row)


textBox1 = tk.Entry(font=("",30),width=50)#テキストボックスの横幅を設定,入力できる文字数？
textBox1.place(relx=0.1, rely=0.1,width=400,height=50)


label_textBox1 = tk.Label(scan_frame,text='Search')
label_textBox1.place(in_ =scan_frame,relx = 0.0, rely = 0.08)


listbox = tk.Listbox(scan_frame,font = ("",25),width=90,height=10)
listbox.place(in_ =scan_frame,relx = 0.5, rely = 0.2, anchor = tk.N)







# 選択された行を削除する関数(テーブルのプライマリーキーが一番左端にある必要がある)
def delete_item():
    index = listbox.curselection()[0]  # 現在選択されている項目のインデックス&項目を取得
    selected_book = listbox.get(index)    # 項目を取得
    sql = "select * from " + global_selected_table
    cur.execute(sql)
    row1 = cur.description[0]
    
    
    sql = "DELETE FROM " + global_selected_table + " WHERE " + str(row1[0]) + " = ?"# + str(selected_book[0])


    cur.execute(sql,(selected_book[0],))
    #↑テーブルの列ごとに配列に入れられる？ので1列目のbook_idを検索するため[0]を指定

    conn.commit()# コミットしないと登録が反映されない
    listbox.delete(index)#行を削除したのをgui上でも疑似反映

def gui_select():
    index =listbox.curselection()[0]  # 現在選択されている項目のインデックス&項目を取得
    selected = listbox.get(index)
    listbox.delete(0,tk.END)
    global global_selected_table
    global_selected_table = selected[0]
    #cur.execute('select sql from sqlite_master where type="table"')
    sql = "select * from " + selected[0]
    cur.execute(sql)
    hoge = ""
    for desc in cur.description:
        
        hoge = hoge + desc[0] +" | "
    listbox.insert('end',hoge)
    for row in cur.fetchall():
        listbox.insert('end', row)
    


# 削除ボタンを作成
delete_button = tk.Button( scan_frame,text='削除',font=18,width=30,height=10, command=delete_item)

delete_button.place(in_ =scan_frame,relx = 0.5, rely = 0.93, relwidth=0.6,relheight=0.1 ,anchor = tk.S)


get_button =  tk.Button(scan_frame,text='テーブル名で検索',font=18,width=10,height=10, command=lambda:get_char(0))
get_button.place(in_ =scan_frame,relx = 0.1, rely = 0.8, relwidth=0.1,relheight=0.1 ,anchor = tk.W)

get_buttonN =  tk.Button(scan_frame,text='テーブル名を表示',font=18,width=10,height=10, command=lambda:get_char(1))
get_buttonN.place(in_ =scan_frame,relx = 0.12, rely = 0.6, relwidth=0.1,relheight=0.1 ,anchor = tk.W)

get_buttonF =  tk.Button(scan_frame,text='テーブルの中を見る',font=18,width=10,height=10, command=gui_select)
get_buttonF.place(in_ =scan_frame,relx = 0.12, rely = 0.7, relwidth=0.1,relheight=0.1 ,anchor = tk.W)



root.mainloop()
