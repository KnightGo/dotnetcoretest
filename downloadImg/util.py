#!/usr/bin/python3

def saveimg(img_byte,code,filePath):
    filename = filePath + code+".png"
    with open(filename, "wb") as f:
            f.write(img_byte) # 将内容写入图片
                  


