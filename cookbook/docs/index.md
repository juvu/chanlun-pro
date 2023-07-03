# 缠论量化分析工具 （Chanlun-PRO）

---

**基于缠论的市场行情量化分析工具**

[在线 Demo 展示](http://www.chanlun-trader.com/)  
_在线Demo只做上证指数的缠论示例_

[缠论解盘 - 善缘版本 Windows](http://docs.chanlun-trader.com/#/WINDOWS_VERSION)

**项目的核心 `cl.py` 缠论计算，需要授权许可文件才可运行，加微信好友可免费获取20天使用授权。**

_(无特殊情况，每周五例行更新)_

### 项目中的计算方法

缠论数据的计算，采用逐Bar方式进行计算，根据当前Bar变化，计算并合并缠论K线，再计算分型、笔、线段、中枢、走势段、背驰、买卖点数据；

再根据下一根K线数据，更新以上缠论数据；

如已经是形成并确认的分型、笔、线段、中枢、走势段等，后续无特殊情况，则不会进行变更。

如上，程序会给出当下的一个背驰或买卖点信息，至于后续行情如何走，有可能确认，也有可能继续延续，最终背驰或买卖点消失；

这种情况就需要通过其他的辅助加以判断，如均线、布林线等指标，也可以看小级别的走势进行判断，以此来增加成功的概率。

这种计算方式，可以很方便实现增量更新，process_klines 方法可以一直喂数据，内部会判断，已处理的不会重新计算，新K线会重复以上的计算步骤；

在进行策略回测的时候，采用以上的增量计算，可以大大缩减计算时间，从而提升回测的效率。

### QQ 群

![QQ](img/qq.png)
