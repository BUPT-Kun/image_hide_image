import os
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tkinter as tk
from tkinter import *
from tkinter import filedialog   #导入文件对话框函数库
import imageio
from PIL import Image,ImageTk
#from SRGAN_model import Generator, Discriminator
import numpy as np




def Open_Img():
    global cover_img_png
    file_path = filedialog.askopenfilename()
    cover_img_png = imageio.v2.imread(file_path)
    wpath = r".\stego_img_png" + '/' + str('cover_img') + '.png'
    imageio.imwrite(wpath,
                    cover_img_png)
    #图像展示
    img = Image.open(wpath)
    pyt = ImageTk.PhotoImage(img)
    img1= tk.Label(b1, image=pyt)
    img1.grid()
    """
    plt.imshow(cover_img)  # 显示图片
    plt.title('cover')
    plt.axis('off')  # 不显示坐标轴
    plt.show()
    """

def Open_Img2():
    global se_img_png
    file_path2 = filedialog.askopenfilename()
    se_img_png = imageio.v2.imread(file_path2)
    wpath = r".\secret_img_png" + '/' + str('secret_img') + '.png'
    imageio.imwrite(wpath,
                    se_img_png)
    #图像展示
    img = Image.open(wpath)
    pyt = ImageTk.PhotoImage(img)
    img1= tk.Label(b2, image=pyt)
    img1.grid()

    """
    plt.imshow(se_img_png)  # 显示图片
    plt.title('secret')
    plt.axis('off')  # 不显示坐标轴
    plt.show()
    """

def Steganography():
    is_training = False
    batch_x = np.zeros([1, 256, 256, 3])
    batch_y = np.zeros([1, 256, 256, 3])
    global cover_img_png
    #cover_img_png = cover_img_png
    global se_img_png
    #se_img_png = se_img_png
    #EnCode = Encode()
    #EnCode.load_weights('./new/Fu_model_weight/' + 'encode170000.ckpt').expect_partial()
    generator = U_Net_S()

    generator.load_weights(r".\encode220000.ckpt").expect_partial()
    #generator.load_weights(r"C:\Users\W1therC\Desktop\实验结果\han ssim-0.25\encode290000.ckpt").expect_partial()

    batch_x[0, :, :, :] = cover_img_png
    batch_y[0, :, :, :] = se_img_png
    batch = tf.concat([batch_x, batch_y], 3)
    stego_img = generator(batch, is_training)
    wpath = r".\stego_img_png" + '/' + str('stego_img') + '.png'
    imageio.imwrite(wpath,
                    np.uint8(stego_img[0, :, :, :]))
    stego_img2 = np.uint8(stego_img[0, :, :, :])
    #图像展示
    img = Image.open(wpath)
    pyt = ImageTk.PhotoImage(img)
    img1= tk.Label(b3, image=pyt)
    img1.grid()
    '''
    plt.imshow(stego_img2)  # 显示图片
    plt.title('stego_img')
    plt.axis('off')  # 不显示坐标轴
    plt.show()
    '''

def Extract_img():
    is_training = False
    global se_img_png
    global cover_img_png
    global stego_img
    global excat_img
    batch_x = np.zeros([1, 256, 256, 3])
    discriminator = Extractor()
    discriminator.load_weights(r".\decode220000.ckpt").expect_partial()
    #discriminator.load_weights(r"C:\Users\W1therC\Desktop\实验结果\han ssim-0.25\decode290000.ckpt").expect_partial()
    file_path = filedialog.askopenfilename()
    stego_img2 = imageio.v2.imread(file_path)
    batch_x[0, :, :, :] = stego_img2
    excat_img = discriminator(batch_x, is_training)
    wpath = r".\secret_img_png" + '/' + str('extract_img') + '.png'
    imageio.imwrite(wpath,
                    np.uint8(excat_img[0, :, :, :]))
    excat_img2 = np.uint8(excat_img[0, :, :, :])
    #图像展示
    img = Image.open(wpath)
    pyt = ImageTk.PhotoImage(img)
    img1= tk.Label(b4, image=pyt)
    img1.grid()
    '''
    plt.imshow(excat_img2)  # 显示图片
    plt.title('extract_img')
    plt.axis('off')  # 不显示坐标轴
    plt.show()
    '''
# 创建窗口 设定大小并命名
root = Tk()
root.title('图隐图隐写器')
root.geometry('1200x600')

global cover_img_png
global se_img_png# 定义全局变量 图像的
global stego_img
global excat_img
var = tk.StringVar()    # 文字变量储存器


image = Image.open(r".\2.jpg")
photo = ImageTk.PhotoImage(image)
#photo = tk.PhotoImage(file=r"D:\pycharm project\stego-style transfer\UI\2.jpg")
canvas_root = Canvas(root, width=1200, height=600)
canvas_root.create_image(0, 0,anchor ="nw", image=photo)
canvas_root.pack()
# 创建打开图像和显示图像函数


# frame=Frame(root,height=2,width=3,bd=5,relief=RIDGE)
# frame.pack()
# 创建打开图像按钮
btn_Open = tk.Button(root,
    text='选择载体图像', font=('Helvetica', '15'),     # 显示在按钮上的文字
    bg='darkviolet',fg='gold',
    cursor='circle',
    width=15, height=2,activebackground='pink',activeforeground='red',
    command=Open_Img,
    relief=FLAT)     # 点击按钮式执行的命令
btn_Open.place(x=80,y=500)
    # 按钮位置

# 创建显示图像按钮
btn_Show = tk.Button(root,
    text='选择秘密图像', font=('Helvetica', '15'),     # 显示在按钮上的文字
    bg='darkviolet',fg='gold',activebackground='cyan',activeforeground='red',
    cursor='circle',
    width=15, height=2,
    command=Open_Img2)     # 点击按钮式执行的命令
btn_Show.place(x=372,y=500)
#btn_Show.pack()    # 按钮位置

btn_Steganography = tk.Button(root,
    text='隐写', font=('Helvetica', '15'),      # 显示在按钮上的文字
    bg='mediumpurple',fg='gold',activebackground='Gold',activeforeground='red',
    cursor='circle',
    width=15, height=2,
    command=Steganography)     # 点击按钮式执行的命令
btn_Steganography.place(x=648,y=500)
# btn_Steganography.grid(row=4,column=2)
# btn_Steganography.pack()    # 按钮位置

btn_Extract = tk.Button(root,
    text='提取秘密图像', font=('Helvetica', '15'),      # 显示在按钮上的文字
    bg='mediumpurple',fg='gold',activebackground='palegreen',activeforeground='red',
    cursor='circle',
    width=15, height=2,
    command=Extract_img)     # 点击按钮式执行的命令
btn_Extract.place(x=924,y=500)
#btn_Extract.pack()    # 按钮位置
#载体图片展示
b1 = tk.Frame(root,bd=3,width=256,height=256)
b1.pack()
b1.place(x=43,y=150)
#嵌入图片展示
b2 = tk.Frame(root,bd=3,width=256,height=256)
b2.pack()
b2.place(x=329,y=150)
#隐写完成后展示
b3 = tk.Frame(root,bd=3,width=256,height=256)
b3.pack()
b3.place(x=615,y=150)
#嵌入提取展示
b4 = tk.Frame(root,bd=3,width=256,height=256)
b4.pack()
b4.place(x=901,y=150)
'''
la1=tk.Label(root,text='载体图片',font=("微软雅黑", 14),anchor = "center",width=256,height=30)   # 定义一个名为la1的标签组件
la1.place(x = 43,y = 90)
la2=tk.Label(root,text='嵌入图片',font=("微软雅黑", 14),anchor = "center",width=256,height=30)   # 定义一个名为la2的标签组件
la2.place(x = 329,y = 90)
la3=tk.Label(root,text='隐写图片',font=("微软雅黑", 14),anchor = "center",width=256,height=30)   # 定义一个名为la3的标签组件
la3.place(x = 615,y = 90)
la4=tk.Label(root,text='提取图片',font=("微软雅黑", 14),anchor = "center",width=256,height=30)   # 定义一个名为la4的标签组件
la4.place(x = 901,y = 90)
'''


# 运行整体窗口
root.mainloop()

