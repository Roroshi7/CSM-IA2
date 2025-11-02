# # simulation.py
# import simpy
# import random
# import statistics

# class ATMSystem:
#     def __init__(self, env, num_atms, service_mean, vip_prob=0.0):
#         self.env = env
#         self.atms = simpy.Resource(env, capacity=num_atms)
#         self.service_mean = service_mean
#         self.vip_prob = vip_prob

#         # Collect stats
#         self.wait_times = []       # wait times for each served customer
#         self.service_times = []    # actual service durations
#         self.arrival_times = []
#         self.departure_times = []
#         self.queue_length_events = []  # (time, queue_length)

#     def record_queue(self):
#         # queue length is number of waiting requests
#         qlen = len(self.atms.queue)
#         self.queue_length_events.append((self.env.now, qlen))

#     def customer(self, name, priority=False):
#         """Process for a single customer."""
#         arrival = self.env.now
#         self.arrival_times.append(arrival)
#         # record queue length at arrival
#         self.record_queue()

#         with self.atms.request() as req:
#             yield req  # wait until an ATM is free
#             wait = self.env.now - arrival
#             self.wait_times.append(wait)
#             # record queue length when service starts
#             self.record_queue()

#             # service time (exponential)
#             service = random.expovariate(1.0 / self.service_mean)
#             self.service_times.append(service)
#             yield self.env.timeout(service)
#             # departure
#             self.departure_times.append(self.env.now)
#             # record queue length when service ends
#             self.record_queue()

# def arrival_process(env, atm_system, arrival_rate, sim_time, seed=None):
#     """Generates customers with Poisson arrivals (interarrival exponential)."""
#     if seed is not None:
#         random.seed(seed)
#     cust_id = 0
#     while env.now < sim_time:
#         interarrival = random.expovariate(arrival_rate) if arrival_rate > 0 else float('inf')
#         yield env.timeout(interarrival)
#         cust_id += 1
#         # decide VIP or not (if vip_prob > 0)
#         is_vip = (random.random() < atm_system.vip_prob)
#         # spawn customer
#         env.process(atm_system.customer(f"Customer-{cust_id}", priority=is_vip))

# def run_simulation(num_atms=2, arrival_rate=0.5, service_mean=3.0,
#                    sim_time=500, vip_prob=0.0, seed=None):
#     """
#     Run the SimPy simulation and return results dict.
#     - num_atms: number of ATM servers
#     - arrival_rate: lambda (avg arrivals per unit time). If 0.5 -> mean interarrival 2.0
#     - service_mean: mean service time
#     - sim_time: total simulation time units
#     - vip_prob: probability customer is VIP (not used for different handling here)
#     """
#     env = simpy.Environment()
#     atm_system = ATMSystem(env, num_atms, service_mean, vip_prob=vip_prob)
#     env.process(arrival_process(env, atm_system, arrival_rate, sim_time, seed=seed))
#     env.run(until=sim_time)

#     # compute statistics
#     wait_times = atm_system.wait_times
#     service_times = atm_system.service_times
#     arrivals = atm_system.arrival_times
#     departures = atm_system.departure_times

#     avg_wait = statistics.mean(wait_times) if wait_times else 0.0
#     max_wait = max(wait_times) if wait_times else 0.0
#     avg_service = statistics.mean(service_times) if service_times else 0.0
#     throughput = len(departures) / sim_time  # customers served per unit time
#     # utilization approximation: total busy time / (num_atms * sim_time)
#     total_service_time = sum(service_times)
#     utilization = total_service_time / (num_atms * sim_time) if sim_time > 0 else 0.0

#     results = {
#         "avg_wait": avg_wait,
#         "max_wait": max_wait,
#         "avg_service": avg_service,
#         "throughput": throughput,
#         "utilization": utilization,
#         "num_served": len(departures),
#         "wait_times": wait_times,
#         "service_times": service_times,
#         "arrivals": arrivals,
#         "departures": departures,
#         "queue_length_events": atm_system.queue_length_events,
#         "sim_time": sim_time,
#         "num_atms": num_atms,
#         "arrival_rate": arrival_rate,
#     }
#     return results

# if __name__ == "__main__":
#     # quick local debug run
#     res = run_simulation(num_atms=2, arrival_rate=0.4, service_mean=3.0, sim_time=200, seed=42)
#     print("Avg wait:", res["avg_wait"])
#     print("Max wait:", res["max_wait"])
#     print("Utilization:", res["utilization"])
#     print("Served:", res["num_served"])

# simulation.py
import simpy
import random
import statistics


class TollBoothSystem:
    def __init__(self, env, num_booths, service_mean, vip_prob=0.0):
        self.env = env
        self.booths = simpy.Resource(env, capacity=num_booths)
        self.service_mean = service_mean
        self.vip_prob = vip_prob

        # Statistics
        self.wait_times = []
        self.service_times = []
        self.arrival_times = []
        self.departure_times = []
        self.queue_length_events = []  # (time, queue_length)

    def record_queue(self):
        """Record current queue length."""
        qlen = len(self.booths.queue)
        self.queue_length_events.append((self.env.now, qlen))

    def vehicle(self, name, is_vip=False):
        """Process for a single vehicle passing through toll."""
        arrival = self.env.now
        self.arrival_times.append(arrival)
        self.record_queue()

        with self.booths.request() as req:
            yield req  # wait for booth availability
            wait = self.env.now - arrival
            self.wait_times.append(wait)
            self.record_queue()

            # Service time (exponential) — VIPs get slightly faster service
            mean_time = self.service_mean * (0.7 if is_vip else 1.0)
            service = random.expovariate(1.0 / mean_time)
            self.service_times.append(service)
            yield self.env.timeout(service)

            # Departure
            self.departure_times.append(self.env.now)
            self.record_queue()


def arrival_process(env, toll_system, arrival_rate, sim_time, seed=None):
    """Generate vehicles arriving according to a Poisson process."""
    if seed is not None:
        random.seed(seed)
    vehicle_id = 0
    while env.now < sim_time:
        interarrival = random.expovariate(arrival_rate) if arrival_rate > 0 else float("inf")
        yield env.timeout(interarrival)
        vehicle_id += 1
        is_vip = random.random() < toll_system.vip_prob
        env.process(toll_system.vehicle(f"Vehicle-{vehicle_id}", is_vip))


def run_simulation(
    num_booths=3,
    arrival_rate=0.5,
    service_mean=4.0,
    sim_time=500,
    vip_prob=0.1,
    seed=None,
):
    """
    Run SimPy car toll booth simulation.
    - num_booths: number of toll booths
    - arrival_rate: vehicles per unit time (λ)
    - service_mean: mean service time per vehicle
    - sim_time: total simulated time
    - vip_prob: fraction of vehicles using fast tag (faster service)
    """
    env = simpy.Environment()
    toll_system = TollBoothSystem(env, num_booths, service_mean, vip_prob=vip_prob)
    env.process(arrival_process(env, toll_system, arrival_rate, sim_time, seed=seed))
    env.run(until=sim_time)

    # --- Compute statistics ---
    wait_times = toll_system.wait_times
    service_times = toll_system.service_times
    arrivals = toll_system.arrival_times
    departures = toll_system.departure_times

    avg_wait = statistics.mean(wait_times) if wait_times else 0.0
    max_wait = max(wait_times) if wait_times else 0.0
    avg_service = statistics.mean(service_times) if service_times else 0.0
    throughput = len(departures) / sim_time if sim_time > 0 else 0.0
    utilization = sum(service_times) / (num_booths * sim_time) if sim_time > 0 else 0.0

    return {
        "avg_wait": avg_wait,
        "max_wait": max_wait,
        "avg_service": avg_service,
        "throughput": throughput,
        "utilization": utilization,
        "num_served": len(departures),
        "wait_times": wait_times,
        "service_times": service_times,
        "arrivals": arrivals,
        "departures": departures,
        "queue_length_events": toll_system.queue_length_events,
        "sim_time": sim_time,
        "num_booths": num_booths,
        "arrival_rate": arrival_rate,
        "vip_prob": vip_prob,
    }


if __name__ == "__main__":
    res = run_simulation(num_booths=3, arrival_rate=0.6, service_mean=4.0, sim_time=300, seed=42)
    print("Average wait time:", res["avg_wait"])
    print("Max wait time:", res["max_wait"])
    print("Utilization:", res["utilization"])
    print("Vehicles served:", res["num_served"])
