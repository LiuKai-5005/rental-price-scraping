
# 使用Python脚本，每日爬取租房价格

在美国租房，特别是旧金山湾区，房租占据每个月的开销的大头。租房的房源通常来自公寓或者私人房东。很多人会选择专门的出租公寓，这种公寓只租不卖，经营也比较专业化。大部分出租公寓会有官网可以查询价格/空房，并且可以在线签约，规模小一些的出租公寓可能就没有官网，租房信息只挂在第三方租房网站上。下面记录了一下我已经实现的过程。

---

## 项目简介

本项目用于每日自动爬取美国湾区公寓的租房价格，帮助租客及时了解价格变动，寻找最佳租房时机。脚本支持抓取 Century Towers 和 Radius 两个公寓的价格信息，并生成价格走势图。

## 需求分析
- 公寓在线价格每天变化，户型选择多，理想户型可能价格高或难抢。
- 房间在 available date 后若未租出，价格会调整（通常递减）。及时掌握价格变动有助于捡漏。
- 使用 Flask 框架的 Python 脚本，每天定时查询房租信息，保存本地或推送至手机、邮箱、微信等。

## 问题分析
- 主动 pull 信息，无法实时感知价格变化，只能设置 pull frequency 反复探测。
- 推送到手机或邮箱功能尚未实现（TODO）。

## 依赖环境

- Python 3.7 及以上
- 依赖库：Flask、requests、matplotlib、csv

安装依赖：
```bash
pip install flask requests matplotlib
```

## 使用方法

1. 克隆本仓库到本地。
2. 运行 `Century_Towers_2b2b.py` 或 `Radius_2b2b.py`，脚本会自动抓取未来 60 天的价格数据。
3. Century Towers 的结果保存在 `C:\temp` 文件夹下，Radius 的结果保存在 `Radius` 文件夹下（csv 和图片）。
4. 查看生成的价格走势图（PNG图片）和数据文件（TXT/CSV）。

## 简介
`Essex` 和 `Avalon` 都是湾区知名连锁出租公寓，以 Essex 举例：

- 官网: https://www.essexapartmenthomes.com/apartments/san-jose/century-towers/floor-plans-and-pricing
- 官网价格区截图:
![price](https://user-images.githubusercontent.com/54691613/147894380-ad5f1766-0cec-4615-a37b-86ecaa8233cb.png)

## 脚本说明

- `Century_Towers_2b2b.py`：抓取 Century Towers 公寓 C1、C2、C3 户型的价格，输出到 TXT 文件并生成价格走势图。
- `Radius_2b2b.py`：抓取 Radius 公寓 Ratio、Locus、Apex、Chord 户型的价格，输出到 CSV 文件并生成价格走势图。

## 实现
最初打算用爬虫抓网页文本，后发现官网有 API 可直接获取数据。按 F12 打开 Inspect，发现 GET 请求获取房源信息，无需鉴权。

API 示例：
https://www.essexapartmenthomes.com/EPT_Feature/PropertyManagement/Service/GetPropertyAvailabiltyByRange/543205/2022-03-03/2022-03-17
![api](https://user-images.githubusercontent.com/54691613/147894396-d1bf9e13-4356-41c1-8d2e-80b7ba967ca6.png)

API 支持参数如最低价格、最高价格、预期入住日期等。

Avalon 公寓的 GET URL:
https://api.avalonbay.com/json/reply/ApartmentSearch?communityCode=CA049&min=2000&max=4000&desiredMoveInDate=2022-03-01T07:00:00.000Z
可指定价格区间和入住日期，Postman 获取 Json 后可分析价格。
![avalon](https://user-images.githubusercontent.com/54691613/148008618-c3a0d534-8073-4c30-b1f5-a6b936b550ab.png)

## 代码
见 repo

## 输出结果

- 文本/CSV 文件：每日价格数据，包含日期和各户型价格。
- 图片文件：价格随时间变化的折线图，便于观察趋势。

示例：
![house_price_2022-01-02_2022-03-04](https://user-images.githubusercontent.com/54691613/147894436-3faccae7-2438-4f16-bf55-6a929f9a27fb.png)

## 未来计划 / TODO

- 实现价格变动自动推送（如邮箱、微信、手机通知）。
- 支持更多公寓和户型。
- 优化数据存储和可视化方式。

## 参考

- Essex 官网: https://www.essexapartmenthomes.com/apartments/san-jose/century-towers/floor-plans-and-pricing
- Avalon 官网: https://api.avalonbay.com/json/reply/ApartmentSearch?communityCode=CA049&min=2000&max=4000&desiredMoveInDate=2022-03-01T07:00:00.000Z

如有问题或建议，欢迎 issue 或联系作者。




