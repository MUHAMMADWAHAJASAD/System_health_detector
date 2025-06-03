import matplotlib.pyplot as plt

def plot_gantt_chart(gantt_data):
    fig, ax = plt.subplots(figsize=(8, 2))
    for task in gantt_data:
        ax.barh(0, task['end'] - task['start'], left=task['start'], height=0.5, label=task['pid'])
        ax.text(task['start'] + (task['end'] - task['start']) / 2, 0, task['pid'],
                ha='center', va='center', color='white', fontsize=10)

    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_xlim(0, max(task['end'] for task in gantt_data) + 2)
    ax.legend()
    return fig

def plot_disk_chart(sequence):
    """
    Plots disk scheduling seek sequence using matplotlib.

    Args:
        sequence (list): List of cylinder positions accessed in order.

    Returns:
        matplotlib.figure.Figure: The plot figure to render in Streamlit.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(len(sequence)), sequence, marker='o', linestyle='-', color='blue')
    ax.set_title("Disk Scheduling Head Movement")
    ax.set_xlabel("Sequence Step")
    ax.set_ylabel("Cylinder Number")
    ax.grid(True)
    ax.set_xticks(range(len(sequence)))
    ax.set_yticks(sorted(sequence))

    for i, pos in enumerate(sequence):
        ax.text(i, pos + 1, str(pos), ha='center', fontsize=9)

    return fig
