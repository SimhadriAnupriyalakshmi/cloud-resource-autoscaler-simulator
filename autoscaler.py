from compute_resource import ComputeResource


class Autoscaler:
    """Controls resources using threshold-based scaling."""

    def __init__(
        self,
        min_resources=1,
        max_resources=5,
        scale_up_threshold=75,
        scale_down_threshold=30,
        resource_capacity=100
    ):
        self.min_resources = min_resources
        self.max_resources = max_resources

        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold

        self.resource_capacity = resource_capacity

        self.resources = []

        self.scale_up_events = 0
        self.scale_down_events = 0

        self.next_resource_id = 1

        # Start with two resources.
        self.add_resource()
        self.add_resource()

    def add_resource(self):
        """Adds one compute resource."""

        if len(self.resources) < self.max_resources:
            resource = ComputeResource(
                self.next_resource_id,
                self.resource_capacity
            )

            self.resources.append(resource)
            self.next_resource_id += 1

            return True

        return False

    def remove_resource(self):
        """Removes one compute resource."""

        if len(self.resources) > self.min_resources:
            self.resources.pop()
            return True

        return False

    def calculate_utilization(self, workload):
        """Calculates CPU utilization."""

        total_capacity = (
            len(self.resources) * self.resource_capacity
        )

        utilization = (
            workload / total_capacity
        ) * 100

        return utilization

    def scale(self, workload):
        """Makes a scaling decision based on CPU usage."""

        resources_before = len(self.resources)

        utilization = self.calculate_utilization(workload)

        action = "STABLE"

        if utilization > self.scale_up_threshold:
            if self.add_resource():
                self.scale_up_events += 1
                action = "SCALE UP"

        elif utilization < self.scale_down_threshold:
            if self.remove_resource():
                self.scale_down_events += 1
                action = "SCALE DOWN"

        resources_after = len(self.resources)

        return (
            utilization,
            action,
            resources_before,
            resources_after
        )

    def get_resource_count(self):
        """Returns the current number of resources."""

        return len(self.resources)