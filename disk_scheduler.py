# disk_scheduler.py

def fcfs_disk_scheduling(requests, head):
    seek_sequence = []
    total_seek_time = 0
    current = head

    for req in requests:
        seek_sequence.append(req)
        total_seek_time += abs(req - current)
        current = req

    return seek_sequence, total_seek_time

def scan_disk_scheduling(requests, head, direction='left'):
    requests = sorted(requests)
    seek_sequence = []
    total_seek_time = 0
    current = head

    if direction == 'left':
        left = [r for r in requests if r < head][::-1]
        right = [r for r in requests if r >= head]
        for r in left:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r
        if left:
            total_seek_time += current
            current = 0
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r
    else:
        right = [r for r in requests if r >= head]
        left = [r for r in requests if r < head][::-1]
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r
        if right:
            total_seek_time += (199 - current)
            current = 199
        for r in left:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r

    return seek_sequence, total_seek_time

def c_scan_disk_scheduling(requests, head):
    requests = sorted(requests)
    seek_sequence = []
    total_seek_time = 0
    current = head

    right = [r for r in requests if r >= head]
    left = [r for r in requests if r < head]

    for r in right:
        seek_sequence.append(r)
        total_seek_time += abs(current - r)
        current = r

    if right:
        total_seek_time += (199 - current)
        total_seek_time += 199
        current = 0

    for r in left:
        seek_sequence.append(r)
        total_seek_time += abs(current - r)
        current = r

    return seek_sequence, total_seek_time

def look_disk_scheduling(requests, head, direction):
    requests = sorted(requests)
    seek_sequence = []
    total_seek_time = 0
    current = head

    if direction == 'left':
        left = [r for r in requests if r < head][::-1]
        right = [r for r in requests if r >= head]
        for r in left:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r
    else:
        right = [r for r in requests if r >= head]
        left = [r for r in requests if r < head][::-1]
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r
        for r in left:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r

    return seek_sequence, total_seek_time

def c_look_disk_scheduling(requests, head):
    requests = sorted(requests)
    seek_sequence = []
    total_seek_time = 0
    current = head

    right = [r for r in requests if r >= head]
    left = [r for r in requests if r < head]

    for r in right:
        seek_sequence.append(r)
        total_seek_time += abs(current - r)
        current = r

    if left:
        total_seek_time += abs(current - left[0])
        current = left[0]
        for r in left:
            seek_sequence.append(r)
            total_seek_time += abs(current - r)
            current = r

    return seek_sequence, total_seek_time
# disk_scheduler.py

def sstf_disk_scheduling(requests, head):
    requests = requests.copy()
    seek_sequence = []
    total_seek_time = 0
    current = head

    while requests:
        distances = {req: abs(current - req) for req in requests}
        closest = min(distances, key=distances.get)
        seek_sequence.append(closest)
        total_seek_time += abs(current - closest)
        current = closest
        requests.remove(closest)

    return seek_sequence, total_seek_time

