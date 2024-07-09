import random
from PIL import Image, ImageDraw, ImageFont
import os

def esta_em_area_proibida(x, y, area):
    ax1, ay1, ax2, ay2 = area
    return ax1 <= x <= ax2 and ay1 <= y <= ay2

def esta_sobrepondo(x, y, coord_list, largura_texto, altura_texto, espaco_minimo):
    for (x0, y0, largura, altura) in coord_list:
        if not (x + largura_texto + espaco_minimo < x0 or x > x0 + largura + espaco_minimo or y + altura_texto + espaco_minimo < y0 or y > y0 + altura + espaco_minimo):
            return True

    return False

def gerar_coordenadas_aleatorias(largura, altura, area_proibida, coord_list, largura_texto, altura_texto, margem, espaco_minimo):
    max_tentativas = 1000

    for _ in range(max_tentativas):
        x = random.randint(margem, largura - margem - largura_texto)
        y = random.randint(margem, altura - margem - altura_texto)

        if (not esta_em_area_proibida(x, y, area_proibida)
                and not esta_sobrepondo(x, y, coord_list, largura_texto, altura_texto, espaco_minimo)):
            return x, y

    return None, None

def gerar_coordenadas_em_grade(largura, altura, area_proibida, coord_list, largura_texto,
                               altura_texto, linhas, colunas, margem, espaco_minimo):
    max_tentativas = 1000

    for _ in range(max_tentativas):
        x = random.randint(0, colunas - 1) * (largura // colunas)
        y = random.randint(0, linhas - 1) * (altura // linhas)

        x = max(margem, min(x, largura - margem - largura_texto))
        y = max(margem, min(y, altura - margem - altura_texto))

        if (not esta_em_area_proibida(x, y, area_proibida)
                and not esta_sobrepondo(x, y, coord_list, largura_texto, altura_texto, espaco_minimo)):
            return x, y

    return None, None  # Caso não encontre uma posição válida

def desenhar_nomes(arte, nomes, fonte, cor, area_proibida, margem, espaco_minimo):
    largura, altura = arte.size
    desenho = ImageDraw.Draw(arte)
    coord_list = []

    linhas = int(len(nomes) ** 0.5) + 1
    colunas = linhas

    for nome in nomes:
        esquerda, superior, direita, inferior = desenho.textbbox((0, 0), nome, font=fonte)
        largura_texto = direita - esquerda
        altura_texto = inferior - superior

        x, y = gerar_coordenadas_em_grade(largura, altura, area_proibida, coord_list,
                                          largura_texto, altura_texto, linhas, colunas, margem, espaco_minimo)

        if x is not None and y is not None:
            desenho.text((x, y), nome, fill=cor, font=fonte)
            coord_list.append((x, y, largura_texto, altura_texto))

    for nome in nomes[len(coord_list):]:
        esquerda, superior, direita, inferior = desenho.textbbox((0, 0), nome, font=fonte)
        largura_texto = direita - esquerda
        altura_texto = inferior - superior

        x, y = gerar_coordenadas_aleatorias(largura, altura, area_proibida, coord_list,
                                            largura_texto, altura_texto, margem, espaco_minimo)

        if x is not None and y is not None:
            desenho.text((x, y), nome, fill=cor, font=fonte)
            coord_list.append((x, y, largura_texto, altura_texto))

def salvar_arte(arte, output):
    if not output.lower().endswith(('.png', '.jpg', '.jpeg')):
        output = os.path.join(output, 'output.png')

    arte.save(output)
    print(f"Arte com nomes de oração gerada em: {output}")

def preencher_nomes(input, nomes, output):
    arte = Image.open(input)
    largura, altura = arte.size
    fonte = ImageFont.truetype("../utils/fonts/Montserrat/static/Montserrat-Bold.ttf", 50)
    cor = (255, 255, 255)
    margem = 50
    espaco_minimo = 20

    area_proibida = (0, altura - 200, largura, altura)
    desenhar_nomes(arte, nomes, fonte, cor, area_proibida, margem, espaco_minimo)
    salvar_arte(arte, output)

def ler_nomes_de_arquivo(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        nomes = [line.strip() for line in file.readlines()]

    return nomes

if __name__ == "__main__":
    input = "../utils/images/input/FUNDO_INTERCESSÃO.jpg"
    nomes = ler_nomes_de_arquivo("../utils/nomes.txt")
    output = "../utils/images/output/intercessão.jpg"

    preencher_nomes(input, nomes, output)