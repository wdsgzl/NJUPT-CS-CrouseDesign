<html>
<head>
<meta charset = "utf-8" />
<title>WELCOME</title>
<style>
  .container {
    display: flex;
    justify-content: space-around; /* 水平方向上等间隔分布 */
    align-items: center; /* 垂直方向上居中对齐 */
    height: 200px; /* 容器高度 */
  }
 
  .section {
    flex: 1; /* 每个section占据等分的空间 */
    border: 1px solid #000; /* 边框，以便于观察位置 */
    padding: 10px; /* 内边距 */
    text-align: center; /* 文本居中 */
  }
  .first-button {
  margin-right: 20px; /* 设置右边距为20像素 */
   margin-left: 20px;
   padding:5px;
}
 
.second-button {
  margin-left: 20px; /* 设置左边距为20像素 */
   padding:5px;
}
  body, html {
            height: 100%;
            margin: 0;
        }
        /* 设置背景图，并使其覆盖整个屏幕 */
        body {
            background-image: url('home.jpeg'); /* 替换为自己的图片路径 */
            background-position: center center; /* 图片居中 */
            background-repeat: no-repeat; /* 不重复 */
            background-size: cover; /* 覆盖整个屏幕 */
        }

</style>


</head>
<body>
<?php
session_start();
if(isset($_POST['submit'])){
   $current=1;
}
if(isset($_POST['nosubmit'])){
   $current=0;   
}

if($current)
{
$pyfile = "sendout.py";
$pyfilel = "sendoutc.py";
$pyfilec = "sendoutl.py";
//$pyfilet ="timeout.py";
exec("python3 {$pyfile}");
exec("python3 {$pyfilec}");
exec("python3 {$pyfilel}");
//exec("python3 sendout.py");


}

$db = new SQLite3('../mytest/db.sqlite3');
 $result = $db->query('select * from Tem order by time desc limit 1');
while ($row = $result->fetchArray()) {
   $temp=$row['Temperature'];
   $statust=$row['status'];
} 
 $result = $db->query('select * from Lig order by time desc limit 1');
while ($row = $result->fetchArray()) {
    $ligh=$row['Lightness'];
    $statusl=$row['status'];
} 
 $result = $db->query('select * from Dio order by time desc limit 1');
while ($row = $result->fetchArray()) {
    $CO=$row['CCOO'];
    $statusc=$row['status'];
} 


?>
<div class="container">
  <div class="section">
    <p> <lable>Temperature：<?php if($statust=="True"){echo $temp;} else{echo "offline";} ?></lable></p>
  </div>
  <div class="section">
    <p><lable>Light：<?php if($statusl=="True"){echo $ligh;} else{echo "offline";} ?></lable></p>
  </div>
  <div class="section">
    <p><lable>C02：<?php if($statusc=="True"){echo $CO;} else{echo "offline";} ?></lable></p>
  </div>
</div>
<img src="a.jpeg" width="200" height="200"/>
<br />
<img src="b.jpeg" width="200" height="200"/>
<br />
<img src="c.jpeg" width="200" height="200"/>

<form action="index.php" method="post">
<label><input type = "submit" name="submit" class="first-button" value = "获取最新数据"/></label>
<label><input type = "submit" name="nosubmit" class="second-button"value = "查询最近数据"/></label>
</form>
</body>
</html>
