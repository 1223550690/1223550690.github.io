---
title: HCIP| IS-IS
abbrlink: 11819
categories:
  - 技术记录
  - 通信网络
  - HCIP
date: 2024-12-04 16:52:06
tags:
---

#  IS-IS核心知识

## NET【网络实体名称】

<img src="https://raw.githubusercontent.com/1223550690/onism.github.io/Photos/2024/12/upgit_20241204_1733302033.png" alt="image-20241204104413233" />

OSI协议栈中设备的网络层信息，主要用于路由计算。

一台设备至少有一个NET，也可以同时配置多个NET，但是这些NET的System ID必须相同。

**Area ID**：

由IDP和DSP中的High Order DSP组成，既能够标识路由域，也能够标识路由域中的区域。

包含：AFI、IDI、High Order DSP。

**System ID**：

用来在区域内唯一标识主机或路由器。

包含：System ID

**NET配置**：

![image-20241204114129936](https://raw.githubusercontent.com/1223550690/onism.github.io/Photos/2024/12/upgit_20241204_1733302040.png)

**步骤：将Router ID补成三位，再进行四位切分，最后补上SEL位**

## 路由器分类

1. **Level-1**路由器：

​	部署在非骨干区域，属于IS-IS区域内部路由器

2. **Level-2**路由器：

​	部署在骨干区域，属于IS-IS骨干路由器

3. **Level-1-2**路由器：

   部署在骨干区域，属于IS-IS骨干路由器，用于跟**L1**与**L2**邻接

## 伪节点

IS-IS需要在所有的路由器中选举一个路由器作为**DIS**（Designated Intermediate System）。

DIS用来创建和更新伪节点（Pseudonodes），并负责生成伪节点的LSP。

DIS的选举规则如下：

- DIS优先级数值（大），缺省为64
- MAC地址（大）

------

**伪节点**是用来模拟广播网络的一个虚拟节点，交互CSNP等信息，用DIS的System ID和Circuit ID（非0值）标识。

在伪节点LSP中，**只包含邻接信息**而不包含路由信息。

------

**邻接前提**：

- 只有同一层次的相邻路由器才有可能成为邻接。
- 对于**Level-1**路由器来说，Area ID必须一致。
- 链路两端IS-IS接口的网络类型必须一致。
- 链路两端IS-IS接口的地址必须处于同一网段（默认情况下）。

## 接口开销

IS-IS有**3**种方式来确定接口的开销，按照优先级由高到低分别是:

- 接口开销: 为单个接口设置开销
- 全局开销: 为所有接口设置开销
- 自动计算开销: 根据接口带宽自动计算开销

接口开销的取值范围和接口开销类型有关。

缺省情况下，IS-IS接口的开销为**10**，最大开销为**63**，开销类型是**narrow**。

一条IS-IS路径的Cost等于本路由器到达目标网段沿的所有链路的Cost总和

## IS-IS报文类型

IS-IS采用**TLV**结构构建报文，灵活性和扩展性好

IS-IS的PDU有**4**种类型：

------

**IIH**(IS-IS Hello)：

用于邻接。

Reserved/Circuit Type：表示路由器的类型（01表示L1，10表示L2，11表示L1/L2）

------

**LSP**（ Link State PDU，链路状态报文）：

用于交换链路信息

------

**CSNP**（Complete Sequence Number PDU，全序列号报文）：

用于交流完整的LSDB信息差。缺省周期为**10秒**。

------

**PSNP**（Partial Sequence Number PDU，部分序列号报文）：

用于交流部分的LSDB信息差

## LSB

![image-20241204112454805](https://raw.githubusercontent.com/1223550690/onism.github.io/Photos/2024/12/upgit_20241204_1733302047.png)

- 命令区：源节点的系统ID
- AREA ADDR：该LSP来源的区域号
- INTF ADDR：该LSP中描述的接口地址
- NBR ID：该LSP中描述的邻接信息
- IP-Internal：该LSP中描述的网段信息

------

**LSP产生的**原因：

- 邻接Up或Down
- IS-IS相关接口Up或Down
- 引入的IP路由发生变化
- 区域间的IP路由发生变化
- 接口被赋了新的metric值
- 周期性更新（刷新间隔15min）

------

**LSP ID:**

由三部分组成，System ID、伪节点ID和LSP分片后的编号。

------

**广播网络同步：**

**LSP -> CSNP -> PSNP -> LSP**

![image-20241204114941137](https://raw.githubusercontent.com/1223550690/onism.github.io/Photos/2024/12/upgit_20241204_1733302053.png)

**点对点网络同步：**

**LSP -> PSNP -> LSP -> PSNP **

## 路由原理

- **Level-1-2**路由器在本区域置位**ATT**，以宣告可以通过自身到达其他区域。**L1**路由器收到后，会产生指向它的默认路由
- 缺省下不设置路由渗透，**L1**（非核心区）会向**L2**（核心区）传递路由，反之则不会
