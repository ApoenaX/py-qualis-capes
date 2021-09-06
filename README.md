# py-qualis-capes

Um pacote python que permite recuperar informações sobre qualis-periódicos da Plataforma Sucupira.

## Qualis-Periódicos

Na [Plataforma Sucupira](https://sucupira.capes.gov.br/), atualmente as informações de Qualis-Periódicos se referem as classificações das revistas do Triênio 2010-2012 e Quadriênio 2013-2016. Segundo informações contidas na própria Plataforma há previsão da publicação de uma nova versão com estratos atualizados até a próxima Avaliação Quadrienal em 2021.

## Como usar

É possível realizar o download dos dados ao usar as instruções a seguir, mas não é necessário, pois a biblioteca já possui os dados baixados.


```python
from qualis_capes import QualisCapes

qualis = QualisCapes()

# Obter a data de quando as tabelas foram baixadas
print(qualis.get_last_update())
#>'02/09/2021 12:34:56'

# Atualizar dados
qualis.update_data()
#>'03/09/2021 21:23:30'

```

É possível obter a tabela contendo todas as revistas por triênio ou quadriênio.

> O argumento `event` aceita apenas as palavras `triênio` e `quadriênio`, por padrão é preenchido como `quadriênio`.

```python
from qualis_capes import QualisCapes

qualis = QualisCapes()
trien = qualis.get_table(event="triênio")
#>>> trien.head()
#        ISSN                                            Título                                  Área de Avaliação Estrato
#0  0102-6720  ABCD. Arquivos Brasileiros de Cirurgia Digestiva  ADMINISTRAÇÃO, CIÊNCIAS CONTÁBEIS E TURISMO   ...      B1
#1  1980-4814                       ABCustos (São Leopoldo, RS)  ADMINISTRAÇÃO, CIÊNCIAS CONTÁBEIS E TURISMO   ...      B4
#2  1516-618X                                    ABMES Cadernos  ADMINISTRAÇÃO, CIÊNCIAS CONTÁBEIS E TURISMO   ...      B5
#3  1012-8255                                Academia (Caracas)  ADMINISTRAÇÃO, CIÊNCIAS CONTÁBEIS E TURISMO   ...      B1
#4  2048-9803         Academic Publishing International Limited  ADMINISTRAÇÃO, CIÊNCIAS CONTÁBEIS E TURISMO   ...      B4
```

As consultas ainda podem ser filtradas de acordo com a área, ISSN, estrato e título da revista.

```python
from qualis_capes import QualisCapes

qualis = QualisCapes()
comp = qualis.by_area("computaç", "triênio")

#>>> comp.head()
#            ISSN                 Título                                  Área de Avaliação Estrato
#12709  2316-9451                 Abakós  CIÊNCIA DA COMPUTAÇÃO                         ...      C 
#12710  1076-6332     Academic Radiology  CIÊNCIA DA COMPUTAÇÃO                         ...      B2
#12711  1519-7859        Ação Ergonômica  CIÊNCIA DA COMPUTAÇÃO                         ...      C 
#12712  0360-0300  ACM Computing Surveys  CIÊNCIA DA COMPUTAÇÃO                         ...      A1
#12713  2153-2184            ACM Inroads  CIÊNCIA DA COMPUTAÇÃO                         ...      B4
```

## Informações

A presente biblioteca tem como propósito permitir o acesso às informações das revistas e suas respectivas avaliações via interface de linha de comando (CLI). Desse modo, permitindo o desenvolvimento de possíveis aplicações, estudos que façam uso dessas informações.

O dados utilizados são obtidos através de *web scraping* realizado na página de Qualis-Periódicos da Plataforma Sucupira. 