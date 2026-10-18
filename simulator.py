import asyncio
import matplotlib.pyplot as plt

from workload import WorkloadGenerator
from autoscaler import Autoscaler


class CloudSimulator:
    """Runs the cloud resource autoscaling simulation."""

    def __init__(self):
        self.workload_generator = WorkloadGenerator()
        self.autoscaler = Autoscaler()

        self.monitoring_interval = 1
        self.simulation_steps = 14

        # Lists to store history for chart generation
        self.history_workloads = []
        self.history_resources = []

    async def monitor(self):
        """Monitors workload and performs autoscaling."""

        print()
        print("=" * 90)
        print("            CLOUD RESOURCE AUTOSCALER SIMULATOR")
        print("=" * 90)

        print(
            f"{'Time':<8}"
            f"{'Workload':<12}"
            f"{'Resources':<14}"
            f"{'CPU Usage':<14}"
            f"{'Action':<16}"
            f"{'After':<8}"
        )

        print("-" * 90)

        for step in range(1, self.simulation_steps + 1):

            workload = self.workload_generator.get_next_workload()

            (
                utilization,
                action,
                resources_before,
                resources_after
            ) = self.autoscaler.scale(workload)

            # Save history data for plotting the graph later
            self.history_workloads.append(workload)
            self.history_resources.append(resources_after)

            resource_change = (
                f"{resources_before} -> {resources_after}"
            )

            print(
                f"{step:<8}"
                f"{workload:<12}"
                f"{resource_change:<14}"
                f"{utilization:<14.2f}"
                f"{action:<16}"
                f"{resources_after:<8}"
            )

            await asyncio.sleep(self.monitoring_interval)

        self.display_summary()

    def display_summary(self):
        """Displays the final simulation results and generates a performance chart."""

        print()
        print("=" * 90)
        print("                    SIMULATION SUMMARY")
        print("=" * 90)

        print(
            f"Scale-up events   : "
            f"{self.autoscaler.scale_up_events}"
        )

        print(
            f"Scale-down events : "
            f"{self.autoscaler.scale_down_events}"
        )

        print(
            f"Final resources   : "
            f"{self.autoscaler.get_resource_count()}"
        )

        print(
            f"Minimum resources : "
            f"{self.autoscaler.min_resources}"
        )

        print(
            f"Maximum resources : "
            f"{self.autoscaler.max_resources}"
        )

        print("=" * 90)
        print("Simulation completed successfully!")
        print("=" * 90)

        # --- GENERATE AND SAVE PERFORMANCE CHART ---
        try:
            steps = list(range(1, len(self.history_workloads) + 1))

            plt.figure(figsize=(10, 5))
            plt.plot(steps, self.history_workloads, label="Workload Demand", color="red", marker="o", linewidth=2)
            plt.plot(steps, self.history_resources, label="Active Resources", color="blue", marker="s", drawstyle="steps-post", linewidth=2)

            plt.title("Cloud Resource Autoscaler Simulator Performance", fontsize=14, fontweight="bold")
            plt.xlabel("Simulation Time Steps", fontsize=11)
            plt.ylabel("Workload / Resource Count", fontsize=11)
            plt.legend(loc="upper left")
            plt.grid(True, linestyle="--", alpha=0.7)

            # Save chart as an image file in your folder
            plt.savefig("autoscaler_report.png")
            print("\n📊 Success! Performance chart saved as 'autoscaler_report.png' in your project folder.")
            
            # Pop up the graph window automatically
            plt.show()
        except Exception as e:
            print(f"Could not generate plot: {e}")