ULTRA AI COMPLETO - INSTALACAO WINDOWS

REQUISITOS
- Windows 10 ou 11
- 8 GB RAM: use o modelo leve qwen2.5:1.5b
- Ollama instalado
- Python 3 instalado (marque "Add Python to PATH" durante a instalacao)
- Internet necessaria para baixar o Ollama e o modelo. Depois, o chat local funciona sem creditos de API.

PASSO 1 - INSTALAR O OLLAMA
1. Abra a pasta ULTRA_AI_COMPLETO.
2. Clique duas vezes em instalar_ollama.bat.
3. Na pagina oficial, baixe e instale Ollama para Windows.
4. Abra o aplicativo Ollama pelo menu Iniciar.
5. Deixe-o rodando.

PASSO 2 - BAIXAR A IA
1. Volte para esta pasta.
2. Clique duas vezes em baixar_modelo.bat.
3. Espere o download terminar. O modelo qwen2.5:1.5b e relativamente leve.
4. Se o comando 'ollama' nao for reconhecido, feche e abra o terminal ou reinicie o Windows.

PASSO 3 - INSTALAR PYTHON
1. Se ainda nao tiver Python, abra https://www.python.org/downloads/windows/
2. Baixe Python 3 para Windows.
3. Na primeira tela do instalador, marque "Add Python to PATH".
4. Conclua a instalacao.

PASSO 4 - ABRIR O ULTRA AI
1. Clique duas vezes em iniciar.bat.
2. Uma janela preta vai ficar aberta; nao feche enquanto usar o robo.
3. O navegador abre em http://localhost:8000.
4. Use "Conversar com IA" para conversar.
5. Use "Criar aplicativo" para gerar um pequeno app web.

COMO USAR O CRIADOR
Exemplo de pedido:
"Crie um aplicativo de controle financeiro pessoal com campos para descricao, valor e categoria, total mensal e botao para excluir lancamentos. Salve os dados no navegador."

Os arquivos serao salvos dentro da pasta projects.
Clique em "Abrir previa do aplicativo" para testar.

SOLUCAO DE PROBLEMAS
- Erro de conexao Ollama: abra o aplicativo Ollama e teste no Prompt de Comando: ollama list
- Modelo ausente: execute baixar_modelo.bat novamente.
- Porta 8000 ocupada: feche outro programa que esteja usando essa porta.
- Python nao encontrado: reinstale Python marcando Add Python to PATH.
- Geracao lenta: feche programas pesados. O PC com 8 GB de RAM tem limites; mantenha prompts simples.

IMPORTANTE
- O ULTRA AI usa modelo local; nao consome creditos de API.
- "Gratuito" nao significa ilimitado: depende da memoria, velocidade e energia do computador.
- A versao inicial cria aplicativos web simples com HTML/CSS/JS. Nao cria automaticamente APK/EXE nem publica apps na internet.
- Revise e teste os arquivos gerados antes de usar ou publicar.
- Por seguranca, nao exponha o servidor local na internet.
