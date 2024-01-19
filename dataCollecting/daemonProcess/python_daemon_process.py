import gc 
import psutil
import csv
import time
import torch


def daemon_function():
  file_name = f'memory.csv'
  cnt = 0
  gpu_mem_list = []
  cpu_mem_list = []
  scale_name = "MB"
    
  if scale_name == "MB":
    scale = 1024 * 1024
  elif scale_name == "B":
    scale = 1
  while True:
    cnt += 1
    # print("cnt", cnt)
    gc.collect()
    
    res = torch.cuda.mem_get_info()  
    gpu_mem = round((res[1] - res[0])/scale, 2)
    vm_stats = psutil.virtual_memory()
    cpu_mem = round((vm_stats.total - vm_stats.available)/scale, 2)
    
    # print(
    #   f"current gpu mem {gpu_mem} {scale_name}, \
    #     max gpu mem {gpu_mem_max} {scale_name}, \
    #       cpu mem {cpu_mem} {scale_name}\
    #   "
    # )
    
    gpu_mem_list.append(gpu_mem)
    cpu_mem_list.append(cpu_mem)
    
    
    if cnt == 100:
      cnt = 0
      print("write to csv")
      with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)

        for row in zip(gpu_mem_list, cpu_mem_list):
          writer.writerow(row)
        
      gpu_mem_list.clear()
      cpu_mem_list.clear()
    time.sleep(0.01) 
    
    
    
import multiprocessing
daemon_process = multiprocessing.Process(target=daemon_function)
daemon_process.daemon = True
daemon_process.start()


# main func