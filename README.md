# Ransomware

Este repositório será utilizado para acompanhar meu trabalho final em ciências da computação sobre ransomware.

### Arquivos

#### ransomware.py
- Listagem de arquivos com extensões comuns (pdf, txt, doc, docx, xls)
- Geração de chaves criptográficas
- Criptografia de arquivos
- Criação de notas de resgate

#### Receita.exe

Arquivo python convertido em executável.

```
pyinstaller –onefile ransomware.py -n Receita.exe
```

#### timeExecutable.py

Arquivo que calcula o tempo entre execução e exclusão do arquivo malicioso.

#### timeExtracted.py

Arquivo que calcula o tempo entre extração e exclusão do arquivo malicioso.

### evidences

Esse diretório contém as métricas utilizadas para calcular o consumo dos antimalwares.

O arquivos Analysis.xlsx contém os registros de tempo dessas métricas, como também os tempos de detecção registradas pelo dos scripts.

### e-mail

Contém os arquivos utilizados na seção de phishing do artigo.
