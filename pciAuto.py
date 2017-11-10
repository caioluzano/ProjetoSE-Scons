import sys
import codecs
import re

def formataDocumento(logHg, texPCI, saidaPCI, modulo, versao, conferente, fase, logSeg):

    i = 0;
    from datetime import date
    hj = date.today()
    hj = hj.strftime("%d/%m/%Y")
    modeloPci = open(texPCI, 'r')
    saida = open(saidaPCI, 'w')
    fase = open(fase,'r')
    fase = fase.read()
    fase = fase[:fase.find(';')]

    for linha in modeloPci:
   
        if   linha.find('\\begin{document}') >=0:
             saida.write(linha)
             if (fase == '0' or logSeg !=1):          
                 for linha in modeloPci:
                     if linha.find('\\startunderscoreletter') >=0:
                        saida.write(linha)
                        saida.write("\\begin{table}[h]\n")
                        if fase == '0':
                             saida.writelines(avaliaFases(logHg))
                        if logSeg != 1:
                             saida.writelines(avaliaVersaoLog(logSeg,versao))
                        saida.write("\\end{table}%\n")
                        break
                                  
        elif linha.find('VXX/XX/XXXXX') >= 0:
             saida.write(hj)
        elif linha.find('XXXXXXXX.exe') >= 0:
             saida.write(modulo+'.exe')
        elif linha.find('VX.X.XX.XX') >= 0:
             saida.write(versao)
        elif linha.find('CXXXXXXXXXX') >= 0:
             saida.write(conferente)
        elif linha.find('PXXXXXXXXXX') >= 0:
             saida.write(pegaNome(logHg))
        elif linha.find('CXX/XX/XXXX') >= 0:
             saida.write(pegaDataCommit(logHg))
        elif linha.find('CX.X.XX.XX') >= 0:
             saida.write(versao)
        elif linha.find('-XXXXXXXXXX') >= 0:
             saida.writelines(pegaDescriCommit(logHg))
        else:
             saida.write(linha)   

    modeloPci.close()
    saida.close()
    
def avaliaFases(logHg):

    log = open(logHg, 'r')

    linha = ''
    wLinha = []
    cWarning = ["\\colorbox{yellow}{\n",
                "\\begin{tabular}{p{16.3cm}}\n",
                "\\centering\n ",
                "WARNING! Este documento foi gerado com ",
                "revisões DRAFT e/ou SECRET, utilize a ",
                "opção fase=1 para retirar este aviso.\n",
                "\\end{tabular}%\n",
                "}\n"]

    for linha in log:
        linha = linha.lower()
        if (linha.find("phases(") >= 0):
            if (linha.find("draft") >= 0 or linha.find("secret") >=0):
                wLinha = cWarning
                repr(wLinha)
                print 'WARNING!'
                print 'WARNING!'
                print 'WARNING!'
                print '================================================================================'
                print '--------------------------------------------------------------------------------'
                print ' WARNING! Este documento foi gerado com revisoes DRAFT e/ou SECRET, utilize a   '
                print ' opcao fase=1 para retirar este aviso                                           '
                print '--------------------------------------------------------------------------------'
                print '================================================================================'
                print 'WARNING!'
                print 'WARNING!'
                print 'WARNING!'
                log.close()
                return wLinha
            else:
                wLinha = "\\startunderscoreletter\n"
              
    return wLinha
    log.close()

def avaliaVersaoLog(logSeg,versao):
    logSeg = open(logSeg,"r")
    i = 0
    j = 0
    data1 = ""
    data2 = ""
    wLinha = []

    cWarning = ["\\colorbox{red}{\n",
                "\\begin{tabular}{p{16.3cm}}\n",
                "\\centering\n ",
                "WARNING! Há mais de 1 commit com a mesma ",
                "versão em seu repositório HG, utilize a ",
                "opção dupli=1 para retirar este aviso.\n",
                "\\end{tabular}%\n",
                "}\n"]

    for linha in logSeg:
        linha = linha.lower()
        if (linha.find(versao) >=0 and (linha.find("etiqueta")<0 and linha.find("ticket")<=0)):
                linha=linha[5:linha.find(")$")]
                searchObj = re.search( r'\A\(?\[?((5|6)\.\d?\d+\.)?\d\d?\.\d?\d?\d+(\/([A-Z]|[a-z])+\d?\d?)?[ |\)|\]]?', linha, re.M|re.I)
                if searchObj:
                        versaoC = searchObj.group()
                        if versaoC.find("[")>=0 or versaoC.find("(")>=0:
                                versaoC = versaoC[1:]
                        if versaoC.find("]")>=0 or versaoC.find(")")>=0 or versaoC.find(" ")>=0:
                                versaoC = versaoC[:-1]
                        if versao == versaoC:
                                i = i + 1
                                for linha in logSeg:
                                        if linha.find("date(") >=0:
                                                if i == 1:
                                                        data1 = linha[linha.find("date(")+5:linha.find('-')]
                                                else:
                                                        data2 = linha[linha.find("date(")+5:linha.find('-')]
                                                if data1 > data2 and data2 != "":
                                                        i = i - 1
                                                break

    if i > 1:
        wLinha = cWarning
        repr(wLinha)
        print 'WARNING!'
        print 'WARNING!'
        print 'WARNING!'
        print '================================================================================'
        print '--------------------------------------------------------------------------------'
        print ' WARNING! Há mais de 1 commit com a mesma versão em seu repositório HG, utilize '
        print ' a opcao dupli=1 para retirar este aviso.                                       '
        print '--------------------------------------------------------------------------------'
        print '================================================================================'
        print 'WARNING!'
        print 'WARNING!'
        print 'WARNING!'
    else:
        wLinha = "\\startunderscoreletter\n"

    logSeg.close()
    return wLinha

def pegaversao(logHg):
    log = open(logHg, 'r')

    linha = ''
    versao = ''

    for linha in log:

            if (linha.find("tags(") >= 0) or (linha.find("desc(") >= 0):
                if (linha.find("tags(") >= 0):
                    versao = linha[linha.find("tags(")+5:linha.find(")$")]
                    if (versao.find("[")>=0):
                        versao = versao[versao.find("[")+1:versao.find("]")]
                    elif (versao.find("(")>=0):
                        versao = versao[versao.find("(")+1:versao.find(")")]
                elif (linha.find("desc") >= 0):
                    versao = linha[linha.find("desc(")+5:linha.find(")$")]
                    if (versao.find("[")>=0):
                        versao = versao[versao.find("[")+1:versao.find("]")]
                    elif (versao.find("(")>=0):
                        versao = versao[versao.find("(")+1:versao.find(")")]
                searchObj = re.search( r'\A\(?\[?((5|6)\.\d?\d+\.)?\d\d?\.\d?\d?\d+(\/([A-Z]|[a-z])+\d?\d?)?[ |\)|\]]?', versao, re.M|re.I)
                if searchObj:
                        versao = searchObj.group()
                        log.close()
                        return versao
                        

    versao = 'x.x.x.x'
    log.close()
    return versao





def pegaNome(logHg):
    log = open(logHg, 'r')

    i = 0
    linha = ''
    nome = ''
    
    for linha in log:

        if (linha.find("author(") >= 0):
            nome = linha[linha.find("author(")+7:linha.find("<")]
            log.close()
            return nome
    
    log.close()

def validaArqs(linha):

    
    if ((linha.find(".c ") >= 0) or (linha.find(".h ") >= 0) or (linha.find(".c)") >= 0) or (linha.find(".h)") >= 0) or (linha.find(".c,") >= 0) or (linha.find(".h,") >= 0)):
        return 1

    return 0


def validaDesc(linha):

    bloqueios = ["warning",
                 "removendo duplicata",
                 "mesclagem",
                 "merge",
                 "salvando",
                 "remove duplicata"]

    linha = linha.lower()

    for palavras in bloqueios:
           
        if (linha.find(palavras) >= 0):
            return 0

    return 1

def confereDesc(linha):

    fLinha = ""

    especiais = ["&",
                 "%",
                 "$",
                 "#",
                 "_",
                 "{",
                 "}",
                 "~",
                 "^",
                 "\\"]

    especiaisF = ["\&",
                 "\%",
                 "\$",
                 "\#",
                 "\_",
                 "\{",
                 "\}",
                 "\\textasciitilde",
                 "\\textasciicircum",
                 "\\textbackslash"]

    nLetra = 0
    fLinha = linha
    for letras in linha:
        key = 0
        for caracteres in especiais:
            if (letras == caracteres):
                fLinha = (fLinha[:nLetra])
                fLinha = (fLinha + especiaisF[key])
                fLinha = (fLinha + linha[nLetra+1:])
                if key < 7: 
                    nLetra = nLetra + 1
                else:
                    nLetra = nLetra + len(especiaisF[key]) - 1
                linha = fLinha
                
            key = key + 1
        nLetra = nLetra + 1

    return fLinha
    

def pegaDataCommit(logHg):
    log = open(logHg, 'r')

    i = 0
    linha = ''
    data = ''
    
    for linha in log:

        if (linha.find("date(") >= 0):
            data = linha[linha.find("date(")+5:linha.find(" ")]
            log.close()
            data = data[8:10] + '/' + data[5:7] + '/' + data[0:4]
            return data
    
    log.close()


def pegaDescriCommit(logHg):
    log = codecs.open(logHg, "r", "iso8859-1")

    i = 0
    commit = ''
    desc = []
    tempDesc = []
    arqValidos = 0
    

    for commit in log:

        commit = commit.encode('utf-8')

        if (commit.find("files(")>=0):
            arqValidos = validaArqs(commit)
            if arqValidos <= 0:
                for commit in log:
                    if (commit == "\n" or commit == "") :
                        break

        if (commit.find("desc(") >= 0):
            if validaDesc(commit):
                if (commit.find (")$")) >= 0:
                    tempDesc.append('• ' + confereDesc(commit[commit.find("desc(")+5:commit.find(")$")]) + '\\\\ & & \n')
                    tempDesc.append('\n')
                else:
                    tempDesc.append('• ' + confereDesc(commit[commit.find("desc(")+5:]) + '\\\\ & & \n')
                    for commit in log:
                        commit = commit.encode('utf-8')
                        if (commit.find (")$")) < 0:
                            tempDesc.append(confereDesc(commit) + '\\\\ & & \n')
                            tempDesc.append('\n')
                        elif (commit.find (")$")) >= 0:
                            tempDesc.append(confereDesc(commit[:commit.find(")$")]) + '\\\\ & & \n')
                            tempDesc.append('\n')
                            break    

        if (arqValidos > 0 and tempDesc != []):
            desc.extend(tempDesc)
            tempDesc = []
            arqValidos = 0

    log.close()
    repr(desc)
    return desc
  
if __name__ == "__main__":  
    #logHg = sys.argv[1]
    logHg = 'saida.txt'
    #texPCI = sys.argv[2]
    texPCI = 'main.tex'
    #saidaPCI = sys.argv[3]
    saidaPCI = 'DRVCOM.tex'
    #modulo = sys.argv[4]
    modulo = 'DRVCOM'
    #versao = sys.argv[5]
    versao = '6.1.1.21'
    #conferente = sys.argv[6]
    conferente = 'Nome'
    formataDocumento(logHg, texPCI, saidaPCI, modulo, versao, conferente)
    

