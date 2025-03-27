# Flask API Melhorada

Este projeto é uma API desenvolvida com Flask, seguindo boas práticas de desenvolvimento, separação de camadas e implementação de autenticação JWT.

## Melhorias Implementadas

### 1. Boas Práticas de Desenvolvimento
- Uso de **funções dedicadas** para conexão e criação de tabelas no banco de dados.
- Implementação de **tratamento de erros** e validação de entrada.
- Utilização de **decoradores** para autenticação e reutilização de código.
- Código modularizado para melhor organização e manutenção.

### 2. Separação de Camadas
- Criamos funções específicas para lidar com a camada de **banco de dados**, separando-a da lógica de negócio.
- Agora, a API possui **módulos organizados**, facilitando a expansão e o gerenciamento do código.

### 3. Autenticação com JWT
- Implementação de **JSON Web Token (JWT)** para garantir acesso seguro à API.
- Apenas usuários autenticados podem acessar as rotas protegidas.
- Rota `/login` para autenticação, que gera um token válido por tempo determinado.
- Uso de **headers HTTP** para envio do token nas requisições.

## Como Usar

### 1. Instalação
```sh
pip install flask 
```

### 2. Executar a API
```sh
python main.py
```

### 3. Autenticação e Uso
1. Criar um usuário no banco de dados.
2. Fazer login via POST `/login` para obter o token JWT.
3. Utilizar o token nas requisições para acessar `/data`.

## Contribuição
Gustavo Rampanelli - RA 1135697

