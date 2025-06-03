import streamlit as st
from streamlit_autorefresh import st_autorefresh
from system_monitor import (
    get_system_info, get_cpu_info, get_memory_info,
    get_disk_info, get_network_info, get_gpu_info
)
from cpu_scheduler import fcfs_scheduling, priority_scheduling, round_robin_scheduling
from disk_scheduler import (
    fcfs_disk_scheduling, scan_disk_scheduling, look_disk_scheduling,
    c_scan_disk_scheduling, c_look_disk_scheduling, sstf_disk_scheduling
)
from memorymanagmet import fifo,lru,logical_to_physical_paging,optimal,segmentation_translation
from utils import plot_gantt_chart, plot_disk_chart

from processmanagment import bankers_algorithm,detect_deadlock,producer_consumer_simulation,readers_writers_simulation

# Page config
st.set_page_config(page_title="System Health, CPU & Disk Scheduler", layout="wide")

# Auto-refresh for System Health Monitor
st_autorefresh(interval=500000, key="system_health_refresh")

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Select Page",
    ["System Health Monitor", "CPU Scheduling Simulator", "Disk Scheduling Simulator", "Memory Management", "Process Management"]
)

# -------------------- System Health Monitor --------------------
if page == "System Health Monitor":
    st.title("🔍 System Health Monitor")

    sys_info = get_system_info()
    cpu_info = get_cpu_info()
    mem_info = get_memory_info()
    disk_info = get_disk_info()
    net_info = get_network_info()
    gpu_data = get_gpu_info()

    st.subheader("🖥️ System Info")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("System", sys_info.get("system", "N/A"))
        st.metric("Node Name", sys_info.get("node_name", "N/A"))
        st.metric("Boot Time", sys_info.get("boot_time", "N/A"))
    with col2:
        st.metric("Release", sys_info.get("release", "N/A"))
        st.metric("Version", sys_info.get("version", "N/A"))
    with col3:
        st.metric("Machine", sys_info.get("machine", "N/A"))
        st.metric("Processor", sys_info.get("processor", "N/A"))

    st.markdown("---")

    st.subheader("⚙️ CPU Info")
    cpu_col1, cpu_col2, cpu_col3 = st.columns(3)
    with cpu_col1:
        st.metric("Physical Cores", cpu_info.get("physical_cores", "N/A"))
        st.metric("Logical Cores", cpu_info.get("logical_cores", "N/A"))
        st.metric("CPU Usage (%)", cpu_info.get("cpu_usage_percent", 0))
    with cpu_col2:
        st.metric("Max Frequency (MHz)", cpu_info.get("max_frequency", 0))
        st.metric("Min Frequency (MHz)", cpu_info.get("min_frequency", 0))
    with cpu_col3:
        st.metric("Current Frequency (MHz)", cpu_info.get("current_frequency", 0))

    st.markdown("---")

    st.subheader("💾 Memory Info")
    mem_total_gb = mem_info.get("total", 0) / (1024 ** 3)
    mem_used_gb = mem_info.get("used", 0) / (1024 ** 3)
    mem_available_gb = mem_info.get("available", 0) / (1024 ** 3)
    st.write(f"**Total Memory:** {mem_total_gb:.2f} GB")
    st.write(f"**Used Memory:** {mem_used_gb:.2f} GB")
    st.write(f"**Available Memory:** {mem_available_gb:.2f} GB")
    st.progress(mem_info.get("percent", 0) / 100)

    swap_total = mem_info.get("swap_total", 0) / (1024 ** 3)
    swap_used = mem_info.get("swap_used", 0) / (1024 ** 3)
    st.write(f"**Swap Memory Used:** {swap_used:.2f} GB / {swap_total:.2f} GB")
    st.progress(mem_info.get("swap_percent", 0) / 100)

    st.markdown("---")

    st.subheader("🗃️ Disk Info")
    for disk in disk_info:
        st.markdown(f"**{disk['device']}** mounted on {disk['mountpoint']} ({disk['fstype']})")
        st.progress(disk.get("usage_percent", 0) / 100)
        used = disk.get("used", 0) / (1024 ** 3)
        total = disk.get("total", 0) / (1024 ** 3)
        st.write(f"Used: {used:.2f} GB / Total: {total:.2f} GB")

    st.markdown("---")

    st.subheader("🌐 Network Info")
    net_col1, net_col2 = st.columns(2)
    with net_col1:
        st.metric("Bytes Sent (MB)", f"{net_info.get('bytes_sent', 0) / (1024**2):.2f}")
        st.metric("Packets Sent", net_info.get("packets_sent", 0))
    with net_col2:
        st.metric("Bytes Received (MB)", f"{net_info.get('bytes_recv', 0) / (1024**2):.2f}")
        st.metric("Packets Received", net_info.get("packets_recv", 0))

    st.markdown("---")

    st.subheader("🧠 GPU Info")
    if gpu_data:
        for idx, gpu in enumerate(gpu_data):
            st.markdown(f"**GPU {idx + 1}: {gpu['Name']}**")
            st.metric("Load (%)", gpu["Load (%)"])
            st.metric("Temperature (°C)", gpu["Temperature (°C)"])
            st.metric("Memory Used / Total (MB)", f"{gpu['Memory Used (MB)']} / {gpu['Memory Total (MB)']}")
    else:
        st.info("No GPU detected.")

# -------------------- CPU Scheduling --------------------
elif page == "CPU Scheduling Simulator":
    st.title("🧠 CPU Scheduling Simulator")

    algorithm = st.selectbox("Choose Scheduling Algorithm", ["FCFS", "Round Robin", "Priority (Non-preemptive)"])
    num = st.number_input("Number of Processes", min_value=1, max_value=10, value=3)

    processes = []
    for i in range(num):
        st.markdown(f"### Process P{i+1}")
        arrival = st.number_input(f"Arrival Time (P{i+1})", key=f"arrival_{i}", min_value=0)
        burst = st.number_input(f"Burst Time (P{i+1})", key=f"burst_{i}", min_value=1)
        priority = None
        if algorithm == "Priority (Non-preemptive)":
            priority = st.number_input(f"Priority (lower = higher) (P{i+1})", key=f"priority_{i}", min_value=1)
        proc = {'pid': f'P{i+1}', 'arrival_time': arrival, 'burst_time': burst}
        if priority is not None:
            proc['priority'] = priority
        processes.append(proc)

    time_quantum = None
    if algorithm == "Round Robin":
        time_quantum = st.number_input("Time Quantum", min_value=1, value=2)

    if st.button("Run Scheduling"):
        if algorithm == "FCFS":
            gantt, waiting, turnaround = fcfs_scheduling(processes)
        elif algorithm == "Round Robin":
            gantt, waiting, turnaround = round_robin_scheduling(processes, time_quantum)
        elif algorithm == "Priority (Non-preemptive)":
            gantt, waiting, turnaround = priority_scheduling(processes)
        else:
            st.error("Invalid algorithm selected.")
            st.stop()

        st.subheader("📊 Gantt Chart (Text)")
        for entry in gantt:
            st.text(f"{entry['pid']} | Start: {entry['start']} | End: {entry['end']}")

        st.subheader("📉 Gantt Chart")
        fig = plot_gantt_chart(gantt)
        st.pyplot(fig)

        st.subheader("⏱️ Waiting Times")
        st.json(waiting)

        st.subheader("🔁 Turnaround Times")
        st.json(turnaround)

# -------------------- Disk Scheduling --------------------
elif page == "Disk Scheduling Simulator":
    st.title("💽 Disk Scheduling Simulator")

    algorithm = st.selectbox("Choose Disk Scheduling Algorithm", ["FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN", "C-LOOK"])
    requests = st.text_input("Enter Disk Requests (comma-separated)", "55, 58, 60, 70, 18, 90, 150, 160, 184")
    head_start = st.number_input("Initial Head Position", min_value=0, value=50)
    disk_size = st.number_input("Disk Size (Optional for SCAN/C-SCAN)", value=200)
    direction = None

    if algorithm in ["SCAN", "C-SCAN", "LOOK", "C-LOOK"]:
        direction = st.radio("Head Movement Direction", ["left", "right"])

    if st.button("Run Disk Scheduling"):
        reqs = list(map(int, requests.split(',')))

        if algorithm == "FCFS":
            sequence, total = fcfs_disk_scheduling(reqs, head_start)
        elif algorithm == "SSTF":
            sequence, total = sstf_disk_scheduling(reqs, head_start)
        elif algorithm == "SCAN":
            sequence, total = scan_disk_scheduling(reqs, head_start,direction)
        elif algorithm == "LOOK":
            sequence, total = look_disk_scheduling(reqs, head_start, direction)
        elif algorithm == "C-SCAN":
            sequence, total = c_scan_disk_scheduling(reqs, head_start)
        elif algorithm == "C-LOOK":
            sequence, total = c_look_disk_scheduling(reqs, head_start)
        else:
            st.error("Invalid algorithm selected.")
            st.stop()

        st.subheader("📄 Seek Sequence")
        st.write(" ➜ ".join(map(str, sequence)))

        st.subheader("📏 Total Seek Distance")
        st.metric("Total Seek", total)

        st.subheader("📊 Disk Head Movement Chart")
        fig = plot_disk_chart(sequence)
        st.pyplot(fig)

# -------------------- Memory Management --------------------
elif page == "Memory Management":
    st.title("🧮 Memory Management Simulator")
    
    memory_option = st.selectbox(
        "Choose Memory Management Technique",
        ["Address Translation", "Page Replacement Algorithms"]
    )
    
    if memory_option == "Address Translation":
        st.subheader("🔄 Address Translation")
        
        translation_type = st.radio("Select Translation Type", ["Paging", "Segmentation"])
        
        if translation_type == "Paging":
            st.markdown("### Paging Address Translation")
            col1, col2 = st.columns(2)
            
            with col1:
                logical_addr = st.number_input("Logical Address", min_value=0, value=1024)
                page_size = st.number_input("Page Size", min_value=1, value=512)
            
            with col2:
                base_addr = st.number_input("Base Address", min_value=0, value=2048)
            
            if st.button("Calculate Physical Address"):
                physical_addr, page_num, offset = logical_to_physical_paging(logical_addr, page_size, base_addr)
                
                st.success("✅ Translation Results:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Page Number", page_num)
                with col2:
                    st.metric("Offset", offset)
                with col3:
                    st.metric("Physical Address", physical_addr)
                
                st.info(f"**Formula:** Physical Address = Base Address + (Page Number × Page Size) + Offset")
                st.info(f"**Calculation:** {physical_addr} = {base_addr} + ({page_num} × {page_size}) + {offset}")
        
        else:  # Segmentation
            st.markdown("### Segmentation Address Translation")
            
            # Define segments
            st.markdown("#### Define Segments")
            num_segments = st.number_input("Number of Segments", min_value=1, max_value=5, value=3)
            
            segments = {}
            for i in range(num_segments):
                col1, col2, col3 = st.columns(3)
                with col1:
                    seg_name = st.text_input(f"Segment {i+1} Name", value=f"seg{i+1}", key=f"seg_name_{i}")
                with col2:
                    base = st.number_input(f"Base Address", min_value=0, value=1000*i, key=f"base_{i}")
                with col3:
                    limit = st.number_input(f"Limit", min_value=1, value=500, key=f"limit_{i}")
                
                segments[seg_name] = (base, limit)
            
            st.markdown("#### Translate Address")
            col1, col2 = st.columns(2)
            with col1:
                selected_segment = st.selectbox("Select Segment", list(segments.keys()))
            with col2:
                offset = st.number_input("Offset", min_value=0, value=100)
            
            if st.button("Translate Segmented Address"):
                result = segmentation_translation(segments, selected_segment, offset)
                
                if result is not None:
                    st.success(f"✅ Physical Address: {result}")
                    base, limit = segments[selected_segment]
                    st.info(f"**Calculation:** {result} = {base} (base) + {offset} (offset)")
                else:
                    st.error("❌ Invalid offset! Offset exceeds segment limit.")
                
                # Display segment table
                st.markdown("#### Segment Table")
                import pandas as pd
                seg_data = []
                for name, (base, limit) in segments.items():
                    seg_data.append({"Segment": name, "Base": base, "Limit": limit, "Size": limit - base})
                st.dataframe(pd.DataFrame(seg_data))
    
    else:  # Page Replacement Algorithms
        st.subheader("📚 Page Replacement Algorithms")
        
        # Input parameters
        col1, col2 = st.columns(2)
        with col1:
            page_sequence = st.text_input("Page Reference Sequence (comma-separated)", "1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5")
            frame_size = st.number_input("Number of Frames", min_value=1, max_value=10, value=3)
        
        with col2:
            algorithms = st.multiselect(
                "Select Algorithms to Compare",
                ["FIFO", "LRU", "Optimal"],
                default=["FIFO", "LRU", "Optimal"]
            )
        
        if st.button("Run Page Replacement Simulation"):
            try:
                pages = list(map(int, page_sequence.split(',')))
                
                results = {}
                traces = {}
                
                # Run selected algorithms
                if "FIFO" in algorithms:
                    faults, trace = fifo(pages, frame_size)
                    results["FIFO"] = faults
                    traces["FIFO"] = trace
                
                if "LRU" in algorithms:
                    faults, trace = lru(pages, frame_size)
                    results["LRU"] = faults
                    traces["LRU"] = trace
                
                if "Optimal" in algorithms:
                    faults, trace = optimal(pages, frame_size)
                    results["Optimal"] = faults
                    traces["Optimal"] = trace
                
                # Display results
                st.subheader("📊 Results Summary")
                cols = st.columns(len(results))
                for i, (alg, faults) in enumerate(results.items()):
                    with cols[i]:
                        st.metric(f"{alg} Page Faults", faults)
                
                # Display detailed trace for each algorithm
                for alg in algorithms:
                    st.subheader(f"🔍 {alg} Algorithm Trace")
                    
                    # Create trace table
                    import pandas as pd
                    trace_data = []
                    for i, page in enumerate(pages):
                        frame_state = traces[alg][i] if i < len(traces[alg]) else []
                        # Pad frame state to match frame size
                        padded_frame = frame_state + ['-'] * (frame_size - len(frame_state))
                        
                        row = {"Step": i+1, "Page": page}
                        for j in range(frame_size):
                            row[f"Frame {j+1}"] = padded_frame[j] if j < len(padded_frame) else '-'
                        
                        # Check if it's a page fault
                        if i == 0:
                            row["Fault"] = "Yes"
                        else:
                            prev_frame = traces[alg][i-1] if i-1 < len(traces[alg]) else []
                            row["Fault"] = "Yes" if page not in prev_frame else "No"
                        
                        trace_data.append(row)
                    
                    df = pd.DataFrame(trace_data)
                    st.dataframe(df, use_container_width=True)
                
                # Calculate hit ratio
                st.subheader("📈 Performance Metrics")
                total_references = len(pages)
                
                perf_data = []
                for alg, faults in results.items():
                    hits = total_references - faults
                    hit_ratio = (hits / total_references) * 100
                    fault_ratio = (faults / total_references) * 100
                    
                    perf_data.append({
                        "Algorithm": alg,
                        "Page Faults": faults,
                        "Page Hits": hits,
                        "Hit Ratio (%)": f"{hit_ratio:.2f}%",
                        "Fault Ratio (%)": f"{fault_ratio:.2f}%"
                    })
                
                st.dataframe(pd.DataFrame(perf_data), use_container_width=True)
                
            except ValueError:
                st.error("❌ Please enter valid comma-separated integers for the page sequence.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# -------------------- Process Management --------------------
elif page == "Process Management":
    st.title("⚙️ Process Management Simulator")
    
    process_option = st.selectbox(
        "Choose Process Management Technique",
        ["Deadlock Management", "Process Synchronization", "Inter-Process Communication"]
    )
    
    if process_option == "Deadlock Management":
        st.subheader("🔒 Deadlock Management")
        
        deadlock_method = st.radio("Select Method", ["Banker's Algorithm (Prevention)", "Deadlock Detection"])
        
        if deadlock_method == "Banker's Algorithm (Prevention)":
            st.markdown("### 🏦 Banker's Algorithm")
            st.info("The Banker's Algorithm ensures the system never enters an unsafe state by checking if granting a request leads to a safe sequence.")
            
            # Input parameters
            col1, col2 = st.columns(2)
            with col1:
                num_processes = st.number_input("Number of Processes", min_value=1, max_value=10, value=5)
                num_resources = st.number_input("Number of Resource Types", min_value=1, max_value=5, value=3)
            
            with col2:
                available_input = st.text_input("Available Resources (comma-separated)", "3, 3, 2")
            
            # Process details input
            st.markdown("#### Process Details")
            processes = []
            allocation = []
            max_need = []
            
            for i in range(num_processes):
                st.markdown(f"**Process P{i}**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("Process Name")
                    processes.append(f"P{i}")
                    st.write(f"P{i}")
                
                with col2:
                    alloc_input = st.text_input(f"Allocated Resources", key=f"alloc_{i}", value="0, 1, 0")
                    try:
                        alloc = list(map(int, alloc_input.split(',')))
                        allocation.append(alloc)
                    except:
                        allocation.append([0] * num_resources)
                
                with col3:
                    max_input = st.text_input(f"Maximum Need", key=f"max_{i}", value="7, 5, 3")
                    try:
                        max_need_val = list(map(int, max_input.split(',')))
                        max_need.append(max_need_val)
                    except:
                        max_need.append([0] * num_resources)
            
            if st.button("Run Banker's Algorithm"):
                try:
                    available = list(map(int, available_input.split(',')))
                    safe_sequence, need_matrix = bankers_algorithm(processes, allocation, max_need, available)
                    
                    if safe_sequence:
                        st.success("✅ System is in SAFE state!")
                        st.subheader("🔐 Safe Sequence")
                        st.write(" → ".join(safe_sequence))
                        
                        # Display matrices
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.subheader("📋 Allocation Matrix")
                            import pandas as pd
                            alloc_df = pd.DataFrame(allocation, index=[f"P{i}" for i in range(num_processes)], columns=[f"R{i}" for i in range(num_resources)])
                            st.dataframe(alloc_df)
                        
                        with col2:
                            st.subheader("📊 Max Need Matrix")
                            max_df = pd.DataFrame(max_need, index=[f"P{i}" for i in range(num_processes)], columns=[f"R{i}" for i in range(num_resources)])
                            st.dataframe(max_df)
                        
                        with col3:
                            st.subheader("📈 Need Matrix")
                            need_df = pd.DataFrame(need_matrix, index=[f"P{i}" for i in range(num_processes)], columns=[f"R{i}" for i in range(num_resources)])
                            st.dataframe(need_df)
                        
                        st.subheader("📌 Available Resources")
                        avail_df = pd.DataFrame([available], columns=[f"R{i}" for i in range(num_resources)])
                        st.dataframe(avail_df)
                        
                    else:
                        st.error("❌ System is in UNSAFE state! Potential deadlock detected.")
                        st.warning("The system cannot find a safe sequence to execute all processes.")
                
                except Exception as e:
                    st.error(f"❌ Error in input format: {str(e)}")
        
        else:  # Deadlock Detection
            st.markdown("### 🔍 Deadlock Detection")
            st.info("This algorithm detects if the current system state has a deadlock by checking if all processes can complete.")
            
            col1, col2 = st.columns(2)
            with col1:
                num_processes_detect = st.number_input("Number of Processes", min_value=1, max_value=10, value=3, key="detect_processes")
                num_resources_detect = st.number_input("Number of Resource Types", min_value=1, max_value=5, value=3, key="detect_resources")
            
            with col2:
                available_detect = st.text_input("Available Resources", "0, 0, 0", key="detect_available")
            
            # Input matrices
            st.markdown("#### Current System State")
            allocation_detect = []
            request_detect = []
            
            for i in range(num_processes_detect):
                col1, col2 = st.columns(2)
                with col1:
                    alloc = st.text_input(f"P{i} - Current Allocation", f"0, 1, 0", key=f"detect_alloc_{i}")
                    try:
                        allocation_detect.append(list(map(int, alloc.split(','))))
                    except:
                        allocation_detect.append([0] * num_resources_detect)
                
                with col2:
                    req = st.text_input(f"P{i} - Request", f"0, 0, 0", key=f"detect_req_{i}")
                    try:
                        request_detect.append(list(map(int, req.split(','))))
                    except:
                        request_detect.append([0] * num_resources_detect)
            
            if st.button("Detect Deadlock"):
                try:
                    available_resources = list(map(int, available_detect.split(',')))
                    deadlocked = detect_deadlock(allocation_detect, request_detect, available_resources)
                    
                    if deadlocked:
                        st.error(f"❌ DEADLOCK DETECTED!")
                        st.write(f"**Deadlocked Processes:** {[f'P{i}' for i in deadlocked]}")
                        
                        # Show the state
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.subheader("Current Allocation")
                            alloc_df = pd.DataFrame(allocation_detect, columns=[f"R{i}" for i in range(num_resources_detect)])
                            alloc_df.index = [f"P{i}" for i in range(num_processes_detect)]
                            st.dataframe(alloc_df)
                        
                        with col2:
                            st.subheader("Request Matrix")
                            req_df = pd.DataFrame(request_detect, columns=[f"R{i}" for i in range(num_resources_detect)])
                            req_df.index = [f"P{i}" for i in range(num_processes_detect)]
                            st.dataframe(req_df)
                        
                        with col3:
                            st.subheader("Available")
                            avail_df = pd.DataFrame([available_resources], columns=[f"R{i}" for i in range(num_resources_detect)])
                            st.dataframe(avail_df)
                    else:
                        st.success("✅ NO DEADLOCK detected! All processes can complete.")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    elif process_option == "Process Synchronization":
        st.subheader("🔄 Process Synchronization")
        
        sync_problem = st.selectbox("Choose Synchronization Problem", ["Producer-Consumer", "Readers-Writers"])
        
        if sync_problem == "Producer-Consumer":
            st.markdown("### 🏭 Producer-Consumer Problem")
            st.info("Simulates the classic synchronization problem where producers add items to a buffer and consumers remove them.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                buffer_size = st.number_input("Buffer Size", min_value=1, max_value=20, value=5)
            with col2:
                num_producers = st.number_input("Number of Producers", min_value=1, max_value=5, value=2)
            with col3:
                items_to_produce = st.number_input("Items to Produce", min_value=1, max_value=20, value=10)
            
            if st.button("Run Producer-Consumer Simulation"):
                operations, produced, consumed = producer_consumer_simulation(buffer_size, num_producers, 1, items_to_produce)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📊 Simulation Results")
                    st.metric("Items Produced", len(produced))
                    st.metric("Items Consumed", len(consumed))
                    st.metric("Buffer Size", buffer_size)
                
                with col2:
                    st.subheader("📈 Statistics")
                    efficiency = (len(consumed) / len(produced)) * 100 if produced else 0
                    st.metric("Consumption Efficiency", f"{efficiency:.1f}%")
                
                st.subheader("📋 Operation Log")
                for i, op in enumerate(operations[:20]):  # Show first 20 operations
                    st.text(f"{i+1:2d}. {op}")
                
                if len(operations) > 20:
                    st.info(f"... and {len(operations) - 20} more operations")
        
        else:  # Readers-Writers
            st.markdown("### 📚 Readers-Writers Problem")
            st.info("Simulates the synchronization problem where multiple readers can access a resource simultaneously, but writers need exclusive access.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                num_readers = st.number_input("Max Readers", min_value=1, max_value=10, value=3)
            with col2:
                num_writers = st.number_input("Max Writers", min_value=1, max_value=5, value=2)
            with col3:
                operations_count = st.number_input("Number of Operations", min_value=5, max_value=50, value=15)
            
            if st.button("Run Readers-Writers Simulation"):
                operations, final_status = readers_writers_simulation(num_readers, num_writers, operations_count)
                
                st.subheader("📊 Final Resource Status")
                st.info(f"Resource Status: {final_status}")
                
                st.subheader("📋 Operation Log")
                for op in operations:
                    if "started" in op:
                        st.success(op)
                    elif "waiting" in op:
                        st.warning(op)
                    elif "finished" in op:
                        st.info(op)
                    else:
                        st.text(op)
    
   