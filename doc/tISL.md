# 临时链路建立机制



## 程序中eISL的建立步骤

参考`eISLs.py`代码


随遇链路的生成在代码中，分四步：

1. 所有可能的建链情况计算
  	任意卫星，两两计算，计算出最宽泛的约束下可能的建链情况。
	计算后，会得到命名为 access_stamps 的dict，其数据结构如下

```json
# access_stamps
{
	"eisls": {
		"eISL-00107-00504": [[1151.0, 1368.0], [4297.0, 4521.0], [7450.0, 7667.0], [10596.0, 10820.0], [13749.0, 13966.0], [16895.0, 17119.0], [20048.0, 20265.0], [23194.0, 23418.0], [26347.0, 26564.0], [29493.0, 29717.0], [32646.0, 32863.0], [35792.0, 36016.0], [38945.0, 39162.0], [42091.0, 42315.0], [45244.0, 45461.0], [48390.0, 48614.0], [51543.0, 51760.0], [54689.0, 54913.0], [57842.0, 58059.0], [60988.0, 61212.0], [64141.0, 64358.0], [67287.0, 67511.0], [70440.0, 70657.0], [73586.0, 73810.0], [76739.0, 76956.0], [79885.0, 80109.0], [83038.0, 83255.0], [86184.0, 86400.0]], 
		"eISL-00103-00500": [[517.0, 741.0], [3670.0, 3888.0], [6816.0, 7040.0], [9969.0, 10187.0], [13115.0, 13339.0]],
		"...":[]
	}
}
```

上述的**键**为可能的eISL(两个)，**值**为eISL建立时刻和结束时刻。后续就是根据以上的数据进行筛选，最后得到一个精简的access_stamps,然后再后处理为czml文件

2. 过滤
	根据自定义的约束，对access_stamps进行处理，处理后得到相同数据结构的数据，自己在 stamps_filter中实现

3. 后处理
   筛除对不在场景时间内的链路，并根据access_stamps，格式化成czml格式

4. 保存

其中，step3是重点。
