# system_monitor.py
import psutil
import platform
from datetime import datetime
import GPUtil

def get_system_info():
    """Return basic system and OS info with consistent keys."""
    uname = platform.uname()
    return {
        "system": uname.system,
        "node_name": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }

def get_cpu_info():
    """Return detailed CPU info including frequency."""
    freq = psutil.cpu_freq()
    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "max_frequency": freq.max if freq else 0,
        "min_frequency": freq.min if freq else 0,
        "current_frequency": freq.current if freq else 0,
    }

def get_memory_info():
    """Return RAM and swap memory info."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total": mem.total,
        "used": mem.used,
        "available": mem.available,
        "percent": mem.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_free": swap.free,
        "swap_percent": swap.percent
    }

def get_disk_info():
    """Return disk usage info for all partitions."""
    partitions = psutil.disk_partitions()
    disk_info_list = []
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        disk_info_list.append({
            "device": part.device,
            "mountpoint": part.mountpoint,
            "fstype": part.fstype,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "usage_percent": usage.percent
        })
    return disk_info_list

def get_network_info():
    """Return network I/O stats."""
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv
    }

def get_gpu_info():
    """Returns GPU usage details if available"""
    gpus = GPUtil.getGPUs()
    gpu_info_list = []

    for gpu in gpus:
        gpu_info_list.append({
            "Name": gpu.name,
            "Load (%)": round(gpu.load * 100, 1),
            "Memory Free (MB)": round(gpu.memoryFree, 1),
            "Memory Used (MB)": round(gpu.memoryUsed, 1),
            "Memory Total (MB)": round(gpu.memoryTotal, 1),
            "Temperature (°C)": gpu.temperature
        })

    return gpu_info_list
