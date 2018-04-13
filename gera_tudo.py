#!/usr/bin/python
# Script pra gerar todas as versoes 5 e 6 do repositorio
# Execute no mesmo diretorio que o scons deve ser executado
import subprocess
import os
import re
import sys

hgrevsetcfg = [
  '--config', "revsetalias.sitc=not ancestors('sitef-comum')",
  '--config', "revsetalias.sitrls=sort(grep(r'\A([\[\(]?\d\.[\d\.]+)') or tag('re:\d+\.\d+'),rev) and sitc",
]

cmd = ['hg', 'log'] + hgrevsetcfg + ['-T', '{desc}--:--{tags}--:--{rev}--;', '-r', 'sitrls']
for log in subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().split('--;')[:-1]:
  
  desc,tag,rev = log.split('--:--')
  m = re.match(r"\A([\[\(]?\d\.[\d\.]+[^ ]*)", desc)
  if not m is None:
    vers = m.groups()[0]
  else:
    vers = tag
  
  vers = vers.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
  
  if len(vers) > 3 and vers[0] not in ['5', '6']:
    # o scons nao funciona com versoes 4 e 3
    continue
  
  scons = 'scons versao={} docpci {}'.format(vers, ' '.join(sys.argv[1:]))
  print(scons)
  os.system(scons)
  os.system('scons docpci -c')
