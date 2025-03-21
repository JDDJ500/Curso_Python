def validar(x):
    if x >= 11  and x <= -1:
        return "valido"
    else:
        if x <= -1 and x <= -1:
            return "invalido"

def media(a, b, c, d):
    media = (a,b,c,d)
    if media >=5:
        print(f"Você foi aprovado. Sua media é {media:,.2f}")
    elif media >=3:
        print("Aluno em recuperação")
    else:
        print(f"Você foi reprovado. Sua media é {media:,.2f}")

while True:
    try:
        nota1 = float(input("insira a nota do 1° bimestre: \n"))
        if validar(nota1) == "invalido":
            print("nota invalida")
        else:
            nota2 = float(input("insira a nota do 2° bimestre: \n"))
            if validar(nota2) == "invalido":
                print("nota invalida")
            else:
                nota3 = float(input("insira a nota do 3° bimestre: \n"))
                if validar(nota3) == "invalido":
                    print("nota invalida")
                else:
                    nota4 = float(input("insira a nota do 4° bimestre: \n"))
                    if validar(nota4) == "invalido":
                        print("nota invalida")
                    else:
                        media(nota1,nota2,nota3,nota4)


    except:
        print("ERRO, VALOR INVALIDO")