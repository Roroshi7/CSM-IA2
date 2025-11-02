# # app.py
# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from simulation import run_simulation
# import io

# # ---------------------------
# # Small CSS to improve appearance
# # ---------------------------
# st.set_page_config(page_title="ATM Queue Simulation", layout="wide", initial_sidebar_state="expanded")

# st.markdown(
#     """
#     <style>
#     /* page background and content width */
#     .main .block-container{padding-top:1.5rem; padding-right:3rem; padding-left:3rem;}
#     /* card look for metric boxes */
#     .kpi {
#         background: #fff;
#         border-radius: 10px;
#         padding: 14px;
#         box-shadow: 0 2px 8px rgba(18,38,63,0.08);
#         border: 1px solid rgba(18,38,63,0.06);
#         text-align:center;
#     }
#     .kpi .title { color: #6b7280; font-size:14px; margin-bottom:6px; }
#     .kpi .value { font-weight:700; font-size:22px; color: #222; }
#     .hero { text-align:center; margin-bottom: 12px; }
#     .small-muted { color: #6b7280; font-size: 14px; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # ---------------------------
# # Header / Hero
# # ---------------------------
# st.markdown('<div class="hero">', unsafe_allow_html=True)
# st.title("Python + Streamlit / SimPy --- ATM Queue Simulation")
# st.markdown('<div class="small-muted">Interactive simulator with multiple ATMs, adjustable arrival/service rates, and visual analytics</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # ---------------------------
# # Sidebar controls
# # ---------------------------
# st.sidebar.header("Simulation parameters")
# num_atms = st.sidebar.slider("Number of ATMs", min_value=1, max_value=6, value=2, step=1)
# arrival_lambda = st.sidebar.slider("Arrival rate (λ) — arrivals per unit time", min_value=0.05, max_value=2.0, value=0.5, step=0.05)
# service_mean = st.sidebar.slider("Mean service time (μ)", min_value=0.5, max_value=10.0, value=3.0, step=0.5)
# sim_time = st.sidebar.slider("Simulation time (time units)", min_value=50, max_value=2000, value=500, step=50)
# seed = st.sidebar.number_input("Random seed (0 for none)", value=42, step=1)
# vip_prob = st.sidebar.slider("VIP probability (optional)", min_value=0.0, max_value=0.5, value=0.0, step=0.01)
# run_button = st.sidebar.button("Run simulation")

# # Small help / tips
# st.sidebar.markdown("---")
# st.sidebar.markdown("**Tips:**\n- Increase ATMs to reduce wait.\n- Increase sim time for smoother metrics.\n- Use seed for reproducible runs.")

# # ---------------------------
# # Run / show results
# # ---------------------------
# if run_button:
#     with st.spinner("Running simulation..."):
#         results = run_simulation(
#             num_atms=num_atms,
#             arrival_rate=arrival_lambda,
#             service_mean=service_mean,
#             sim_time=sim_time,
#             vip_prob=vip_prob,
#             seed=seed if seed != 0 else None
#         )

#     # ---------- Top KPI row ----------
#     kpi1, kpi2, kpi3, kpi4 = st.columns([1,1,1,1], gap="large")
#     kpi1.markdown('<div class="kpi"><div class="title">Avg wait time</div><div class="value">{:.3f}</div></div>'.format(results["avg_wait"]), unsafe_allow_html=True)
#     kpi2.markdown('<div class="kpi"><div class="title">Max wait time</div><div class="value">{:.3f}</div></div>'.format(results["max_wait"]), unsafe_allow_html=True)
#     kpi3.markdown('<div class="kpi"><div class="title">Throughput (served / time)</div><div class="value">{:.3f}</div></div>'.format(results["throughput"]), unsafe_allow_html=True)
#     kpi4.markdown('<div class="kpi"><div class="title">Utilization (approx)</div><div class="value">{:.3f}</div></div>'.format(results["utilization"]), unsafe_allow_html=True)

#     # Add a short summary row
#     st.markdown(f"**Number served:** {results['num_served']}  •  **Sim time:** {results['sim_time']}  •  **ATMs:** {results['num_atms']}  •  **λ:** {results['arrival_rate']}  •  **μ:** {results['avg_service']:.2f}")

#     st.markdown("---")

#     # ---------- Charts ----------
#     col1, col2 = st.columns([2,1], gap="large")

#     # Queue length over time: prepare step-like data for plotting
#     q_events = results["queue_length_events"]
#     if q_events:
#         times, qlens = zip(*q_events)
#         qdf = pd.DataFrame({"time": times, "queue_length": qlens})
#         # Plotly line chart (interactive)
#         fig_q = px.line(qdf, x="time", y="queue_length", title="Queue length over time", labels={"time":"Time", "queue_length":"Queue length (waiting)"})
#         fig_q.update_layout(margin=dict(l=40,r=20,t=40,b=20), height=450)
#         col1.plotly_chart(fig_q, use_container_width=True)
#     else:
#         col1.write("No queue events recorded.")

#     # Histogram of wait times
#     wait_times = results["wait_times"]
#     if wait_times:
#         wdf = pd.DataFrame({"wait_time": wait_times})
#         fig_h = px.histogram(wdf, x="wait_time", nbins=30, title="Wait time distribution", labels={"wait_time":"Wait time"})
#         fig_h.update_layout(margin=dict(l=20,r=20,t=40,b=20), height=450)
#         col2.plotly_chart(fig_h, use_container_width=True)
#     else:
#         col2.write("No completed customers to show wait histogram.")

#     st.markdown("---")

#     # ---------- Raw data & download ----------
#     st.subheader("Event data (sample)")
#     df_events = pd.DataFrame({
#         "arrival_time": results["arrivals"],
#         "departure_time": results["departures"] + [None]*(max(0, len(results["arrivals"])-len(results["departures"])))
#     })
#     st.dataframe(df_events.head(100))

#     # CSV download
#     csv_buffer = io.StringIO()
#     df_events.to_csv(csv_buffer, index=False)
#     csv_bytes = csv_buffer.getvalue().encode()
#     st.download_button("Download event data (CSV)", data=csv_bytes, file_name="atm_sim_events.csv", mime="text/csv")

#     st.success("Simulation completed. Adjust parameters and re-run as needed.")

# else:
#     # show small interactive demo image + quick instructions
#     st.info("Set parameters in the sidebar and click **Run simulation**. Try changing number of ATMs or arrival rate to see how metrics change.")
#     st.markdown("""
#     **Quick experiments to try**
#     - Keep μ fixed and increase λ until utilization ~1.0 → queue grows quickly.  
#     - Increase ATMs to bring avg wait down.  
#     - Set a seed for reproducible runs.
#     """)

# # ---------------------------
# # Footer
# # ---------------------------
# st.markdown("---")
# st.markdown("Made with ❤️ — `SimPy` for simulation logic, `Plotly` for charts, `Streamlit` for UI. Customize for VIP priority using `simpy.PriorityResource`.")


# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import run_simulation
import io

# ---------------------------
# Page config and styling
# ---------------------------
st.set_page_config(page_title="Car Toll Booth Simulation", layout="wide")

st.markdown("""
<style>
.main .block-container{padding-top:1.5rem; padding-right:3rem; padding-left:3rem;}
.kpi {
    background: #fff;
    border-radius: 10px;
    padding: 14px;
    box-shadow: 0 2px 8px rgba(18,38,63,0.08);
    border: 1px solid rgba(18,38,63,0.06);
    text-align:center;
}
.kpi .title { color: #6b7280; font-size:14px; margin-bottom:6px; }
.kpi .value { font-weight:700; font-size:22px; color: #222; }
.hero { text-align:center; margin-bottom: 12px; }
.small-muted { color: #6b7280; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.title("🚗 Car Toll Booth Queue Simulation")
st.markdown('<div class="small-muted">Simulate traffic flow, booth utilization, and queue buildup using SimPy</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Sidebar parameters
# ---------------------------
st.sidebar.header("Simulation Parameters")

num_booths = st.sidebar.slider("Number of Toll Booths", 1, 10, 3, 1)
arrival_rate = st.sidebar.slider("Arrival rate (λ) — vehicles per unit time", 0.05, 3.0, 0.8, 0.05)
service_mean = st.sidebar.slider("Mean service time (μ)", 0.5, 10.0, 4.0, 0.5)
sim_time = st.sidebar.slider("Simulation duration (time units)", 50, 2000, 500, 50)
vip_prob = st.sidebar.slider("Fast Tag (VIP) fraction", 0.0, 0.5, 0.1, 0.01)
seed = st.sidebar.number_input("Random seed (0 for none)", value=42, step=1)
run_button = st.sidebar.button("Run Simulation")

st.sidebar.markdown("---")
st.sidebar.markdown("**Tips:**\n- More booths = less waiting.\n- Increase λ (arrival rate) to simulate congestion.\n- VIPs get faster service (~30% quicker).")

# ---------------------------
# Run Simulation
# ---------------------------
if run_button:
    with st.spinner("Simulating toll booth traffic..."):
        results = run_simulation(
            num_booths=num_booths,
            arrival_rate=arrival_rate,
            service_mean=service_mean,
            sim_time=sim_time,
            vip_prob=vip_prob,
            seed=seed if seed != 0 else None
        )

    # KPI Display
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="kpi"><div class="title">Avg Wait Time</div><div class="value">{results["avg_wait"]:.3f}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi"><div class="title">Max Wait Time</div><div class="value">{results["max_wait"]:.3f}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi"><div class="title">Throughput (veh/unit)</div><div class="value">{results["throughput"]:.3f}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi"><div class="title">Utilization</div><div class="value">{results["utilization"]:.3f}</div></div>', unsafe_allow_html=True)

    st.markdown(f"**Vehicles Served:** {results['num_served']}  •  **Sim Time:** {results['sim_time']}  •  **Booths:** {results['num_booths']}  •  **λ:** {results['arrival_rate']}  •  **μ (mean service):** {results['avg_service']:.2f}")

    st.markdown("---")

    # ---------------------------
    # Charts
    # ---------------------------
    col1, col2 = st.columns([2, 1])

    # Queue length chart
    q_events = results["queue_length_events"]
    if q_events:
        q_times, q_vals = zip(*q_events)
        qdf = pd.DataFrame({"Time": q_times, "Queue Length": q_vals})
        fig_q = px.line(qdf, x="Time", y="Queue Length", title="Queue Length Over Time")
        fig_q.update_layout(height=450)
        col1.plotly_chart(fig_q, use_container_width=True)
    else:
        col1.warning("No queue data available.")

    # Wait time histogram
    wait_times = results["wait_times"]
    if wait_times:
        wdf = pd.DataFrame({"Wait Time": wait_times})
        fig_w = px.histogram(wdf, x="Wait Time", nbins=30, title="Wait Time Distribution")
        fig_w.update_layout(height=450)
        col2.plotly_chart(fig_w, use_container_width=True)
    else:
        col2.warning("No wait time data to display.")

    st.markdown("---")

    # ---------------------------
    # Raw Event Data
    # ---------------------------
    st.subheader("Sample Event Data")
    df_events = pd.DataFrame({
        "Arrival Time": results["arrivals"],
        "Departure Time": results["departures"] + [None]*(max(0, len(results["arrivals"])-len(results["departures"]))),
    })
    st.dataframe(df_events.head(100))

    csv_buf = io.StringIO()
    df_events.to_csv(csv_buf, index=False)
    st.download_button("Download Vehicle Event Data (CSV)", csv_buf.getvalue(), "toll_booth_events.csv", "text/csv")

    st.success("✅ Simulation completed. Adjust parameters and re-run for different traffic scenarios!")

else:
    st.info("Set parameters in the sidebar and click **Run Simulation**.")
    st.markdown("""
    **Try these experiments:**
    - Increase λ gradually → see queue buildup and longer waits.
    - Add more booths to see throughput improvement.
    - Increase Fast Tag fraction → faster service, less congestion.
    """)

st.markdown("---")
st.markdown("Made with ❤️ using `SimPy`, `Plotly`, and `Streamlit` — for realistic queue simulations.")
