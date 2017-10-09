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
env['fase'] = ""
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
        pciAuto.formataDocumento(log, modelo, (saida + versao + '.tex'), modulo, versao, pegaNome(arquivo), fase)
    else:
        pciAuto.formataDocumento(log, modelo, (saida + versao + '.tex'), modulo, versao, conferente, fase)
    return None

bld = Builder(action = build_tex,
                    src_suffix = '.txt')
                     
env.Append(BUILDERS = {'gTex' : bld})

def gera_PDF(target, source, env):
    log = str(source[0])
    tex = str(source[1])
    versao = pciAuto.pegaversao(log)
    arq = tex + versao + '.pdf'
    pdfOutput = env.PDF(target=(arq),source=(tex + versao + '.tex'))
    env.AlwaysBuild(pdfOutput)
    return None
    
bld3 = Builder(action = gera_PDF,
                     src_suffix = '.txt',
                     suffix = '.pdf')
                    
env.Append(BUILDERS = {'gPDF': bld3})

def copia_pdf(target, source, env):
    if os.environ.get('PCI'):
        log = str(source[0])
        nPDF = str(target[0])
        nPDF = nPDF[:nPDF.find('.pdf')]
        tex = nPDF
        versao = pciAuto.pegaversao(log)
        nPDF = nPDF + versao +'.pdf'
        DST = os.environ.get('PCI')+"\\"#Projeto SiTef - drvcom - 6.1.1.21.pdf"
        Instala1 = env.Install([''], nPDF)
        Instala2 = env.Install([DST], nPDF)
        env.Depends(Instala1, Instala2)
    return None
    
bld4 = Builder(action = copia_pdf,
                        src_suffix = '.txt',
                        suffix = '.pdf')
                    
env.Append(BUILDERS = {'cPDF': bld4})

if 'Documento' in ARGUMENTS: 
    parametro = ARGUMENTS.get("Documento")
    parametro = parametro.split(",")
    
    if 'Fase' in ARGUMENTS:
        parametro = ARGUMENTS.get("Fase")
        fase = parametro
    else:
        fase = 0
    
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
        comando = 'hg log --template "date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\nphases({phase})$\\n\\n" -r ' + parametro+' > $TARGET'
        env.Command(target='saida.txt', source=None, action= comando )
    else:
        interRev = ''
        interRev = env.lRev('',str(comando[0]))
        if env['PLATFORM'] == 'win32':
            interRev = env.Command(target='saida.txt', source='interRev.txt', action= "for /f \"delims=\" %i in ('type $SOURCE') do hg log --template \"date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\nphases({phase})$\\n\\n\"  -r %i > $TARGET")
            env.AlwaysBuild(interRev)
        else:
            interRev = env.Command(target='saida.txt', source='interRev.txt', action= "var=$(cat &SOURCE) | hg log --template \"date({date|isodate})$\\nfiles({files})$\\ndesc({desc})$\\ntags({tags})$\\nauthor({author})$\\nparents({parents})$\\nphases({phase})$\\n\\n\"  -r $var > $TARGET")
            #var = $(cat TST) | $var
            env.AlwaysBuild(interRev)
    documento = env.gTex(target=('Projeto SiTef - '+ modulo +' - '), source='saida.txt')
    env.AlwaysBuild(documento)
    geraPDF = env.gPDF(target=('Projeto SiTef - p'+ modulo +' - '),source=[('saida.txt'),documento])
    copiaPDF = env.cPDF(target=('Projeto SiTef - '+ modulo +' - '),source=[('saida.txt'),geraPDF])
    env.Depends(copiaPDF, geraPDF)
    Install("", "../placeins.sty")
    Install("", "../setspace.sty")
    Install("", "../ltablex.sty")
    Install("", "../xcolor.sty")
    Install("", "../fundoSE.jpg")
