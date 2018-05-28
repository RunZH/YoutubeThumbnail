from datetime import datetime
import urllib3

def verificar_url():
    global endereco
    url = ""
    while url == "":
        url = input("Insira o endereço: ")
        url = url.rstrip(" ")
        endereco = url.split("watch?v=")
        if endereco[0] != 'https://www.youtube.com/':
            print("Endereço incorreto. Tente novamente.")
            url = ""
    return True


def definir_thumbnails():
    codigo_video = endereco[1]
    url_imagem = "https://img.youtube.com/vi/" + codigo_video
    mq  = url_imagem + "/mqdefault.jpg"
    hq  = url_imagem + "/hqdefault.jpg"
    sd  = url_imagem + "/sddefault.jpg"
    max = url_imagem + "/maxresdefault.jpg"

    return [mq, hq, sd, max]


def arquivo_existe(pedido):
    resposta = pedido.status
    if resposta == 200:
        return True
    else:
        return False


def salvar_arquivos(thumbnails):
    i = 3
    existe_arquivo = False

    while not existe_arquivo and i > 0:
        http = urllib3.PoolManager()
        pedido = http.request('GET', thumbnails[i])

        if arquivo_existe(pedido):
            hora = registrar_hora()
            nome = str(hora) + "-" + str(i) + ".jpg"
            arquivo_local = open(nome, 'w+b')
            arquivo_local.write(pedido.data)
            arquivo_local.close()
            existe_arquivo = True

        http.clear()
        i -= 1


def registrar_hora():
    agora = datetime.now()
    hora = int(agora.timestamp())
    return hora


def main():
    if (verificar_url()):
        thumbnails = definir_thumbnails()
        salvar_arquivos(thumbnails)
        print("Concluído.")


if __name__ == '__main__':
    main()