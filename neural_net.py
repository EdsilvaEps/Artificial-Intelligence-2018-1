import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.contrib.layers import fully_connected
from math import floor, ceil
from pylab import rcParams
from time import gmtime, strftime


# quantidade de exemplos que serão usados para treino
tam_treino = 0.9

# abaixo vamos carregar nossos dados
cl_positivas = pd.read_csv("trabFinal/dataset_ia_positivos_2.csv", sep=",")
cl_negativas = pd.read_csv("trabFinal/dataset_ia_negativos_2.csv", sep=",")

# juntando todos os nossos exemplos
exemplos = cl_positivas.append(cl_negativas)

# misturando os exemplos pq queremos ver exemplos positivos e negativos
# na saida
exemplos = exemplos.sample(frac=1).reset_index(drop=True)

# função para codificar nossos exemplos e labels em vetores "one-hot"
def encode(series):
    return  pd.get_dummies(series.astype(str))

exemplos_xplain = exemplos.drop('hd(X)',1)
exemplos_y = encode(exemplos['hd(X)'])

# separando nosso dataset em dados de treino e dados de teste
cnt_treino = floor(exemplos_xplain.shape[0] * tam_treino)
x_treino = exemplos_xplain.iloc[0:cnt_treino].values
y_treino = exemplos_y.iloc[0:cnt_treino].values
x_teste =  exemplos_xplain.iloc[cnt_treino:].values
y_teste = exemplos_y.iloc[cnt_treino:].values

# problemas com os tamanhos dos arrays
print(x_teste.shape)
print(y_teste.shape)

# comparando com um dataset conhecido
#tx,ty = mnist.train.next_batch(1)
#print(ty.shape)
#print(tx.shape)



################################################################
# camada 1 tem 1 neuron pra cada feature
neurons_camada_1 = x_treino.shape[1]
# camada 2 tem 1 neuron pra cada clausula
neurons_camada_2 = exemplos.shape[0]
neurons_saida = 2
taxa_aprendizado = 0.01

X = tf.placeholder(tf.float32, shape=(None, neurons_camada_1), name="X")
y = tf.placeholder(tf.int64,shape=(None,2), name="y")


# a rede neural é criada com os seguintes argumentos:
with tf.name_scope("rede_neural"):
    camada_1 = fully_connected(X, neurons_camada_1, scope="camada_1")
    camada_2 = fully_connected(camada_1, neurons_camada_2, scope="camada_2")
    saida = fully_connected(camada_2, neurons_saida, scope="saida", activation_fn=None)

################################################################
# computando o backprop na função de custo
with tf.name_scope("funcao_de_custo"):

    y_float = tf.cast(y, tf.float32)
    sigmoidtropy = tf.nn.sigmoid_cross_entropy_with_logits(
        labels=y_float, logits=saida)
    custo = tf.reduce_mean(sigmoidtropy, name="custo")


# configurando as operações de treino
with tf.name_scope("treino"):
    otimizador = tf.train.GradientDescentOptimizer(taxa_aprendizado)
    op_treino = otimizador.minimize(custo)



################################################################
# avaliando a eficiencia da rede
print(saida.shape)
print(y[1].shape)
#with tf.name_scope("eval"):
#    correto = tf.nn.in_top_k(saida, y[1], 1)
#    eficacia = tf.reduce_mean(tf.cast(correto, tf.float32))

with tf.name_scope("eval"):
    previsao_correta = tf.equal(tf.argmax(saida,1), tf.argmax(y,1))
    eficiencia = tf.reduce_mean(tf.cast(previsao_correta, "float"))


################################################################
init = tf.global_variables_initializer()
saver = tf.train.Saver()

n_epocas = 15
tam_particao = 1 # usaremos gradient descent estocástico, pois temos poucos exemplos para treinar
saver_path = "./trabFinal/output/" + strftime("%d-%m-%Y-%H:%M:%S/model", gmtime())
mostrar_dados = 1

with tf.Session() as sess:
    init.run()
    for epoca in range(n_epocas):
        particao_total = int(len(x_treino) / tam_particao)
        x_parts = np.array_split(x_treino, particao_total)
        y_parts = np.array_split(y_treino, particao_total)
        for i in range(particao_total):
            part_x, part_y = x_parts[i], y_parts[i]
            sess.run(op_treino,feed_dict={X: part_x, y: part_y})
            acc_treino = eficiencia.eval(feed_dict={X: part_x, y: part_y})
            acc_teste = eficiencia.eval(feed_dict={X: x_teste, y: y_teste})
        if epoca % mostrar_dados == 0:
            print(epoca," - Eficiencia do treino: " ,acc_treino, " - Eficiencia do teste:" ,acc_teste)
    print("otimização completa!\n")
    #save_path = saver.save(sess, saver_path)
    x_t = np.array_split(x_teste, 5)
    y_t = np.array_split(y_teste, 5)
    for k in range(5):
            x_t2, y_t2 = x_t[k], y_t[k]
            predicao = ''
            label = ''
            print("Entrada: ", x_t2)
            #print(x_teste[k].shape)
            #x = tf.placeholder(tf.float32, shape=(1, 12), name="X")
            if (y_t2.item(0) == 1): label = 'hd(X) falso'
            elif(y_t2.item(1) == 1): label = 'hd(X) verdadeiro'
            pred = saida.eval(feed_dict={X:x_t2})
            if (pred.item(0) > pred.item(1)): predicao = 'hd(X) falso'
            elif(pred.item(1) > pred.item(0)): predicao = 'hd(X) verdadeiro'
            print("Saída da rede: ", saida.eval(feed_dict={X:x_t2}), " - Label: ", y_t2)
            print("Predicao: ", predicao, " - Label: ", label,"\n")


    #previsao_correta = tf.equal(tf.argmax(saida,1), tf.argmax(y,1))
    #eficiencia = tf.reduce_mean(tf.cast(previsao_correta, "float"))
    #print("eficiencia: ", eficiencia.eval({X: x_teste, y: y_teste}))
