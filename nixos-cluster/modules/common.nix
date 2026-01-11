{ config, pkgs, ... }:

{
  system.stateVersion = "24.05";
  
  # Kernel setup
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  boot.kernelPackages = pkgs.linuxPackages_latest;
  
  # IOMMU for GPU Passthrough
  # Using intel_iommu as primary, but will be adjusted per-host if needed
  boot.kernelParams = [
    "intel_iommu=on"
    "iommu=pt"
    "kvm.ignore_msrs=1" # Better stability for Windows VMs
  ];
  
  # System Packages
  environment.systemPackages = with pkgs; [
    vim 
    git 
    htop 
    pciutils 
    usbutils 
    lshw 
    tmux 
    jq 
    kubectl 
    k9s 
    wget 
    curl 
    iproute2
  ];
  
  # Networking
  services.openssh.enable = true;
  services.openssh.settings.PasswordAuthentication = false;
  
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 22 6443 10250 ];
    allowedUDPPorts = [ 8472 ]; # Flannel VXLAN
  };
  
  # User setup
  users.users.admin = {
    isNormalUser = true;
    extraGroups = [ "wheel" "libvirtd" "docker" ];
    openssh.authorizedKeys.keys = [
      "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPqG57L6X6n6G6n6G6n6G6n6G6n6G6n6G6n6G6n6G6n6 admin@unified"
    ];
  };
  
  security.sudo.wheelNeedsPassword = false;

  # Nix Settings
  nix.settings.experimental-features = [ "nix-command" "flakes" ];
  nix.gc = {
    automatic = true;
    dates = "weekly";
    options = "--delete-older-than 14d";
  };
}
