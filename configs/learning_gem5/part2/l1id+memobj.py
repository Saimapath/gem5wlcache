# Import the m5 (gem5) library created when gem5 is built
import m5
import os
from m5.objects import *

# Create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range

# Create a simple CPU
system.cpu = X86TimingSimpleCPU()

# Create a memory bus, a coherent crossbar, in this case
system.membus = SystemXBar()

# Create the write buffer-like custom memory object
system.memobj = SimpleMemobj()
# Define separate L1 instruction and data caches with MSHR and response latency parameters
system.l1i_cache = Cache(size='32kB', assoc=2, tag_latency=2, data_latency=2,
                      mshrs=8, tgts_per_mshr=20, response_latency=1)
system.l1d_cache = Cache(size='32kB', assoc=2, tag_latency=2, data_latency=2,
                      mshrs=8, tgts_per_mshr=20, response_latency=1)


# Connect the CPU's I and D cache ports to the respective caches
system.cpu.icache_port = system.l1i_cache.cpu_side
system.cpu.dcache_port = system.l1d_cache.cpu_side

# Hook the caches up to the memory bus
system.l1i_cache.mem_side = system.membus.cpu_side_ports
system.l1d_cache.mem_side = system.membus.cpu_side_ports



# Connect the write buffer memory object to the memory bus
system.memobj.mem_side = system.membus.cpu_side_ports
system.memobj.cpu_side = system.cpu.dcache_port 

# Create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports



# Create a process for a simple "Hello World" application
process = Process()
# Set the command
# grab the specific path to the binary
thispath = os.path.dirname(os.path.realpath(__file__))
binpath = os.path.join(
    thispath, "../../../", "tests/test-progs/hello/bin/x86/linux/hello"
)
# cmd is a list which begins with the executable (like argv)
process.cmd = [binpath]
# Set the CPU to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

system.workload = SEWorkload.init_compatible(binpath)

# Set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
# Instantiate all of the objects we've created above
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
