from enum import Enum

class Arteria(Enum):
    
    TCE = 'Tronco da Coronária Esquerda (TCE)'
    
    RI = 'Ramo Intermédio (RI)'
    
    ADA = 'Artéria Descendente Anterior (ADA)'
    DG = 'Ramo Diagonal (DG)'
    DG1 = 'Primeiro Ramo Diagonal (DG1)'
    DG2 = 'Segundo Ramo Diagonal (DG2)'
    DG3 = 'Terceiro Ramo Diagonal (DG3)'
    DG4 = 'Quarto Ramo Diagonal (DG4)'
    DG5 = 'Quinto Ramo Diagonal (DG5)'
    
    ACX = 'Artéria Circunflexa (ACX)'
    MG = 'Ramo Marginal Esquerdo (MG)'
    MG1 = 'Primeiro Ramo Marginal (MG1)'
    MG2 = 'Segundo Ramo Marginal (MG2)'
    MG3 = 'Terceiro Ramo Marginal (MG3)'
    MG4 = 'Quarto Ramo Marginal (MG4)'
    MG5 = 'Quinto Ramo Marginal (MG5)'
    VPE = 'Ramo Ventricular Posterior (VP), proveniente da CX'
    VPE1 = 'Primeiro Ramo Ventricular Posterior (VPE1), proveniente da CX'
    VPE2 = 'Segundo Ramo Ventricular Posterior (VPE2), proveniente da CX'
    DPE = 'Ramo Descendente Posterior (DP), proveniente da CX'
    DPE1 = 'Primeiro Ramo Descendente Posterior (DPE1), proveniente da CX'
    DPE2 = 'Segundo Ramo Descendente Posterior (DPE2), proveniente da CX'

    ACD = 'Artéria Coronária Direita (ACD)'
    MGD = 'Ramo Marginal Direito (MGD)'
    MGD1 = 'Primeiro Ramo Marginal Direito (MGD1)'
    MGD2 = 'Segundo Ramo Marginal Direito (MGD2)'
    MGD3 = 'Terceiro Ramo Marginal Direito (MGD3)'
    DP = 'Ramo Descendente Posterior (DP), proveniente da CD'
    DP1 = 'Primeiro Ramo Descendente Posterior (DP1), proveniente da CD'
    DP2 = 'Segundo Ramo Descendente Posterior (DP2), proveniente da CD'
    VP = 'Ramo Ventricular Posterior (VP), proveniente da CD'
    VP1 = 'Primeiro Ramo Ventricular Posterior (VP1), proveniente da CD'
    VP2 = 'Segundo Ramo Ventricular Posterior (VP2), proveniente da CD'

class Importancia(Enum):

    SEM = ''
    PI = 'pequena importância'
    MI = 'moderada importância'
    GI = 'grande importância'

class Placa(Enum):

    SEM = ''
    NC = 'placa não calcificada'
    PC = 'placa predominantemente calcificada'
    PNC = 'placa predominantemente não calcificada'

class Local(Enum):

    SEM = ''
    SP = 'segmento proximal'
    SM = 'segmento médio'
    SD = 'segmento distal'

class Repercussao(Enum):

    SEM = 'sem redução luminal'
    RLMIN = 'redução luminal mínima'
    RLD = 'redução luminal discreta'
    RLMOD = 'redução luminal moderada'
    RLI = 'redução luminal importante'
    SUB = 'suboclusão'
    SUBOT = 'suboclusão ou oclusão'
    OT = 'oclusão'

def frase_laudo(arteria, importancia, placa, local, repercussao):

    # Definição dos ramos principais. Diferentemente dos subramos (DG, MG, DP, VP)
    # os ramos principais não deverão possuir o campo importância
    ramos_principais = (Arteria.TCE.value, Arteria.ADA.value, Arteria.ACX.value, Arteria.ACD.value)
    
    arteria = arteria.value
    importancia = importancia.value
    repercussao = repercussao.value
    placa = placa.value
    local = local.value

    # Se é um ramo principal a importância não é necessária
    if arteria in ramos_principais:
        importancia = Importancia.SEM.value
    else:
        if importancia == Importancia.SEM.value:
            raise Exception('Insira a importância do subramo coronariano!')
        else:
            importancia = importancia.value

    # Se tem placa tem que ter redução luminal
    if placa != Placa.SEM.value and repercussao == Repercussao.SEM.value:
        raise Exception('Se tem placa deve ter alguma redução luminal!')

    # Concatenar a frase
    if arteria in ramos_principais:
        if (importancia, placa, local, repercussao) == (
            Importancia.SEM.value, Placa.SEM.value, Local.SEM.value, Repercussao.SEM.value):
                frase_laudo = '{0} {1}.'.format(arteria, repercussao)
        else:
            frase_laudo = '{0} com {1} no {2} determinando {3}.'.format(arteria, placa, local, repercussao)
    
    else:
        if (placa, local, repercussao) == (Placa.SEM.value, Local.SEM.value, Repercussao.SEM.value):
            frase_laudo = '{0} de {1} e {2}.'.format(arteria, importancia, repercussao)
        else:
            frase_laudo = '{0} de {1} e com {2} no {3} determinando {4}.'.format(
                arteria, importancia, placa, local, repercussao)

    return frase_laudo
