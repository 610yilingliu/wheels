import os
import time
import math
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.io


def de_project(np_arr):
    """
    project numpy array from [-1, 1] to [0, 255] for visualization
    """
    item = (np_arr +1)*255 / 2
    return item.astype(np.int32, copy=True) 

def time_helper(seperator = '_', to_sec = False):
    """
    return a string like 2020_09_11_22_43_00 (if to_sec is True) or 2020_09_11_22_43 (if to_sec is False)
    """
    localtime = time.asctime(time.localtime(time.time()))
    if to_sec:
        return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M" + seperator + "%S", time.localtime()) 
    return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M", time.localtime()) 

def show_imgs(np_arr, dest_path, specific_sep = None, specific_suf = None, show_num = None, show = False):
    """
    :type np_arr: numpy array contains images
    :type dest_path: String, destination folder to export images
    :type specific_sep: String, seperator inside output file name. like 2020_01_01_01_01.png or 202001010101.png
    :type specific_suf: String, if you specific a suffix like a, the filename will be 2020_01_02_01_01_a.png
    :type show_num: int. How many number of pictures will be shown in the plot
    """
    make_dir(dest_path)
    if show_num is None:
        data_size = np_arr.shape[0]
    else:
        data_size = min(show_num, np_arr.shape[0])
    plot_size = int(math.sqrt(data_size))
    l = plot_size
    if l == 0:
        print('empty numpy array')
        return
    h = data_size // l if data_size % l == 0 else (data_size // l) + 1
    plt.figure(figsize=(8, 8))
    for i in range(data_size):
        p = plt.subplot(h, l, i + 1)
        p.axis('off')
        # HWC to CHW
        new = np_arr[i].transpose((1, 2, 0))
        plt.imshow(new)
    f = plt.gcf()
    if show:
        plt.show()
        
    plt.draw()
    if specific_suf and specific_sep:
        fname = time_helper(specific_sep) + specific_sep + specific_suf
    elif specific_sep:
        fname = time_helper(specific_sep)
    elif specific_suf:
        fname = time_helper() + '_' + specific_suf
    else:
        fname = time_helper()
    name = dest_path + '/' + fname + '.png'
    f.savefig(name)
    try:
        f.savefig(name)
    except:
        print('The file name you defined is ' + name + ', please make sure that there are no system-rejected symbol in file name.\n')
        print('Program terminated...')
        exit(0)
    plt.close()

## Export system output to a log file
class Logger(object):
    def __init__(self, filename='dcgan.log', stream=sys.stdout):
	    self.terminal = stream
	    self.log = open(filename, 'a')

    def write(self, message):
	    self.terminal.write(message)
	    self.log.write(message)

    def flush(self):
	    pass


def loss_graph(losses, dest_path, name):
    make_dir(dest_path)
    fig, ax = plt.subplots()
    losses = np.array(losses)
    plt.plot(losses.T[0], label='Discriminator', alpha=0.5)
    plt.plot(losses.T[1], label='Generator', alpha=0.5)
    plt.title("Training Losses")
    plt.legend()
    f = plt.gcf()
    plt.draw()
    f.savefig(dest_path + '/' + name)
    plt.close()


def pic_to_npz(path, outname, target_folder = None):
    """
    :type path: String, folder that stores pictures
    :type outname: String, name of the output .npz file. Remember you do not have to input '.npz' suffix.
    :type target_folder: root path of the 
    """
    if not os.path.exists(path):
        print(path + ' not exists')
        return
    x = []
    files = os.listdir(path)
    for f in files:
        img = cv2.imread(path + '/' + f)
        img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = img.transpose((2,0,1))
        x.append(img)
    if target_folder is None:
        np.savez(outname, train = x)
    else:
        make_dir(target_folder)
        np.savez(target_folder + '/' + outname, train = x)

def mat_tonpz(mat_file, outname, target_folder = None):
    """
    :type mat_file: String, path of a .mat file
    :type outname: String, name of the output(not the whole path name)
    :type target_folder: String, name of the folder to export .npz file
    
    ### Explain:

    After you read `.mat` file with scipy, the data that stores in your memory is a dictionary. For dataset that Yuliya is using,
    the dictionary has two keys with data: 'X' and 'y' (You can view the datatype by add some break points in your ide(not Jupyter Notebook!)), and enter debug mode to run. The data we export is numpy in 'X', which are images we want.
    One thing you have to be careful in .mat file is that the first three keys in that file are not data, these keys are listed in set invalid in the 
    following code, you need to skip it
    """
    data = scipy.io.loadmat(mat_file)
    invalid = ('__header__', '__version__', '__globals__')
    for key in data:
        if key in invalid:
            continue
        ## Only store X data
        train_data = data[key]
        ## Original data is in HWCN style (height, width, channel, images). TF GPU version calculates NCHW faster, but matplotlib.pyplot and TF CPU version requires NHWC. 
        ## Transpose it into NCHW for tf, and we will do NHWC for plotting in visualize_tools.show_image()
        ## The reason why GPU prefers NCHW format explained here(in Chinese, use Google translate if you cannot read it):
        ## https://blog.csdn.net/weixin_37801695/article/details/86614566
        train_data = train_data.transpose((3, 2, 0, 1))
        if target_folder is None:
            np.savez(outname, train = train_data)
        else: 
            make_dir(target_folder)
            np.savez(target_folder + '/' + outname, train = train_data)
        break


def make_dir(path):
    """
    :type path: String. Only separator '/' is supported
    
    This is a helper function to build an directory. os.mkdir does not allow you to create floder like `./abc/def`, you must create `./abc` first
    and create `./abc/def` inside it
    """
    path = path.split('/')
    cur = './'
    for i in range(len(path)):
        if path[i] == '' or path[i] == '.':
            continue
        cur = cur + '/' + path[i]
        if not os.path.exists(cur):
            try:
                os.mkdir(cur)
            except:
                print('Something Strange happend while creating directory ' + cur + '\n')
                return