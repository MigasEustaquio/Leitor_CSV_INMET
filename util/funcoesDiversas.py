def calculaHSP(vertices):

    area_grafico=0

    for i in range(len(vertices)-1):
        area_grafico+=(vertices[i]+vertices[i+1])/2

    HSP=area_grafico/1000

    tamanho_horizontal_grafico = HSP/2

    return [12-tamanho_horizontal_grafico, HSP, 12-tamanho_horizontal_grafico]
