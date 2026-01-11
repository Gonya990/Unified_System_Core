{ config, pkgs, ... }:

{
  networking.hostName = "node1";
  
  services.k3s = {
    role = "server";
    # On the first node, we don't have a serverAddr
    extraFlags = toString [
      "--cluster-init"
      "--disable=traefik" # Using our own ingress if needed
      "--node-label=gpu-0-status=available"
      "--node-label=gpu-1-status=available"
    ];
  };
  
  # Host-specific GPU mappings for gpu-arbiter
  environment.etc."gpu-arbiter/config" = {
    text = ''
      declare -A GPU_PCI
      declare -A VM_NAMES
      NODE_NAME="node1"
      
      # Mapping for Node 1
      GPU_PCI[0]="0000:01:00.0"  # Example RTX 3080
      GPU_PCI[1]="0000:02:00.0"  # Example RTX 2080
      
      VM_NAMES[0]="win-gaming-0"
      VM_NAMES[1]="win-gaming-1"
    '';
    mode = "0644";
  };

  # Static IP (optional, better via DHCP reservation but spec shows static)
  # networking.interfaces.enp0s31f6.ipv4.addresses = [{
  #   address = "192.168.1.101";
  #   prefixLength = 24;
  # }];
}
