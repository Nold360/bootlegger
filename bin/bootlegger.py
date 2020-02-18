#!/usr/bin/env python
import yaml
import subprocess
import argparse
from sys import exit

def exe(command):
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, executable='/bin/bash', shell=True)
  (out, err) = proc.communicate()
  return out, err

def skopeo_copy(src, dest, src_auth=None, dest_auth=None, verbose=False):
  cmd = "skopeo copy"
  if src_auth:
    cmd = "%s --src-creds %s" %(cmd, src_auth)
  if dest_auth:
    cmd = "%s --dest-creds %s" %(cmd, dest_auth)

  cmd = cmd + " %s %s" % (src, dest)
  if verbose:  print("Copy: %s -> %s" %(src, dest))
  exe(cmd)

if __name__== "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("config", help="Pfad zur .list/yaml config")
  parser.add_argument("-v", "--verbose", help="Be more verbose", action="store_true", default=False)
  parser.add_argument("-p", "--prefix", help="Target Registry Prefix", required=True)
  parser.add_argument("-s", "--src-creds", help="Credentials for source registry", default=None)
  parser.add_argument("-d", "--dest-creds", help="Credentials for destination registry", default=None)
  args = parser.parse_args()

  # Load yaml config
  images=[]
  if ".yaml" in args.config:
    config = yaml.load(open(args.config, 'r'))
    for image in config['images']:
      for tag in config['images'][image]['tags']:
        src = "%s:%s" % (image, tag)
        images.append(src)
  elif ".list" in args.config:
    with open(args.config, 'r') as f:
      for src in f:
        images.append(src.rstrip())
  else:
    print("We need a .yaml or .list file")

  for src in images:
    skopeo_copy(src, "%s/%s" % (str(args.prefix), src), src_auth=args.src_creds, dest_auth=args.dest_creds, verbose=args.verbose)
  exit(0)
