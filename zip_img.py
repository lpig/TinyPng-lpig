#!/usr/bin/python
# encoding=utf-8

import os
import sys
import getopt
from multiprocessing import Pool
import tinify


tinify.key = "zEBHCcjmE6XhTx368FdwkOKyNd-boIdo"
poolLimite = 10
orver_write = False
file_path = ""

opts, args = getopt.getopt(sys.argv[1:], "hi:o:r:")


for op, value in opts:
    if op == "-i":
        file_path = value
    elif op == "-r":
        orver_write = True
        file_path = value
    elif op == "-h":
        print("使用方法- python zip_img.py -i FILE_PATH")
    else:
        print("please use -h get help")


def zipimg(path, file_path):
    source = tinify.from_file(path)
    name = path.split('/')[-1]

    if not orver_write:
        out_path = os.path.join(file_path, "out_put")
        if not os.path.exists(out_path):
            os.mkdir(out_path)
    else:
        out_path = file_path

    source.to_file("%s/%s" % (out_path, name))


def main(file_path):
    filePaths = []

    if not file_path:
        print "file_path error!!"
        return

    # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(file_path):
        # for dirname in dirnames: #输出文件夹信息
        #     print("parent is:" + parent)
        #     print("dirname is" + dirname)
        #     outDir = os.path.join(output_doc_path, os.path.relpath(
        #         os.path.join(parent, dirname), input_doc_path))
        #     if not os.path.exists(outDir):
        #         os.mkdir(outDir)

        for filename in filenames:  # 输出文件信息
            # print("parent is:" + parent)
            # print("filename is:" + filename)
            filePaths.append(os.path.join(parent, filename))

    pngFilePaths = filter(lambda x: os.path.splitext(
        x)[1] == '.png' or os.path.splitext(x)[1] == '.jpg', filePaths)
    # print('Parent process %s.' % os.getpid())

    p = Pool(poolLimite)
    for fileName in pngFilePaths:
        p.apply_async(zipimg(fileName, file_path))

    p.close()
    p.join()

    print "All Done!!XD"
    if not orver_write:
        print("Your image is in %s" % os.path.join(file_path, "out_put"))
    else:
        print("Your image is in %s" % file_path)

if __name__ == "__main__":

    if os.path.isdir(file_path):
        main(file_path)
    elif "-h" not in sys.argv:
        print("please use -h get help")
