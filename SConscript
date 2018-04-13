Import('env', 'depsolver')
import os
import SCons
import shutil

import sys
srcdir = env.Dir('.').srcnode()
sys.path.append(srcdir.abspath)

import pciAuto

def clean_mlstring(s):
  return ' '.join(s.replace('\r', ' ').replace('\n', ' ').split())

hgrevsetcfg = clean_mlstring('''
--config "revsetalias.sitc=not ancestors('sitef-comum')"
--config "revsetalias.sitrls=sort(grep(r'\A([\[\(]?\d\.[\d\.]+)') or tag('re:\d+\.\d+'),rev) and sitc"
--config "revsetalias.sitv(v)=(grep(r'\A\(?\[?((5|6)\.\d+\.)?'##v##r'($| |\)|\]|\:|\n)') or tag('re:\A\(?\[?((5|6)\.\d+\.)?'##v##'($| |\)|\]|\:)'))"
--config "revsetalias.doc(rlsrev, allrlsrev, finalfilter)=((ancestors(rlsrev))-ancestors(ancestors(parents(rlsrev)) and allrlsrev)) and finalfilter"
--config "revsetalias.sitdoc(rlsrev)=doc(rlsrev, sitrls, sitc)"
--config "revsetalias.sitdocv(v)=sitdoc(sitv(v))"
''')

hgtemplate = clean_mlstring('''
  --template "date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\nphases({phase})$\\n\\n"
''')

def mktpath(name,name_path):
  return os.path.join('$buildroot', 'docpci', name_path, name)

def pegaNome(file):
    file= str(file[0])
    nome = ''
    file = open(file, 'r')
    nome = file.read()
    nome = nome[:nome.find("<")]
    file.close()
    return nome

def formatVers(versao):
    while versao.count(".")>1:
        versao= versao[versao.find('.')+1:]
    return versao

def build_tex(target, source, env):
    
    saida = str(target[0])
    log = str(source[0])
    fase = str(source[3])
    log2 = str(source[4])
    log = (os.path.join(os.path.abspath('.'),log))
    log2 = (os.path.join(os.path.abspath('.'),log2))
    if env['dadosDoc'].versao=="x.x.x.x":
        pciAuto.formataDocumento(log, env['dadosDoc'].modelo, (saida), env['dadosDoc'].modulo, pciAuto.pegaversao(log), pegaNome(env['dadosDoc'].arquivo), fase, log2)
    else:
        pciAuto.formataDocumento(log, env['dadosDoc'].modelo, (saida), env['dadosDoc'].modulo, env['dadosDoc'].versao, pegaNome(env['dadosDoc'].arquivo), fase, log2)
    
    if 'assets' in ARGUMENTS:
        saidaAssets = os.path.join(os.path.abspath(os.path.dirname(saida)),'')
        src_files = os.path.join(env['dadosDoc'].assetsModelo,'')
        for file_name in os.listdir(src_files):
                full_file_name = os.path.join(env['dadosDoc'].assetsModelo, file_name)
                if (os.path.isfile(full_file_name)):
                    shutil.copy2(full_file_name, saidaAssets)
        
    return None

bld1 = Builder(action = build_tex,
              src_suffix = '.txt',
              suffix = '.tex')

def copia_pdf(target, source, env):
    
    oPDF = str(source[0])
    log = str(source[1])
    log = (os.path.join(os.path.abspath('.'),log))
    DST = str(target[0])
    
    shutil.copy2(oPDF, DST)
    
    if env['dadosDoc'].versao.find('/'):
        env['dadosDoc'].versao = env['dadosDoc'].versao.replace('/','-')
    
    if env['dadosDoc'].versao=="x.x.x.x":
        DST = DST[:DST.find('.pdf')] + ' - ' + pciAuto.pegaversao(log) + '.pdf'
    else:
        DST = DST[:DST.find('.pdf')] + ' - ' + env['dadosDoc'].versao + '.pdf'
    
    shutil.copy2(oPDF, DST)
    
    if os.environ.get('PCI'):
        nPDF = oPDF[oPDF.find('Projeto'):oPDF.find('.pdf')]
        if env['dadosDoc'].versao=="x.x.x.x":
            nPDF = nPDF + ' - ' + pciAuto.pegaversao(log) + '.pdf'
        else:
            nPDF = nPDF + ' - ' + env['dadosDoc'].versao + '.pdf'
        DST2 = os.path.join(os.environ.get('PCI'),env['dadosDoc'].destino ,nPDF)
        
        shutil.copy2(DST, DST2)
    
    return None
    
bld2 = Builder(action = copia_pdf,
              src_suffix = '.txt',
              suffix = '.pdf')           

def CriaDocPCI(env, nome_executavel, pasta_destino):
    
    fase = ARGUMENTS.get("fase", '0')
    
    env['dadosDoc'].modulo = ARGUMENTS.get("modulo", nome_executavel)
    
    if env['PLATFORM'] == 'win32':
        moduloeFase = env.Command(
          target=mktpath("moduloeFase.txt",env['dadosDoc'].modulo),
          source=None,
          action = 'echo {} > $TARGET'.format(fase+';'+env['dadosDoc'].modulo))
    else:
        moduloeFase = env.Command(
          target=mktpath("moduloeFase.txt",env['dadosDoc'].modulo),
          source=None,
          action = 'echo "{}" > $TARGET'.format(fase+';'+env['dadosDoc'].modulo))
    
    conferente = ARGUMENTS.get("conferente", None)
    if not conferente is None:
        env['dadosDoc'].conferente = conferente
        env['dadosDoc'].arquivo = env.Command(
          target=mktpath("nomehg.txt",env['dadosDoc'].modulo),
          source=moduloeFase,
          action="echo {} > $TARGET".format(conferente))
    else:
        env['dadosDoc'].arquivo = env.Command(
          target=mktpath("nomehg.txt",env['dadosDoc'].modulo),
          source=moduloeFase,
          action="hg showconfig ui.username > $TARGET")
        
        env['dadosDoc'].conferente = ""
    
    env['dadosDoc'].modelo = ARGUMENTS.get("modelo", srcdir.File('main.tex').abspath)
    
    if 'assets' in ARGUMENTS: 
        parametro = ARGUMENTS.get("assets")
        env['dadosDoc'].assetsModelo = parametro
        
    parametro = ARGUMENTS.get("versao")
    if not parametro is None:
        env['dadosDoc'].versao = parametro
        versaoF = formatVers(parametro)
        action = 'hg log {} {} -r "{}(\'{}\')" > $TARGET'.format(hgrevsetcfg, hgtemplate, 'sitdocv' if '.' in parametro else 'sitdoc', versaoF)
    else:
        env['dadosDoc'].versao = 'x.x.x.x'
        action = 'hg log {} {} -r "sitdocl" > $TARGET'.format(hgrevsetcfg, hgtemplate)
        
    log = env.Command(
      target=mktpath('hglog.txt',env['dadosDoc'].modulo),
      source=env['dadosDoc'].arquivo,
      action=(action))
    
    parametro = ARGUMENTS.get("query", None)
    if not parametro is None:
        log = env.Command(
          target=mktpath('hglog.txt',env['dadosDoc'].modulo),
          source=env['dadosDoc'].arquivo,
          action=('hg log {} -r {} > $TARGET').format(hgtemplate, parametro))
    
    dupli = ARGUMENTS.get("dupli")
    if not dupli is None:
        log2 = env.Command(
          target=mktpath("hglog2.txt",env['dadosDoc'].modulo),
          source=log,
          action = "echo {} > $TARGET".format(dupli))
    else:
        log2 = env.Command(
          target=mktpath('hglog2.txt',env['dadosDoc'].modulo),
          source=log,
          action=('hg log --template "desc({desc})$\\ntags({tags})$\\ndate({date|shortdate})$\\n\\n" > $TARGET'''))
    
    env.AlwaysBuild(log2)

    Documento = env.gTex(target=mktpath('Projeto SiTef - '+ env['dadosDoc'].modulo,env['dadosDoc'].modulo), source=[log,env['dadosDoc'].arquivo,env['dadosDoc'].modelo,moduloeFase,log2])
    
    files = ['placeins.sty', 'setspace.sty', 'ltablex.sty', 'xcolor.sty', 'fundoSE.jpg']
    for file in files:
      env.Install(mktpath("",env['dadosDoc'].modulo), srcdir.File(file).abspath)
    
    geraPDF = env.PDF(target=mktpath('Projeto SiTef - '+ env['dadosDoc'].modulo,env['dadosDoc'].modulo),source=(Documento))
    env['dadosDoc'].destino = pasta_destino
    copiaPDF = env.cPDF(target=mktpath(os.path.join('PDF','Projeto SiTef - '+ env['dadosDoc'].modulo),env['dadosDoc'].modulo),source=[geraPDF,log])
    env.Alias('docpci',copiaPDF)
    env.Alias('all','docpci')

def docpci(env):
    safadeza = env.Clone(ENV = os.environ)
    
    paths = set([os.path.dirname(p) for p in [
        safadeza.WhereIs('pdflatex'),
        safadeza.WhereIs('tex'),
        safadeza.WhereIs('hg')
      ] if not p is None
    ])
    
    if len(paths) > 0:
    
      for path in paths:
        env.PrependENVPath('PATH', path)
      
      if 'HOMEPATH' in os.environ:
        # Para o hg achar a configuracao (usado no "nomehg")
        env['ENV']['HOMEPATH'] = os.environ['HOMEPATH']
      
      tools = Split('tex pdf dvi dvipdf dvips pdftex pdflatex')
      for t in tools:
        SCons.Tool.Tool(t)._tool_module().generate(env)
    
    class dadosDoc(object):
        def __init__(self):
            self.versao = ''
            self.modelo = ''
            self.modulo = ''
            self.arquivo = ''
            self.destino = ''
            self.assetsModelo = ''
        
    env.Prepend(dadosDoc = dadosDoc())
      
    env.Append(BUILDERS = {'gTex': bld1})
    env.Append(BUILDERS = {'cPDF': bld2})
    env.AddMethod(CriaDocPCI)
    env.AddMethod(CriaDocPCI,"nome_docpci")

depsolver.AddProvides({'docpci':docpci})
