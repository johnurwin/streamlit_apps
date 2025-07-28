import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def run():
    st.header("Monte Carlo Simulation for Project Timeline Estimation")

    # Sidebar inputs: Get values from st.session_state or set defaults to avoid re-runs
    num_tasks = st.sidebar.number_input("Number of Tasks", min_value=1, max_value=20, value=5, step=1)
    num_simulations = st.sidebar.slider("Number of Simulations", 100, 10000, 1000, step=100)
    hist_bins = st.sidebar.slider("Histogram Bins", 10, 100, 30, step=5)
    show_sample_timeline = st.sidebar.checkbox("Show Sample Timeline", value=True)

    st.markdown("""
    Estimate your project’s duration under uncertainty using Monte Carlo simulation.  
    Specify tasks, their estimated durations, and dependencies.
    """)

    # --- Task Input Form ---
    st.subheader("Step 1: Define Tasks and Dependencies")

    with st.form("task_input_form"):
        task_data = []

        for i in range(int(num_tasks)):
            st.markdown(f"**Task {i+1}**")
            name = st.text_input(f"Name of Task {i+1}", value=f"Task {i+1}", key=f"name_{i}")

            col1, col2 = st.columns(2)

            min_days = col1.number_input(
                f"Minimum days for {name}",
                min_value=0.0,
                value=2.0,
                key=f"min_{i}",
                step=0.1,
                format="%.2f"
            )

            max_days = col2.number_input(
                f"Maximum days for {name}",
                min_value=min_days,
                value=min_days + 3.0,
                key=f"max_{i}",
                step=0.1,
                format="%.2f"
            )

            available_deps = [task["name"] for task in task_data]
            dependencies = st.multiselect(
                f"Tasks that must finish before **{name}** starts",
                options=available_deps,
                key=f"deps_{i}"
            )

            task_data.append({
                "name": name,
                "min": min_days,
                "max": max_days,
                "dependencies": dependencies
            })

        submitted = st.form_submit_button("Run Simulation")

    # --- Simulation ---
    if submitted:
        st.subheader("Step 2: Simulation Results")

        # Validate task names to avoid empty or duplicates
        names = [task["name"] for task in task_data]
        if len(set(names)) != len(names) or any(not n.strip() for n in names):
            st.error("Task names must be unique and not empty.")
            return

        task_dict = {task["name"]: task for task in task_data}

        # Build DAG
        graph = nx.DiGraph()
        for task in task_data:
            graph.add_node(task["name"])
            for dep in task["dependencies"]:
                graph.add_edge(dep, task["name"])

        if not nx.is_directed_acyclic_graph(graph):
            st.error("❌ Task dependencies contain a cycle. Please fix before continuing.")
            return

        execution_order = list(nx.topological_sort(graph))
        total_durations = []

        for _ in range(num_simulations):
            task_start = {}
            task_end = {}

            for task_name in execution_order:
                task = task_dict[task_name]
                duration = np.random.uniform(task["min"], task["max"])
                if not task["dependencies"]:
                    start_time = 0
                else:
                    start_time = max([task_end[dep] for dep in task["dependencies"]])
                end_time = start_time + duration
                task_start[task_name] = start_time
                task_end[task_name] = end_time

            total_durations.append(max(task_end.values()))

        results = np.array(total_durations)
        mean_duration = results.mean()
        p90 = np.percentile(results, 90)

        st.markdown(f"**Average project duration:** `{mean_duration:.2f}` days")
        st.markdown(f"**90% of simulations completed in under:** `{p90:.2f}` days")

        # Histogram
        st.subheader("Distribution of Simulated Project Durations")
        fig, ax = plt.subplots()
        ax.hist(results, bins=hist_bins, color='skyblue', edgecolor='black')
        ax.axvline(p90, color='red', linestyle='--', label='90th percentile')
        ax.set_xlabel("Total Project Duration (days)")
        ax.set_ylabel("Frequency")
        ax.set_title("Monte Carlo Simulation Results")
        ax.legend()
        st.pyplot(fig)

        # Optional Sample Timeline
        if show_sample_timeline:
            st.subheader("Sample Task Timeline from One Simulation")

            task_start = {}
            task_end = {}

            for task_name in execution_order:
                task = task_dict[task_name]
                duration = np.random.uniform(task["min"], task["max"])
                if not task["dependencies"]:
                    start_time = 0
                else:
                    start_time = max([task_end[dep] for dep in task["dependencies"]])
                end_time = start_time + duration
                task_start[task_name] = start_time
                task_end[task_name] = end_time

            timeline = pd.DataFrame({
                "Task": list(task_start.keys()),
                "Start": list(task_start.values()),
                "Duration": [task_end[t] - task_start[t] for t in task_start],
            }).sort_values("Start")

            fig2, ax2 = plt.subplots(figsize=(10, 0.5 * len(timeline)))
            for i, row in enumerate(timeline.itertuples()):
                ax2.barh(i, row.Duration, left=row.Start, color='skyblue')
                ax2.text(row.Start + row.Duration / 2, i, row.Task, va='center', ha='center', color='black')
            ax2.set_yticks(range(len(timeline)))
            ax2.set_yticklabels([])
            ax2.set_xlabel("Days")
            ax2.set_title("One Simulated Task Schedule")
            st.pyplot(fig2)
