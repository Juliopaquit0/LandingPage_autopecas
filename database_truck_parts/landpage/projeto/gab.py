cadastro = False
base = False 

print("1 - fazer cadastro")
print("2 - sair")
gb = input("")


if gb == "1":
        while cadastro == False:
            nome = input("Digite seu nome: ")
            email = input("Digite seu email: ")
            senha = input("Digite sua senha: ")
            cadastro = True
            print("Cadastro realizado com sucesso!")
    

if gb == "2":
        print("Saindo do cadastro...")
        

if gb == "1" and cadastro == True:
        print("Cadastro ja realizado,usuario", nome, "!")
        # Aqui você pode adicionar a lógica para redirecionar o usuário para a página principal do site
