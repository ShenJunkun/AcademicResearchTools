# AcademicResearchTools --- 学术研究工具
## overview
科学研究中使用的一些工具，包括[数据采集工具](https://github.com/ShenJunkun/AcademicResearchTools/tree/master/dataCollecting)，[数据可视化工具](https://github.com/ShenJunkun/AcademicResearchTools/tree/master/dataVisualization)。

- [dataCollecting](https://github.com/ShenJunkun/AcademicResearchTools/tree/master/dataCollecting):数据采集工具。

- [dataVisualization](https://github.com/ShenJunkun/AcademicResearchTools/tree/master/dataVisualization):数据可视化工具。

## 数据采集工具

### 使用`ThreadPoolExecutor`收集CPU、GPU使用信息

- [memCollect.py](https://github.com/ShenJunkun/AcademicResearchTools/blob/master/dataCollecting/memCollect.py): 收集CPU memory, GPU memory的使用情况。

- [usage_metrics_gpu.py](https://gist.github.com/jmansour/17c9d4e6767fab22a317ba795e171df1): GPU使用率收集。

- [How Can I Obtain GPU Usage Through Code](https://support.huaweicloud.com/intl/en-us/modelarts_faq/modelarts_05_0374.html): GPU使用率收集

### 使用守护线程和subprocess收集信息
- [example](https://github.com/ShenJunkun/AcademicResearchTools/blob/master/dataCollecting/daemonProcess/example.py): 使用守护线程收集信息的示例。
- 如何需要收集其他的系统信息，可以对 [example](https://github.com/ShenJunkun/AcademicResearchTools/blob/master/dataCollecting/daemonProcess/example.py)中的`daemon_function`进行修改，非常感谢[@esir kings](https://gist.github.com/esirK/)在gist的代码示例。具体讲解可以参考[Machine monitoring tool using python from scratch](https://medium.com/the-andela-way/machine-monitoring-tool-using-python-from-scratch-8d10411782fd)。
  - [monitor.py](https://github.com/ShenJunkun/AcademicResearchTools/blob/master/dataCollecting/daemonProcess/monitor.py)
