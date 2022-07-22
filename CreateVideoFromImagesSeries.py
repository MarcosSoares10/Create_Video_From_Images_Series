import cv2 
import os
import shutil

def listFiles(path):
    lstFiles = []
    for dirName, subdirList, fileList in os.walk(path):
        for filename in fileList:
            lstFiles.append(os.path.join(dirName, filename))

    return lstFiles

def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def savePng(image, path, name):
    if not os.path.exists(str(path)):
        os.makedirs(str(path))
    cv2.imwrite(path+"/"+name+".png",image)


DirsNames = ["IMG"]

framerate = 30 #(FPS)
bitrate = 20000 #(kbps)
codec = "h264" #(FFmpeg flag for Encoder)
# You can find a list of available encoders and another paramenters that may interest you inside FFMPEG documentation

for dirN in DirsNames:
    if not os.path.exists(str(dirN)):
        continue
    
    DirName = dirN

    listFls = listFiles(DirName)

    outputPath = DirName+"_aux_tmp"

    numImages = len(listFls)

    for i in range(numImages):
        print(listFls[i])
        img = cv2.imread(listFls[i])

        # You can do any filter here with images if you wanna it
        # Example --> img = cv2.medianBlur(img,3)

        savePng(img, outputPath, "IMG"+str(i + 1).zfill(5)) # Making sure new file will be all the same extension

    os.system("ffmpeg -framerate "+str(framerate)+" -i "+outputPath+"/IMG%05d.png -codec copy "+outputPath+"/video_aux.mp4")
    os.system("ffmpeg -i " +outputPath+"/video_aux.mp4 -vcodec "+codec+" -b:v "+str(bitrate)+"k "+DirName+"/Result_video.mp4")

    remove(outputPath)