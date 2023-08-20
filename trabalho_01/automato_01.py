import json

def carrega_json(nome_json):
    #carregar o json desejado, que contem o dados do automato
    with open(nome_json, 'r') as f:
        data = json.load(f)

    #transforma o diagrama de estados (delta) de json para dicionário 
    delta_dict = {}
    for transition in data["delta"]:
        estado_atual = transition["estado_atual"]
        simbolo = transition["simbolo"]
        proximo_estado = transition["proximo_estado"]
        delta_dict[(estado_atual, simbolo)] = proximo_estado

    #cria o dfa, que contem todas as variáveis
    dfa = [data["estados"], data["sigma"], delta_dict, data["estado_inicial"], data["estados_finais"]]
    return dfa

def simular_dfa(dfa, entrada):

    #assinala as variáveis do dfa
    Q = dfa[0]
    Sigma = dfa[1]
    delta =  dfa[2]
    q0 = dfa[3]
    F = dfa[4]
    posicao = q0  
    
    entrada_inalterada = entrada
    flag = True

    while flag == True:
        #consome primeiro caracter da "entrada" e armazena-o em "proximo_char"
        proximo_char = entrada[0]
        entrada = entrada[1:]  

        #primeiro tratamento de erro paracaso o char removido não esteja no conjunto.
        if proximo_char not in Sigma:
            print(f"{proximo_char} não pertence ao alfabeto do autômato!\n")
            entrada = proximo_char + entrada
            flag = False
            break
        #segundo tratamento de erro: se o estado pertence ao conjunto de estados do autônomo
        elif posicao not in Q:
            
            print(f"O estado {posicao} não pertence ao conjunto de estados do autômato!")
            flag = False
            break
        #terceiro tratamento de erro: verifica se é possível realizar a transação
        elif (posicao, proximo_char) not in delta:
            print(f"Não foi possível realizar a transição do estado {posicao} com entrada '{proximo_char}'")
            flag = False
            break
        
        #quarto tratamento de erro: verifica se a entrada foi completamente consumida 
        elif len(entrada) == 0 and flag:
            posicao = delta[(posicao, proximo_char)]
            flag= False
            break
        #caso a entrada não tenha sido inteiramente consumida, ele atualiza a posição atual e a anterior
        else:
            posicao_anterior = posicao
            posicao = delta[(posicao, proximo_char)]
        print(f"({posicao_anterior}, {proximo_char}) - > {posicao}")

    #verifica se houve sucesso ou não, verificando se o vértice onde foi finalizado era pertencente ao conjunto dos estados finais
    if posicao in F:
        print(f"\nposicao sendo considerada: {posicao}")
        print('\nA cadeia', entrada_inalterada , 'foi aceita pelo autômato!\n\n\n---------------------------')
    else:
        print('\nA cadeia', entrada_inalterada , 'foi rejeitada pelo autômato!\n\n\n-----------------------')


def main():
    nome_json = input("digite o nome do json que gostaria de usar: ")
    nome_json = "trabalho_01/dados/"+nome_json+".json"
    dfa = carrega_json(nome_json)

    #aqui, fora do while loop, o programa aguarda por novas cadeias. Caso hava um ctrl+C ou qualquer atalho para cancelamento do terminal, o programa é finalizado com uma menasgem de erro específica
    try:
        while True:
            entrada = input("Digite a cadeia: ")
                
            simular_dfa(dfa, entrada)
    except KeyboardInterrupt:
        print("\nPrograma finalizado pelo usuário!")


    
if __name__ == "__main__":
    main()
