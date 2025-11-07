# IASX-SCADA-DANA

Sistema de monitoramento para prensas de forjaria automotiva com integração CLP Siemens S7-1200.

## Visão Geral
- Interface gráfica moderna desenvolvida com CustomTkinter
- Comunicação PROFINET (S7-ISO-on-TCP) via biblioteca snap7
- Monitoramento contínuo 24/7
- Armazenamento de dados em MariaDB
- Visualização em tempo real para TV 50"
- Exportação de dados históricos em CSV

## Requisitos
- Python 3.8+
- CustomTkinter
- python-snap7
- mariadb
- pandas

## Estrutura
- `/src`: Código fonte principal
  - `/interfaces`: Interfaces gráficas (Monitor e Histórico)
  - `/database`: Gerenciamento do banco de dados
  - `/communication`: Comunicação com CLP
- `/assets`: Recursos gráficos
- `/config`: Arquivos de configuração

## Instalação
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure o banco de dados MariaDB
4. Execute: `python main.py`