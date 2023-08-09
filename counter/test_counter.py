#import logging
#logging.basicConfig(level=logging.NOTSET)
#logger = logging.getLogger()
#logging.setLevel(logging.DEBUG)

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles, FallingEdge

# We could return 0 on X or Z, now we get an exception
def get_int(signal):
    return int(signal.value)

@cocotb.test()
async def no_count(dut):
    """Test for reset of counter."""
    clock = Clock(dut.clk, 2, units="ns")
    cocotb.start_soon(clock.start())
    dut.reset_n.value = 0
    await ClockCycles(dut.clk, 5)
    count = get_int(dut.count)
    assert count == 0, f"Counter should be 0 at reset, not {count}"
    dut._log.info("Reset OK")

@cocotb.test()
async def three_count(dut):
    """Test for three counts."""
    clock = Clock(dut.clk, 2, units="ns")
    cocotb.start_soon(clock.start())
    dut.reset_n.value = 0
    await FallingEdge(dut.clk)
    dut.reset_n.value = 1
    await ClockCycles(dut.clk, 3, rising=False)
    count = get_int(dut.count)
    assert count == 3, f"Counter should be 3 after 3 cycles, not {count}"
    dut._log.info("Three count OK")
