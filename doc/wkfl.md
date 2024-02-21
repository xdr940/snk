# 工作流

snk的工作流程，遵循 场景构建、场景载入、产生实例、评估等主要四个部分

![](../fig/wkfl.png)

## 场景创建
snk通过snk-scenario创建空间网络场景。
每个场景通过config.yaml文件描述（图中（1）Input），并在`run.sh`中编辑生成路径。创建场景时，执行
`bash run.sh`即可，此时产生Scenario文件 (图中（2）Generate)



## 场景载入

1. **step1**
在config.yaml文件中，有场景生成路径，创建后会生成一个文件夹，里面就是场景所需的文件。
`dump_path: "/home/roit/datasets/cesiumData/XZL" `

2. **step2**
在snk-visualizer 的config.yaml文件中，修改为相同的路径（图中（3）Load）
`base:"../data/XZL/"`
所以，不同的场景比较需要修改为各自不同的路径。
注意，已经通过软连接 连接了 /home/roit/datasets/cesiumData 和snk-visualizer/data 两个文件夹。

3. **step3**
  修改场景后，编辑
`snk-visualizer/configs/config.yaml` 的`load_data`参数，选择性载入不同类的场景实体 ，例如仅载入卫星，链路和随遇链路编辑为：`load_data: ['sats','isls','eisls']`

4. **step4**
 在vsc中点击右下go live，弹出系统前端，场景显示


## 产生实例

实例文件产生的一般步骤如下：

- 编辑`snk-server/configs/config.yaml` 配置文件，实例保存路径为`save_path: "/home/roit/models/xzl"`

- 打开snk-server后端

- 打开snk-visualizer前端，连接成功

- snk-visualizer中点击init

- 选择procedure，包括`edge2edge, conTest, async, sce2ins`

- 实例计算产生中，如果嫌慢最小化snk-visualizer，实例产生完毕并保存为之前的路径，文件夹格式为`yyyymmdd_hhmmss`（图中（5）Calculate）


```对于eISL的相关评估，选择conTest```

## 评估

对应图中（6）（7）。包括场景评估和实例评估。

```bash
评估
├── 场景评估
│     ├── eISL综合评估
│     └── ...
└──  实例评估
      ├── 全局时延
      ├── 全局伸张率
      └── 随机可达率

```

场景评估：通过生成不同的场景（Scenario）来评估，包括eISL数量及其分布、


实例评估：**相同**路由策略等因素下，载入**不同**场景(scenario)， 得到实例文件ins1, ins2, ins3....然后对其评估比较。


评估一般步骤如下:

- 在snk-analyzer中，写脚本

- 脚本中载入产生的场景\实例文件

- 计算指标，得到图表

对于eISL相关评估，主要包括时延评估，路径伸张率评估，随机可达性评估等。



#### 全局时延评估

conTest中，任意端点卫星相同，最短路径算法(非最小跳数？)测试时延比较。

#### 随机可达率


conTest中，任意端点卫星相同，MPLF算法，能否可达。


#### 网络容量

  $C(\mathcal{G}^t)  = \mathop{min}[ \sum\limits_{e \in \mathcal{E}^t} C(e), \sum\limits_{v \in \mathcal{V}} C(v) ]$

  链路FSL在变，C也在变

#### 网络吞吐量

 $\mathcal{T}(\mathcal{P}^t) = \mathop{maxflow}[ \mathcal{P}^t, v_{src},v_{dst}]$

$\mathcal{P}^t$ 是t时刻，网络中所有的通信会话 路径集合。网络吞吐量就等价为 抽象出 超级源点、超级sink点的最大流。












