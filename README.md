# Serverless-Aws

# Funcionalidades
- Lambda 1 (downloadCSVs): Baixa arquivos CSV de URLs definidas no arquivo links.yml, salva-os no Amazon S3.
- Lambda 2 (processCSV): Processa arquivos CSV do Amazon S3, extrai métricas específicas e salva no banco de dados MySQL.
- Step Function: Orquestra o fluxo de execução das funções Lambda, iniciando pelo download dos CSVs e terminando com o processamento dos dados.

# Instalação
1. Clone o repositório:
> git clone https://github.com/UwUsca/serverless-aws.git
> cd serverless-aws

2. Instale as dependências:
> pip install -r requirements.txt


# Como usar
1. Configure as variáveis de ambiente necessárias:
> export BUCKET_NAME={name}

> export DB_HOST={host}

> export DB_USER={user}

> export DB_PASSWORD={password}

> export DB_NAME={db_name}

2. Deploy das funções Lambda e Step Function utilizando o Serverless Framework:
> serverless deploy

3. Execute a Step Function para iniciar o processamento:
> aws stepfunctions start-execution --state-machine-name processCSVStateMachine --input '{"road_name": "Via Araucaria"}'

4. Acompanhe o progresso e verifique os logs:
> serverless logs --function lambda1 --tail
> serverless logs --function lambda2 --tail

# Estrutura do Projeto
- **lambda1.py:** Código da primeira função Lambda para download e salvamento no S3.
- **lambda2.py:** Código da segunda função Lambda para processamento e salvamento no banco de dados.
- **serverless.yml:** Arquivo de configuração do Serverless Framework para deploy das funções Lambda e Step Function.
- **requirements.txt:** Lista de dependências do projeto.
- **README.md:** Este arquivo de documentação.
