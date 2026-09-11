# Conjuntos de dados didáticos

## Palmer Penguins

Conjunto de dados utilizado nas aulas.

Os arquivos locais foram obtidos do pacote Python `palmerpenguins` 0.1.6, que distribui os dados publicados pelo projeto [Palmer Station LTER](https://allisonhorst.github.io/palmerpenguins/).

- `raw/penguins_raw.csv`: versão bruta, com 344 registros e 17 colunas, utilizada para organização e pré-processamento básico.
- `processed/penguins.csv`: versão organizada, com 344 registros e oito colunas, utilizada nas análises estatísticas subsequentes.

Referência dos dados:

> GORMAN, Kristen B.; WILLIAMS, Tony D.; FRASER, William R. Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins (genus *Pygoscelis*). *PLoS ONE*, v. 9, n. 3, e90081, 2014.

Licença e condições de uso devem ser consultadas na página oficial do projeto.

## Ames Housing

Base utilizada nas avaliações práticas AP1, AP2 e AP3. Reúne vendas de imóveis residenciais em Ames, Iowa, entre 2006 e 2010, com informações provenientes do órgão municipal de avaliação imobiliária e organizadas por Dean De Cock.

- [raw/AmesHousing.txt](raw/AmesHousing.txt): dados brutos, com 2.930 observações e 82 colunas, incluindo os identificadores `Order` e `PID`. Cada observação corresponde à venda de um imóvel.
- [raw/DataDocumentation.txt](raw/DataDocumentation.txt): dicionário com descrições das variáveis, categorias e códigos.

Os arquivos foram obtidos do acervo do *Journal of Statistics Education* e preservados sem alterações:

- [Dados originais](https://jse.amstat.org/v19n3/decock/AmesHousing.txt).
- [Documentação original](https://jse.amstat.org/v19n3/decock/DataDocumentation.txt).

O arquivo de dados usa tabulação como separador. Consulte o dicionário antes de interpretar códigos e valores ausentes, pois `NA` pode representar a ausência de uma característica do imóvel. Preserve os arquivos em `raw/` e registre as decisões de tratamento no notebook da AP1. O arquivo `processed/AmesHousing.csv` será produzido pelos estudantes nessa etapa e utilizado nas AP2 e AP3.

Referência dos dados:

> DE COCK, Dean. Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project. *Journal of Statistics Education*, v. 19, n. 3, 2011. DOI: [10.1080/10691898.2011.11889627](https://doi.org/10.1080/10691898.2011.11889627).

O [artigo de referência](../artigos/cock2011.pdf) está disponível no repositório.
