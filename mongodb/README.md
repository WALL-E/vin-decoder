
# mongodb doc

## 数据库

* vin
* wmi

## 常用命令
*查看
  * show dbs
 
*使用数据库
  * use year
 
*查看文档
  * db.printCollectionStats()
  * db.getCollection("year").find()
  * db.getCollection("wmi-from-offline").find().pretty()
  * db.getCollection("wmi-from-offline").find({"WMI":"LGB"}).pretty()
 
*删除文档
  * db.getCollection("year").drop();
  * db.getCollection("wmi-from-offline").drop();

*删除数据库
  * db.dropDatabase()
