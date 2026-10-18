import asyncio

from simulator import CloudSimulator


async def main():
    """Starts the cloud autoscaler simulation."""

    simulator = CloudSimulator()

    await simulator.monitor()


if __name__ == "__main__":
    asyncio.run(main())