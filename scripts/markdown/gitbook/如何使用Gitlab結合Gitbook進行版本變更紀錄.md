---
title: 如何使用Gitlab結合Gitbook進行版本變更紀錄
updated: 2024-07-24 08:03:36Z
created: 2024-02-17 03:46:22Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Gitlab
  - Gitbook
  - release
---

# 1. 如何使用Gitlab結合Gitbook進行版本變更紀錄


## 1.1. 簡介

學習如何透過`Gitlab`進行`版本變更紀錄`


## 1.2. 目錄

- [1. 如何使用Gitlab結合Gitbook進行版本變更紀錄](#1-如何使用gitlab結合gitbook進行版本變更紀錄)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 專案架構](#13-專案架構)
  - [1.4. 事前準備](#14-事前準備)
  - [1.5. 操作步驟](#15-操作步驟)
  - [1.6. 使用方式](#16-使用方式)
  - [1.7. 完成畫面](#17-完成畫面)
  - [1.8. 參考網站](#18-參考網站)
  - [1.9. 常見問題](#19-常見問題)
    - [1.9.1. Gitlab CICD佈署出現 SemanticReleaseError: The repository gidlabprojectteam/test doesn't exist.](#191-gitlab-cicd佈署出現-semanticreleaseerror-the-repository-gidlabprojectteamtest-doesnt-exist)



## 1.3. 專案架構

```
myProject
├─ package.json
├─ README.md
└─ SUMMARY.md
```

## 1.4. 事前準備

如果要使用 gitlab 的 CI/CD 功能，需要申請他們的 api token。進入 gitlab 網站後，右上角頭像點選「Edit Profile」➡️「Access Tokens」申請 個 Token name。

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6c6af99d-upload-8ff1852803ee2436dd5b563839d9ed45.png)

Scope 可以選擇 api, read_repository, 以及 write_repository  種即可 (不過我自己是全選 😂)

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/53faa50c-upload-a86ec0d3db58df301fb95f30ad41add0.png)

接著到要自動發佈版本的專案中，選擇「Settings」➡️「CI/CD」➡️「Variables」，將剛剛申請的 token 貼上，Key 欄位寫 GL_TOKEN：

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/nTx7955de54-upload-99bd25070d6bac52c2a464bc0fd5789a.png)

<!--more-->
## 1.5. 操作步驟

1. 撰寫`.gitlab-ci.yml`

> [!note] 小提示 
> 1.  一定要用node:10的版本，否則會出現TypeError: cb.apply is not a function，這個屬於gitbook的bug
> 2. 這邊分別定義 個流水線，他們會互相相依，請善用`needs`語法


```yaml
image: node:10

cache:
  paths:
    - node_modules/

stages:
  - check_commit_message
  - gilab_pages
  - semantic-release

check_commit_message:
  stage: check_commit_message
  image: node:latest
  script:
    - npm install -g @commitlint/cli @commitlint/config-conventional
    - commitlint --config commitlint.config.js --from=$CI_COMMIT_BEFORE_SHA --to=$CI_COMMIT_SHA

gilab_pages:
  stage: gilab_pages
  script:
    - npm install gitbook-cli -g 
    - gitbook fetch 3.2.3 
    - apt-get -y update && apt-get install -y python python-pip
    - gitbook init
    - gitbook install
    - gitbook build . public 
    - rm -rf /var/opt/gitlab/host_data/gitbook/_book/gitbooknpmproject/gitlabpageforgitbook/*
    - mkdir -p /var/opt/gitlab/host_data/gitbook/_book/gitbooknpmproject/gitlabpageforgitbook
    - cp -r public/* /var/opt/gitlab/host_data/gitbook/_book/gitbooknpmproject/gitlabpageforgitbook
    - cp SUMMARY.md /var/opt/gitlab/host_data/gitbook/_book/gitbooknpmproject/gitlabpageforgitbook
  artifacts:
    paths:
      - public
    expire_in: 1 week
  only:
    - master 
  needs:
    - check_commit_message

semantic-release:
  stage: semantic-release
  image: node:latest
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" >> .npmrc
    - npm -g install --save-dev conventional-changelog-conventionalcommits semantic-release @semantic-release/changelog @semantic-release/gitlab @semantic-release/git @semantic-release/npm @semantic-release/release-notes-generator @semantic-release/gitlab-config
    - export GL_TOKEN=${GL_TOKEN}
    - GL_TOKEN=${GL_TOKEN} npx semantic-release
  needs:
    - gilab_pages
  tag:
    - docker
```

2. 撰寫`package.json`

```json
{
    "name": "mygitbook",
    "version": "2.1.0",
    "author": "markhsu",
    "private": true,
    "workspaces": [
        "packages/*"
    ],
    "scripts": {
        "semantic-release": "semantic-release"
    },
    "repository": {
        "type": "git",
        "url": "git+https://markweb.idv.tw:10443/gitbooknpmproject/gitlabpageforgitbook.git"
    },
    "release": {
        "extends": "@semantic-release/gitlab-config",
        "plugins": [
            [
                "@semantic-release/commit-analyzer",
                {
                    "releaseRules": [
                        {
                            "type": "✨feat",
                            "release": "minor"
                        },
                        {
                            "type": "🐞fix",
                            "release": "patch"
                        },
                        {
                            "type": "📃docs",
                            "release": "patch"
                        },
                        {
                            "type": "🌈style",
                            "release": "patch"
                        },
                        {
                            "type": "🛠️chore",
                            "release": "patch"
                        },
                        {
                            "type": "🔨refactor",
                            "release": "patch"
                        },
                        {
                            "type": "🔬test",
                            "release": "patch"
                        },
                        {
                            "type": "🔧build",
                            "release": "patch"
                        },
                        {
                            "type": "🐎ci",
                            "release": "patch"
                        }
                    ]
                }
            ],
            [
                "@semantic-release/release-notes-generator",
                {
                    "preset": "conventionalcommits",
                    "presetConfig": {
                        "types": [
                            {
                                "type": "feat",
                                "section": "✨ 新增功能"
                            },
                            {
                                "type": "fix",
                                "section": "🐞 錯誤修正"
                            },
                            {
                                "type": "perf",
                                "section": "🚀 效能調整"
                            },
                            {
                                "type": "revert",
                                "section": "⏪ 退版"
                            },
                            {
                                "type": "docs",
                                "section": "📃 文件調整",
                                "hidden": false
                            },
                            {
                                "type": "style",
                                "section": "🌈 樣式調整",
                                "hidden": false
                            },
                            {
                                "type": "chore",
                                "section": "🛠️ 重大更新",
                                "hidden": true
                            },
                            {
                                "type": "refactor",
                                "section": "🔨 程式碼重構",
                                "hidden": true
                            },
                            {
                                "type": "test",
                                "section": "🔬 單元測試",
                                "hidden": false
                            },
                            {
                                "type": "build",
                                "section": "🔧 程式重構",
                                "hidden": false
                            },
                            {
                                "type": "ci",
                                "section": "🐎 持續整合",
                                "hidden": false
                            },
                            {
                                "type": "other",
                                "section": "🔄 其他",
                                "hidden": false
                            }
                        ]
                    }
                }
            ],
            "@semantic-release/gitlab"
        ],
        "prepare": [
            "@semantic-release/changelog",
            "@semantic-release/npm",
            {
                "path": "@semantic-release/git",
                "assets": [
                    "package.json",
                    "package-lock.json",
                    "CHANGELOG.md"
                ],
                "message": "${nextRelease.type === 'major' ? '🛠️chore(release):這次是重大版更!!!' : '🐞feat/fix(release):這只是小版更!!!'}\n\n v${nextRelease.version} 新的專案版本已釋出!!! [skip ci]"
            }
        ]
    }
}

```

3. 撰寫`commitlint.config.js`


> [!note] 小提示 
> 1. 此功能用於驗證commit_message是否符合語意化規範
> 2. 提示訊息可在此進行改寫


```javascript
const matchAnyEmojiWithSpaceAfter =
  /^(feat|fix|docs|style|refactor|test|chore|feat!|fix!):\s/;
// const matchOptionalTicketNumberWithSpaceAfter = /(?:\[(T-\d+)\]\s)?/; // "[T-4605] ", "[T-1]"
const subjectThatDontStartWithBracket = /([^\[].+)/; // "Add tests" but don't allow "[ Add tests"

module.exports = {
  parserPreset: {
    parserOpts: {
      headerPattern: new RegExp(
        "^" +
          matchAnyEmojiWithSpaceAfter.source +
          subjectThatDontStartWithBracket.source +
          "$"
      ),
      headerCorrespondence: ["type", "subject"],
    },
  },
  plugins: [
    {
      rules: {
        "header-match-team-pattern": (parsed) => {
          const { type, subject } = parsed;
          if (type === null && subject === null) {
            return [
              false,
              `請檢查您的提交訊息是否正確喔~
🎸feat: 新增/修改功能 (Feature)
🐛fix: 修正 Bug (bug fix)
⚡️ perf: 提高效能的程式碼修正
💡refactor: 重構 or 優化，不屬於 bug 也不屬於新增功能等
🏹release: 新增正式釋出的 release commit 訊息
💄style: 修改程式碼格式或風格，不影響原有運作
💍test: 增加測試功能           
              `,
            ];
          }
          return [true, ""];
        },
        "explained-emoji-enum": (parsed, _when, emojisObject) => {
          const { emoji } = parsed;
          if (emoji && !Object.keys(emojisObject).includes(emoji)) {
            return [
              false,
              `emoji must be one of:
${Object.keys(emojisObject)
                .map((emojiType) => `${emojiType} - ${emojisObject[emojiType]}`)
                .join("\n")}`,
            ];
          }
          return [true, ""];
        },
        'body-max-line-length': [0], // 跳过 body 部分的行长度检查
        'footer-max-line-length': [0], // 跳过 footer 部分的行长度检查
      },
    },
  ],
  rules: {
    "header-match-team-pattern": [2, "always"],
    "explained-emoji-enum": [
      2,
      "always",
      {
        "⭐️": "新增/修改功能",
        "🐞": "修正 Bug",
        "✅": "增加測試功能",
        "♻️": "重構 or 優化，不屬於 bug 也不屬於新增功能等",
        "📝": "文件更新",
      },
    ],
  }
};

```

4. 測試畫面如下

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/eJHcd474d30-upload-423ba6b5dfc592d07979269faa2987c8.png)

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ds2213f68cc-upload-210dbcf19cdb2a78079435604413697e.png)

## 1.6. 使用方式

跳版號的規則可以參考這個網站
https://www.conventionalcommits.org/zh-hant/v1.0.0/


> [!note] 小提示 
> 請依照這個格式輸入提交訊息，否則不會跳號 
>1. Major(大版號)
> BREAKING CHANGE：在 body 開始處 或 footer 處包含 BREAKING CHANGE:，並在其後描述重大變更。
> feat 或 fix 後面加入 !
>2. Minor (中版號)
> feat
>3. Patch (小版號)
> fix：除了 bug 修復外，上線後如果有小功能要更新，也推薦用 fix 來代替 feat
> perf：性能的優化
> revert：撤銷先前的提交
## 1.7. 完成畫面

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/zlQb549dd24-upload-19882f6c08a1a02cd2d3e4d6b92bc9b9.png)

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/T5X47cc15d1-upload-3930456587bf783f62211b6e21c3caf7.png)

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/69ccfee5-upload-03a302243fd2aeee81ddca0eb0f98782.png)


## 1.8. 參考網站
1. 發佈 npm 套件 - 從手動到自動：semantic-release 自動更新版號

>  https://pjchender.dev/devops/devops-publish-npm-4/

2.約定式提交規範
> https://www.conventionalcommits.org/zh-hant/v1.0.0/


## 1.9. 常見問題

### 1.9.1. Gitlab CICD佈署出現 SemanticReleaseError: The repository gidlabprojectteam/test doesn't exist.

1. 確認repo這邊設定正確

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/bf7956b7-upload-53c1a29683bdc9488e4d5871395aed95.png)

2. 檢查是否有設置token

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/un7a440c02d-upload-7e9c11978a5241332ab5ba751a392b71.png)

3.檢查變數是否有設定
 
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/B6lca6b9129-upload-f25921e5b84cf1249a3ec85d820207f1.png)

4.檢查CICD是否有傳入token

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/79bedb63-upload-275d2422d018cb9b7076ff4ad3f5a521.png)
