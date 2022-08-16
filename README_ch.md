# spaceflow

[English](README.md) | 中文文档

空间网络的仿真\模拟框架。


*spaceflow* 是一个仿真/仿真框架，可以对空间进行仿真，例如卫星、车辆、星际链路等，以及上述实体之间的网络仿真。该框架支持在空间网络中开发新的协议、架构和管理。

![](./fig/framework.png)

## 目录


  - [组成](#组成)
  - [cite](#cite)
  - [scenario](#scenario)
  - [visualizer](#visualizer)
  - mininet-space
  
## 组成

该框架包含三个部分：
- [scenario](https://github.com/xdr940/scenario)
- mininet-space
- [visualizer](https://github.com/xdr940/visualizer)

*scenario*用于构建空间网络的模拟场景，生成*visualizer*需要的CZML文件。

*mininet-space* 是一个基于 mininet 的网络仿真器，目前仍在开发中。暂时嵌入到整个框架中，以[visualizer-backend](https://github.com/xdr940/visualizer-backend)作为替代，实现基本操作。

*visualizer*是一个可视化工具，不仅可以将*scenario*生成的场景可视化，还可以连接到*mininet-space(visualizer-backend)*，将网络过程可视化。


## scenario

基于python，包含卫星(SATs)，地面站(GSs)，飞行器(ACs)，sensor，转发(FWDs), 链路.
其中链路又包括星间链路(ISLs), 星地链路(GSLs), 飞行器-卫星链路(ASLs), 临时兴建链路(tISLs)

构建顺序：
    `SAT.py -> ISL.py -> FWD.py`
    `GS.py -> GSL.py`
    `SAT.py -> ISL.py -> tISL.py`
    `ACs.py -> ASL.py`

## visualizer

- SAT
![](./fig/SAT.png)

- GS
![](./fig/GS.png)
- GSL
![](./fig/GSL.png)
- ISL
![](./fig/ISL.png)

- FWD
![](./fig/FWD.png)

- tISL
![](./fig/tISL.png)

- ASL
![](./fig/ASL.png)

## cite
```tex
@misc{spaceflow,

author={Wang Xiangtong},

title={SpaceFlow},
year = {2022},

howpublished={\url{https://github.com/xdr940/spaceflow}}

}


```