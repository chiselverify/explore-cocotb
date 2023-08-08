import cocotb
from cocotb.queue import Queue, QueueFull, QueueEmpty
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock


async def producer(dut, queue, nn, delay=None):
    """Producer coroutine."""
    for i in range(1, nn + 1):
        if delay is not None:
            await Timer(delay, units='ns')
        await queue.put(i)
        dut._log.info(f"Producer: put {i}")

async def consumer(dut, queue):
    """Consumer coroutine."""
    while True:
        val = await queue.get()
        dut._log.info(f"Consumer: got {val}")

@cocotb.test()
async def run_test(dut):
    queue = Queue(maxsize=1)
    cocotb.start_soon(consumer(dut, queue))
    await cocotb.start_soon(producer(dut, queue, 3, 5))
    await Timer(1, units='ns')

async def producer2(dut, queue, nn, delay=None):
    """Producer2 coroutine."""
    for i in range(1, nn + 1):
        if delay is not None:
            await Timer(delay, units='ns')
        try:
            queue.put_nowait(i)
        except QueueFull:
            dut._log.info(f"Producer: queue is full")
            await Timer(2, units='ns')
        dut._log.info(f"Producer sent {i}")

async def consumer2(dut, queue):
    """Consumer2 coroutine."""
    while True:
        while True:
            try:
                val = queue.get_nowait()
                break
            except QueueEmpty:
                dut._log.info(f"Consumer: queue is empty")
                await Timer(2, units='ns')          
        dut._log.info(f"Consumer got {val}")    

@cocotb.test()
async def run_test2(dut):
    queue = Queue(maxsize=1)
    cocotb.start_soon(consumer2(dut, queue))
    await producer2(dut, queue, 3)
    await Timer(3, units='ns')
