{ config, pkgs, lib, ... }:

{
  # Graphics / OpenGL (renamed to graphics in 24.11 but we stick to 24.05 opengl for now)
  hardware.opengl = {
    enable = true;
    driSupport = true;
    driSupport32Bit = true;
  };

  # NVIDIA Configuration
  services.xserver.videoDrivers = [ "nvidia" ];
  
  hardware.nvidia = {
    package = config.boot.kernelPackages.nvidiaPackages.stable;
    modesetting.enable = true;
    powerManagement.enable = false;
    open = false; # Proprietary drivers needed for stable passthrough/reset
    nvidiaSettings = false;
  };
  
  # Crucial for K8s GPU sharing
  hardware.nvidia-container-toolkit.enable = true;
  
  # Soft dependency to ensure vfio-pci claims the GPU before nvidia driver if requested
  boot.extraModprobeConfig = ''
    softdep nvidia pre: vfio-pci
  '';

  # Persist NVIDIA compute mode settings
  systemd.services.nvidia-persistence = {
    description = "NVIDIA Persistence Daemon";
    wantedBy = [ "multi-user.target" ];
    serviceConfig = {
      ExecStart = "${config.hardware.nvidia.package.bin}/bin/nvidia-smi -pm 1";
      Type = "oneshot";
    };
  };
}
