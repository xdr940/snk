

# ACCESS


## overview

access 数据结构是构建 eISL\GSL\MSL\oISL等非持久链路所需要的。 
节点两两access需要考虑相对位姿以及sensor覆盖范围。
目前仅实现了球面sensor，如下

$| p_{src} - p_{tgt} | - L(t,p_{src}) =0$

其中$p_{src}$本节点的笛卡尔坐标

未来，应实现$p_{src}$为运动曲面（sensor），随着时间，若$p_{tgt}$在

$F(r_{src},p_{tgt},t) =0$

其中$r_{src}$是源点的6D位姿。

## implementation

1. API code

```python
#1. build access structure
 acc = Access(
	start_time=sce_start_time,
	end_time=sce_end_time,
	time_step=time_step,
	borderDistance=layer_radius/np.cos(np.deg2rad(layer_steering_angle))
	)
#2. load src and tgt nodes (core)
 for sat in sats:
	acc.sat_with_gses_stamp_update(sat,gses)

#3. get access stamps
access_stamps = acc.get_access_stamps()

```

2. built-in code (前面#2的部分)

```python
# sats with gses (fixed nodes)
    def sat_with_gses_stamp_update(self,sat,gses):
        '''
        :param sat:
        :param gses:
        :return: self.access_stamps
        '''
        self.load_sat(sat) #step 1
        for gs in gses:
            self.load_gs(gs) #step 2
            # caculate range between sat,gs
            self.range_log_gs() #step 3

# sat with mses (mobile nodes)
	def sat_with_mses_stamp_update(self,sat,mses):
        '''
        :param sat:
        :param mses:
        :return: self.access_stamps
        '''
        self.load_sat(sat)
        for ms in mses:
            self.load_ms(ms)
            self.range_log_ms()# calculate stamp

```


- step.1 
```bash
/-full time-/
src: o---o---o---o---o
tgt: 
```
载入src nodes，一般都是卫星，并根据卫星czml的关键点数据，构建插值函数fx,fy,fz


- step.2 
```bash
     /---full time----/
src: o---o---o---o---o
tgt: o #load gs
tgt: o---o---o---o---o #load mses
```

- step.3 #range_log

```bash
     /---full time----/
src: ooooooooooooooooo
tgt: ooooooooooooooooo #range_log_gs
tgt: ooooooooooooooooo #range_log_ms
```