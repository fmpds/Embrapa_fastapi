# Plano de build

Desenvolvimento de API Rest em Python para extração de dados da vinicultura da Embrapa e alimentação de modelo de Machine Learning. 

Primeiro realizamos o fluxo de importação e filtragem dos dados da embrapa e apos isso realizamos a carga dos dados em um banco de dados (Postgresql). Após isso a API consome os dados do banco de dados que depois poderá ser utilizado para alimentar um modelo de machine learning para gerar insights em uma ferramenta de visualização de dados/BI.

![PlanoBuild](https://cdn.discordapp.com/attachments/1220530021802709027/1244829660181823518/arquitetura_embrapa.PNG?ex=66568976&is=665537f6&hm=7519514a235d9444486aa2809e2baa23b93381a7a2b5e50f10fff92a11459212&)