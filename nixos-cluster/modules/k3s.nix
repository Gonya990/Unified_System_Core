{ config, pkgs, lib, ... }:

{
  # K3s configuration
  services.k3s = {
    enable = true;
    role = lib.mkDefault "agent";
    serverAddr = lib.mkIf (config.services.k3s.role == "agent") "https://node1:6443";
    tokenFile = "/etc/k3s/token";
    
    extraFlags = toString [
      "--container-runtime-endpoint=unix:///run/containerd/containerd.sock"
    ];
  };

  # Custom containerd config to use nvidia-container-runtime
  # This is often needed for K3s to correctly pass GPUs to pods
  # Note: K3s provides a way to override containerd config via /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl
  # In NixOS we can manage this via virtualisation.containerd or specific etc files

  environment.etc."rancher/k3s/config.yaml" = {
    text = ''
      write-kubeconfig-mode: "0644"
      kube-apiserver-arg:
        - "feature-gates=DevicePlugins=true"
    '';
  };

  environment.systemPackages = with pkgs; [
    kubectl 
    kubernetes-helm 
    k9s
  ];
}
