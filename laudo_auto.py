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
    O = 'óstio'
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


class ImportanciaError(ValueError):
    pass


class PlacaError(ValueError):
    pass


frase = ''


def frase_laudo(arteria, importancia, placa, local, repercussao):
    # Definição dos ramos principais.
    # Diferentemente dos subramos (DG, MG, DP, VP)
    # os ramos principais não deverão possuir o campo importância
    ramos_principais = (Arteria.TCE, Arteria.ADA, Arteria.ACX, Arteria.ACD)

    # Se é um ramo principal a importância não é necessária
    if (arteria in ramos_principais) and importancia != Importancia.SEM:
        raise ImportanciaError('Não é preciso especificar a importância do ramo principal!')
    if (arteria not in ramos_principais) and importancia == Importancia.SEM:
        raise ImportanciaError('Insira a importância do subramo coronariano!')

    # Se tem placa tem que ter redução luminal e o inverso é valido
    if placa != Placa.SEM and local == Local.SEM:
        raise PlacaError(
            'Se tem placa é preciso localizar e determinar a redução luminal!')

    if placa == Placa.SEM and (local != Local.SEM or repercussao != Repercussao.SEM):
        raise PlacaError(
            'Se não tem placa não é preciso localizar e/ou determinar a redução luminal!')

    # Concatenar a frase
    if arteria in ramos_principais:
        if (importancia, placa, local, repercussao) == (
                Importancia.SEM, Placa.SEM, Local.SEM, Repercussao.SEM):
            frase = '{0.value} {1.value}.'.format(arteria, repercussao)
        else:
            frase = '{0.value} com {1.value} no {2.value} determinando {3.value}.'.format(
                arteria, placa, local, repercussao)

    else:
        if (placa, local, repercussao) == (Placa.SEM, Local.SEM, Repercussao.SEM):
            frase = '{0.value} de {1.value} e {2.value}.'.format(
                arteria, importancia, repercussao)
        else:
            frase = '{0.value} de {1.value} e com {2.value} no {3.value} determinando {4.value}.'\
                .format(arteria, importancia, placa, local, repercussao)

    return frase


assert frase_laudo(Arteria.TCE, Importancia.SEM, Placa.PC, Local.SM, Repercussao.RLD) == \
       'Tronco da Coronária Esquerda (TCE) com placa predominantemente calcificada ' \
       'no segmento médio determinando redução luminal discreta.'

assert frase_laudo(Arteria.MG1, Importancia.MI, Placa.PNC, Local.SP, Repercussao.RLI) == \
       'Primeiro Ramo Marginal (MG1) de moderada importância e com placa ' \
       'predominantemente não calcificada no segmento proximal determinando redução luminal importante.'

assert frase_laudo(Arteria.DG1, Importancia.MI, Placa.PC, Local.O, Repercussao.RLI) == \
       'Primeiro Ramo Diagonal (DG1) de moderada importância e com placa predominantemente calcificada ' \
       'no óstio determinando redução luminal importante.'

assert frase_laudo(Arteria.ADA, Importancia.SEM, Placa.SEM, Local.SEM, Repercussao.SEM) == \
       'Artéria Descendente Anterior (ADA) sem redução luminal.'

assert frase_laudo(Arteria.DG1, Importancia.MI, Placa.SEM, Local.SEM, Repercussao.SEM) == \
       'Primeiro Ramo Diagonal (DG1) de moderada importância e sem redução luminal.'
