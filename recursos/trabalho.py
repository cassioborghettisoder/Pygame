def calcular_nivel(pontos):
    if pontos < 3:
        return "Iniciante"
    elif pontos < 6:
        return "Intermediario"
    elif pontos < 10:
        return "Avancado"
    else:
        return "Lendario"