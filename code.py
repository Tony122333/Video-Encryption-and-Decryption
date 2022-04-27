import streamlit as st
import random as rd
import numpy as np
import os
import cv2
subkeys=[]
keys=[subkeys]
# Phase-1 -> Encryption
def encryption(video_name):
    cam = cv2.VideoCapture(video_name)
    x = int(cam.get(cv2.CAP_PROP_FPS))
    try:
        if not os.path.exists('Phase-1_Part-1 Video Frames'):
            os.makedirs('Phase-1_Part-1 Video Frames')
    except OSError:
        print('Error: Creating directory of data!')
    try:
        if not os.path.exists('Phase-1_Part-2 Video Frames'):
            os.makedirs('Phase-1_Part-2 Video Frames')
    except OSError:
        print('Error: Creating directory of data!')
    ret, frame = cam.read()
    x1 = 0
    while (True):
        ret, frame = cam.read()
        x1 += 1
        if ret:
            name = './Phase-1_Part-1 Video Frames/frame' + str(x1) + '.jpg'
            cv2.imwrite(name, frame)
            image_input = cv2.imread(name)
            h,w,c=image_input.shape
            image = []
            for i in range(h):
                arr = []
                for j in range(w):
                    color = image_input[i,j]#color = b,g,r
                    key = [rd.randrange(0, 255, 2), rd.randrange(0, 255, 2), rd.randrange(0, 255, 2)]
                    pixel_encrypted =  [color[0]^key[0],color[1]^key[1],color[2]^key[2]]
                    subkeys.append(key)
                    arr.append(pixel_encrypted)
                image.append(arr)
                keys.append(subkeys)
            img = np.asarray(image)
            name1 = './Phase-1_Part-2 Video Frames/frame' + str(x1) + '.jpg'
            cv2.imwrite(name1, img)
        else:
            break
    st.write("Successfully Encrypted!")
    output = './enc.mp4'
    dir_path = './Phase-1_Part-2 Video Frames'
    files = os.listdir("./Phase-1_Part-2 Video Frames")

    img_array = []
    for f in files:
      img = cv2.imread(dir_path + "/" + f)
      img_array.append(img)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(output, fourcc, x, (img_array[0].shape[1], img_array[0].shape[0]))
    for i in range(len(img_array)):
      out.write(img_array[i])
    out.release()
    st.video('./enc.mp4')
# Phase-2 -> Decryption
def decryption(video_name):
    cam = cv2.VideoCapture(video_name)
    x = int(cam.get(cv2.CAP_PROP_FPS))
    try:
        if not os.path.exists('Phase-2_Part-1 Video Frames'):
            os.makedirs('Phase-2_Part-1 Video Frames')
    except OSError:
        print('Error: Creating directory of data!')
    try:
        if not os.path.exists('Phase-2_part-2 Video Frames'):
            os.makedirs('Phase-2_part-2 Video Frames')
    except OSError:
        print('Error: Creating directory of data!')
    x1 = 0
    while (True):
        ret, frame = cam.read()
        x1 += 1
        if ret:
            name = './Phase-2_Part-1 Video Frames/frame' + str(x1) + '.jpg'
            cv2.imwrite(name, frame)
            xl = 0
            arr = frame
            h,w,c = arr.shape
            image = []
            for i in range(h):
                arrs = []
                for j in range(w):
                    color = arr[i][j]  # color = b,g,r
                    pixel_encrypted = [color[0] ^ subkeys[xl][0], color[1] ^ subkeys[xl][1], color[2] ^ subkeys[xl][2]]
                    xl += 1
                    arrs.append(pixel_encrypted)
                image.append(arrs)
            img = np.asarray(image)
            name1 = './Phase-2_part-2 Video Frames/frame' + str(x1) + '.jpg'
            cv2.imwrite(name1, img)
        else:
            break
    st.write("Successfully Decrypted!")
    output = './dec.mp4'
    dir_path = './Phase-2_part-2 Video Frames'
    files = os.listdir("./Phase-2_part-2 Video Frames")
    img_array = []
    for f in files:
      img = cv2.imread(dir_path + "/" + f)
      img_array.append(img)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(output, fourcc, x, (img_array[0].shape[1], img_array[0].shape[0]))
    for i in range(len(img_array)):
      out.write(img_array[i])
    out.release()
    st.video('./dec.mp4')

if __name__ == '__main__':
    st.markdown("<h1 style='text-align: center; color: red;'>VIDEO</h1>", unsafe_allow_html=True)
    #st.write()
    st.markdown("<h1 style='text-align: center; color: red;'>Encryption & Decryption</h1>", unsafe_allow_html=True)
    #st.title("VIDEO\n", "center")
    #st.header("Encryption-n-Decryption")
    uploaded_file = st.file_uploader('FILE UPLOAD')
    print(uploaded_file)
    if uploaded_file:
        st.video(uploaded_file)
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    encrypt = col1.button("ENCRYPT")
    col2.write("                           ")
    col3.write("                           ")
    col4.write("                           ")
    col5.write("                           ")
    col6.write("                           ")
    decrypt = col7.button("DECRYPT")
    if encrypt:
        encryption(uploaded_file.name)
    if decrypt:
        decryption('./enc.mp4')