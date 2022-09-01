# spaceflow

[English](README.md) | 中文文档

空间网络的仿真\模拟框架。


*spaceflow* 是一个仿真/模拟框架，可以对空间进行仿真，例如巨星座、车辆、飞行器、舰船、星间链路等，以及上述实体之间的网络模拟，实现iperf、ping的测量。该框架支持在空间网络中开发新的设施架构、协议架构和管理架构。该框架包含三个部分：*Scenario*、*mininet-space* 和*Visualizer*，现逐个介绍

![](./fig/framework.png)


## 1.*scenario*


*scenario*为一组用户程序，用于构建空间网络的模拟场景，针对生成*visualizer*需要的`*.czml`文件，以及针对*mininet-space*生成`*.plc`文件制定网络过程。
`*.czml`文件和`*.plc`文件是仿真场景在空间和网络两个方面的不同抽象，但具有一致性，例如同一个节点在空间部分的`*.czml`文件中和和网络部分的`*.plc`文件中具有同一ID，链路等其他单元也是类似。

## 2.*visualizer*

*visualizer*是一个基于*Cesium*的Web端可视化工具，不仅可以将*scenario*生成的场景可视化，还可以连接到*mininet-space(visualizer-backend)*，将网络过程可视化。

## 3.*mininet-space*

*mininet-space* 是一个基于mininet 的网络仿真器，在整个框架中起主干部分，也是整个框架中最复杂的部分，目前以*visualizer-backend*暂时嵌入到整个框架中，以作为替代，实现基本操作。
在主体结构中，可以根据功能分为四个部分：核心子系统、CLI子系统、外部程序调用的API子系统和网络评估子系统。另外，控制器代码执行在另一个进程中，通过socket和网络仿真器交互，这里暂不讨论。

**CLI（Command Line Interface）子系统**：是用户和网络模拟器的交互接口，通过拓展mininet 命令集实现交互。拓展命令除了核心子系统的操作还包括visualizer操作（例如空间部分的开始和停止，图层的显示、隐藏等）、评估子系统（EVA）的操作等拓展。

**核心子系统**：是以mininet为基础，能根据`*.plc`文件，构建与空间场景能相互映射的网络场景，实现网络仿真的基本保障。其与mininet、mininet-space最重要的不同是添加了两个特性：
- 节点运动模型并非运行在本地进程空间而是在visualizer内；
- 节点距离变化导致的传播时延计算要在链路(link)属性中实时更新。

另外，现有核心子系统中传播模型较少，并且执行在主进程空间，在节点数量少的场景性能瓶颈不严重，后期需要将其通过异步编程，提升结点数量较多场景下的性能。


**API子系统**：主要负责网络仿真器与外部程序、其他仿真单元的交互功能。API的实现是通过开启一个独立线程，来承载Websocket服务器，并通过自定义协议，实现高通量数据交互（包括上千节点的位置或者上万个链路长度等信息）。为此，我们根据仿真需求，设计了仿真单元数据交互协议（Simulation Unit Data Interaction protocol, SUDI），并以JSON数据格式传输。

报文分为三个字段，DO、OPTION、VALUE。DO字段决定报文种类，OPTION为报文的执行参数，VALUE为报文所携带的数据。报文种类包括get报文、set报文、post报文、clear报文以及两种响应控制报文。为了后期报文的拓展以及人工干预，报文的设计类似linux命令行风格，可读性较强。另外，从Net->Space（NS）过程中，报文头部需要在visualizer内以js解析；而SN过程中用python解析。

报文各个字段含义如下：

| [DO]  | [OPTION]      | [VALUE]     | note |                  | 响应      |
| ----- | ------------- | ----------- | ---- | ---------------- | --------- |
| get   | -p,(position) | id1,id2,... | N->S |                  | post,nack |
|       | -l,(length)   | id1,id2,... | N->S |                  |
|       | --all         |             |      |                  |
|       | --sat         |             |      | 卫星             | post,nack |
|       | --gs          |             |      | 地面站           | post,nack |
|       | --ac          |             |      | 飞行器           | post,nack |
|       | --isl         |             |      | ISL              | post,nack |
| set   | -t            |             | N->S |                  |           |
|       |               |             |      |                  |           |
| post  | -p            |             | S->N | 传输position信息 | ack,nack  |
|       | -l            |             | S->N | 传输link信息     |
|       | -f            |             | N->S | 传输fwd信息      |           |
| clear | -f            |             | N->S | 清除显示的fwd    | ack,nack  |
|       |               |             |      |                  |
| ack   | -             | -           |      |                  | -         |
| nack  | -             | -           |      |                  | -         |


API子系统的技术关键在于不影响核心子系统内网络仿真、且运行时不妨碍CLI子系统正常与用户交互下实现不同仿真单元的交互。

**EVA子系统**：EVA是对网络进行可视化评估的子系统，目前实现了通过matplotlib对端到端时延、可见性、星座统计等信息的可视化演示，后期计划将其融合到SUDI中，并在visualizer中显示。


  





## cite
```tex
@misc{spaceflow,
author={Wang Xiangtong},
title={SpaceFlow},
year = {2022},
howpublished={\url{https://github.com/xdr940/spaceflow}}
}
```


![](./fig/ISL.png)

![](./fig/FWD.png)