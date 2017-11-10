Import('env', 'depsolver')
import os
import SCons
import shutil

import sys
srcdir = env.Dir('.').srcnode()
sys.path.append(srcdir.abspath)

import pciAuto

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
    if len(versao) > 5:
        versao = versao.split('.')
        versao = versao [2] + '.' + versao[3]
    return versao

def LerInterRev(target, source, env):
    seg_rev = 0
    target = str(target[0])
    source= str(source[0])
    arq = open(source,'r')
    interRev = arq.read()
    arq.close()
    if (interRev.find(":") != interRev.rfind(":")):
        interRev = interRev[:interRev.rfind(":")]
        seg_rev = interRev[interRev.find(":")+1:]
        seg_rev = int(float(seg_rev)) + 1
    pri_rev = interRev[:interRev.find(":")]
    interRev = pri_rev +':'+ str(seg_rev) + ' and ancestors('+pri_rev+') and not ancestors("sitef-comum")'
    arq = open(target, 'w')
    arq.writelines(interRev)
    arq.close()
    return None
    
bld1 = Builder(action = LerInterRev,
               suffix = '.txt')

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

bld2 = Builder(action = build_tex,
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
    
bld3 = Builder(action = copia_pdf,
              src_suffix = '.txt',
              suffix = '.pdf')           
              
def clean_mlstring(s):
  return ' '.join(s.replace('\r', ' ').replace('\n', ' ').split())

def CriaDocPCI(env, nome_executavel, pasta_destino):
    
    if 'fase' in ARGUMENTS:
        parametro = ARGUMENTS.get("fase")
        fase = parametro
        env['dadosDoc'].fase = parametro
    else:
        fase = '0'
        env['dadosDoc'].fase = '0'
    
    if 'modulo' in ARGUMENTS: 
        parametro = ARGUMENTS.get("modulo")
        env['dadosDoc'].modulo = parametro
    else:
        env['dadosDoc'].modulo = nome_executavel
    
    if env['PLATFORM'] == 'win32':
      moduloeFase = env.Command(target=mktpath("moduloeFase.txt",env['dadosDoc'].modulo), source=None, action = 'echo {} > $TARGET'.format(fase+';'+env['dadosDoc'].modulo))
    else:
      moduloeFase = env.Command(target=mktpath("moduloeFase.txt",env['dadosDoc'].modulo), source=None, action = 'echo "{}" > $TARGET'.format(fase+';'+env['dadosDoc'].modulo))
    
    if 'conferente' in ARGUMENTS: 
        parametro = ARGUMENTS.get("conferente")
        conferente = parametro
        env['dadosDoc'].conferente = parametro
        env['dadosDoc'].arquivo = env.Command(target=mktpath("nomehg.txt",env['dadosDoc'].modulo), source=moduloeFase, action = "echo {} > $TARGET".format(conferente))
    else:
        env['dadosDoc'].arquivo = env.Command(target=mktpath("nomehg.txt",env['dadosDoc'].modulo), source=moduloeFase, action = "hg showconfig ui.username > $TARGET")
        conferente = ""
        env['dadosDoc'].conferente = ""
    
    if 'versao' in ARGUMENTS: 
        parametro = ARGUMENTS.get("versao")
        env['dadosDoc'].versao = parametro
        versaoF = formatVers(parametro)
        interRev = env.Command(target=mktpath('interRev.txt',env['dadosDoc'].modulo), source=env['dadosDoc'].arquivo, action=(clean_mlstring('''
        hg --config revsetalias.sitclean="not ancestors('sitef-comum')"
        --config revsetalias.sitrelease="(grep(r'\A([\[\(]?\d\.[\d\.]+)') or tag('re:\d+\.\d+')) and sitclean"
        --config "revsetalias.sitversion(v)=1::(grep(r'\A\(?\[?((5|6)\.\d+\.)?'##v##r'+[ |\)|\]|$]?$') or tag('re:((5|6)\.\d+\.)?'##v##'+[ |\)|\]|$]?$'))"
        log --template "{rev}:" -r "last(((sitrelease) and (sitversion("''' +versaoF+ '''"))) ^ 0, 2)" > $TARGET''')))
    else:
        env['dadosDoc'].versao = 'x.x.x.x'
        interRev = env.Command(target=mktpath('interRev.txt',env['dadosDoc'].modulo), source=env['dadosDoc'].arquivo, action=(clean_mlstring('''
        hg --config revsetalias.sitclean="not ancestors('sitef-comum')" 
        --config revsetalias.sitrelease="(grep(r'\A([\[\(]?\d\.[\d\.]+)') or tag('re:\d+\.\d+')) and sitclean" 
        --config "revsetalias.sitversion(v)=1::(grep(r'\A\(?\[?((5|6)\.\d+\.)?'##v##r'+[ |\)|\]|$]?$') or tag('re:((5|6)\.\d+\.)?'##v##'+[ |\)|\]|$]?$'))" 
        log --template "{rev}:" -r "last((sitrelease) ^ 0, 2)" > $TARGET''')))
    if 'modelo' in ARGUMENTS: 
        parametro = ARGUMENTS.get("modelo")
        env['dadosDoc'].modelo = parametro
        if 'assets' in ARGUMENTS: 
            parametro = ARGUMENTS.get("assets")
            env['dadosDoc'].assetsModelo = parametro
    else:
        env['dadosDoc'].modelo = srcdir.File('main.tex').abspath
    
    if 'query' in ARGUMENTS: 
        parametro = ARGUMENTS.get("query")
        env['dadosDoc'].versao = 'x.x.x.x'
        log = env.Command(target=mktpath('hglog.txt',env['dadosDoc'].modulo), source=interRev, action= 'hg log --template "date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\nphases({phase})$\\n\\n" -r ' + parametro+' > $TARGET')
    else:
        interRev2 = env.lRev(mktpath('interRev2.txt',env['dadosDoc'].modulo), interRev)
        if env['PLATFORM'] == 'win32':
            log = env.Command(target=mktpath('hglog.txt',env['dadosDoc'].modulo), source=interRev2, action=(clean_mlstring('''
            for /f \"delims=\" %i in ('type $SOURCE') do 
            hg log --template "date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\nphases({phase})$\\n\\n"  -r "%i" > $TARGET''')))
        else:
            log = env.Command(target=mktpath('hglog.txt',env['dadosDoc'].modulo), source=interRev2, action=(clean_mlstring('''
            var=$(cat &SOURCE) | 
            hg log --template "date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\nphases({phase})$\\n\\n"  -r "$var" > $TARGET''')))
     
    if 'dupli' in ARGUMENTS: 
        parametro = ARGUMENTS.get("dupli")
        dupli = parametro
        log2 = env.Command(target=mktpath("hglog2.txt",env['dadosDoc'].modulo), source=log, action = "echo {} > $TARGET".format(dupli))
    else:
        dupli = '0'
        log2 = env.Command(target=mktpath('hglog2.txt',env['dadosDoc'].modulo), source=log, action= (clean_mlstring('''
        hg log --template "desc({desc})$\\ntags({tags})$\\ndate({date|shortdate})$\\n\\n" > $TARGET''')))
    
    env.AlwaysBuild(log2)
    
    Documento = env.gTex(target=mktpath('Projeto SiTef - '+ env['dadosDoc'].modulo,env['dadosDoc'].modulo), source=[log,env['dadosDoc'].arquivo,env['dadosDoc'].modelo,moduloeFase,log2])
    env.Install(mktpath("",env['dadosDoc'].modulo), srcdir.File('placeins.sty').abspath)
    env.Install(mktpath("",env['dadosDoc'].modulo), srcdir.File('setspace.sty').abspath)
    env.Install(mktpath("",env['dadosDoc'].modulo), srcdir.File('ltablex.sty').abspath)
    env.Install(mktpath("",env['dadosDoc'].modulo), srcdir.File('placeins.sty').abspath)
    env.Install(mktpath("",env['dadosDoc'].modulo), srcdir.File('xcolor.sty').abspath)
    env.Install(mktpath("",env['dadosDoc'].modulo), srcdir.File('fundoSE.jpg').abspath)
    geraPDF = env.PDF(target=mktpath('Projeto SiTef - '+ env['dadosDoc'].modulo,env['dadosDoc'].modulo),source=(Documento))
    env['dadosDoc'].destino = pasta_destino
    copiaPDF = env.cPDF(target=mktpath(os.path.join('PDF','Projeto SiTef - '+ env['dadosDoc'].modulo),env['dadosDoc'].modulo),source=[geraPDF,log])
    env.Alias('docpci',copiaPDF)
    env.Alias('all','docpci')

    if 'rangeversao' in ARGUMENTS: 
        parametro = ARGUMENTS.get("rangeversao")
        loopVersao = parametro.split(",")
        env['dadosDoc'].modulo = nome_executavel
        if env['PLATFORM'] == 'win32':
            loopdeversao = env.Command(target=mktpath('Projeto SiTef - '+ env['dadosDoc'].modulo + '.txt',env['dadosDoc'].modulo), source=loopVersao, action=(clean_mlstring('''
            for /f \"delims=\" %i in ('type $SOURCE') do 
            scons -i docpci versao=\"%i\" > $TARGET''')))
        else:
            loopdeversao = env.Command(target=mktpath('Projeto SiTef - '+ env['dadosDoc'].modulo + '.txt',env['dadosDoc'].modulo), source=loopVersao, action=(clean_mlstring('''
            var=$(cat &SOURCE) | 
            scons -i docpci versao=\"%i\" > $TARGET''')))
        env.Default(loopdeversao)

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
    
    class dadosDoc:
        versao = ''
        modelo = ''
        modulo = ''
        arquivo = ''
        destino = ''
        assetsModelo = ''
        
    env.Prepend(dadosDoc = dadosDoc)
      
    env.Append(BUILDERS = {'lRev': bld1})
    env.Append(BUILDERS = {'gTex': bld2})
    env.Append(BUILDERS = {'cPDF': bld3})
    env.AddMethod(CriaDocPCI)
    env.AddMethod(CriaDocPCI,"nome_docpci")

depsolver.AddProvides({'docpci':docpci})
