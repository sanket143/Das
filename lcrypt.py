import os, random
import subprocess

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

LIZ_HOME = os.environ["HOME"] + "/.liz/";

def generateKey(password):
  return SHA256.new(password).digest();

def enc(password, content):
  os.chdir(LIZ_HOME);
  key = generateKey(password);
  content += "signed";
  chunksize = 64*1024;
  outputFile = "lizpk";
  filesize = str(len(content)).zfill(16);

  with open(outputFile + ".tmp", "wb") as outfile:
    outfile.write(content + "Signed");

  IV = "";

  for i in range(16):
    IV += chr(random.randint(0, 0xFF));

  encryptor = AES.new(key, AES.MODE_CBC, IV);

  with open(outputFile + ".tmp", "rb") as infile:
    with open(outputFile, "wb") as outfile:
      outfile.write(filesize);
      outfile.write(IV);

      while True:
        chunk = infile.read(chunksize);

        if len(chunk) == 0:
          break;
        elif len(chunk) % 16 != 0:
          chunk += " " * (16 - (len(chunk) % 16));

        outfile.write(encryptor.encrypt(chunk));
  subprocess.call(["rm", outputFile + ".tmp"]);

def dec(password):
  os.chdir(LIZ_HOME);
  key = generateKey(password);
  chunksize = 64*1024;
  filename = "lizpk";

  with open(filename, "rb") as infile:
    filesize = long(infile.read(16));
    IV = infile.read(16);

    decryptor = AES.new(key, AES.MODE_CBC, IV);

    with open(filename + ".liz", "wb") as outfile:
      while True:
        chunk = infile.read(chunksize);

        if len(chunk) == 0:
          break;
        outfile.write(decryptor.decrypt(chunk))
      outfile.truncate(filesize);

    content = "";
    with open(filename + ".liz", "r") as passfile:
      content = passfile.read();

    subprocess.call(["rm", filename + ".liz"]);
    if(content[-6:] == "signed"):
      return content[:-6];
      return True;
    else:
      return False;

