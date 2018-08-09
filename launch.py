#!/usr/bin/python

import requests;
import sys;
import lcrypt;
import subprocess;
import getpass;
import requests;
import os;

ps = False;

if len(sys.argv) < 2:
  import liz_help;
  sys.exit();


if sys.argv[1] == "login":
  os.chdir(os.environ["HOME"]);
  if not os.path.isfile(".liz/lizpk"):
    print("Please configure credentials.\n$ liz config");
    exit();

  url = "https://10.100.56.55:8090/login.xml"
  LoggedIn = False;
  try:
    key = getpass.getpass("Liz Key: ");
  except KeyboardInterrupt:
    sys.exit();

  content = lcrypt.dec(key);
  if(content):
    content = content.split("\n");
    content = [x.split(" ") for x in content];
  else:
    print("Decryption Failed. Please provide correct key.");
    exit();

  for cred in content:
    label = cred[0];
    username = cred[1];
    password = cred[2];

    data = {
      "a": "1524343263066",
      "mode": 191,
      "producttype": 0,
      "username": username,
      "password": password
    }

    r = requests.post(url = url, data = data, verify = False)
    if("logged in" in str(r.content)):
      print("Successfully Logged In as " + label);
      sys.exit();

  print("All Credentials failed to Log In.");

elif sys.argv[1] == "logout":
  data = {
    "a": "1524343263066",
    "mode": 193,
    "producttype": 0,
    "username": "whoever"
  }

  r = requests.post(url = url,data = data, verify=False);
  if("logged off" in str(r.content)):
    print("Successfully Logged Out");
  else:
    print("Error Occured in Logging Out");

elif sys.argv[1] == "uninstall":
  os.chdir("/");
  subprocess.call(["sudo", "rm", "usr/local/bin/liz"]);

elif sys.argv[1] == "config":
  os.chdir(os.environ["HOME"])
  if os.path.isfile(".liz/lizpk"):
    print("Credentials are configured..");
    try:
      choice = raw_input("Do you want to reset credentials?(y/N)");
      if choice.lower() == "y":
        code = subprocess.call(["rm", ".liz/lizpk"]);
        if(code == 0):
          print("Configuration Reset");
        else:
          print("Error Occured");
      
    except KeyboardInterrupt:
      exit();
    
  else:
    priority_no = 0;
    content = "";

    print("""
\bLiZ v1.1.0 Created by Sanket Chaudhari

Use multiple credentials to login to DA Captive Portal

Ex:
  #0 Cred0
  #1 Cred1
  #2 Cred2

For above priority sequence
  login with Cred0
        OR
  login with Cred1
        OR
  login with Cred2
        OR
  Fail to Login.
""");
    while(True):
      print("Credential #" + str(priority_no) + " (Ctrl+C When done!)");
      try:
        label = raw_input("Label: ");
        username = raw_input("Username: ");
        password = getpass.getpass();

        cred = label.replace(" ", "-") + " " + username + " " + password;
        content += cred + "\n";
      except KeyboardInterrupt:
        content = content[:-1];
        break;

    print("\b\nWarning: Liz Key cannot get reset!");
    try:
      while(True):
        ENC_KEY = getpass.getpass("Liz Key: ");
        CONFIRM_ENC_KEY = getpass.getpass("Confirm Liz Key: ");
        if(ENC_KEY == CONFIRM_ENC_KEY):
          break;
        else:
          print("Key did not matched.");
    except KeyboardInterrupt:
      exit();

    lcrypt.enc(ENC_KEY, content);

else:
  print("Invalid Command",sys.argv[1]);
  import liz_help;
