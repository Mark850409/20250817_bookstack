---
title: HEXONEXT主題客製化設定
updated: 2024-07-23 13:29:15Z
created: 2023-08-04 08:26:29Z
tags:
  - hexo
---

# 1. HEXONEXT主題客製化設定

## 1.1. 簡介
學習如何用hexo客製化開發原生next主題

## 1.2. 目錄

- [1. HEXONEXT主題客製化設定](#1-hexonext主題客製化設定)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
    - [1.2.1. 設定大頭貼](#121-設定大頭貼)
    - [1.2.2. 建立相片集](#122-建立相片集)
      - [1.2.2.1. 事前準備](#1221-事前準備)
      - [1.2.2.2. 開始撰寫腳本](#1222-開始撰寫腳本)
      - [1.2.2.3. python腳本](#1223-python腳本)
      - [1.2.2.4. 開始執行腳本](#1224-開始執行腳本)
      - [1.2.2.5. 看到此畫面表示佈署成功](#1225-看到此畫面表示佈署成功)
    - [1.2.3. gittalk留言板配置](#123-gittalk留言板配置)
      - [1.2.3.1. 進入此網址開始建立第 方認證登入](#1231-進入此網址開始建立第-方認證登入)
      - [1.2.3.2. 填寫以下相關內容後，點選update application](#1232-填寫以下相關內容後點選update-application)
      - [1.2.3.3. 建立client secrets，由於金鑰只會產生 次，因此請先複製到記事本或剪貼簿存放](#1233-建立client-secrets由於金鑰只會產生-次因此請先複製到記事本或剪貼簿存放)
      - [1.2.3.4. 打開next主題目錄下的\_config.xml，搜尋到gitalk，依據以下內容進行建立](#1234-打開next主題目錄下的_configxml搜尋到gitalk依據以下內容進行建立)
      - [1.2.3.5. 開啟下方指令介面，輸入hexo clean \&\& hexo g \&\& hexo d](#1235-開啟下方指令介面輸入hexo-clean--hexo-g--hexo-d)
      - [1.2.3.6.建立 個倉庫，請將倉庫選擇public，否則會找不到](#1236建立-個倉庫請將倉庫選擇public否則會找不到)
      - [1.2.3.7. 以下為倉庫建立成功之畫面](#1237-以下為倉庫建立成功之畫面)
      - [1.2.3.8. 登入hexo部落格，點選github登入，可看到以下畫面](#1238-登入hexo部落格點選github登入可看到以下畫面)
      - [1.2.3.9. 測試 下留言，可以留言成功!!!](#1239-測試-下留言可以留言成功)
      - [1.2.3.10. 留言後的內容可以到倉庫的issue去查看](#12310-留言後的內容可以到倉庫的issue去查看)
    - [1.2.4. 同場佳映](#124-同場佳映)
      - [1.2.4.1. 請先建立目錄存放金鑰](#1241-請先建立目錄存放金鑰)
      - [1.2.4.2.  以下為此次實作參考連結](#1242--以下為此次實作參考連結)



### 1.2.1. 設定大頭貼

- 開啟themes下的_config.yml，更改url網址

![](https://markweb.idv.tw/uploads/upload_bfec6a30d4384961f4013dd14a56a41f.png)

- 建立hexo專用相簿

![](https://markweb.idv.tw/uploads/upload_51d9edeeaa079a38c7c92040f3d1f8da.png)

- 點選分享按鈕複製相片連結

![](https://markweb.idv.tw/uploads/upload_e19327eace8e67e4294a3b896cdb8fc3.png)

- 點選複製圖片位址

![](https://markweb.idv.tw/uploads/upload_e7a084eac8cf201160458b8b76a4da65.png)

- 找到avatar的url選項，複製並貼上url

![](https://markweb.idv.tw/uploads/upload_18d5c392a77c4ff9fa2ea7a85f9db5dd.png)

- 輸入以下指令重新佈署hexo

```bash
hexo clean && hexo g && hexo d
```

![](https://markweb.idv.tw/uploads/upload_ce82cdedc1fb4f7fc48f795cdb24a4c1.png)

- 看到此畫面表示佈署成功

![](https://markweb.idv.tw/uploads/upload_7aa447904921bbf8fc6ba8b6b71835a7.png)

- enjoy

![](https://markweb.idv.tw/uploads/upload_4afb28479c20048bd1f1463e387b2317.png)

* * *

<!--more-->

### 1.2.2. 建立相片集

#### 1.2.2.1. 事前準備



1. 準備python腳本(進行圖片壓縮、轉檔)

2. 準備自動上傳腳本

3. 準備存放照片的目錄(照片可從nextcloud透過腳本複製到此目錄)



![](https://markweb.idv.tw/uploads/upload_b105a823e015c573949638b8e110b391.png)

#### 1.2.2.2. 開始撰寫腳本

```bash
# 2 !/bin/bash
# 3 
# 4 自動上傳照片到HEXO
# 5 

# 6 日期參數
date=$(date +%Y-%m-%d)
datetime=$(date +%Y-%m-%d_%H:%M)
# 7 ==============================================================
# 8 檔案複製、刪除參數
photocount=20
scriptpath=/home/markhsu/photowall
soucephoto=/media/markhsu/Data3/DockerProtainer/nextcloud/web/data/admin/files/photo/20230501/*.jpg
targetphoto="/home/markhsu/photowall/photo/$date"
photopath=/home/markhsu/photowall/photo
foldername=OutputPhoto
photolistpath="/var/lib/docker/volumes/53007dfd70be43e0e378796a257dc26ee4a78213d19b2ea8e6e4d680be2a09cc/_data/blog/themes/next/source/photo/"
photolist=photoslist.json
# 9 =============================================================
# 10 git參數
gitemail="xiaoyan850409@gmail.com"
gitname="markhsu"
gitcommit="$gitname在$datetime更新了照片..."
giturl="https://markhsu:mark850409@markweb.idv.tw:8443/markhsu/20230627_hexo_photowall.git"
# 11 ==============================================================
# 12 hexo參數
hexopath="/var/lib/docker/volumes/53007dfd70be43e0e378796a257dc26ee4a78213d19b2ea8e6e4d680be2a09cc/_data/blog"
## 12.1 ===========刪除json、photo下所有目錄及檔案並重新建立=========#
rm -f $photolistpath$photolist
rm -rf $photopath/*
mkdir -p $photopath/$foldername
## 12.2 ===========隨機複製指定目錄照片20張=========#
mkdir -p $photopath/$date
shuf -zn$photocount -e $soucephoto | xargs -0 cp -vt $targetphoto
## 12.3 ===========切換到指定目錄執行python腳本=========#
cd $scriptpath
python3 phototool.py
## 12.4 ===========git指定目錄初始化，並將圖片自動上傳至gitea(目前無大小限制)=========#
git init
git config --global user.email $gitemail
git config --global user.name $gitname
git config --global credential.helper cache
git add --all
git commit -am $gitcommit
git config credential.helper store
git push --set-upstream $giturl master
## 12.5 ===========hexo重新佈署=========#
cd $hexopath
hexo clean && hexo d && hexo g
```

#### 1.2.2.3. python腳本

```python
# 13 !/usr/bin/env python
# 14 -*- coding:utf8  -*-
import os
import glob
from PIL import Image, ExifTags
import json
from datetime import date
config = {
    # gitea倉庫儲存目錄
    "github_img_host_base": "/media/markhsu/Data3/DockerProtainer/gitea/data/git/repositories/markhsu/20230627_hexo_photowall.git",
    # 上傳圖片目錄(含子目錄會自動掃描)
    "img_path": "/home/markhsu/photowall/photo",
    # 圖片URL前綴
    "cdn_url_prefix": "https://markweb.idv.tw:8443/markhsu/20230627_hexo_photowall/raw/branch/master/photo/OutputPhoto/",
    # hexo指定格式json文件
    "photo_info_json": "/var/lib/docker/volumes/53007dfd70be43e0e378796a257dc26ee4a78213d19b2ea8e6e4d680be2a09cc/_data/blog/themes/next/source/photo/photoslist.json",
    "source_photo":"/home/markhsu/photowall/photo/",
    "target_photo":"/home/markhsu/photowall/photo/OutputPhoto/"
    
}
# 15 压缩图片到 90%(目的是为了移除 些gps 等信息，并非真的为了压缩）
def compress_img(img_path, rate=0.99, override=False):
    support_ftype_list = ["png", "PNG", "jpeg", "JPEG", "gif", "GIF", "bmp"]
    sp_img = img_path.split(".")
    if not sp_img or sp_img[-1] not in support_ftype_list:
       print("not support image type:{0}", img_path)
       return False
    sp_img = img_path.split("/")
    if not sp_img:
        print("please give the right image path:{0}", img_path)
        return False
    img_full_name = sp_img[-1]
    img_name = img_full_name.split(".")[0]
    img_type = img_full_name.split(".")[1]
    img_path_prefix = img_path[: -len(img_full_name)]

    # 覆盖原图或者另存为
    compress_img_path = ""
    if override:
        compress_img_path = img_path
    else:
        compress_img_path = "{0}{1}_com.{2}".format(img_path_prefix, img_name, img_type)

    img = Image.open(img_path)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except Exception as e:
        print("catch exception:{0}", e)

    try:
        original_size = img.size
        length = original_size[0]
        height = original_size[1]
        new_length = int(length * rate)
        new_height = int(height * rate)
        print("originla length:{0} height:{1}", length, height)
        print("after compress length:{0} height:{1}", new_length, new_height)
        img = img.resize((new_length, new_height), Image.ANTIALIAS)
        img.save(compress_img_path, img_type)
        print("save compress img {0}".format(compress_img_path))
        return True
    except Exception as e:
        print("catch exception:{0}", e)

    return False


# 16 对 img_path 目录下的文件夹递归生成缩略图保存到同目录下
def thumbnail_pic(github_img_host_base, img_path, cdn_url_prefix):
    # 删除最后 个 '/'
    if img_path[-1] == "/":
        img_path = img_path[:-1]
    if github_img_host_base[-1] == "/":
        github_img_host_base = github_img_host_base[:-1]
    if cdn_url_prefix[-1] == "/":
        cdn_url_prefix = cdn_url_prefix[:-1]

    photo_info_list = []

    for item in os.listdir(img_path):
        print(item)
        abs_item = os.path.join(img_path, item)
        if os.path.isdir(abs_item):  # sub-dir
            sub_img_path = abs_item
            print("cd dir:{0}".format(sub_img_path))
            sub_photo_info_list = thumbnail_pic(
                github_img_host_base, sub_img_path, cdn_url_prefix
            )
            photo_info_list.extend(sub_photo_info_list)
        else:  # file
            ftype = item.split(".")
            if not ftype or len(ftype) != 2:
               print("error: invalid file:{0}".format(item))
               continue
            fname = ftype[0]  # a.png -> a
            ftype = ftype[1]  # a.png -> png
            support_ftype_list = ["png", "PNG", "jpeg", "JPEG", "gif", "GIF", "bmp"]
            if ftype not in support_ftype_list:
               print(
                  "error: file type {0} not support, only support {1}".format(
                        ftype, json.dumps(support_ftype_list)
                    )
                )
               continue

            abs_file = abs_item
            if item.find("_small") != -1:  # 这是缩略图
                continue
            small_file = "{0}_small.{1}".format(fname, ftype)
            abs_small_file = os.path.join(img_path, small_file)  # 缩略图绝对路径
            if os.path.exists(abs_small_file):
                # 对应的 _small 缩略图已经存在
                continue

            compress_status = compress_img(abs_file, 0.4, True)
            if not compress_status:
                print("compress_img fail:{0}", abs_file)
                continue

            im = Image.open(abs_file)
            original_size = im.size
            length = original_size[0]
            height = original_size[1]
            m = int(float(length) / 300.0)  # 计算缩小比例 (缩略图限制 300 长度)
            new_length = int(float(length) / m)
            new_height = int(float(height) / m)
            im.thumbnail((new_length, new_height))  # 生成缩略图
            im.save(abs_small_file, ftype)  # 保存缩略图
            print("save thumbnail img {0}".format(abs_small_file))
                            
            relative_file = abs_file[len(github_img_host_base) + 1 :]  # 计算相对路径，用来拼接 cdn
            relative_small_file = abs_small_file[len(github_img_host_base) + 1 :]

            cdn_url_file = "{0}/{1}".format(cdn_url_prefix, relative_file)
            cdn_url_small_file = "{0}/{1}".format(cdn_url_prefix, relative_small_file)

            # 格式: 690.690;8.png;http://cdn_file_url;http://cdn_small_file_url;
            line = "{0}.{1};{2};{3};{4}".format(
                length,
                height,
                item,
                cdn_url_file + small_file, #此處可以取到檔名，請加入small_file參數
                cdn_url_small_file + small_file, #此處可以取到檔名，請加入small_file參數
            )
            photo_info_list.append(line)

    # end for loop
    print("dir:{0} Done!".format(img_path))
    return photo_info_list


if __name__ == "__main__":
    github_img_host_base = config.get("github_img_host_base")
    img_path = config.get("img_path")
    cdn_url_prefix = config.get("cdn_url_prefix")
    photo_info_json = config.get("photo_info_json")
    source_photo = config.get("source_photo")
    target_photo = config.get("target_photo")

    photo_info_list = []
    photo_info_list_has = []
    counter = 0
    
    #圖片轉檔語法，請增加在產生縮略圖之前
    for image in glob.iglob(source_photo + '**/*.jpg', recursive=True):
        counter = counter + 1
        img = Image.open(image)
        today = date.today()
        img.save(target_photo +str(today)+'_'+str(counter)+'.png', "png")
    
    #產生縮略圖的function
    photo_info_list = thumbnail_pic(github_img_host_base, img_path, cdn_url_prefix)

    if os.path.exists(photo_info_json):
        with open(photo_info_json, "r") as fin:
            photo_info_list_has = json.loads(fin.read())
            fin.close()

    photo_info_list_has.extend(photo_info_list)  # 追加此次新增的 photo info

    with open(photo_info_json, "w") as fout:
        fout.write(json.dumps(photo_info_list_has, indent=2))
        print("save photo_info_list to {0}".format(photo_info_json))
        fout.close()

    print("\nAll Done")
```

#### 1.2.2.4. 開始執行腳本

```bash
sh autoUploadImageToHexo.sh
```

![](https://markweb.idv.tw/uploads/upload_deb0014cc4e415e3b0178aee73e44dc0.png)

#### 1.2.2.5. 看到此畫面表示佈署成功

![](https://markweb.idv.tw/uploads/upload_26c81e158f11ee5441afca059118f286.png)

* * *

### 1.2.3. gittalk留言板配置

#### 1.2.3.1. 進入此網址開始建立第 方認證登入

https://github.com/settings/applications/new

#### 1.2.3.2. 填寫以下相關內容後，點選update application

![](https://markweb.idv.tw/uploads/upload_f7ff04f6d6d03886c8a741df05f3b051.png)

#### 1.2.3.3. 建立client secrets，由於金鑰只會產生 次，因此請先複製到記事本或剪貼簿存放

![](https://markweb.idv.tw/uploads/upload_e30588d6ee4633c00836414eae95e91b.png)

#### 1.2.3.4. 打開next主題目錄下的_config.xml，搜尋到gitalk，依據以下內容進行建立

- github_id：請輸入所有者
- repo：請輸入倉庫名稱
- client\_id：請輸入剛才建立的client\_id
- client\_secret：請輸入剛才建立的client\_secret
- admin\_user：可輸入和github\_id 樣
- distraction\_free\_mode：可設定為true or false，呈現效果不同

![](https://markweb.idv.tw/uploads/upload_55a25c34e0bf234f31ac67a8d0b29e45.png)

#### 1.2.3.5. 開啟下方指令介面，輸入hexo clean && hexo g && hexo d

![](https://markweb.idv.tw/uploads/upload_a033148856c3d7913d7c37dd783e885d.png)

#### 1.2.3.6.建立 個倉庫，請將倉庫選擇public，否則會找不到

![](https://markweb.idv.tw/uploads/upload_ecac650abd08820114824a6169df5d09.png)

#### 1.2.3.7. 以下為倉庫建立成功之畫面

![](https://markweb.idv.tw/uploads/upload_c24e5da924e836a84f7527c4bcda5645.png)

#### 1.2.3.8. 登入hexo部落格，點選github登入，可看到以下畫面

![](https://markweb.idv.tw/uploads/upload_e5ba3444af0affdc332ccf11654c35e5.png)

#### 1.2.3.9. 測試 下留言，可以留言成功!!!

![](https://markweb.idv.tw/uploads/upload_5cd40e514eb33c7a4334f8f71f7770b3.png)

#### 1.2.3.10. 留言後的內容可以到倉庫的issue去查看

![](https://markweb.idv.tw/uploads/upload_d41d8636e89cb867cd5f92fecc997c1b.png)

### 1.2.4. 同場佳映


**腳本撰寫以下為參考連結**


https://rebootcat.com/2020/09/19/nextphotowall/

https://pinlyu.com/posts/31/

https://asdfv1929.github.io/2018/05/26/next-add-photos/

* * *

 如果想要每次照片呈現順序不同的話，可參考 下連結及程式碼 


```javascript
$.getJSON('js/questions1.json').done(function(data){
    window.questionnaire = data;
    window.questionnaire.sort(function() { return .5 - Math.random();});
    console.log(window.questionnaire);
    startGame();
});
```

https://stackoverflow.com/questions/30061969/select-random-object-from-json


隨機複製指定張數照片到指定目錄


1\. -zn 後面的數字為張數

2\. target/ 這個要替換為目的地目錄


```bash
shuf -zn8 -e *.jpg | xargs -0 cp -vt target/
```

https://unix.stackexchange.com/questions/217712/randomly-copy-certain-amount-of-certain-file-type-from-one-directory-into-anothe


如何設定自動上傳到gitea server呢?參考以下連結


#### 1.2.4.1. 請先建立目錄存放金鑰

![](https://markweb.idv.tw/uploads/upload_170fe734d6283271adc0ce3a7c35486d.png)

```bash
cat id_ed25519.pub
//輸出以下公開金鑰，請複製到gitea的管理SSH
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIILEuddyDHY5JpRtj5smouvZbhu0uBeUw2bqufWV5vLk root@markhsu-server
```

![](https://markweb.idv.tw/uploads/upload_0338e8c333b9ba75548d0fcf2a03a9d7.png)

![96091ea510658310d2bb769a13f0f22e.png](../../_resources/96091ea510658310d2bb769a13f0f22e.png)



> [!note] 小提示 
>  如果發現因為權限問題無法同步專案，請參考以下權限進行設定

| 檔案或資料夾                 | 權限設定 | 指令            |
| ---------------------- | ---- | ------------- |
| ~/.ssh/                | 700  | chmod 700 XXX |
| ~/.ssh/authorized_keys | 600  | chmod 600 XXX |
| ~/.ssh/config          | 600  | chmod 600 XXX |
| `~/.ssh/identity`      |      |               |
| `~/.ssh/id_dsa`        |      |               |
| `~/.ssh/id_rsa`        | 600  | chmod 600 XXX |
| `~/.ssh/identity.pub`  |      |               |
| `~/.ssh/id_dsa.pub`    |      |               |
| `~/.ssh/id_rsa.pub`    | 644  | chmod 644 XXX |

請先建立倉庫，記得設為公開，否則會無法存取圖片

![](https://markweb.idv.tw/uploads/upload_d8663f3e225abff65e34acfd7138537a.png)

![](https://markweb.idv.tw/uploads/upload_7a6108c3c86d63fbbce154e69d4b1011.png)


圖片連結不能取這 層，會找不到


![](https://markweb.idv.tw/uploads/upload_8d21fe82e8736830d02a65e44133230e.png)

![](https://markweb.idv.tw/uploads/upload_0622e1eeff41d6ca5c89b1af40db881f.png)

* * *

#### 1.2.4.2.  以下為此次實作參考連結

https://www.techaddressed.com/tutorials/add-verify-ssh-keys-gitea/

https://www.cnblogs.com/Gitea/p/ssh.html

https://superuser.com/questions/215504/permissions-on-private-key-in-ssh-folder