""" ESTA LISTA SE ORDENA PARA QUE SALGA DE PRIMERAS EL DESTINATARIO ESCOGIDO AL EDITAR """

def ordenar(destinatarios,ID):
    # recorrer lsta
    print(destinatarios)
    print(ID)
    iterador=0
    lista=[]
    numero_destinatarios=len(destinatarios)

    while iterador<numero_destinatarios:
        destino= destinatarios[iterador]
            
        if  (int(ID) in destino):
            lista.insert(0,destino) # inserta el destino de  primero en la lista para que se vea de  primero en el html porque es la persona a la que se le envió el mensaje
        else:
            lista.append(destino)
    
        iterador+=1

    return lista 