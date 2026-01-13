{ pkgs, lib, config, inputs, ... }:
let
  # To use packages from nixpkgs-unstable
  pkgs-unstable = import inputs.nixpkgs-unstable { system = pkgs.stdenv.system; };
in
{
  cachix.enable = false; #disable cacheix for binaries

  dotenv.enable = true;

  # https://devenv.sh/basics/
  env.GREET = "devenv";
  # Ensure libstdc++.so.6 is visible to dynamically linked binaries (e.g. opencode/bun/node)
  env.LD_LIBRARY_PATH = lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib ];

  # https://devenv.sh/packages/
  # Include git, beads, Bun (from nixpkgs-unstable), and GCC's C++ runtime (libstdc++).
  packages = [
    pkgs.git
    pkgs.ast-grep
    pkgs-unstable.beads
    pkgs-unstable.bun
    pkgs.stdenv.cc.cc
  ];

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    package = pkgs.python312;
    venv.enable = true;
    venv.requirements = ''
      python-dotenv
      requests
    '';
  };
  # languages.rust.enable = true;

  # https://devenv.sh/processes/
  # processes.dev.exec = "${lib.getExe pkgs.watchexec} -n -- ls -la";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo hello from $GREET
  '';

  # https://devenv.sh/basics/
  enterShell = ''
    hello         # Run scripts directly
    git --version # Use packages
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
