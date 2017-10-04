import os
import pciAuto
import shutil

env = Environment(ENV=os.environ)
env['ENV']['LANG'] = 'en_GB.UTF-8'

env['arquivo'] = []
env['Documento'] = []
env['parametro'] = ''
env['log'] = ""
env['modelo'] = ""
env['saida'] = ""
env['modulo'] = ""
env['versao'] = ""
env['conferente'] = ""
env['comando'] = ""
env['interRev'] = ""

def pegaNome(arquivo):
    arquivo= str(arquivo[0])
    nome = ''
    arquivo = open(arquivo, 'r')
    nome = arquivo.read()
    nome = nome[:nome.find("<")]
    arquivo.close()
    return nome
    

def formatVers(versao):
    if len(versao) > 5:
        versao = versao.split('.')
        versao = versao [2] + '.' + versao[3]
    return versao

def LerInterRev(target, source, env):
    target = str(target[0])
    source= str(source[0])
    arquivo = open(source,'r')
    interRev = arquivo.read()
    interRev = interRev[:interRev.rfind(":")]
    arquivo = open(source, 'w')
    arquivo.writelines(interRev)
    arquivo.close()
    return None
    
bld = Builder(action = LerInterRev,
                    suffix = '.txt')
                    
env.Append(BUILDERS = {'lRev': bld})

def build_tex(target, source, env):
    saida = str(target[0])
    log = str(source[0])
    modelo = 'main.tex'
    versao = pciAuto.pegaversao(log)
    if not conferente:
        pciAuto.formataDocumento(log, modelo, (saida + versao + '.tex'), modulo, versao, pegaNome(arquivo))
    else:
        pciAuto.formataDocumento(log, modelo, (saida + versao + '.tex'), modulo, versao, conferente)
    DST = (os.environ.get('PCI') + '\\' + saida + versao + '.pdf')
    if os.environ.get('PCI'):        
        pdfOutput2 = env.Install(os.environ.get('PCI') + '\\', (saida + versao + '.pdf'))
        #pdfOutput2 = env.PDF(target=[DST,(saida + versao + '.pdf')],source=(saida + versao + '.tex'))   
        pdfOutput = env.PDF(target=(saida +'P'+ versao + '.pdf'),source=(saida + versao + '.tex'))   
        Depends(pdfOutput, pdfOutput2)
    
    #pdfOutput = env.PDF(target=[DST,(saida + versao + '.pdf')],source=(saida + versao + '.tex'))
    # copiaPDF = env.cArq(target=('../'),source=([str(pdfOutput),'saida.txt']))
    # env.AlwaysBuild(copiaPDF)
    
    return None

bld = Builder(action = build_tex,
                    src_suffix = '.txt')
                     
env.Append(BUILDERS = {'gTex' : bld})

def copia_arq(target, source, env):
    if os.environ.get('PCI'):
        #saida = str(target[0])
        log= str(source[1])
        versao = pciAuto.pegaversao(log)
        arq = 'Projeto SiTef - '+ modulo +' - ' + versao + '.pdf'
        arq = str(arq)
        arq = str(source[0])
        prefixo = str(source[0])
        prefixo = prefixo[:prefixo.find('\\')+1]
        shutil.copy2( (prefixo+'\\'+arq), (os.environ.get('PCI') + '\\' + arq))
    
    return None
    
bld3 = Builder(action = copia_arq,
                     src_suffix = '.txt',
                     suffix = '.pdf')
                    
env.Append(BUILDERS = {'cArq': bld3})

if 'Documento' in ARGUMENTS: 
    parametro = ARGUMENTS.get("Documento")
    parametro = parametro.split(",")
    
    if 'Conferente' in ARGUMENTS: 
        parametro = ARGUMENTS.get("Conferente")
        conferente = parametro
    else:
        arquivo = env.Command(target="nomehg.txt", source=None, action = "hg showconfig ui.username > $TARGET")
        env.AlwaysBuild(arquivo)
        conferente = ""
    
    if 'Modulo' in ARGUMENTS: 
        parametro = ARGUMENTS.get("Modulo")
        modulo = parametro
    else:
        Import('nome_executavel')
        modulo = nome_executavel
    
    if 'Versao' in ARGUMENTS: 
        parametro = ARGUMENTS.get("Versao")
        versao = parametro
        versaoF = formatVers(parametro)
        comando = env.Command(target='interRev.txt', source=None, action= "hg --config revsetalias.sitclean=\"not ancestors('sitef-comum')\" --config revsetalias.sitrelease=\"(grep(r'\A([\[\(]?\d\.[\d\.]+)') or tag('re:\d+\.\d+')) and sitclean\" --config revsetalias.sitversion(v)=\"1::(grep(r'\A\(?\[?(5|6)\.\d+\.'## v) or tag('re:(5|6)\.\d+\.'## v))\" log --template \"{rev}:\" -r \"last(((sitrelease) and  (sitversion('" +versaoF+ "'))) ^ 0, 2)\" > $TARGET")
        env.AlwaysBuild(comando)
    else:
        versao = 'x.x.x.x'
        comando = env.Command(target='interRev.txt', source=None, action= "hg --config revsetalias.sitclean=\"not ancestors('sitef-comum')\" --config revsetalias.sitrelease=\"(grep(r'\A([\[\(]?\d\.[\d\.]+)') or tag('re:\d+\.\d+')) and sitclean\" --config revsetalias.sitversion(v)=\"1::(grep(r'\A\(?\[?(5|6)\.\d+\.'## v) or tag('re:(5|6)\.\d+\.'## v))\" log --template \"{rev}:\" -r \"last((sitrelease) ^ 0, 2)\" > $TARGET")
        env.AlwaysBuild(comando)
        
    if 'Modelo' in ARGUMENTS: 
        parametro = ARGUMENTS.get("Modelo")
        modelo = parametro
    else:
        modelo = 'main.tex'   
    
    if 'Query' in ARGUMENTS: 
        parametro = ARGUMENTS.get("Query")
        versao = 'x.x.x.x'
        comando = 'hg log --template "date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\n\\n" -r ' + parametro+' > $TARGET'
        env.Command(target='saida.txt', source=None, action= comando )
    else:
        interRev = ''
        interRev = env.lRev('',str(comando[0]))
        interRev = env.Command(target='saida.txt', source='interRev.txt', action= "for /f \"delims=\" %i in ('type $SOURCE') do hg log --template \"date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\n\\n\"  -r %i > $TARGET")
        env.AlwaysBuild(interRev)
    documento = env.gTex(target=('Projeto SiTef - '+ modulo +' - '), source='saida.txt')
    #documento = env.gTex(target=('Projeto SiTef - '+ modulo +' - '), source='saida.txt')
    #copiaPDF = env.cArq(target=('../'),source=('saida.txt'))
    Install("", "../placeins.sty")
    Install("", "../setspace.sty")
    Install("", "../ltablex.sty")
    Install("", "../fundoSE.jpg")
