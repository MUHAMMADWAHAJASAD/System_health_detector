import streamlit as st


from memorymanagmet import (
    logical_to_physical_paging,
    segmentation_translation,
    fifo,
    lru
)

st.set_page_config(page_title="Memory Management Simulator", layout="wide")
st.title("🧠 Linux System Memory Management Simulator")

module = st.sidebar.radio("Select Simulator", ["Paging", "Segmentation", "Virtual Memory"])

# -------------------- Paging --------------------
if module == "Paging":
    st.header("📄 Paging Address Translation")

    logical_address = st.number_input("Enter Logical Address", min_value=0, value=400)
    page_size = st.number_input("Enter Page Size", min_value=1, value=100)
    base_address = st.number_input("Enter Base Physical Address", min_value=0, value=1000)

    if st.button("Translate Paging"):
        physical_address, page_number, offset = logical_to_physical_paging(logical_address, page_size, base_address)
        st.success(f"Page Number: {page_number}")
        st.success(f"Offset: {offset}")
        st.success(f"Physical Address: {physical_address}")

# -------------------- Segmentation --------------------
elif module == "Segmentation":
    st.header("📐 Segmentation Address Translation")

    num_segments = st.number_input("Number of Segments", min_value=1, max_value=10, value=3)
    segments = {}

    st.markdown("**Define Segment Table (Base, Limit)**")
    for i in range(int(num_segments)):
        seg_name = st.text_input(f"Segment Name {i+1}", value=f"S{i}", key=f"segname_{i}")
        base = st.number_input(f"Base of {seg_name}", min_value=0, key=f"base_{i}")
        limit = st.number_input(f"Limit of {seg_name}", min_value=0, key=f"limit_{i}")
        segments[seg_name] = (base, limit)

    selected_seg = st.selectbox("Select Segment", list(segments.keys()))
    offset = st.number_input("Enter Offset", min_value=0)

    if st.button("Translate Segmentation"):
        result = segmentation_translation(segments, selected_seg, offset)
        if result is None:
            st.error("Invalid offset! Exceeds segment limit.")
        else:
            st.success(f"Physical Address: {result}")

# -------------------- Virtual Memory --------------------
elif module == "Virtual Memory":
    st.header("💾 Virtual Memory Page Replacement Simulation")

    page_ref = st.text_input("Enter Page Reference String (comma-separated)", "7,0,1,2,0,3,0,4,2,3,0,3,2")
    pages = [int(x.strip()) for x in page_ref.split(",") if x.strip().isdigit()]
    num_frames = st.number_input("Number of Frames", min_value=1, value=3)
    algo = st.selectbox("Replacement Algorithm", ["FIFO", "LRU"])

    if st.button("Simulate Virtual Memory"):
        if algo == "FIFO":
            faults = fifo(pages, num_frames)
        else:
            faults = lru(pages, num_frames)
        st.success(f"Total Page Faults using {algo}: {faults}")
