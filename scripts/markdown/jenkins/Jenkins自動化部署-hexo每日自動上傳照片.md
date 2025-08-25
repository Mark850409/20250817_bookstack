---
title: Jenkins自動化部署-hexo每日自動上傳照片
updated: 2024-07-23 13:29:47Z
created: 2023-10-06 08:54:27Z
latitude: 24.8387226
longitude: 121.0177246
altitude: 0
tags:
  - Jenkins
  - hexo
  - upload
  - photo
---

# 1. Jenkins(CICD)自動化佈署-hexo每日自動上傳照片

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]

## 1.1. 簡介

## 1.2. 專案結構

- [1. Jenkins(CICD)自動化佈署-hexo每日自動上傳照片](#1-jenkinscicd自動化佈署-hexo每日自動上傳照片)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 專案結構](#12-專案結構)
  - [1.3. 目錄](#13-目錄)
  - [1.4. 使用方式](#14-使用方式)
    - [1.4.1. 建立`Gitea`倉庫](#141-建立gitea倉庫)
  - [1.5. 執行步驟](#15-執行步驟)
    - [1.5.1. 在hexo事先建立相簿範本\&撰寫程式碼](#151-在hexo事先建立相簿範本撰寫程式碼)
    - [1.5.2. 撰寫Python腳本](#152-撰寫python腳本)
    - [1.5.3. 使用`Jenkins`設計腳本流程](#153-使用jenkins設計腳本流程)
    - [1.5.4. 建立 個作業流程，開始定義要傳入腳本的`參數`](#154-建立-個作業流程開始定義要傳入腳本的參數)
    - [1.5.5. 設定此`作業流程觸發`的時間，本案例為每日早上7:40觸發](#155-設定此作業流程觸發的時間本案例為每日早上740觸發)
    - [1.5.6. 撰寫`shell腳本`](#156-撰寫shell腳本)
    - [1.5.7. 設定建置後要觸發`email寄信`](#157-設定建置後要觸發email寄信)
    - [1.5.8. 請先`手動建置`執行，確認無誤後再使用`排程執行`](#158-請先手動建置執行確認無誤後再使用排程執行)
    - [1.5.9. 執行成功如附圖](#159-執行成功如附圖)

## 1.3. 目錄

```table-of-contents
title: 
style: nestedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
includeLinks: true # Make headings clickable
debugInConsole: false # Print debug info in Obsidian console
```


## 1.4. 使用方式

### 1.4.1. 建立`Gitea`倉庫

![](https://markweb.idv.tw/uploads/upload_061153df73075b68074b10aae76e3ea1.png)

<!--more-->
## 1.5. 執行步驟

### 1.5.1. 在hexo事先建立相簿範本&撰寫程式碼

進入hexo container `根目錄` 下，blog/theme/next/source/js/mygrid.js，撰寫以下腳本

- WindowPath：改成自己放置`hexo`的`圖片根目錄`
- imgDataPath：改成自己`json`格式路徑(請先確認此路徑在瀏覽器開啟可正常顯示資料)
- imgMaxNum：圖片呈現`數量`，可自行調整
- photoslist.json：透過Python程式產生特定格式的資料內容(請勿手動建立)

```javascript
// 获取网页不含域名的路径
var windowPath = 'https://markweb.idv.tw:23443/photo/';
console.log(windowPath);
// 图片信息文件路径
var imgDataPath = 'https://markweb.idv.tw:23443/photo/photoslist.json'; 
// 图片显示数量
var imgMaxNum = 20; 
// 获取窗口宽度（以确定图片显示宽度）
var windowWidth = window.innerWidth
|| document.documentElement.clientWidth
|| document.body.clientWidth;
if (windowWidth < 768) {
    var imageWidth = 145; // 图片显示宽度(手机)
} else {
    var imageWidth = 215; // 图片显示宽度
}
// 腾讯云图片处理样式（根据图片显示宽度）
var imgStyle = '!' + imageWidth + 'x';


// 图片卡片（照片页面）
if (windowPath.indexOf('photo') > 0 ) {
    var LinkDataPath = imgDataPath;
    photo ={
    page: 1,
    offset: imgMaxNum,
    init: function () {
        var that = this;
        $.getJSON(LinkDataPath, function (data) {
            window.questionnaire = data;
            window.questionnaire.sort(function() { return .5 - Math.random();});
            console.log(window.questionnaire);
            that.render(that.page, window.questionnaire);
        });
    },
    render: function (page, data) {
        var begin = (page - 1) * this.offset;
        var end = page * this.offset;
        if (begin >= data.length) return;
        var html, imgNameWithPattern, imgName, imageSize, imageX, imageY, li = "";
        
// Date object
const date = new Date();

let currentDay= String(date.getDate()).padStart(2, '0');

let currentMonth = String(date.getMonth()+1).padStart(2,"0");

let currentYear = date.getFullYear();

// we will display the date as DD-MM-YYYY 

let currentDate = `${currentYear}-${currentMonth}-${currentDay}`;

var ischeck=false;
        for (var i = begin; i < end && i < data.length; i++) {
                imgNameWithPattern = data[i].split(';')[1];  // a.png
                imgName = imgNameWithPattern.split('.')[0]  // a
                let result = imgName.includes(currentDate);
                imageSize = data[i].split(';')[0]; // length.height 
                imageX = imageSize.split('.')[0]; //  length
                imageY = imageSize.split('.')[1]; // height
			    cdn_url       = data[i].split(';')[2]; // 原图 cdn url
				small_cdn_url = data[i].split(';')[3]; // 缩略图 cdn url
                if(result){
                     li += '<div class="card" style="width:300px">' +
                        '<div class="ImageInCard" style="height:'+ 300 * imageY / imageX + 'px">' +
                            '<a data-fancybox="gallery" href="' + cdn_url + '" data-caption="' + imgName + '" title="' +  imgName + '">' +
                                '<img style="width:100%;" data-src="' + small_cdn_url + '" src="' + small_cdn_url + '" data-loaded="true">' +
                            '</a>' +
                        '</div>' +
                      '</div>'
                }
                else{
                   if(i==0){
                        alert("今日沒有照片喔，請檢查腳本是否有"+currentDate+"的照片!!!")
                   }
                          
                }
        }
        
        
        $(".MyGrid").append(li);
        this.minigrid();
    },
    minigrid: function() {
        var grid = new Minigrid({
            container: '.MyGrid',
            item: '.card',
            gutter: 12
        });
        grid.mount();
        $(window).resize(function() {
           grid.mount();
        });
    }
}
photo.init();
}
```

進入hexo container `根目錄` 下，blog/source/_data/body-end.swig，撰寫以下腳本

```javascript
{% if page.type ==='picture' %}
  <script src="//cdn.jsdelivr.net/npm/minigrid@3.1.1/dist/minigrid.min.js"></script>
  <script src="/js/mygrid.js"></script>
{% endif %}
```

進入hexo container `根目錄` 下，blog/source/photo/index.md，撰寫以下腳本

```html
---
title: photo
type: picture
date: 2023-06-26 10:50:35
---
    
<!-- CSS Code -->
<style>
.MyGrid{width:100%;max-width:1040px;margin:0 auto;text-align:center}.card{overflow:hidden;transition:.3s ease-in-out;border-radius:8px;background-color:#efefef;padding:1.4px}.ImageInCard img{padding:0;border-radius:8px}
@media(prefers-color-scheme:dark){.card{background-color:#333;}}
</style>
<!-- CSS Code End -->
<div class="MyGrid"></div>

```



### 1.5.2. 撰寫Python腳本

建立phototool.py，並撰寫以下程式碼

此程式碼撰寫目的如下：

- 抓取GitServer倉庫的圖檔
- 進行圖片壓縮
- 產生縮略圖檔
- 圖片轉檔(JPG轉為PNG)

```python
# !/usr/bin/env python
# -*- coding:utf8  -*-
import os
import glob
from PIL import Image, ExifTags
import json
from datetime import date
config = {
    # gitea倉庫儲存目錄
    "github_img_host_base": "/var/jenkins_home/workspace/自動化佈署-hexo相簿+寄信通知/",
    # 上傳圖片目錄(含子目錄會自動掃描)
    "img_path": "/var/jenkins_home/workspace/自動化佈署-hexo相簿+寄信通知/photowall/photo",
    # 圖片URL前綴
    "cdn_url_prefix": "https://markweb.idv.tw:8443/jenkins_autoBuild_team/BuildPhotoHexo/raw/branch/master/",
    # hexo指定格式json文件
    "photo_info_json": "/var/jenkins_home/workspace/自動化佈署-hexo相簿+寄信通知/photowall/photoslist.json",
    "source_photo":"/var/jenkins_home/workspace/自動化佈署-hexo相簿+寄信通知/photowall/photo/",
    "target_photo": "/var/jenkins_home/workspace/自動化佈署-hexo相簿+寄信通知/photowall/photo/OutputPhoto/"
}
# 4 压缩图片到 90%(目的是为了移除 些gps 等信息，并非真的为了压缩）
def compress_img(img_path, rate=0.99, override=False):
    support_ftype_list = ["jpg","png", "PNG", "jpeg", "JPEG", "gif", "GIF", "bmp"]
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


# 5 对 img_path 目录下的文件夹递归生成缩略图保存到同目录下
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
            support_ftype_list = ["jpg","png", "PNG", "jpeg", "JPEG", "gif", "GIF", "bmp"]
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
            m = int(float(length) / 250.0)  # 计算缩小比例 (缩略图限制 300 长度)
            new_length = int(float(length) / m)
            new_height = int(float(height) / m)
            im.thumbnail((new_length, new_height))  # 生成缩略图
            im.save(abs_small_file, ftype)  # 保存缩略图
            print("save thumbnail img {0}".format(abs_small_file))
                            
            relative_file = abs_file[len(github_img_host_base) + 1 :]  # 计算相对路径，用来拼接 cdn
            relative_small_file = abs_small_file[len(github_img_host_base) + 1 :]
            print("relative_file:"+relative_file)
           # print("relative_small_file:"+relative_small_file)
            cdn_url_file = "{0}/{1}".format(cdn_url_prefix, relative_file)
            cdn_url_small_file = "{0}/{1}".format(cdn_url_prefix, relative_small_file)
            print("cdn_url_small_file:"+cdn_url_small_file)

            # 格式: 690.690;8.png;http://cdn_file_url;http://cdn_small_file_url;
            line = "{0}.{1};{2};{3};{4}".format(
                length,
                height,
                item,
                cdn_url_file, #此處可以取到檔名，請加入small_file參數
                cdn_url_small_file, #此處可以取到檔名，請加入small_file參數
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

### 1.5.3. 使用`Jenkins`設計腳本流程

### 1.5.4. 建立 個作業流程，開始定義要傳入腳本的`參數`
![](https://markweb.idv.tw/uploads/upload_a8b72676b1e10db0dde676fe4ccf704d.png)


![](https://markweb.idv.tw/uploads/upload_2c197a9a1d40f9bca3e1a681e6c8172e.png)


![](https://markweb.idv.tw/uploads/upload_d254c40e68a7eccc380d1941b9146e74.png)


![](https://markweb.idv.tw/uploads/upload_a309690cb04e0839ca59c68d89e1acb9.png)


![](https://markweb.idv.tw/uploads/upload_fb6c38d296b022948fc67886d1e89322.png)

### 1.5.5. 設定此`作業流程觸發`的時間，本案例為每日早上7:40觸發
![](https://markweb.idv.tw/uploads/upload_8df079eb9ffa8c4f0807054fd7627b4d.png)


### 1.5.6. 撰寫`shell腳本`

```bash
#!/bin/bash
#+-------------------------------------腳本說明--------------------------------------------+
# 一鍵佈署並上傳照片到hexo腳本
#
# (C) 2023 - markhsu - licensed under markweb License v1.
# 
#+----------------------------------------------------------------------------------------+
date=$(date +%Y-%m-%d)
#+----------------------------------------------------------------------------------------+
#清空上傳檔案
#+----------------------------------------------------------------------------------------+
rm -f ${WORKSPACE}/photowall/photo/OutputPhoto/*
rm -f ${WORKSPACE}/photowall/photo/hexo_photo_share/${date}/*
rm -f ${WORKSPACE}/photowall/photoslist.json
#+----------------------------------------------------------------------------------------+
#複製檔案到hexo container
#+----------------------------------------------------------------------------------------+
docker exec nextcloud-app-1 bash -c 'cd '${hexo_photo_share}' && \
mkdir -p '${date}' && \
shuf -zn20 -e '${nextcloud_src}'/* | xargs -0 cp -vt '${hexo_photo_share}'/'${date}''
#+----------------------------------------------------------------------------------------+
#執行python腳本
#+----------------------------------------------------------------------------------------+
python3 phototool.py
#+----------------------------------------------------------------------------------------+
#複製json檔案到hexo
#+----------------------------------------------------------------------------------------+
docker cp ${WORKSPACE}/photowall/photoslist.json hexo:${hexo_container}
#+----------------------------------------------------------------------------------------+
#佈署到hexo
#+----------------------------------------------------------------------------------------+
docker exec hexo bash -c 'hexo clean && hexo g && hexo d'
#+----------------------------------------------------------------------------------------+

#推送到git

#初始化
git init
#先將git server專案拉回，避免不同步問題導致報錯
git pull ${GIT_URL}
#git初始化設定
git config --global user.email ${GIT_AUTHOR_EMAIL}
git config --global user.name ${GIT_AUTHOR_NAME}
git config --global init.defaultBranch ${GIT_BRANCH}
#將異動檔案全部加入
git add .
#提交
git commit -m "${date}_${GIT_MESSAGE}"
#遠端上傳
git remote -v | grep -w origin && \
git remote set-url origin ${GIT_URL} || \
git remote add origin ${GIT_URL}
git checkout ${GIT_BRANCH}
git push origin ${GIT_BRANCH}

```

### 1.5.7. 設定建置後要觸發`email寄信`
![](https://markweb.idv.tw/uploads/upload_ed3113b1dc3c68a05cca70c1ce2f51d5.png)


![](https://markweb.idv.tw/uploads/upload_2b0f01e5717c2fffd7a2fb1ae6ddaa19.png)


### 1.5.8. 請先`手動建置`執行，確認無誤後再使用`排程執行`
![](https://markweb.idv.tw/uploads/upload_69f1e10c91e9f3063926943661229997.png)


### 1.5.9. 執行成功如附圖
![](https://markweb.idv.tw/uploads/upload_e7ab87b8bcfb53c81f1d819a4e41c450.png)