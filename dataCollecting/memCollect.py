##########################################
#### tool to collect cpu/gpu memory
##########################################


import torch
import time
from concurrent.futures import ThreadPoolExecutor

import gc
import torch
import psutil
import csv
def see_memory_usage(force=True, scale_name="MB"):
    # if not force:
    #     return

    # python doesn't do real-time garbage collection so do it explicitly to get the correct RAM reports
    gc.collect()

    if scale_name == "MB":
        scale = 1024 * 1024
    elif scale_name == "B":
        scale = 1
    # Print message except when distributed but not rank 0
    # print(message)
    
    
    print(
        f"Current gpu mem {round(torch.cuda.memory_allocated() / scale, 2)} {scale_name} \
        Peak gpu mem {round(torch.cuda.max_memory_allocated() / scale, 2)} {scale_name} \
                CA {round(torch.cuda.memory_reserved() / scale, 2)} {scale_name} \
        Max_CA {round(torch.cuda.max_memory_reserved() / scale, 2)} {scale_name} \
        "
    )
    
    gpu_mem = round(torch.cuda.memory_allocated() / scale, 2)
    gpu_mem_max = round(torch.cuda.max_memory_allocated() / scale, 2)
    
    vm_stats = psutil.virtual_memory()
    cpu_mem = round(((vm_stats.total - vm_stats.available) / (1024 ** 2)), 2)
    # print(f"CPU Virtual Memory: used = {used_mb} GB, percent = {vm_stats.percent}%")

    # if hasattr(torch.cuda, "reset_peak_memory_stats"):  
    #     torch.cuda.reset_peak_memory_stats()
    return gpu_mem, gpu_mem_max, cpu_mem

file_name = "../data/bert_yes_optimize.csv"

class MemoryMonitor:
    def __init__(self) -> None:
        self.mem_gpu = []
        self.mem_gpu_max = []
        self.mem_cpu = []
        self.cnt = 0
        self.isRunning = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.monitor_thread = None
        self.interval = 0.01
    def _measure_memory(self):
        while self.isRunning:
            self.cnt+=1
            gpu_mem, gpu_mem_max, cpu_mem = see_memory_usage()
            self.mem_gpu.append(gpu_mem)
            self.mem_gpu_max.append(gpu_mem_max)
            self.mem_cpu.append(cpu_mem)
            #把数据写入到csv文件中
            if self.cnt == 1:
                self.cnt = 0
                #写入csv文件\
                with open(file_name, mode="a", newline='') as file:
                    writer = csv.writer(file)
                    for row in zip(self.mem_gpu, self.mem_gpu_max, self.mem_cpu):
                        writer.writerow(row)
                self.mem_cpu.clear()
                self.mem_gpu.clear()
                self.mem_gpu_max.clear()
            time.sleep(self.interval)
        if self.cnt != 0:
            self.cnt = 0
            #写入csv文件\
            with open(file_name, mode="a", newline='') as file:
                writer = csv.writer(file)
                for row in zip(self.mem_gpu, self.mem_gpu_max, self.mem_cpu):
                    writer.writerow(row)
            self.mem_cpu.clear()
            self.mem_gpu.clear()
            self.mem_gpu_max.clear()
        return 1
    
    def start(self):
        self.isRunning = True
        self.monitor_thread = self.executor.submit(self._measure_memory)
        
        
    def finish(self):
        self.isRunning = False
        res = self.monitor_thread.result()
        if res != 1:
            AssertionError
        
    
    