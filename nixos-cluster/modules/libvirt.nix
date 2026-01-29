{ config, pkgs, ... }:

{
  virtualisation.libvirtd = {
    enable = true;
    
    qemu = {
      package = pkgs.qemu_kvm;
      
      # UEFI/SecureBoot support
      ovmf = {
        enable = true;
        packages = [ pkgs.OVMFFull.fd ];
      };
      
      # Permissions for VFIO
      verbatimConfig = ''
        user = "root"
        group = "root"
        cgroup_device_acl = [
          "/dev/null", "/dev/full", "/dev/zero",
          "/dev/random", "/dev/urandom",
          "/dev/ptmx", "/dev/kvm",
          "/dev/vfio/vfio"
        ]
      '';
    };
  };
  
  environment.systemPackages = with pkgs; [
    virt-manager 
    virt-viewer 
    spice-gtk
    libguestfs # For disk image manipulation
  ];
}
