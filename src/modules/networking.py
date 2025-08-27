import sys
import subprocess

# Check platform and initialize network interface handling
if sys.platform.startswith("darwin"):  # macOS
    ipr = "macos"  # Placeholder to indicate macOS-specific handling
elif sys.platform.startswith("linux"):
    from pyroute2 import IPRoute
    ipr = IPRoute()
else:
    ipr = None

def list_interfaces():
    if ipr == "macos":
        try:
            # Use ifconfig to list network interfaces
            result = subprocess.run(["ifconfig", "-l"], capture_output=True, text=True, check=True)
            interfaces = result.stdout.split()
            # Filter out loopback and non-physical interfaces if needed
            return [iface for iface in interfaces if iface.startswith(("en", "utun", "bridge"))]
        except subprocess.CalledProcessError:
            print("Error listing interfaces.")
            return []
    elif ipr:
        # Linux case with pyroute2
        return [x.get_attr('IFLA_IFNAME') for x in ipr.get_links()]
    return []

def create_veth_pair(name1, name2):
    if ipr == "macos":
        print("Virtual Ethernet (veth) pairs are not supported on macOS")
        return
    elif not ipr:
        print("Networking module not supported on this OS")
        return
    # Linux case
    ipr.link("add", ifname=name1, kind="veth", peer=name2)
    ipr.link("set", ifname=name1, state="up")
    ipr.link("set", ifname=name2, state="up")