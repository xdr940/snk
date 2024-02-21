# Space Networking Kit

English | [中文文档](README_ch.md)

A simulation\emulation system for space networking.



*SNK* is a simulation\emulation  platform designed to evaluate the network performance of constellation systems for global Internet services.  SNK offers real-time communication visualization and supports the simulation of routing between edge node of network.  The platform enables the evaluation of routing and network performance metrics such as latency, stretch, network capacity, and throughput under different network structures and density.   The effectiveness of SNK is demonstrated through various simulation cases, including the routing between fixed edge stations or mobile edge stations and analysis of space network structures.

This framework contains:
- [snk-scenario](https://github.com/xdr940/snk-scenario)
- [snk-visualizer](https://github.com/xdr940/snk-visualizer)
- [snk-server](https://github.com/xdr940/snk-server)
- [snk-analyzer](https://github.com/xdr940/snk-analyzer)


# SNK workflow

![](./fig/wkfl.png)

# SNK arch

![](./fig/framework.png)




# scenario

![](./fig/sce_abs.png)

![](./fig/har2lon.png)


# evaluation
![](./fig/cities.png)

![](./fig/loads_thp.png)
![](./fig/stretch_evo.png)


# citation

```
@inproceedings{snk,
title={Space Networking Kit: A Novel Simulation Platform for Emerging LEO Mega-constellations},
author={Xiangtong, Wang and Xiaodong, Han and Menglong, Yang and Songchen, Han and Wei Li}
booktitle={IEEE International Conference on Communications 2024},
year={2024}
}

@misc{snk,
title={Space Networking Kit: A Novel Simulation Platform for Emerging LEO Mega-constellations},
author={Xiangtong Wang and Xiaodong Han and Menglong Yang and Songchen Han and Wei Li},
year={2024},
eprint={2401.07511},
archivePrefix={arXiv},
primaryClass={cs.NI}
}
```