import subprocess as ps;
import sys;
import os;

def CHECK_PIP():
  try:
    import pip;
  except:
    print("Requires pip to install requirements.");
    sys.exit();

def CHECK_REQUESTS():
  try:
    print("Checking 'requests'");
    import requests;
    print("'requests' module Detected");
  except:
    print("Unmatch dependency, 'requests' module required");
    OP = raw_input("Do you want to Install? (No):")
    if(OP.lower() == "y" or OP.lower() == "yes"):
      CHECK_PIP();
      ps.call(["pip", "install", "requests"]);
    else:
      print("Aborting Installation!");
      sys.exit();

def CHECK_PYINST():
  try:
    print("Checking PyInstaller");
    status = ps.call(["pyinstaller", "--version"]);
  except:
    print("Building Dependency PyInstaller not found");
    OP = raw_input("Do you want to Install PyInstaller? (No):");
    if(OP.lower() == "y" or OP.lower() == "yes"):
      CHECK_PIP();
      ps.call(["pip", "install", "pyinstaller", "-g"]);
    else:
      print("Aborting Installation!");
      sys.exit();

def main():
  CHECK_REQUESTS();
  CHECK_PYINST();

if __name__ == "__main__":
  try:
    main();
  except KeyboardInterrupt:
    try:
      sys.exit(0);
    except SystemExit:
      os._exit(0);


