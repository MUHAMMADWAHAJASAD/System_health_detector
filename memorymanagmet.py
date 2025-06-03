def logical_to_physical_paging(logical_address, page_size, base_address):
    page_number = logical_address // page_size
    offset = logical_address % page_size
    physical_address = base_address + (page_number * page_size) + offset
    return physical_address, page_number, offset

def segmentation_translation(segments, seg_name, offset):
    base, limit = segments.get(seg_name, (0, 0))
    if offset > (limit - base):
        return None  # Invalid offset
    return base + offset

def fifo(pages, frame_size):
    frame = []
    faults = 0
    page_trace = []
    
    for page in pages:
        if page not in frame:
            faults += 1
            if len(frame) < frame_size:
                frame.append(page)
            else:
                frame.pop(0)
                frame.append(page)
        page_trace.append(frame.copy())
    
    return faults, page_trace

def lru(pages, frame_size):
    frame = []
    history = []
    faults = 0
    page_trace = []
    
    for page in pages:
        if page not in frame:
            faults += 1
            if len(frame) < frame_size:
                frame.append(page)
            else:
                lru_page = history.pop(0)
                frame.remove(lru_page)
                frame.append(page)
        else:
            history.remove(page)
        history.append(page)
        page_trace.append(frame.copy())
    
    return faults, page_trace

def optimal(pages, frame_size):
    frame = []
    faults = 0
    page_trace = []
    
    for i in range(len(pages)):
        page = pages[i]
        if page not in frame:
            faults += 1
            if len(frame) < frame_size:
                frame.append(page)
            else:
                future = pages[i+1:]
                index = []
                for f in frame:
                    if f in future:
                        index.append(future.index(f))
                    else:
                        index.append(float('inf'))
                victim = index.index(max(index))
                frame[victim] = page
        page_trace.append(frame.copy())
    
    return faults, page_trace