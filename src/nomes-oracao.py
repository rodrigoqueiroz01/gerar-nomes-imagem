import random
from PIL import Image, ImageDraw, ImageFont
import os

def esta_em_area_proibida(x, y, area):
    ax1, ay1, ax2, ay2 = area
    return ax1 <= x <= ax2 and ay1 <= y <= ay2

def esta_sobrepondo(x, y, coord_list, largura_texto, altura_texto):
    for (x0, y0, largura, altura) in coord_list:
        if not (x + largura_texto < x0 or x > x0 + largura or y + altura_texto < y0 or y > y0 + altura):
            return True

    return False

def gerar_coordenadas_aleatorias(largura, altura, area_proibida, coord_list, largura_texto, altura_texto):
    while True:
        x = random.randint(0, largura - largura_texto)
        y = random.randint(0, altura - altura_texto)

        if not esta_em_area_proibida(x, y, area_proibida) and not esta_sobrepondo(x, y, coord_list, largura_texto, altura_texto):
            return x, y

def desenhar_nomes(arte, nomes, fonte, cor, area_proibida):
    largura, altura = arte.size
    desenho = ImageDraw.Draw(arte)
    coord_list = []

    for nome in nomes:
        esquerda, superior, direita, inferior = desenho.textbbox((0, 0), nome, font=fonte)
        largura_texto = direita - esquerda
        altura_texto = inferior - superior
        x, y = gerar_coordenadas_aleatorias(largura, altura, area_proibida, coord_list, largura_texto, altura_texto)
        desenho.text((x, y), nome, fill=cor, font=fonte)
        coord_list.append((x, y, largura_texto, altura_texto))

def salvar_arte(arte, output):
    if not output.lower().endswith(('.png', '.jpg', '.jpeg')):
        output = os.path.join(output, 'output.png')

    arte.save(output)
    print(f"Arte com nomes de oração gerada em: {output}")

def preencher_nomes(path, nomes, output):
    arte = Image.open(path)
    largura, altura = arte.size
    fonte = ImageFont.truetype("../utils/fonts/Montserrat/static/Montserrat-Bold.ttf", 50)
    cor = (255, 255, 255)

    area_proibida = (0, altura - 200, largura, altura)
    desenhar_nomes(arte, nomes, fonte, cor, area_proibida)
    salvar_arte(arte, output)

if __name__ == "__main__":
    path = "../utils/images/input/input-test.jpg"

    nomes = [
        "Bone", "Suzi", "Nessie", "Gil", "Marcos", "Dierdre", "Perrine", "Muffin", "Patti", "Kendricks",
        "Janeva", "Jaymee", "Babbette", "Marietta", "Filia", "Harrison", "Georgeanna", "Jammal", "Dorene",
        "Jilly", "Almire", "Babara", "Linus", "Horatia", "Allis", "Jeana", "Axel", "Virginie", "Otes", "Tabina"
    ]

    output = "../utils/images/output/output-test.jpg"
    preencher_nomes(path, nomes, output)
