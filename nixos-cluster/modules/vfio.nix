{ config, pkgs, lib, ... }:

{
  # Kernel modules needed for passthrough
  boot.kernelModules = [
    "vfio_pci"
    "vfio"
    "vfio_iommu_type1"
  ];
  
  # Load in initrd for early binding if needed (though we want dynamic)
  boot.initrd.kernelModules = [
    "vfio_pci"
    "vfio"
    "vfio_iommu_type1"
  ];
  
  boot.extraModprobeConfig = ''
    options vfio-pci disable_vga=1
  '';
  
  # Utility to check groups
  environment.systemPackages = with pkgs; [
    (writeShellScriptBin "iommu-groups" ''
      for d in /sys/kernel/iommu_groups/*/devices/*; do
        n=$(basename $(dirname $(dirname $d)))
        echo "IOMMU Group $n: $(${pkgs.pciutils}/bin/lspci -nns ''${d##*/})"
      done | sort -V
    '')
  ];
}
