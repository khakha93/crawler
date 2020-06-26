import os
import urllib.request
import urllib.error


def make_directory(di):
    print('make image directory')
    if not os.path.isdir(di):
        os.mkdir(di)
    return


def img_url_2_file(img_src, abs_path):
    ret = 0
    if not os.path.exists(abs_path):
        try:
            urllib.request.urlretrieve(img_src, abs_path)
        except urllib.error.HTTPError:
            print('Http error')
            ret = -1
    else:
        print('This image file already exists!!')
    return ret





