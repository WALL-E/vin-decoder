# vin-decoder

车架号(车辆识别码)查询服务/校验服务


## 使用方法
提供web查询服务

```
curl http://127.0.0.1/vin/v1/LVSHCAMB1CE054249
```

## 技术栈

* Python
* Tornado
* Mongodb

## 正确性校验服务
从组成规则验证vin是否合法

 * 只包含阿拉伯数字和罗马字母(字母I,O,Q不能使用)
 * 校验码验证

## Mongodb文档

* WMI
  * 判断是否为欧版还是美版
  * [WMI Region](https://en.wikibooks.org/wiki/Vehicle_Identification_Numbers_(VIN_codes)/World_Manufacturer_Identifier_(WMI))
* WMI+VDS
  * 美版(中国)，包含校验码，需要忽略
  * 欧版，没有校验码
* YEAR
  * 年份代码表（30年循环一次）