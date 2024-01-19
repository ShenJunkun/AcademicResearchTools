python train.py --n_epoch 50 --n_layer 2 --bs 200 -d wikipedia  --enable_random --reuse --lr 1e-4 --gpu 0 &

ai_pid=$!

echo "Timestamp,CPU Usage (%),Memory Usage (MB),GPU Memory Usage (MB)" > resource_usage.csv

# 循环获取资源信息，每隔10毫秒一次
while ps -p $ai_pid > /dev/null; do
    # timestamp=$(date +"%Y-%m-%d %H:%M:%S.%N")
    
    # 使用 free 获取内存使用情况
    memory_info=$(free -m | grep Mem)
    memory_total=$(echo $memory_info | awk '{print $2}')
    memory_available=$(echo $memory_info | awk '{print $7}')
    memory_used=$((memory_total - memory_available))


    # 获取CPU和内存使用情况
    cpu_usage=$(ps -p $ai_pid -o %cpu | tail -n 1)

    # memory_usage=$(ps -p $ai_pid -o %mem | tail -n 1)
    
    # 获取GPU内存使用情况（如果使用NVIDIA GPU）
    gpu_memory_usage=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)

    # 写入CSV文件
    echo "$cpu_usage,$memory_used,$gpu_memory_usage" >> resource_usage.csv

    # 等待10毫秒
    sleep 0.01
done

echo "AI model process finished. Resource usage data saved to resource_usage.csv"