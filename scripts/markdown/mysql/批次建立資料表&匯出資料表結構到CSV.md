---
title: 批次建立資料表&匯出資料表結構到CSV
updated: 2024-07-23 13:31:44Z
created: 2024-07-14 08:43:37Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Mysql
  - CSV
  - SP
---

# 1. 批次建立資料表&匯出資料表結構到CSV

## 1.1. 簡介

自動化建立資料表&匯出資料結構至CSV

## 1.2. 目錄

- [1. 批次建立資料表\&匯出資料表結構到CSV](#1-批次建立資料表匯出資料表結構到csv)
	- [1.1. 簡介](#11-簡介)
	- [1.2. 目錄](#12-目錄)
	- [1.3. 常見問題](#13-常見問題)
		- [1.3.1. 20231026 更新](#131-20231026-更新)
	- [1.4. 使用方式](#14-使用方式)
	- [1.5. 執行步驟](#15-執行步驟)
		- [1.5.1. (1) 自動執行](#151-1-自動執行)
		- [1.5.2. (2) 手動執行](#152-2-手動執行)
		- [1.5.3. (3) 注意事項](#153-3-注意事項)
		- [1.5.4. (4) 步驟開始](#154-4-步驟開始)


## 1.3. 常見問題

### 1.3.1. 20231026 更新

發現給同學的`bat檔`，遇到了 個小問題，很開心`點兩下執行`出現如下圖畫面...


![image-20231026200612113](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/80ace8e9-image-20231026200612113.png)

這時可以打開`NOTEPAD++`，查看`文件編碼`，發現被改掉變成`UNIX換行格式`
![image-20231026200659464](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4nxa1d7ff3b-image-20231026200659464.png)


點選編輯→換行格式→`Windows格式`
![image-20231026200733515](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ba81a69d-image-20231026200733515.png)


確定`格式已變更`，看`右下角`
![image-20231026200806432](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/pMw6bdda375-image-20231026200806432.png)


再次執行就成功囉~
![image-20231026201503318](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6c949e34-image-20231026201503318.png)

<!--more-->
## 1.4. 使用方式

1. 進入到以下網址，`下載專案`到本地端
https://github.com/Mark850409/mysqlAutoCreateDB

2. 點選Code→Download ZIP

![image-20231026201802967](https://markweb.idv.tw/uploads/image-20231026201802967.png)

3. `解壓`後會看到如下圖檔案
![image-20231026201715865](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/27676990-image-20231026201715865.png)

<!--more-->


## 1.5. 執行步驟

### 1.5.1. (1) 自動執行

1. 點兩下執行`AutoImportSP.bat`
![image-20231025201337284](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/F6We6ec71e9-image-20231025201337284.png)


2. 輸入資料庫帳號&輸入資料庫密碼
![image-20231025213728682](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6dab6403-image-20231025213728682.png)

3. 等待執行完成
![image-20231025210327458](https://markweb.idv.tw/uploads/image-20231025210327458.png)

4. 執行結果
![image-20231025211146465](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/30fbe7df-image-20231025211146465.png)

附上`AutoImportSP.bat`原始碼給大家參考

```bat
@echo off
chcp 65001
echo ===========================
echo 歡迎使用資料庫匯入小程式!!!
echo 請依照以下提示訊息輸入!!!
echo ===========================

echo.
echo.

echo =========注意事項==========
echo 1.提示訊息的輸入不得為空!!!
echo 2.請事先下載好SQL檔案
echo 3.MYSQL SERVER是否啟動!!!
echo ===========================

echo.

:CheckMysql
echo =========以下為您的MYSQL狀態==========
netstat -ano | findstr 3306
echo ======================================
if %ERRORLEVEL% equ 0 goto UserNamePrompt
echo "MYSQL未啟動，請檢查詳細原因!!!"
goto end


:UserNamePrompt
echo.
set /P name=請輸入資料庫帳號：
if not defined name goto UserNamePrompt
if %name% neq "" goto pwPrompt

:pwPrompt
set /p pw=請輸入資料庫密碼：
if not defined pw goto pwPrompt
if %pw% neq "" goto importsql


REM :pathPrompt
REM set /p mypath=請輸入資料庫檔案路徑：
REM if not defined mypath goto pathPrompt
REM if %mypath% neq "" goto checkpath

REM :checkpath
REM if exist %mypath% (
  REM goto importsql 
REM ) else (
  REM echo "路徑輸入錯誤，請重新輸入!!!"
  REM goto end
REM )


:importsql
"C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe" mysql -u %name% -p%pw% -e "source Createstocktable.sql;" -e "use stock;" -e "source ExportstockTable.sql;"
if "%ERRORLEVEL%" EQU "0" (
  goto openfiles
) else (
   echo "MYSQL帳密輸入錯誤，請重新輸入!!!"
   goto UserNamePrompt
)

:openfiles
start  "" "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads"
goto end

:end
pause

```
### 1.5.2. (2) 手動執行

補上SP語法直接讓大家複製貼上

1. 第 隻要執行的SP為`procCreateTableSchema`

```sql
-- ====================================================================
-- SP Name     : procCreateTableSchema
-- Function    : 批次建立 stock table
-- Author      : Mark
-- Create Date : 2023-10-22
-- Parameter   : DBName
-- Modify His  : 
-- (1) 2023-10-22 : Mark    : CREATE 
-- (2) 2023-10-23 : Mark    : Modify SP describe 
-- ===================================================================

-- 如果stock資料庫不存在就建立 個新的
CREATE DATABASE IF NOT EXISTS stock DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- 使用stock資料庫
USE stock;
-- 如果PROCEDURE存在就先移除
DROP PROCEDURE IF EXISTS stock.CreateStockTable; 
DELIMITER //
-- 建立PROCEDURE
CREATE PROCEDURE CreateStockTable()
BEGIN
		-- 這邊可以開始寫SQL，以下為建立資料表語法
		DROP TABLE IF EXISTS stock_daily;
		CREATE TABLE IF NOT EXISTS stock_daily
		(
			sdate varchar(10),
			id varchar(10),
			sname varchar(255),
			trs_qty decimal(18, 0),
			trs_count decimal(18, 0),
			trs_amt decimal(18, 0),
			open_price decimal(18, 2),
			h_price decimal(18, 2),
			l_price decimal(18, 2),
			close_price decimal(18, 2),
			s_status varchar(255),
			dec_price decimal(18, 2),
			lb_price decimal(18, 2),
			lb_amt decimal(18, 2),
			ls_price decimal(18, 2),
			ls_amt decimal(18, 2),
			PE decimal(18, 2)
		);
        
		DROP TABLE IF EXISTS stock_list;
		CREATE TABLE IF NOT EXISTS stock_list
		(
			id varchar(10),
			sname varchar(255),
			stock_attr varchar(255),
			industry varchar(255),
			CONSTRAINT PK_stock_list
				PRIMARY KEY (id)
		);

		DROP TABLE IF EXISTS stock_monthly_revenue;
		CREATE TABLE IF NOT EXISTS stock_monthly_revenue
		(
			yyyymm varchar(6),
			id varchar(10),
			sname varchar(255),
			month_amt decimal(18, 0),
			pre_m_amt decimal(18, 0),
			pre_y_amt decimal(18, 0),
			pre_m_percent decimal(18, 2),
			pre_y_percent decimal(18, 2),
			sum_amt decimal(18, 0),
			per_sum_amt decimal(18, 0),
			sum_percent decimal(18, 2),
			memo_str varchar(255),
			CONSTRAINT PK_stock_monthly_revenue
				PRIMARY KEY
				(
					id,
					yyyymm
				)
		);

		DROP TABLE IF EXISTS stock_daily_3;
		CREATE TABLE IF NOT EXISTS stock_daily_3
		(
			sdate varchar(10),
			id varchar(10),
			f_qty decimal(18, 0),
			i_qty decimal(18, 0),
			s_qty decimal(18, 0),
			t_qty decimal(18, 0),
			est_f_qty decimal(18, 0),
			est_i_qty decimal(18, 0),
			est_s_qty decimal(18, 0),
			est_t_qty decimal(18, 0),
			trs_f_percent decimal(18, 2),
			trs_3_percent decimal(18, 2),
			CONSTRAINT PK_stock_daily_3
				PRIMARY KEY
				(
					id,
					sdate
				)
		);

		DROP TABLE IF EXISTS stock_daily_MT;
		CREATE TABLE IF NOT EXISTS stock_daily_MT
		(
			sdate varchar(10),
			id varchar(10),
			mt_b_qty decimal(18, 0),
			mt_s_qty decimal(18, 0),
			mt_r_qty decimal(18, 0),
			mt_qty decimal(18, 0),
			mt_dec_qty decimal(18, 0),
			mt_limit_qty decimal(18, 0),
			mt_use_percent decimal(18, 2),
			ss_b_qty decimal(18, 0),
			ss_s_qt decimal(18, 0),
			ss_r_qty decimal(18, 0),
			ss_qty decimal(18, 0),
			ss_dec_qty decimal(18, 0),
			ms_percent decimal(18, 2),
			ms_dec_qty decimal(18, 0),
			CONSTRAINT PK_stock_daily_MT
				PRIMARY KEY
				(
					id,
					sdate
				)
		);

		DROP TABLE IF EXISTS stock_daily_MR;
		CREATE TABLE IF NOT EXISTS stock_daily_MR
		(
			sdate varchar(10),
			id varchar(50),
			id_sub varchar(50),
			id_mr varchar(50),
			mrname varchar(255),
			b_qty decimal(18, 0),
			s_qty decimal(18, 0),
			dec_qty decimal(18, 0),
			dstatus int,
			trs_percent decimal(18, 2),
			CONSTRAINT PK_stock_daily_MR
				PRIMARY KEY
				(
					id,
					sdate
				)
		);
END //
DELIMITER ;
-- 呼叫PROCEDURE
CALL CreateStockTable();
```

2. 第 隻要執行的SP為`procExportTableSchema`

```sql
-- ====================================================================
-- SP Name     : procExportTableSchema
-- Function    : 批次匯出table schema
-- Author      : Mark
-- Create Date : 2023-10-22
-- Parameter   : DBName
-- Modify His  : 
-- (1) 2023-10-22 : Mark    : CREATE 
-- (2) 2023-10-23 : Mark    : 
-- a、Modify SP describe
-- b、CREATE COLUMN CHINESE NAME
-- c、UPDATE SP NAME
-- d、UPDATE CSV COLUMN NAME
-- e、Add CSV Header For User Choose Language
-- f、UPDATE COLUMN CHINESE NAME
-- g、UPDATE FIRST USE DB
-- ===================================================================
-- 使用stock資料庫
use stock;
DELIMITER $$
-- 如果PROCEDURE存在就先移除                                                                                                                                                                   
DROP PROCEDURE IF EXISTS procExportTableSchema $$       
-- 建立PROCEDURE(傳入資料庫名稱參數)                                                                                                                           
CREATE PROCEDURE procExportTableSchema(DBName varchar(255),title_language varchar(255))    
BEGIN   
		-- 變數宣告
			-- 1. 資料表集合名稱
			-- 2. 取得最後 張資料表
			-- 3. 時間戳記
        DECLARE table_name VARCHAR(255);                                                                                                                                        
        DECLARE end_of_tables INT DEFAULT 0;
        DECLARE mylocaltimestamp DATETIME;
		
        -- 利用SQL取出指定資料庫裡面所有資料表的list，直到最後 張資料表為止
        DECLARE cur CURSOR FOR                                                                                                                                                  
            SELECT t.table_name                                                                                                                                                 
            FROM information_schema.tables t                                                                                                                                    
            WHERE t.table_schema = DBName AND t.table_type='BASE TABLE';                                                                                                 
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET end_of_tables = 1;                                                                                                           
		
        OPEN cur;                                                                                                                                                               
		
        -- 迴圈開始
        tables_loop: LOOP                   
            	
			-- 將資料集透過迴圈取出，最後 張表時強制離開迴圈
            FETCH cur INTO table_name;             			
            IF end_of_tables = 1 THEN                                                                                                                                           
                LEAVE tables_loop;                                                                                                                                              
            END IF;                                                                                                                                                             
			
            -- 使用CONCAT串接SQL語法(這 段是查看SQL結果，可以拿掉不執行)
            -- SET @show_schema = CONCAT("desc"," ",DBName,".",table_name);
            -- 建立PREPARE STATEMENT，並執行
            -- PREPARE stmt FROM @show_schema;                                                                                                                                               
            -- EXECUTE stmt;     
  
            -- 取得當下時間戳記
			SET @mylocaltimestamp=DATE_FORMAT(NOW(),'%Y-%m-%d %H-%i-%s');
            -- 取得CSV匯出路徑
            SET @windows_path='C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/';
            
            -- 取得CSV檔名
            CASE title_language
			WHEN 'ch' THEN 
				 SET @file_name=CONCAT(@windows_path,@mylocaltimestamp,"_",table_name,'_ch.csv');
			WHEN 'en' THEN 
				 SET @file_name=CONCAT(@windows_path,@mylocaltimestamp,"_",table_name,'_en.csv');
				 ELSE BEGIN END;  
			END CASE;
                       
            -- 判斷不同的資料表，給予不同的中文欄位名稱
			CASE table_name
			WHEN 'stock_list' THEN
			   SET @table_type='證券清冊';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱' 
                            WHEN COLUMN_NAME='stock_attr' THEN '上市上櫃類別'
                            WHEN COLUMN_NAME='industry' THEN '產業分類'
						ELSE 'null'
						END)"
						);
                        
			WHEN  'stock_daily' THEN
			   SET @table_type='每日收盤資訊';
			   SET @caseSQL=CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱'
                            WHEN COLUMN_NAME='trs_qty' THEN '成交股數'
                            WHEN COLUMN_NAME='trs_count' THEN '成交筆數'
                            WHEN COLUMN_NAME='trs_amt' THEN '成交金額'
                            WHEN COLUMN_NAME='open_price' THEN '開盤價'
                            WHEN COLUMN_NAME='h_price' THEN '最高價'
                            WHEN COLUMN_NAME='l_price' THEN '最低價'
                            WHEN COLUMN_NAME='close_price' THEN '收盤價'
                            WHEN COLUMN_NAME='s_status' THEN '漲跌(+/-)'
                            WHEN COLUMN_NAME='dec_price' THEN '漲跌價差'
                            WHEN COLUMN_NAME='lb_price' THEN '最後揭示買價'
                            WHEN COLUMN_NAME='lb_amt' THEN '最後揭示買量'
                            WHEN COLUMN_NAME='ls_price' THEN '最後揭示賣價'
                            WHEN COLUMN_NAME='ls_amt' THEN '最後揭示賣量'
                            WHEN COLUMN_NAME='PE' THEN '本益比'
						ELSE 'null'
						END)"
						);
                        
			   WHEN 'stock_monthly_revenue' THEN
			    SET @table_type='每月營收';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='yyyymm' THEN '營收年月' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱'
                            WHEN COLUMN_NAME='month_amt' THEN '當月營收'
                            WHEN COLUMN_NAME='pre_m_amt' THEN '上月營收'
                            WHEN COLUMN_NAME='pre_y_amt' THEN '去年當月營收'
                            WHEN COLUMN_NAME='pre_m_percent' THEN '上月比較增減(%)'
                            WHEN COLUMN_NAME='pre_y_percent' THEN '去年同月增減(%)'
                            WHEN COLUMN_NAME='sum_amt' THEN '當月累計營收'
                            WHEN COLUMN_NAME='per_sum_amt' THEN '去年累計營收'
                            WHEN COLUMN_NAME='sum_percent' THEN '前期比較增減(%)'
                            WHEN COLUMN_NAME='memo_str' THEN '備註'
						ELSE 'null'
						END)"
						);
                        
			WHEN 'stock_daily_3' THEN
               SET @table_type=' 大法人進出';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='f_qty' THEN '外資'
                            WHEN COLUMN_NAME='i_qty' THEN '投信'
                            WHEN COLUMN_NAME='s_qty' THEN '自營商'
                            WHEN COLUMN_NAME='t_qty' THEN '單日合計'
                            WHEN COLUMN_NAME='est_f_qty' THEN '估計外資持股'
                            WHEN COLUMN_NAME='est_i_qty' THEN '估計投信持股'
                            WHEN COLUMN_NAME='est_s_qty' THEN '估計自營商持股'
                            WHEN COLUMN_NAME='est_t_qty' THEN '合計'
                            WHEN COLUMN_NAME='trs_f_percent' THEN '外資比例'
                            WHEN COLUMN_NAME='trs_3_percent' THEN ' 大法人比例'
						ELSE 'null'
						END)"
						);
			WHEN 'stock_daily_mr' THEN
               SET @table_type='主力進出';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '日期' 
							WHEN COLUMN_NAME='id' THEN '股票代號'
                            WHEN COLUMN_NAME='id_sub' THEN '券商代號'
                            WHEN COLUMN_NAME='id_mr' THEN '券商主代號'
                            WHEN COLUMN_NAME='mrname' THEN '券商名稱'
                            WHEN COLUMN_NAME='b_qty' THEN '買進'
                            WHEN COLUMN_NAME='s_qty' THEN '賣出'
                            WHEN COLUMN_NAME='dec_qty' THEN '買超'
                            WHEN COLUMN_NAME='dstatus' THEN '買or賣'
                            WHEN COLUMN_NAME='trs_percent' THEN '佔成交比重'
						ELSE 'null'
						END)"
						);
			WHEN 'stock_daily_mt' THEN
               SET @table_type='融資融券';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='mt_b_qty' THEN '融資買進'
                            WHEN COLUMN_NAME='mt_s_qty' THEN '融資賣出'
                            WHEN COLUMN_NAME='mt_r_qty' THEN '融資現償'
                            WHEN COLUMN_NAME='mt_qty' THEN '融資餘額'
                            WHEN COLUMN_NAME='mt_dec_qty' THEN '融資增減'
                            WHEN COLUMN_NAME='mt_limit_qty' THEN '融資限額'
                            WHEN COLUMN_NAME='mt_use_percent' THEN '融資使用率'
                            WHEN COLUMN_NAME='ss_b_qty' THEN '融券賣出'
                            WHEN COLUMN_NAME='ss_s_qt' THEN '融券買進'
                            WHEN COLUMN_NAME='ss_r_qty' THEN '融券券償'
                            WHEN COLUMN_NAME='ss_qty' THEN '融券餘額'
                            WHEN COLUMN_NAME='ss_dec_qty' THEN '融券增減'
                            WHEN COLUMN_NAME='ms_percent' THEN '券資比'
                            WHEN COLUMN_NAME='ms_dec_qty' THEN '資券相抵'
						ELSE 'null'
						END)"
						);	

				ELSE BEGIN END;  
			END CASE;
		
			-- 判斷CSV表頭要使用哪種語言(中文、英文)
            CASE title_language
			WHEN 'ch' THEN 
				SET @title= CONCAT("'",'欄位名稱',"'",",","'",'資料型態',"'",",","'",'是否null',"'",",","'",'主鍵/外來鍵',"'",",","'",'欄位描述',"'",",","'",'資料表分類',"'");
                
			WHEN 'en' THEN 
				SET @title= CONCAT("'",'COLUMN_NAME',"'",",","'",'DATA_TYPE',"'",",","'",'IS_NULLABLE',"'",",","'",'COLUMN_KEY',"'",",","'",'DESC',"'",",","'",'COLUMN_NAME',"'");
				ELSE BEGIN END;  
			END CASE;
            
            -- 串接SQL匯出語句
			SET @export_csv = CONCAT("SELECT ",@title,"
			UNION
			select COLUMN_NAME,DATA_TYPE,IS_NULLABLE,COLUMN_KEY,",@caseSQL,",","'",@table_type,"' FROM information_schema.columns 
			where table_schema = '",DBName,"' AND table_name='",table_name,"' 
			INTO OUTFILE '",@file_name,"' CHARACTER SET Big5 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n'"); 
            
            -- 這 段供測試用
            SELECT @export_csv;
            -- 執行SQL
			PREPARE stmt2 FROM @export_csv;                                                                                                                                               
  			EXECUTE stmt2; 

         -- 迴圈結束
        END LOOP;                                                                                                                                                               
        CLOSE cur;                                                                                                                                                              
    END $$                                                                                                                                                                      
DELIMITER ;
-- 設定資料庫名稱、表頭語言參數 
SET @DBName='stock';
SET @title='en';
-- 呼叫PROCEDURE並傳入參數(資料庫名稱、表頭語言)
call procExportTableSchema(@DBName,@title);
```


### 1.5.3. (3) 注意事項

1. 請依序執行SP，先執行`建立資料表SP`，再執行`匯出資料表結構SP`
2. 請將代碼複製貼上`整段執行`(不要`單獨執行`會`出錯`)
3. 請先安裝`mysql workbench`，並確認`mysql`程序`可正常執行`

### 1.5.4. (4) 步驟開始

1. 將剛才下載的檔案`批次建立stock table.sql`，將語法整段複製起來，貼到`mysql Workbench`，如下圖
![image-20231023101347673](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/eb43ff5b-image-20231023101347673.png)

2. 點選`執行`按鈕，看到以下執行結果為綠勾勾，表示執行無誤，此時`重新整理`左側的`資料庫清單`，可以發現`已建立stock`資料庫以及對應的`6個資料表`，如下圖
![image-20231023101459437](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/d5ee3841-image-20231023101459437.png)

3. 將剛才下載的檔案`批次匯出table schema.sql`，將語法整段複製起來，貼到`mysql Workbench`，如下圖
![image-20231023101534154](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/sCY715a88d7-image-20231023101534154.png)

4. 點選`執行`按鈕，看到以下執行結果為`綠勾勾`，表示執行無誤，此時會出現`資料表結構查詢結果`，以及在`指定目錄下生成CSV`
![image-20231023101622238](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7e3b9051-image-20231023101622238.png)

5. 執行完成到此目錄，C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/，查看是否成功產生CSV檔案。
![image-20231023101709795](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/VOK079750be-image-20231023101709795.png)