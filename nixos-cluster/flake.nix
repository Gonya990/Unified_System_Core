{
  description: "Unified AI + Gaming Cluster (NixOS + K3s)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  };

  outputs = { self, nixpkgs }: 
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
    nixosConfigurations = {
      # Master Node / K3s Server
      node1 = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          ./modules/common.nix
          ./modules/nvidia.nix
          ./modules/vfio.nix
          ./modules/libvirt.nix
          ./modules/k3s.nix
          ./modules/gpu-arbiter.nix
          ./hosts/node1.nix
        ];
      };
      
      # Worker Nodes / K3s Agents
      node2 = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          ./modules/common.nix
          ./modules/nvidia.nix
          ./modules/vfio.nix
          ./modules/libvirt.nix
          ./modules/k3s.nix
          ./modules/gpu-arbiter.nix
          ./hosts/node2.nix
        ];
      };

      node3 = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          ./modules/common.nix
          ./modules/nvidia.nix
          ./modules/vfio.nix
          ./modules/libvirt.nix
          ./modules/k3s.nix
          ./modules/gpu-arbiter.nix
          ./hosts/node3.nix
        ];
      };

      node4 = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          ./modules/common.nix
          ./modules/nvidia.nix
          ./modules/vfio.nix
          ./modules/libvirt.nix
          ./modules/k3s.nix
          ./modules/gpu-arbiter.nix
          ./hosts/node4.nix
        ];
      };
    };
  };
}
