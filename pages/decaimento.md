Decaimentos radioativos seguem uma equação diferencial onde a quantidade de decaimentos
em um intervalo de tempo, $N$, depende de uma constante de decaimento exponencial,
$\lambda$, conforme a equação

$$\dfrac{dN}{dt} = - \lambda N$$

A solução dessa equação diferencial é

$$N(t) = N_0 \text{e}^{-\lambda t}$$

onde $N(t)$ é o decaimento no tempo $t$ e $N_0 = N(0)$.

Por vezes, a equação é descrita em função de outra constante, a 
*constante de tempo exponencial*, $\tau$, que é definida como 
$\tau = \frac{1}{\lambda}$.

Dessa forma, a equação pode ser reescrita como

$$N(t) = N_0 \text{e}^{-\frac{t}{\tau}}$$

Uma forma útil de de estudar decaimentos exponenciais é avaliando o tempo que a amostra 
leva para decair à metade da quantidade inicial. Esse tempo é chamado 
*tempo de meia-vida* e usualmente é denotado com o símbolo $t_{1/2}$. 
O tempo de meia-vida se relaciona com a constante $\lambda$ e com a constante $\tau$ de 
acordo com a equação

$$t_{1/2} = \dfrac{\ln(2)}{\lambda} = \tau \ln(2)$$

Da literatura, o tempo de meia-vida do fósforo-32 é 14,29 dias, de forma que 
se pode construir um gráfico do perfil de decaimento teórico de uma amostra de tal 
isótopo e compará-lo com os dados de um experimento, como os 
presentes na tabela (data frame).

Uma análise visual do gráfico até permite a determinação do tempo de meia-vida. 
No entanto, se o gráfico fosse uma reta, seria mais fácil. A equação 
pode ser linearizada aplicando-se $\ln$ em ambos os lados da equação, obtendo-se

$$\ln(N(t)) = \ln(N_0) - \dfrac{t}{\tau}$$

Ao fazer a operação de logaritmo nos dados, não se pode esquecer de realizar a 
propagação de erros adequada. O coeficiente angular da reta obtido pela regressão 
linear dos dados experimentais fornecidos foi de $-0,048 \pm 0,001$. 
Como o coeficiente angular corresponde a $-1/\tau$, temos que $\tau = 20,5 \pm 0,5$. 
Logo, o tempo de meia-vida obtido pelos dados experimentais é de 
$t_{1/2} = 14,2 \pm 0,3 \text{ dias}$. Uma boa correspondência com o valor de 14,29 
dias reportado na literatura.
