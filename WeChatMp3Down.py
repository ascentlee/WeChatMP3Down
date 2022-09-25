from tkinter import *
from tkinter import messagebox
import time
import requests,re
import wget
root = Tk()
# 设置窗口前段显示
root.wm_attributes('-topmost',1)
#设置居中显示
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
width = 400
height = 260
size = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(size)
# 设置窗口标题及大小
root.title('微信网页mp3下载|QQ403096966')
#root['width'] = 310;root['height'] = 265
#设置接受UI界面中Entry的数据
url_input=Label(root,text='请在下方输入微信页面网址',width=21,height=1,font=("微软雅黑",12))
url_input.pack(side="top",pady=20)
t = Entry(root,width=40,font=("微软雅黑",12))
#设置entry获得焦点
t.focus_set()
t.pack(side="top",pady=5)
#设置右键菜单
def callback1(event=None):
    t.event_generate('<<Cut>>')
def callback2(event=None):
    t.event_generate('<<Copy>>')
def callback3(event=None):
    t.event_generate('<<Paste>>')
menu = Menu(root,tearoff=False)#bg="black",
menu.add_command(label="剪切", command=callback1)
menu.add_command(label="复制", command=callback2)
menu.add_command(label="粘贴", command=callback3)
def popup(event):
    menu.post(event.x_root, event.y_root)
t.bind("<Button-3>", popup)
def readurl(url):
    """
    获取某个网页的内容，并筛选出3个mp3的ID,返回mp3的ID的列表 
    """
    text = requests.get(url).text
    patt = r'voice_encode_fileid="(.*?)"' #匹配mediaid
    filename= r'size="\d+\.\d+" name="(.*?)"'# 匹配文件名
    ID_list = re.findall(patt,text)
    file_list= re.findall(filename,text)
    return ID_list,file_list
def downmp3(lst):
    """
    获取给定的某个网页下的mp3
    """
    num=len(lst[0])
    for p in range(num):
        path = 'https://res.wx.qq.com/voice/getvoice?mediaid='
        name = path + lst[0][p]  #组合生成下载地址
        wget.download(name,out=lst[1][p].replace("&nbsp;","")+".mp3")
    
def main():
    """调用tkinter，生成UI界面"""
    #设置按纽
    def b_showup():
        url=str(t.get())
        if url=="":
            messagebox.showinfo("错误提示！","请录入网址！")
        else:
            try:
                text=readurl(url)
                #print(text)
                start_time=time.time()
                downmp3(text)
                end_time=time.time()
                total_time=round(end_time-start_time,3)
                messagebox.showinfo("完成提示！",f"已经下载完成！共下载{len(text[0])}个mp3文件!,用时{total_time}s")
            except Exception as exc:
                messagebox.showinfo("警告！","网址错误！")
    def b_quitprog():
        root.destroy()
    def b_clear(event=None):
        t.delete(0,END)
    b_quit = Button(root,text="退出程序",width=10,height=1,font=("微软雅黑",12),command=b_quitprog)
    b_down = Button(root,text='清空内容',width=10,height=1,font=("微软雅黑",12),command=b_clear)
    b_show = Button(root,text='下载音频',fg="blue",width=10,height=1,font=("微软雅黑",12),command=b_showup)
    b_quit.pack(side="left",padx=13)
    b_show.pack(side="left")
    b_down.pack(side="left")
    root.mainloop()
main()