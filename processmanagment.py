def bankers_algorithm(processes, allocation, max_need, available):
    """Banker's Algorithm for Deadlock Avoidance"""
    n = len(processes)
    m = len(available)
    
    # Calculate need matrix
    need = []
    for i in range(n):
        need.append([max_need[i][j] - allocation[i][j] for j in range(m)])
    
    # Track finished processes
    finished = [False] * n
    safe_sequence = []
    work = available.copy()
    
    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finished[i]:
                # Check if process can be satisfied
                can_proceed = all(need[i][j] <= work[j] for j in range(m))
                if can_proceed:
                    # Add allocated resources back to work
                    for j in range(m):
                        work[j] += allocation[i][j]
                    safe_sequence.append(processes[i])
                    finished[i] = True
                    found = True
                    break
        
        if not found:
            return None, None  # Unsafe state
    
    return safe_sequence, need

def detect_deadlock(allocation, request, available):
    """Deadlock Detection Algorithm"""
    n = len(allocation)
    m = len(available)
    
    # Work array starts with available resources
    work = available.copy()
    finished = [False] * n
    
    while True:
        found = False
        for i in range(n):
            if not finished[i]:
                # Check if process can complete
                can_complete = all(request[i][j] <= work[j] for j in range(m))
                if can_complete:
                    # Process can complete, add its allocation to work
                    for j in range(m):
                        work[j] += allocation[i][j]
                    finished[i] = True
                    found = True
                    break
        
        if not found:
            break
    
    # If any process is not finished, there's a deadlock
    deadlocked_processes = [i for i in range(n) if not finished[i]]
    return deadlocked_processes

def producer_consumer_simulation(buffer_size, num_producers, num_consumers, items_to_produce):
    """Simulate Producer-Consumer Problem"""
    import random
    
    buffer = []
    produced_items = []
    consumed_items = []
    operations = []
    
    total_produced = 0
    total_consumed = 0
    
    # Simulate the process
    for step in range(items_to_produce * 2):  # Allow enough steps
        if total_produced < items_to_produce:
            # Producer tries to produce
            if len(buffer) < buffer_size:
                item = f"Item-{total_produced + 1}"
                buffer.append(item)
                produced_items.append(item)
                operations.append(f"Producer: Added {item} to buffer")
                total_produced += 1
            else:
                operations.append("Producer: Buffer full, waiting...")
        
        # Consumer tries to consume
        if buffer and total_consumed < total_produced:
            item = buffer.pop(0)
            consumed_items.append(item)
            operations.append(f"Consumer: Consumed {item}")
            total_consumed += 1
        elif total_consumed < total_produced:
            operations.append("Consumer: Buffer empty, waiting...")
        
        if total_consumed >= items_to_produce:
            break
    
    return operations, produced_items, consumed_items

def readers_writers_simulation(num_readers, num_writers, operations_count):
    """Simulate Readers-Writers Problem"""
    import random
    
    active_readers = 0
    active_writers = 0
    waiting_readers = 0
    waiting_writers = 0
    operations = []
    resource_status = "Available"
    
    for i in range(operations_count):
        # Randomly choose operation
        operation = random.choice(['reader_request', 'writer_request', 'reader_finish', 'writer_finish'])
        
        if operation == 'reader_request':
            if active_writers == 0 and waiting_writers == 0:
                active_readers += 1
                operations.append(f"Step {i+1}: Reader {active_readers} started reading")
                resource_status = f"{active_readers} Reader(s) active"
            else:
                waiting_readers += 1
                operations.append(f"Step {i+1}: Reader waiting (Writer active/waiting)")
        
        elif operation == 'writer_request':
            if active_readers == 0 and active_writers == 0:
                active_writers = 1
                operations.append(f"Step {i+1}: Writer started writing")
                resource_status = "Writer active"
            else:
                waiting_writers += 1
                operations.append(f"Step {i+1}: Writer waiting (Readers/Writer active)")
        
        elif operation == 'reader_finish' and active_readers > 0:
            active_readers -= 1
            operations.append(f"Step {i+1}: Reader finished")
            if active_readers == 0 and waiting_writers > 0:
                active_writers = 1
                waiting_writers -= 1
                operations.append(f"Step {i+1}: Waiting writer started")
                resource_status = "Writer active"
            else:
                resource_status = f"{active_readers} Reader(s) active" if active_readers > 0 else "Available"
        
        elif operation == 'writer_finish' and active_writers > 0:
            active_writers = 0
            operations.append(f"Step {i+1}: Writer finished")
            # Priority to waiting readers
            if waiting_readers > 0:
                active_readers = waiting_readers
                waiting_readers = 0
                operations.append(f"Step {i+1}: {active_readers} waiting readers started")
                resource_status = f"{active_readers} Reader(s) active"
            elif waiting_writers > 0:
                active_writers = 1
                waiting_writers -= 1
                operations.append(f"Step {i+1}: Waiting writer started")
                resource_status = "Writer active"
            else:
                resource_status = "Available"
    
    return operations, resource_status