import cocotb
from cocotb.triggers import Timer, Combine
import logging

async def counter(dut, name, delay, count):
    """Counts up till count"""
    for i in range(1, count + 1):
        await Timer(delay, units="ns")
        dut._log.info(f"{name} count = {i}")

@cocotb.test()
async def my_test(dut):
    """Hello my test starts here"""
    dut._log.info("Launching counter coroutines")
    task = cocotb.start_soon(counter(dut, "simple counter", 1, 5))
    task2 = cocotb.start_soon(counter(dut, "simple counter 2", 2, 3))
    await Combine(task, task2)
    dut._log.info("Ignored running counter")