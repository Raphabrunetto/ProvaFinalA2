### O que cada Dockerfile faz

#### 1. Dockerfile da API de Produtos (Node.js)
Vai criar uma imagem para a API de produtos em Node, vai instalar as dependências usando o comando de npm install, expor a porta da API, e vai executar a aplicação com `node index.js`.

#### 2. Dockerfile da API de Pedidos (Python Flask)
Vai criar a imagem para a API de pedidos em Python/Flask, instalar as dependências usando o comando de pip install -r requirements.txt, expor a porta da API, e por fim executar a aplicação Flask.

#### 3. Dockerfile da API de Pagamentos (PHP)
- Vai criar uma imagem para a API de pagamentos em PHP, usar o servidor embutido do PHP, expor a porta da API, e por fim vai executar o servidor PHP.

---

### O que cada elemento do docker-compose.yml faz

- **version:** - Vai Definir a versão do Docker Compose que será usada.
- **services:**  - Vão definir os containers que compõem o sistema, que são:

  - **products-api:** - Container da API de produtos.
  - **orders-api:** - Container da API de pedidos.
  - **payments-api:** - Container da API de pagamentos.
  - **db:** - Container do banco MySQL.
  - **redis:** - Container do Redis.

- **volumes:** - São utilizados para persistir dados do banco e do Redis.
- **networks:** - É o que vai possibilitar a comunicação entre os containers.

---
