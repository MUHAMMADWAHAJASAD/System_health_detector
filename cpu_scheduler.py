def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x['arrival_time'])
    current_time = 0
    gantt_chart = []
    waiting_times = {}
    turnaround_times = {}

    for p in processes:
        start = max(current_time, p['arrival_time'])
        end = start + p['burst_time']
        gantt_chart.append({'pid': p['pid'], 'start': start, 'end': end})

        waiting_time = start - p['arrival_time']
        turnaround_time = end - p['arrival_time']
        waiting_times[p['pid']] = waiting_time
        turnaround_times[p['pid']] = turnaround_time

        current_time = end

    return gantt_chart, waiting_times, turnaround_times


def round_robin_scheduling(processes, time_quantum):
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    queue = []
    gantt_chart = []
    time = 0
    waiting_time = {}
    turnaround_time = {}
    remaining_bt = {p['pid']: p['burst_time'] for p in processes}
    arrival_dict = {p['pid']: p['arrival_time'] for p in processes}
    ready_queue = []
    completed = set()

    while len(completed) < len(processes):
        # Add newly arrived processes
        for p in processes:
            if p['arrival_time'] <= time and p['pid'] not in [proc['pid'] for proc in ready_queue] and p['pid'] not in completed:
                ready_queue.append({'pid': p['pid']})

        if not ready_queue:
            time += 1
            continue

        current = ready_queue.pop(0)
        pid = current['pid']
        start_time = time
        exec_time = min(time_quantum, remaining_bt[pid])
        time += exec_time
        remaining_bt[pid] -= exec_time
        gantt_chart.append({'pid': pid, 'start': start_time, 'end': time})

        # Re-add process if not completed
        if remaining_bt[pid] > 0:
            # Add any new processes that arrived during execution
            for p in processes:
                if start_time < p['arrival_time'] <= time and p['pid'] not in [proc['pid'] for proc in ready_queue] and p['pid'] not in completed:
                    ready_queue.append({'pid': p['pid']})
            ready_queue.append({'pid': pid})
        else:
            completed.add(pid)
            turnaround_time[pid] = time - arrival_dict[pid]
            waiting_time[pid] = turnaround_time[pid] - next(p['burst_time'] for p in processes if p['pid'] == pid)

    return gantt_chart, waiting_time, turnaround_time


def priority_scheduling(processes):
    """
    Non-preemptive priority scheduling:
    - Lower priority number means higher priority.
    """
    n = len(processes)
    completed = 0
    current_time = 0
    gantt_chart = []
    waiting_times = {}
    turnaround_times = {}
    processes_left = sorted(processes, key=lambda x: x['arrival_time'])

    while completed < n:
        # Get processes that have arrived by current_time
        ready_queue = [p for p in processes_left if p['arrival_time'] <= current_time]

        if not ready_queue:
            # If no process is ready, advance time to next arriving process
            current_time = processes_left[0]['arrival_time']
            ready_queue = [p for p in processes_left if p['arrival_time'] <= current_time]

        # Pick process with highest priority (lowest priority number)
        proc = min(ready_queue, key=lambda x: x['priority'])

        start = max(current_time, proc['arrival_time'])
        end = start + proc['burst_time']
        gantt_chart.append({'pid': proc['pid'], 'start': start, 'end': end})

        turnaround_times[proc['pid']] = end - proc['arrival_time']
        waiting_times[proc['pid']] = start - proc['arrival_time']

        current_time = end
        completed += 1
        processes_left.remove(proc)

    return gantt_chart, waiting_times, turnaround_times

