# `TODOs`

网络模拟单元难度太大，空间仿真部分暂时不整了，其暂未完成工作如下

### 1. 开发、重构
  - [X] **异步交互模式开发$(\star\star\star)$:** 参考onos [通过文件共享，以及ontick（）实现]
 
  - [x] **考虑tISL的连通性$(\star\star)$：** 实现随遇卫星可达性(reachability)分析
  - [ ] **Access锥形方程$(\star\star)$：** 目前access使用的方程是$F_1 = \|p_1 - p_2\|-L \leq 0$, 后面加入圆锥方程以及更复杂的sensor方程，以实现椭圆轨道球层的层间链路（lISL）
  - [x] **Procedures整合$(\star)$：** 把exp1,exp2等单独放一坨，目前只有replay
  - [ ] **集成到mininet/CLI$(\star\star\star)$**
  - [ ] replay 模式重新搞
  - [ ] Analysor 独立，考虑opnet的statistics分析器
  - [x] fwd高亮后颜色还原，另外fwd要重新处理下
  - [x] fwd 颜色变化(类似宏定义)
  - [x] sat的颜色变化
  - [x] SAT 的ID重新设置为“SAT-00001”,但是label还是00001
  - [ ] 对于utils 包，发布？统一整理、应用   snk_utils # under going
  - [ ] scenario中，小规模构建场景，通过mask？
  - [x] 整个系统中关于时间的控制，2000-01-01
  - [x] GS的ID "GS-001"，name = Harbin
  - [x] 面向对象的GET POST，抽象类，放到snklib？
  - [ ] access rename as association.
  - [ ] 通过独立组件控制报文的一致性
  - [ ] 对路径中的一般卫星节点和邻接边缘的卫星节点做区分，（edge2edge.py, line 131 132）
  - [x] 更新其他过程，将过程中的cmd交互统一写到snklib中，减少代码修改量
  - [ ] 轨道颜色的循环
  - [ ] func sat 那里的msl还不支持卫星，搞一下

### 2. 加速、优化
  - [ ] **ECI坐标下临时链路过多$(\star\star)$** 
  - [x] **tFWD$(\star\star)$:** 每个ISL配有两个方向的FWD，entities的数量与时间无关，但如果tISL采用类似做法，则仿真时间比较长的时候entities会非常多，匹配的tFWD也会很多，考虑如何处理

