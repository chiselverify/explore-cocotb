import cocotb
from cocotb.triggers import FallingEdge
import random

from pathlib import Path
parent_path = Path("..").resolve()

import sys
sys.path.insert(0, str(parent_path))

from tinyalu_utils import Ops, alu_prediction, logger, get_int

@cocotb.test()
async def test_alu(dut):
    passed = True
    cvg = set()
    await FallingEdge(dut.clk)
    dut.reset_n.value = 0
    dut.start.value = 0
    await FallingEdge(dut.clk)
    dut.reset_n.value = 1
    cmd_count = 1
    op_list = list(Ops)
    num_ops = len(op_list)
    while cmd_count <= num_ops:
        await FallingEdge(dut.clk)
        st = get_int(dut.start)
        dn = get_int(dut.done)
        if st == 0 and dn == 0:
            aa = random.randint(0, 255)
            bb = random.randint(0, 255)
            op = op_list.pop(0)
            cvg.add(op)
            dut.op.value = op
            dut.A.value = aa
            dut.B.value = bb
            dut.start.value = 1
        if st == 0 and dn == 1:
            raise AssertionError("DUT Error, done without a start")
        if st == 1 and dn == 0:
            continue
        if st == 1 and dn == 1:
            dut.start.value = 0
            result = get_int(dut.result)
            pr = alu_prediction(aa, bb, op)
            if result == pr:
                dut._log.info(f"PASSED: {aa:2x} {op.name} {bb:2x} = {result:04x}")
            else:
                passed = False
                dut._log.error(f"Test {cmd_count} failed")
                dut._log.error(f"aa = {aa}, bb = {bb}, op = {op}")
                dut._log.error(f"result = {result}, prediction = {pr}")
            cmd_count += 1

    if len(set(Ops) - cvg) > 0:
        passed = False
        dut._log.error(f"Not all operations covered, missing {Ops - cvg}")
    else:
        dut._log.info("All operations covered")
    
    assert passed, "Test failed"