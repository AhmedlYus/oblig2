from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopology(Topo):
    def build(self, **_opts):
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        r2 = self.addNode("r2", cls=LinuxRouter, ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.1.2/24")

        self.addLink(h1, r2, intfName1="h1-eth0", intfName2="r2-eth0", 
                     params1={'ip': '10.0.0.1/24'}, params2={'ip': '10.0.0.2/24'},
                     bw=10, delay='5ms')
        self.addLink(r2, h3, intfName1="r2-eth1", intfName2="h3-eth0",
                     params1={'ip': '10.0.1.1/24'}, params2={'ip': '10.0.1.2/24'},
                     bw=10, delay='5ms', max_queue_size=17)

def run():
    topo = NetworkTopology()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    # Configure routing
    net["h1"].cmd("ip route add 10.0.1.0/24 via 10.0.0.2 dev h1-eth0")
    net["h3"].cmd("ip route add 10.0.0.0/24 via 10.0.1.1 dev h3-eth0")
    
    # Start Mininet CLI for debugging
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
