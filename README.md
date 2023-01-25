# PROJETO DEVNOLOGY

## Sobre.
-  **Este projeto é uma api onde replica os dados de produtos raspados de um site via Webscraping.**
**O usuário tem que estar logado e com acesso liberado via TOKEN (este token é criado pelo admin do sistema dentro do ADM do Django) para ter acesso a api, e na requisição terá que enviar o TOKEN no header, como mostrado na imagem abaixo**

<img src='media/project_img/request_token.png' width='400px'><br>

- Foi desenvolvido a conexão com Cache Redis, que tem por sua vez a funcionalidade de armazenar a primeira requisição feita pelo usuário, para que nas proximas buscas dentro de 10 minutos, a api não precise fazer o Scrapy novamente, assim economizando memoria e tempo.

- A api retorna os mesmo dados em Json tanto nas raspagens de dados quanto nos dados retornados pelo Cache Redis

- Foi desenvolvido a conexão com AWS Dynamodb, para armazenar os dados a cada nova cada nova consulta após os 10 minutos, foi criado com a funcionalidade de alguma necessidade para obter os dados futuramente sem ser utilizando o Redis.

- Fazer busca pelo preço do produto:
~~~shel
http://127.0.0.1:8000/api/v1/product?price=2999
~~~

- Fazer busca pela marca e modelo do produto:
~~~shel
http://127.0.0.1:8000/api/v1/product?product=lenovo
~~~