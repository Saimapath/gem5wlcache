import argparse

import sys
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import *

# Importing common utilities
addToPath("../../")
from common import Options
from common import Simulation
from common import CacheConfig
from common import MemConfig
from common.FileSystemConfig import config_filesystem
# WriteLightCache Class Definition
class WriteLightCache(Cache):
    def __init__(self, size='8kB', assoc=2):
        super(WriteLightCache, self).__init__()
        self.size = size
        self.assoc = assoc
        # Internal max_dirty_lines and waterline settings
        self._max_dirty_lines = 6  
        self._waterline = 5

    def insert_dirty_line(self, line):
        if not hasattr(self, '_dirty_queue'):
            self._dirty_queue = []
        self._dirty_queue.append(line)
        if len(self._dirty_queue) >= self._max_dirty_lines:
            self.flush_dirty_queue()

    def flush_dirty_queue(self):
        while len(self._dirty_queue) > self._waterline:
            dirty_line = self._dirty_queue.pop(0)
            self.send_writeback_to_nvm(dirty_line)

    def send_writeback_to_nvm(self, line):
        print("Writing dirty line to NVM:", line)


# Simulation Setup
parser = argparse.ArgumentParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)
args = parser.parse_args()

system = System()
system.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())
system.cpu = TimingSimpleCPU()

# Set up icache and dcache with WriteLightCache
system.cpu.icache = Cache(size='8kB', assoc=2, tag_latency=1.6, data_latency=0.3, response_latency=0.1)
system.cpu.dcache = WriteLightCache(size='8kB', assoc=2)

# Connect the cache ports
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

# Set up the memory bus and connect it to the caches
system.membus = SystemXBar()
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

# Connect the NVM
system.nvm = SimpleMemory(range=AddrRange('512MB'), latency='100ns')
system.nvm.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

root = Root(full_system=False, system=system)
m5.instantiate()
print("Starting simulation")
exit_event = m5.simulate()
print("Simulation ended at tick %d because %s" % (m5.curTick(), exit_event.getCause()))

