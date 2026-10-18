class ComputeResource:
    """Represents one compute resource."""

    def __init__(self, resource_id, capacity=100):
        self.resource_id = resource_id
        self.capacity = capacity

    def __str__(self):
        return f"Resource-{self.resource_id}"