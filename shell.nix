{ pkgs ? import <nixpkgs> {} }:

# Pro mode:
# { pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/2c0034d5fbcb1b6b511a2369329a2446c84bf884.tar.gz") {}}:

with pkgs; mkShell {
  buildInputs = [
    toilet

    #python38
    # the rule is: python *tooling* is added here,
    # while *libraries* are added through a python package manager.
    #python38Packages.jupyter 
    #python38Packages.poetry

    chromedriver
  ];

  shellHook = ''
    toilet " art vs. artist " -f term -F border --gay
  '';
}
