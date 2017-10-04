import sys
import codecs

def formataDocumento(logHg, texPCI, saidaPCI, modulo, versao, conferente):

    i = 0;
    from datetime import date
    hj = date.today()
    hj = hj.strftime("%d/%m/%Y")
    modeloPci = open(texPCI, 'r')
    saida = open(saidaPCI, 'w')


    for linha in modeloPci:

        if   linha.find('VXX/XX/XXXXX') >= 0:
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


def formataDocumentoSemVersao(logHg, texPCI, saidaPCI, modulo, conferente):

    i = 0;
    from datetime import date
    hj = date.today()
    hj = hj.strftime("%d/%m/%Y")
    modeloPci = open(texPCI, 'r')
    saida = open(saidaPCI, 'w')


    for linha in modeloPci:

        if   linha.find('VXX/XX/XXXXX') >= 0:
             saida.write(hj)
        elif linha.find('XXXXXXXX.exe') >= 0:
             saida.write(modulo+'.exe')
        elif linha.find('VX.X.XX.XX') >= 0:
             saida.write(pegaversao(logHg))
        elif linha.find('CXXXXXXXXXX') >= 0:
             saida.write(conferente)
        elif linha.find('PXXXXXXXXXX') >= 0:
             saida.write(pegaNome(logHg))
        elif linha.find('CXX/XX/XXXX') >= 0:
             saida.write(pegaDataCommit(logHg))
        elif linha.find('CX.X.XX.XX') >= 0:
             saida.write(pegaversao(logHg))
        elif linha.find('-XXXXXXXXXX') >= 0:
             saida.writelines(pegaDescriCommit(logHg))
        else:
             saida.write(linha)   

    modeloPci.close()
    saida.close()


def pegaversao(logHg):
    log = open(logHg, 'r')

    i = 0
    linha = ''
    versao = ''

    for linha in log:

        if (linha.find("tags(") >= 0):
            versao = linha[linha.find("tags(")+5:linha.find(")")]
            if (versao.find("[")>=0):
                versao = versao[versao.find("[")+1:versao.find("]")]
            versao = versao.split(".")
            if versao[0].isdigit() and versao[1].isdigit():
                versao = linha[linha.find("tags(")+5:linha.find(")")]
                log.close()
                return versao
        elif (linha.find("desc") >= 0):
            versao = linha[linha.find("desc(")+5:linha.find(")")]
            if (versao.find("[")>=0):
                versao = versao[versao.find("[")+1:versao.find("]")]
                versao = versao.split(".")
                if versao[0].isdigit() and versao[1].isdigit():
                    versao = linha[linha.find("[")+1:linha.find("]")]
                    log.close()
                    return versao
                    
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

    
    if ((linha.find(".c") >= 0) or (linha.find(".h") >= 0)):
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

    linha = linha.lower()
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
    #log = open(logHg, 'r')

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
                print "algo errado na validação de arquivos"
                for commit in log:
                    if (commit == "\n" or commit == "") :
                        break

        if (commit.find("desc(") >= 0):
            if validaDesc(commit):
                if (commit.find (")$")) >= 0:
                    tempDesc.append('-' + confereDesc(commit[commit.find("desc(")+5:commit.find(")$")]) + '\\\\ & & \n')
                    tempDesc.append('\n')
                else:
                    tempDesc.append('-' + confereDesc(commit[commit.find("desc(")+5:]) + '\\\\ & & \n')
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
  
#logHg = 'C:\Users\caio.luzano\Desktop\melhorsaida.txt'
#texPci = 'C:\Users\caio.luzano\Desktop\main.tex'
#saidaPci = 'C:\Users\caio.luzano\Desktop\PCI.tex'
#modulo = "DRVCOM"
#versao = "6.1.2.3"
#conferente = "Susan"

if __name__ == "__main__":  
    logHg = sys.argv[1]
    texPci = sys.argv[2]
    saidaPci = sys.argv[3]
    modulo = sys.argv[4]
    versao = sys.argv[5]
    conferente = sys.argv[6]
    formataDocumento(logHg, texPCI, saidaPCI, modulo, versao, conferente)
    

