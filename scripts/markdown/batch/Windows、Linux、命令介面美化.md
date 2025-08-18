---
title: Windows、Linux、命令介面美化
updated: 2024-07-23 13:27:53Z
created: 2024-04-07 12:28:30Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - terminal
  - Linux
  - Windows
  - beautiful
---

# 1. Windows、Linux、命令介面美化

## 1.1. 簡介

用來美化`cmd`


## 1.2. 目錄

- [1. Windows、Linux、命令介面美化](#1-windowslinux命令介面美化)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
    - [1.2.1. 使用方式](#121-使用方式)
      - [1.2.1.1. Windows CMD](#1211-windows-cmd)
    - [1.2.2. Windows POWERSHELL](#122-windows-powershell)
      - [1.2.2.1. 安裝oh-my-posh](#1221-安裝oh-my-posh)
      - [1.2.2.2. 進入windows市集，輸入`oh-my-posh`進行安裝\[^1\]](#1222-進入windows市集輸入oh-my-posh進行安裝1)
      - [1.2.2.3. 輸入以下指令，開啟notepad++](#1223-輸入以下指令開啟notepad)
    - [1.2.3. LINUX、WSL、Git Bash](#123-linuxwslgit-bash)
  - [1.3. 成功畫面](#13-成功畫面)
  - [1.4. 參考連結](#14-參考連結)


### 1.2.1. 使用方式

#### 1.2.1.1. Windows CMD

安裝Clink
https://chrisant996.github.io/clink/

 在`你的安裝目錄\clink\`下撰寫以下指令

```lua
-- 引入模組
local os = require("os")
local io = require("io")
local math = require("math")

-- 指定主题路徑
local themeFolderPath = "E:\\Project\\CMD\\oh-my-posh\\oh-my-posh-main\\themes"

-- 列出主题文件
local themes = {}
local themeDir = io.popen('dir "'..themeFolderPath..'" /b')
for filename in themeDir:lines() do
    table.insert(themes, filename)
end

-- 隨機選擇 個主題
math.randomseed(os.time())
local randomIndex = math.random(1, #themes)
local randomTheme = themes[randomIndex]

-- 清除螢幕畫面
local function clear_screen()
    -- For Windows
    if os.execute("cls") == nil then
        -- For Unix/Linux/MacOS
        os.execute("clear")
    end
end

clear_screen()

-- 建立提示詞
local hello = [[
 __   __  _______  ___      ___      _______    __   __  _______  ______    ___   _ 
|  | |  ||       ||   |    |   |    |       |  |  |_|  ||   _   ||    _ |  |   | | |
|  |_|  ||    ___||   |    |   |    |   _   |  |       ||  |_|  ||   | ||  |   |_| |
|       ||   |___ |   |    |   |    |  | |  |  |       ||       ||   |_||_ |      _|
|       ||    ___||   |___ |   |___ |  |_|  |  |       ||       ||    __  ||     |_ 
|   _   ||   |___ |       ||       ||       |  | ||_|| ||   _   ||   |  | ||    _  |
|__| |__||_______||_______||_______||_______|  |_|   |_||__| |__||___|  |_||___| |_|
																										
]]
print(hello)
print("歡迎回來, Mark,您今天的幸運主題是...："..randomTheme)

-- 執行命令並輸出
load(io.popen('oh-my-posh init cmd --config E:\\Project\\CMD\\oh-my-posh\\oh-my-posh-main\\themes\\' .. randomTheme):read("*a"))()
```

![](https://markweb.idv.tw/uploads/202404091929270.png)

<!--more-->
### 1.2.2. Windows POWERSHELL

#### 1.2.2.1. 安裝oh-my-posh

#### 1.2.2.2. 進入windows市集，輸入`oh-my-posh`進行安裝[^1]

![](https://markweb.idv.tw/uploads/202404091933392.png)

#### 1.2.2.3. 輸入以下指令，開啟notepad++
```
notepad $PROFILE
```

![](https://markweb.idv.tw/uploads/202404091935320.png)


> [!NOTE] 筆記
>  1. 若提示“系统找不到路徑”，先在%HOMEPATH%\Documents\（即“文件”）下建立名稱為WindowsPowerShell的目錄，再執行 notepad $PROFILE


> [!NOTE] Q2. 可以使用指令建立嗎?
>  mkdir "$env:HOMEPATH\Documents\WindowsPowerShell"; Set-Content $env:HOMEPATH\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 ‘oh-my-posh init pwsh | Invoke-Expression’ 

> [!NOTE] Q3. 請以系統管理員身分執行這行
> Set-ExecutionPolicy -ExecutionPolicy Unrestricted

> [!NOTE] Q4：請記得先安裝以下套件
```powershell
Install-Module -Name Terminal-Icons -Repository PSGallery
Install-Module PSReadLine -Scope CurrentUser
Install-Module posh-git -Scope CurrentUserr
Install-Module oh-my-posh -Scope CurrentUser
```


> [!NOTE] Q5：若powershell執行會出現中文亂碼
> 請先使用Notepad++，將檔案編碼設定為UTF-8-BOM就可以解決


 在`Microsoft.PowerShell_profile.ps1`下撰寫以下指令

```powershell
# 引入自定義模組
Import-Module oh-my-posh
Import-Module posh-git
Import-Module Terminal-icons
Import-Module PSReadLine

# 設定預設使用者
$DefaultUser = 'MarkHSU'

# 關閉 PowerShell 下載進度條
$ProgressPreference = 'SilentlyContinue'

# tab 展開路徑下檔案並選擇
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete 

# Autocompletion for arrow keys
Set-PSReadlineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward
Set-PSReadLineOption -PredictionSource History

# 設定預設表情符號
function prompt {"PS $pwd 😴 >" }

# 設定主題檔名
$themeDirectory = 'E:\\Project\\CMD\\oh-my-posh\\oh-my-posh-main\\themes'
$themeFiles = Get-ChildItem -Path $themeDirectory -Filter *.omp.json | Select-Object -ExpandProperty Name

# 讀取隨機主題檔名
$selectedTheme = Get-Random -InputObject $themeFiles

# 套用主題
oh-my-posh init pwsh --config "$themeDirectory\$selectedTheme" | Invoke-Expression

# 清除版面的內容
clear

# 增加歡迎提示詞
$hello = @"

 __   __  _______  ___      ___      _______    __   __  _______  ______    ___   _ 
|  | |  ||       ||   |    |   |    |       |  |  |_|  ||   _   ||    _ |  |   | | |
|  |_|  ||    ___||   |    |   |    |   _   |  |       ||  |_|  ||   | ||  |   |_| |
|       ||   |___ |   |    |   |    |  | |  |  |       ||       ||   |_||_ |      _|
|       ||    ___||   |___ |   |___ |  |_|  |  |       ||       ||    __  ||     |_ 
|   _   ||   |___ |       ||       ||       |  | ||_|| ||   _   ||   |  | ||    _  |
|__| |__||_______||_______||_______||_______|  |_|   |_||__| |__||___|  |_||___| |_|


"@

Write-Host $hello
Write-Host "歡迎回來, ${DefaultUser}: 今天的幸運主題是: $selectedTheme :)"
```

在設定檔增添更多樣式配置[^2]

![](https://markweb.idv.tw/uploads/202404102118846.png)



```json
{
    "$help": "https://aka.ms/terminal-documentation",
    "$schema": "https://aka.ms/terminal-profiles-schema",
    "actions": 
    [
        {
            "command": 
            {
                "action": "copy",
                "singleLine": false
            },
            "keys": "ctrl+c"
        },
        {
            "command": "paste",
            "keys": "ctrl+v"
        },
        {
            "command": 
            {
                "action": "splitPane",
                "split": "auto",
                "splitMode": "duplicate"
            },
            "keys": "alt+shift+d"
        },
        {
            "command": "find",
            "keys": "ctrl+shift+f"
        }
    ],
    "copyFormatting": "none",
    "copyOnSelect": false,
    "defaultProfile": "{0caa0dad-35be-5f56-a8ff-afceeeaa6101}",
    "newTabMenu": 
    [
        {
            "type": "remainingProfiles"
        }
    ],
    "profiles": 
    {
        "defaults": 
        {
            "backgroundImage": "E:\\Project\\CMD\\eberhard-grossgasteiger-HDxsIFHz4TI-unsplash.jpg",
            "backgroundImageOpacity": 0.8,
            "backgroundImageStretchMode": "fill",
            "colorScheme": "flexoki-dark",
            "cursorColor": "#000000",
            "cursorShape": "filledBox",
            "font": 
            {
                "face": "JetBrainsMono Nerd Font"
            },
            "name": "\ud83d\ude0a You Open the commandline \ud83d\ude0a",
            "useAcrylic": true
        },
        "list": 
        [
            {
                "colorScheme": "Tango Dark",
                "commandline": "%SystemRoot%\\System32\\cmd.exe -nologo",
                "cursorShape": "filledBox",
                "elevate": false,
                "font": 
                {
                    "face": "JetBrainsMono Nerd Font",
                    "size": 12.0,
                    "weight": "medium"
                },
                "guid": "{0caa0dad-35be-5f56-a8ff-afceeeaa6101}",
                "hidden": false,
                "name": "\ud83d\ude0a \u5c0f\u5f65\u7684CMD \ud83d\ude0a",
                "opacity": 100,
                "suppressApplicationTitle": true,
                "tabTitle": null,
                "useAcrylic": true
            },
            {
                "altGrAliasing": true,
                "antialiasingMode": "grayscale",
                "backgroundImageOpacity": 0.8,
                "closeOnExit": "graceful",
                "colorScheme": "Flat UI Palette v1 Modified",
                "commandline": "ssh root@markweb.idv.tw",
                "cursorShape": "filledBox",
                "font": 
                {
                    "face": "JetBrainsMono Nerd Font",
                    "size": 12.0
                },
                "guid": "{825b4a95-af71-4ce6-9a91-6ae2c1f68b95}",
                "hidden": false,
                "historySize": 9001,
                "icon": "ms-appx:///ProfileIcons/{0caa0dad-35be-5f56-a8ff-afceeeaa6101}.png",
                "intenseTextStyle": "all",
                "name": "\ud83d\ude0a \u5c0f\u5f65\u7684Ubuntu \u9060\u7aef \ud83d\ude0a",
                "padding": "8, 8, 8, 8",
                "snapOnInput": true,
                "startingDirectory": "%USERPROFILE%",
                "useAcrylic": true
            },
            {
                "altGrAliasing": true,
                "antialiasingMode": "grayscale",
                "closeOnExit": "automatic",
                "colorScheme": "Terminal Salf Scheme",
                "commandline": "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -nologo",
                "cursorShape": "filledBox",
                "font": 
                {
                    "face": "JetBrainsMono Nerd Font",
                    "size": 12.0
                },
                "guid": "{a3c1d619-bcf5-4dd7-9bfe-9ccde7aebe94}",
                "hidden": false,
                "historySize": 9001,
                "icon": "ms-appx:///ProfileIcons/{61c54bbd-c2c6-5271-96e7-009a87ff44bf}.png",
                "name": "\ud83d\ude0a \u5c0f\u5f65\u7684 Powershell \ud83d\ude0a",
                "opacity": 100,
                "padding": "8, 8, 8, 8",
                "snapOnInput": true,
                "startingDirectory": "%USERPROFILE%",
                "suppressApplicationTitle": true,
                "tabTitle": null,
                "useAcrylic": false
            }
        ]
    },
    "schemes": 
    [
        {
            "background": "#161719",
            "black": "#000000",
            "blue": "#85BEFD",
            "brightBlack": "#000000",
            "brightBlue": "#96CBFE",
            "brightCyan": "#85BEFD",
            "brightGreen": "#94FA36",
            "brightPurple": "#B9B6FC",
            "brightRed": "#FD5FF1",
            "brightWhite": "#E0E0E0",
            "brightYellow": "#F5FFA8",
            "cursorColor": "#D0D0D0",
            "cyan": "#85BEFD",
            "foreground": "#C5C8C6",
            "green": "#87C38A",
            "name": "Atom",
            "purple": "#B9B6FC",
            "red": "#FD5FF1",
            "selectionBackground": "#444444",
            "white": "#E0E0E0",
            "yellow": "#FFD7B1"
        },
        {
            "background": "#0C0C0C",
            "black": "#0C0C0C",
            "blue": "#0037DA",
            "brightBlack": "#767676",
            "brightBlue": "#3B78FF",
            "brightCyan": "#61D6D6",
            "brightGreen": "#16C60C",
            "brightPurple": "#B4009E",
            "brightRed": "#E74856",
            "brightWhite": "#F2F2F2",
            "brightYellow": "#F9F1A5",
            "cursorColor": "#FFFFFF",
            "cyan": "#3A96DD",
            "foreground": "#CCCCCC",
            "green": "#13A10E",
            "name": "Campbell",
            "purple": "#881798",
            "red": "#C50F1F",
            "selectionBackground": "#FFFFFF",
            "white": "#CCCCCC",
            "yellow": "#C19C00"
        },
        {
            "background": "#012456",
            "black": "#0C0C0C",
            "blue": "#0037DA",
            "brightBlack": "#767676",
            "brightBlue": "#3B78FF",
            "brightCyan": "#61D6D6",
            "brightGreen": "#16C60C",
            "brightPurple": "#B4009E",
            "brightRed": "#E74856",
            "brightWhite": "#F2F2F2",
            "brightYellow": "#F9F1A5",
            "cursorColor": "#FFFFFF",
            "cyan": "#3A96DD",
            "foreground": "#CCCCCC",
            "green": "#13A10E",
            "name": "Campbell Powershell",
            "purple": "#881798",
            "red": "#C50F1F",
            "selectionBackground": "#FFFFFF",
            "white": "#CCCCCC",
            "yellow": "#C19C00"
        },
        {
            "background": "#000000",
            "black": "#0C0C0C",
            "blue": "#0037DA",
            "brightBlack": "#767676",
            "brightBlue": "#3B78FF",
            "brightCyan": "#61D6D6",
            "brightGreen": "#16C60C",
            "brightPurple": "#B4009E",
            "brightRed": "#E74856",
            "brightWhite": "#F2F2F2",
            "brightYellow": "#F9F1A5",
            "cursorColor": "#FFFFFF",
            "cyan": "#3A96DD",
            "foreground": "#FFFFFF",
            "green": "#13A10E",
            "name": "Color Scheme 16",
            "purple": "#881798",
            "red": "#C50F1F",
            "selectionBackground": "#FFFFFF",
            "white": "#CCCCCC",
            "yellow": "#C19C00"
        },
        {
            "background": "#1C2024",
            "black": "#000000",
            "blue": "#2980B9",
            "brightBlack": "#52677C",
            "brightBlue": "#3498DB",
            "brightCyan": "#1ABC9C",
            "brightGreen": "#2ECC71",
            "brightPurple": "#9B59B6",
            "brightRed": "#E67E22",
            "brightWhite": "#ECF0F1",
            "brightYellow": "#F1C40F",
            "cursorColor": "#FFFFFF",
            "cyan": "#16A085",
            "foreground": "#ECF0F1",
            "green": "#27AE60",
            "name": "Flat UI Palette v1 Modified",
            "purple": "#8E44AD",
            "red": "#E74C3C",
            "selectionBackground": "#FFFFFF",
            "white": "#FFFFFF",
            "yellow": "#F1C40F"
        },
        {
            "background": "#FFFFFF",
            "black": "#3C5712",
            "blue": "#17B2FF",
            "brightBlack": "#749B36",
            "brightBlue": "#27B2F6",
            "brightCyan": "#13A8C0",
            "brightGreen": "#89AF50",
            "brightPurple": "#F2A20A",
            "brightRed": "#F49B36",
            "brightWhite": "#741274",
            "brightYellow": "#991070",
            "cursorColor": "#FFFFFF",
            "cyan": "#3C96A6",
            "foreground": "#000000",
            "green": "#6AAE08",
            "name": "Frost",
            "purple": "#991070",
            "red": "#8D0C0C",
            "selectionBackground": "#FFFFFF",
            "white": "#6E386E",
            "yellow": "#991070"
        },
        {
            "background": "#1E1E1E",
            "black": "#1E1E1E",
            "blue": "#377375",
            "brightBlack": "#7F7061",
            "brightBlue": "#719586",
            "brightCyan": "#7DB669",
            "brightGreen": "#AAB01E",
            "brightPurple": "#C77089",
            "brightRed": "#F73028",
            "brightWhite": "#E6D4A3",
            "brightYellow": "#F7B125",
            "cursorColor": "#E6D4A3",
            "cyan": "#578E57",
            "foreground": "#E6D4A3",
            "green": "#868715",
            "name": "Gruvbox Dark",
            "purple": "#A04B73",
            "red": "#BE0F17",
            "selectionBackground": "#E6D4A3",
            "white": "#978771",
            "yellow": "#CC881A"
        },
        {
            "background": "#282C34",
            "black": "#282C34",
            "blue": "#61AFEF",
            "brightBlack": "#5A6374",
            "brightBlue": "#61AFEF",
            "brightCyan": "#56B6C2",
            "brightGreen": "#98C379",
            "brightPurple": "#C678DD",
            "brightRed": "#E06C75",
            "brightWhite": "#DCDFE4",
            "brightYellow": "#E5C07B",
            "cursorColor": "#FFFFFF",
            "cyan": "#56B6C2",
            "foreground": "#DCDFE4",
            "green": "#98C379",
            "name": "One Half Dark",
            "purple": "#C678DD",
            "red": "#E06C75",
            "selectionBackground": "#FFFFFF",
            "white": "#DCDFE4",
            "yellow": "#E5C07B"
        },
        {
            "background": "#FAFAFA",
            "black": "#383A42",
            "blue": "#0184BC",
            "brightBlack": "#4F525D",
            "brightBlue": "#61AFEF",
            "brightCyan": "#56B5C1",
            "brightGreen": "#98C379",
            "brightPurple": "#C577DD",
            "brightRed": "#DF6C75",
            "brightWhite": "#FFFFFF",
            "brightYellow": "#E4C07A",
            "cursorColor": "#4F525D",
            "cyan": "#0997B3",
            "foreground": "#383A42",
            "green": "#50A14F",
            "name": "One Half Light",
            "purple": "#A626A4",
            "red": "#E45649",
            "selectionBackground": "#FFFFFF",
            "white": "#FAFAFA",
            "yellow": "#C18301"
        },
        {
            "background": "#3C0315",
            "black": "#282A2E",
            "blue": "#0170C5",
            "brightBlack": "#676E7A",
            "brightBlue": "#80C8FF",
            "brightCyan": "#8ABEB7",
            "brightGreen": "#B5D680",
            "brightPurple": "#AC79BB",
            "brightRed": "#BD6D85",
            "brightWhite": "#FFFFFD",
            "brightYellow": "#FFFD76",
            "cursorColor": "#FFFFFF",
            "cyan": "#3F8D83",
            "foreground": "#FFFFFD",
            "green": "#76AB23",
            "name": "Raspberry",
            "purple": "#7D498F",
            "red": "#BD0940",
            "selectionBackground": "#FFFFFF",
            "white": "#FFFFFD",
            "yellow": "#E0DE48"
        },
        {
            "background": "#002B36",
            "black": "#002B36",
            "blue": "#268BD2",
            "brightBlack": "#073642",
            "brightBlue": "#839496",
            "brightCyan": "#93A1A1",
            "brightGreen": "#586E75",
            "brightPurple": "#6C71C4",
            "brightRed": "#CB4B16",
            "brightWhite": "#FDF6E3",
            "brightYellow": "#657B83",
            "cursorColor": "#FFFFFF",
            "cyan": "#2AA198",
            "foreground": "#839496",
            "green": "#859900",
            "name": "Solarized Dark",
            "purple": "#D33682",
            "red": "#DC322F",
            "selectionBackground": "#FFFFFF",
            "white": "#EEE8D5",
            "yellow": "#B58900"
        },
        {
            "background": "#FDF6E3",
            "black": "#002B36",
            "blue": "#268BD2",
            "brightBlack": "#073642",
            "brightBlue": "#839496",
            "brightCyan": "#93A1A1",
            "brightGreen": "#586E75",
            "brightPurple": "#6C71C4",
            "brightRed": "#CB4B16",
            "brightWhite": "#FDF6E3",
            "brightYellow": "#657B83",
            "cursorColor": "#002B36",
            "cyan": "#2AA198",
            "foreground": "#657B83",
            "green": "#859900",
            "name": "Solarized Light",
            "purple": "#D33682",
            "red": "#DC322F",
            "selectionBackground": "#FFFFFF",
            "white": "#EEE8D5",
            "yellow": "#B58900"
        },
        {
            "background": "#000000",
            "black": "#000000",
            "blue": "#3465A4",
            "brightBlack": "#555753",
            "brightBlue": "#729FCF",
            "brightCyan": "#34E2E2",
            "brightGreen": "#8AE234",
            "brightPurple": "#AD7FA8",
            "brightRed": "#EF2929",
            "brightWhite": "#EEEEEC",
            "brightYellow": "#FCE94F",
            "cursorColor": "#FFFFFF",
            "cyan": "#06989A",
            "foreground": "#D3D7CF",
            "green": "#4E9A06",
            "name": "Tango Dark",
            "purple": "#75507B",
            "red": "#CC0000",
            "selectionBackground": "#FFFFFF",
            "white": "#D3D7CF",
            "yellow": "#C4A000"
        },
        {
            "background": "#FFFFFF",
            "black": "#000000",
            "blue": "#3465A4",
            "brightBlack": "#555753",
            "brightBlue": "#729FCF",
            "brightCyan": "#34E2E2",
            "brightGreen": "#8AE234",
            "brightPurple": "#AD7FA8",
            "brightRed": "#EF2929",
            "brightWhite": "#EEEEEC",
            "brightYellow": "#FCE94F",
            "cursorColor": "#000000",
            "cyan": "#06989A",
            "foreground": "#555753",
            "green": "#4E9A06",
            "name": "Tango Light",
            "purple": "#75507B",
            "red": "#CC0000",
            "selectionBackground": "#FFFFFF",
            "white": "#D3D7CF",
            "yellow": "#C4A000"
        },
        {
            "background": "#000000",
            "black": "#EDECE3",
            "blue": "#007A99",
            "brightBlack": "#00FFCC",
            "brightBlue": "#EDECE3",
            "brightCyan": "#CC0029",
            "brightGreen": "#00CC00",
            "brightPurple": "#FF33FF",
            "brightRed": "#FF7792",
            "brightWhite": "#FF9900",
            "brightYellow": "#EDECE3",
            "cursorColor": "#FFFFFF",
            "cyan": "#21EFEF",
            "foreground": "#EDECE3",
            "green": "#FF7792",
            "name": "Terminal Salf Scheme",
            "purple": "#FF8F44",
            "red": "#EDECE3",
            "selectionBackground": "#FFFFFF",
            "white": "#FFFFFF",
            "yellow": "#FF7792"
        },
        {
            "background": "#300A24",
            "black": "#2E3436",
            "blue": "#3465A4",
            "brightBlack": "#555753",
            "brightBlue": "#729FCF",
            "brightCyan": "#34E2E2",
            "brightGreen": "#8AE234",
            "brightPurple": "#AD7FA8",
            "brightRed": "#EF2929",
            "brightWhite": "#EEEEEC",
            "brightYellow": "#FCE94F",
            "cursorColor": "#BBBBBB",
            "cyan": "#06989A",
            "foreground": "#EEEEEC",
            "green": "#4E9A06",
            "name": "Ubuntu Classic",
            "purple": "#75507B",
            "red": "#CC0000",
            "selectionBackground": "#B5D5FF",
            "white": "#D3D7CF",
            "yellow": "#C4A000"
        },
        {
            "background": "#000000",
            "black": "#000000",
            "blue": "#000080",
            "brightBlack": "#808080",
            "brightBlue": "#0000FF",
            "brightCyan": "#00FFFF",
            "brightGreen": "#00FF00",
            "brightPurple": "#FF00FF",
            "brightRed": "#FF0000",
            "brightWhite": "#FFFFFF",
            "brightYellow": "#FFFF00",
            "cursorColor": "#FFFFFF",
            "cyan": "#008080",
            "foreground": "#C0C0C0",
            "green": "#008000",
            "name": "Vintage",
            "purple": "#800080",
            "red": "#800000",
            "selectionBackground": "#FFFFFF",
            "white": "#C0C0C0",
            "yellow": "#808000"
        },
        {
            "background": "#1C1B1A",
            "black": "#1C1B1A",
            "blue": "#4385BE",
            "brightBlack": "#575653",
            "brightBlue": "#4385BE",
            "brightCyan": "#3AA99F",
            "brightGreen": "#879A39",
            "brightPurple": "#CE5D97",
            "brightRed": "#D14D41",
            "brightWhite": "#CECDC3",
            "brightYellow": "#D0A215",
            "cursorColor": "#CECDC3",
            "cyan": "#3AA99F",
            "foreground": "#CECDC3",
            "green": "#879A39",
            "name": "flexoki-dark",
            "purple": "#CE5D97",
            "red": "#D14D41",
            "selectionBackground": "#CECDC3",
            "white": "#B7B5AC",
            "yellow": "#D0A215"
        }
    ],
    "theme": "system",
    "themes": []
}
```

### 1.2.3. LINUX、WSL、Git Bash

安裝oh-my-posh，請逐行輸入以下指令
```bash
sudo wget https://github.com/JanDeDobbeleer/oh-my-posh/releases/latest/download/posh-linux-amd64 -O /usr/local/bin/oh-my-posh

sudo chmod +x /usr/local/bin/oh-my-posh

mkdir ~/.poshthemes

wget https://github.com/JanDeDobbeleer/oh-my-posh/releases/latest/download/themes.zip -O ~/.poshthemes/themes.zip

unzip ~/.poshthemes/themes.zip -d ~/.poshthemes

chmod u+rw ~/.poshthemes/*.json

rm ~/.poshthemes/themes.zip
```

輸入指令 `vim ~/.bashrc`，增加以下指令

```bash
function get_random_theme() {
  local dir=~/.poshthemes
  local files=("$dir"/*)  # 修改這行以避免因為空白造成的問題
  local num_files=${#files[@]}  # 主題檔案數量
  local random_index=$(($RANDOM % num_files))  # 隨機索引值
  local file="${files[$random_index]}"  # 隨機選取的主題檔案
  posh_theme=$(basename "$file")  # 取得檔案名稱
  full_posh_theme="$file"  # 完整路徑名稱
}
get_random_theme
echo "哈囉! 今天的幸運主題是 is: $posh_theme :)"
eval "$(oh-my-posh init bash --config "$full_posh_theme")"
```

![](https://markweb.idv.tw/uploads/202404072025741.png)

輸入指令 `source ~/.bashrc`，讓設定生效

## 1.3. 成功畫面

![](https://markweb.idv.tw/uploads/202404102123718.png)

![](https://markweb.idv.tw/uploads/202404102123304.png)

![](https://markweb.idv.tw/uploads/202404102123788.png)


## 1.4. 參考連結



3. 找不到與參數名稱key的解法
https://blog.csdn.net/thinszx/article/details/131857064

4. 教學文章1
https://www.jeremyjone.com/917/

5. 教學文章2
https://www.bilibili.com/read/cv20467382/

6. 教學文章3 
https://blog.csdn.net/qq_62888264/article/details/132551059

7. 教學文章4  
https://oldmoon.top/post/141#%E5%AD%97%E4%BD%93%E9%85%8D%E7%BD%AE

8. 教學文章5 
https://ithelp.ithome.com.tw/articles/10230798

9. CLIMK
https://chrisant996.github.io/clink/

10. 增加提示表情符號
https://www.cnblogs.com/enjoy233/p/simple_guide_to_beautify_powershells_in_Windows_Terminal.html#%E5%B0%86powershell%E7%9A%84%E6%8F%90%E7%A4%BA%E7%AC%A6%E6%94%B9%E4%B8%BA-emoji

11. 教學文章6
https://www.cnblogs.com/taylorshi/p/16482694.html

12. 教學文章7
https://molly1024.medium.com/windows-%E7%B5%82%E7%AB%AF%E6%A9%9F%E6%8E%A8%E8%96%A6-windows-terminal-%E7%BE%8E%E5%8C%96-%E5%B0%87-terminal-%E6%94%B9%E9%80%A0%E6%88%90%E4%BD%A0%E5%96%9C%E6%AD%A1%E7%9A%84%E6%A8%A3%E5%AD%90-9f6835951837

13. 教學文章8
https://juejin.cn/post/7122814751603687438

14. 教學文章9
https://juejin.cn/post/6847902225059020813

15. Windows Terminal Themes
https://windowsterminalthemes.dev/


[^1]: 1. 字型下載
https://www.nerdfonts.com/font-downloads
[^2]: 2. 官網主題
https://ohmyposh.dev/docs/themes
