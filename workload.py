class WorkloadGenerator:
    """Generates changing workload demand."""

    def __init__(self):
        self.workloads = [
            40, 80, 120, 170, 230, 280,
            150, 90, 40, 260, 320, 180, 70, 30
        ]
        self.index = 0

    def get_next_workload(self):
        """Returns the next workload value."""

        workload = self.workloads[self.index]

        self.index += 1

        if self.index >= len(self.workloads):
            self.index = 0

        return workload