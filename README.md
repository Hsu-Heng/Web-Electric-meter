# Web-Electric-meter(智慧電錶API)

使用Django框架，功能為查詢使用的電度，資料庫使用Mongo, Hbase
hbaset.py, /mater/madetest.py 能生成測試資料

```html
  <head>
    <meta charset="utf-8"> 
    <title> Test </title>
  </head>
    <body>
      <form action="" method="post">
        <label for="begin_time">開始時間</label>
        <input id = "begin_time" type="text" name="begin_time" >
        <span style= "display:block"></span>
        <label for="end_time">結束時間</label>
        <input id = "end_time" type="text" name="end_time" >
        <span style= "display:block"></span>
        <label for="range">range</label>
        <input id = "queryrange" type="text" name="queryrange" >
        <span style= "display:block"></span>
        <label for="device_id">device_id</label>
        <input id = "device_id" type="text" name="device_id" >
        <span style= "display:block"></span>
        <input type="hidden" name="ok" value="yes">
        <input type="submit" value="query">
      </form>
    </body>
```
