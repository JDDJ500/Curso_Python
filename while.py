while True:
    try:
        pare = input("deseja encerrar o programa?\nDigite s = sim | n = não\n")
        if pare == "s":
            break
        else:
            nota1 = float(input("insira a nota do 1° bimestre: \n"))
            if nota1 >= 11  or nota1 <= -1:
                print("nota invalida")
            else:
                nota2 = float(input("insira a nota do 2° bimestre: \n"))
                if nota2 >= 11  or nota2 <= -1:
                    print("nota invalida")
                else:
                    nota3 = float(input("insira a nota do 3° bimestre: \n"))
                    if nota3 >= 11  or nota3 <= -1:
                        print("nota invalida")
                    else:
                        nota4 = float(input("insira a nota do 4° bimestre: \n"))
                        if nota4 >= 11  or nota4 <= -1:
                            print("nota invalida")
                        else:
                            media = (nota1 + nota2 + nota3 + nota4) / 4
                            if media >=5:
                                print(f"Você foi aprovado. Sua media é {media:,.2f}")
                            elif media >=3:
                                print(f"Aluno em recuperação. Sua media é {media:,.2f}")
                            else:
                                print(f"Você foi reprovado. Sua media é {media:,.2f}")
    except:
        print("ERRO, VALOR INVALIDO")
