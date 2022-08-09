import re
import csv
# import requests
import pprint
import os
import re
import cv2


plant_names = []
with open('plants.csv', 'r') as csv_file:
  csv_reader = csv.reader(csv_file)

  for line in csv_reader:

    regexLine = re.search("\(([^()]+)\)", line[0]).group()
    regexLine = regexLine.replace("(","")
    regexLine = regexLine.replace(")","")

    # print(regexLine)
    plant_names.append(regexLine)

# print(plant_names)

# url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG/1280px-Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG"
# split = url.split("/")
# last_item = split[-1]

# second_split = last_item.split("?")

# if len(second_split) > 1:
#   last_item = second_split[0]

# print(last_item)

# third_split = last_item.split("!")

# if len(third_split) > 1:
#   last_item = third_split[0]

#   print(last_item)


# four_split = last_item.split("px-")

# if len(four_split) > 1:
#   last_item = four_split[-1]

# print(last_item)

# web_header = {'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}

# result = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG/1280px-Pilea_cadierei_-_Copenhagen_Botanical_Garden_-_DSC07398.JPG", headers=web_header);

# pprint.pprint(result)


def check_images( s_dir, ext_list):
    bad_images=[]
    bad_ext=[]
    s_list= os.listdir(s_dir)
    for klass in s_list:
        klass_path=os.path.join (s_dir, klass)
        print ('processing class directory ', klass)
        if os.path.isdir(klass_path):
            file_list=os.listdir(klass_path)
            for f in file_list:               
                f_path=os.path.join (klass_path,f)
                index=f.rfind('.')
                ext=f[index+1:].lower()
                if ext not in ext_list:
                    print('file ', f_path, ' has an invalid extension ', ext)
                    bad_ext.append(f_path)
                    # if os.path.exists(f_path):
                    #     os.remove(f_path)
                    #     print(f"file removed: {f_path}")
                    # else:
                    #     print("The file does not exist")
                if os.path.isfile(f_path):
                    try:
                        img=cv2.imread(f_path)
                        shape=img.shape
                    except:
                        print('file ', f_path, ' is not a valid image file')
                        bad_images.append(f_path)
                        # if os.path.exists(f_path):
                        #     os.remove(f_path)
                        #     print(f"file removed: {f_path}")
                        # else:
                        #     print("The file does not exist")
                else:
                    print('*** fatal error, you a sub directory ', f, ' in class directory ', klass)
        else:
            print ('*** WARNING*** you have files in ', s_dir, ' it should only contain sub directories')
    return bad_images, bad_ext

source_dir =r'./plants'
good_exts=['jpg', 'png', 'jpeg', 'gif', 'bmp' ] # list of acceptable extensions
bad_file_list, bad_ext_list=check_images(source_dir, good_exts)
if len(bad_file_list) !=0:
    print('improper image files are listed below')
    for i in range (len(bad_file_list)):
        print (bad_file_list[i])
        if os.path.exists(bad_file_list[i]):
          os.remove(bad_file_list[i])
          print(f"file removed: {bad_file_list[i]}")
        else:
          print("The file does not exist")
else:
    print(' no improper image files were found')
