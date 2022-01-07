# seatapp
> 2020年開始的新冠疫情，讓我們的生活型態產生許多改變，當參加大型活動時，需要實名制，甚至連座位都需要紀錄，以方便後續疫調；因此在2021年台灣疫情再次爆發時，開發了這個網站，紀錄與會者的出席紀錄，同時也將座位以圖像化來呈現。

## 使用方法
- 與會者：  
與會者進場時，先掃描QRCode填寫Google表單，填寫基本資料和座位編號後送出表單
- 工作人員：  
監看頁面
![img](https://github.com/JT-427/seatapp/blob/main/assets/screenshot.png)  
右下區為座位圖，黑色代表該位子已經有人，灰色則為空座位

## 程式設計
- **框架**  
[Dash](https://dash.plotly.com)，是一個能夠簡單快速的將前端、後端，一次解決的框架

- **資料儲存位置**  
    - 用Google Sheet來進行紀錄，串接Google提供的[Sheet API](https://developers.google.com/sheets/api)，來讀取資料。  
        ```py
        gc = pygsheets.authorize(service_account_file=DATA_PATH.joinpath("xxxxx.json"))
        survey_url = 'https://docs.google.com/spreadsheets/xxxxx'
        sh = gc.open_by_url(survey_url).sheet1.get_all_values()
        ```
    - 網頁每5秒會對Sheet Api送出請求，以取得更新資料。


- **Server**  
以[Heroku](https://www.heroku.com)這個免費的伺服器來讓此網頁上架到公網上，以便隨時瀏覽

## 專案停止
- **疫情升溫**  
因疫情持續升溫，不再像2021/5以前一樣，各場所自行紀錄出入人員（我們是透過Google表單紀錄），而是改由政府推出的簡訊實聯制來計入蹤跡，因此串接Google Sheet之功能不再符合需求。

- **框架不符合使用需求**  
Dash是個很方便的框架，只需要用到Python即可完成前後端的設計，但也是因為這個框架都幫我們設計好了，導致前端頁面不夠自由。

- **資料儲存**  
利用Google試算表固然方便，但也有一些隱私的隱憂；除此之外，若需建置一個完整的系統，只有一張Table勢必無法符合需求，因此需改為以資料庫來儲存資料。

- **伺服器**  
Heroku是一個免費且方便的伺服器，它已將許多伺服器相關的設定完成，我們只需要按著規範將程式碼上傳，即可部署完成。但在我的使用經驗中，常常遇到一陣子沒有打開網頁，伺服器就會進入休眠，需要一段時間等待伺服器重啟，才能連上線，造成使用體驗不佳，因此如果需要上線使用，還是得租借虛擬伺服器，自行部署網頁。


***
### 專案開發期間
2021/5~2021/6