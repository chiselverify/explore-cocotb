import cocotb

@cocotb.test()
async def hello_world(dut):
    """Say Hello!"""
    dut._log.info("Hello World!")