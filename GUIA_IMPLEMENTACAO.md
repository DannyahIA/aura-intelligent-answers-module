# 🐍 Guia de Implementação: Backend Python para IA Financeira

## Visão Geral

Este é o módulo backend em Python para o sistema de IA financeira da Aura. O módulo processa requisições de assistentes de voz (como Alexa) e gera respostas inteligentes usando múltiplos provedores de IA.

## Características Principais

✅ **Suporte a Múltiplos Provedores de IA**
- Google Gemini
- OpenAI GPT
- Arquitetura modular permite adicionar novos provedores facilmente

✅ **Sistema de Logging Completo**
- Todas as interações são registradas
- Logs estruturados em JSON
- Níveis de log configuráveis

✅ **Configuração Flexível**
- Variáveis de ambiente
- Arquivos de configuração JSON
- Valores padrão sensatos

✅ **Processamento Assíncrono**
- Suporte completo a async/await
- Alta performance e escalabilidade

✅ **Tratamento de Erros Robusto**
- Exceções customizadas
- Fallback entre provedores
- Logs detalhados de erros

## Estrutura do Projeto

```
aura-intelligent-answers-module/
├── src/
│   └── aura_ia/
│       ├── __init__.py           # Módulo principal
│       ├── core/                 # Componentes principais
│       │   ├── __init__.py
│       │   ├── ai_provider.py    # Interface base para provedores
│       │   ├── logger.py         # Sistema de logging
│       │   └── processor.py      # Processador de requisições
│       ├── providers/            # Implementações de provedores
│       │   ├── __init__.py
│       │   ├── gemini_provider.py
│       │   └── gpt_provider.py
│       └── utils/                # Utilitários
│           ├── __init__.py
│           ├── config.py         # Gerenciamento de configuração
│           └── exceptions.py     # Exceções customizadas
├── tests/                        # Testes unitários
├── logs/                         # Logs de interações (criado automaticamente)
├── main.py                       # Ponto de entrada para testes
├── requirements.txt              # Dependências Python
├── .env.example                  # Exemplo de configuração
├── config.example.json           # Exemplo de config JSON
└── README.md                     # Documentação
```

## Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/DannyahIA/aura-intelligent-answers-module.git
cd aura-intelligent-answers-module
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
python -m venv venv

# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar API Keys

#### Opção 1: Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas chaves:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas chaves de API:

```env
GEMINI_API_KEY=sua_chave_aqui
OPENAI_API_KEY=sua_chave_aqui
DEFAULT_AI_PROVIDER=gemini
```

Carregue as variáveis de ambiente:

```bash
# Usando python-dotenv (recomendado)
pip install python-dotenv
```

#### Opção 2: Arquivo de Configuração JSON

```bash
cp config.example.json config.json
```

Edite `config.json` e adicione suas configurações.

## Uso Básico

### 1. Teste Rápido via CLI

```bash
python main.py
```

### 2. Uso Programático

```python
import asyncio
from aura_ia.core.processor import RequestProcessor
from aura_ia.utils.config import Config

async def exemplo():
    # Inicializar processador
    config = Config()  # Usa variáveis de ambiente
    processor = RequestProcessor(config)
    
    # Processar requisição
    resultado = await processor.process_request(
        request="Quais são os melhores investimentos para iniciantes?",
        context={
            "user_type": "investor",
            "expertise_level": "beginner"
        }
    )
    
    # Usar resposta
    if resultado["success"]:
        print(f"Resposta: {resultado['response']}")
    else:
        print(f"Erro: {resultado['error']}")

# Executar
asyncio.run(exemplo())
```

### 3. Com Histórico de Conversa

```python
resultado = await processor.process_request(
    request="E quanto preciso investir?",
    context={"user_type": "investor"},
    conversation_history=[
        {"role": "user", "content": "Quais são os melhores investimentos?"},
        {"role": "assistant", "content": "Para iniciantes, recomendo..."}
    ]
)
```

### 4. Especificar Provedor

```python
# Usar Gemini
resultado = await processor.process_request(
    request="Explique diversificação de portfólio",
    provider_name="gemini"
)

# Usar GPT
resultado = await processor.process_request(
    request="Explique diversificação de portfólio",
    provider_name="gpt"
)
```

## API Reference

### RequestProcessor

Processador principal de requisições.

#### `__init__(config: Optional[Config] = None)`

Inicializa o processador.

#### `async process_request(request: str, context: Optional[Dict] = None, conversation_history: Optional[List] = None, provider_name: Optional[str] = None) -> Dict`

Processa uma requisição e retorna resposta.

**Parâmetros:**
- `request`: String com a pergunta/requisição do usuário
- `context`: Dicionário com contexto adicional (opcional)
- `conversation_history`: Lista com histórico de mensagens (opcional)
- `provider_name`: Nome do provedor específico a usar (opcional)

**Retorna:**
```python
{
    "success": bool,
    "response": str,  # Se success=True
    "error": str,     # Se success=False
    "provider": str,
    "request": str
}
```

#### `get_available_providers() -> List[str]`

Retorna lista de provedores disponíveis.

#### `switch_default_provider(provider_name: str) -> bool`

Altera o provedor padrão.

### Config

Gerenciamento de configuração.

#### `__init__(config_path: Optional[str] = None)`

Inicializa configuração (de arquivo ou ambiente).

#### `get(key: str, default: Any = None) -> Any`

Obtém valor de configuração (suporta notação com pontos).

#### `set(key: str, value: Any) -> None`

Define valor de configuração.

#### `get_provider_config(provider_name: str) -> Dict`

Obtém configuração de um provedor específico.

## Configuração Avançada

### Parâmetros dos Provedores

```python
from aura_ia.core.ai_provider import AIProviderConfig
from aura_ia.providers.gemini_provider import GeminiProvider

config = AIProviderConfig(
    api_key="sua_chave",
    model="gemini-pro",
    temperature=0.7,      # Criatividade (0.0-1.0)
    max_tokens=2048,      # Máximo de tokens na resposta
    additional_params={}  # Parâmetros adicionais
)

provider = GeminiProvider(config)
```

### Níveis de Log

- `DEBUG`: Informações detalhadas para diagnóstico
- `INFO`: Confirmação de que tudo está funcionando
- `WARNING`: Indicação de algo inesperado
- `ERROR`: Erro que impediu alguma funcionalidade
- `CRITICAL`: Erro grave que pode impedir o sistema de funcionar

```python
# Via ambiente
LOG_LEVEL=DEBUG

# Via código
logger = InteractionLogger(log_level="DEBUG")
```

## Adicionando Novos Provedores

1. Crie um novo arquivo em `src/aura_ia/providers/`
2. Implemente a classe herdando de `AIProvider`
3. Implemente os métodos abstratos:
   - `generate_response()`
   - `get_provider_name()`
   - `is_available()`

Exemplo:

```python
from ..core.ai_provider import AIProvider, AIProviderConfig

class NovoProvider(AIProvider):
    def __init__(self, config: AIProviderConfig):
        super().__init__(config)
        # Inicializar cliente
    
    async def generate_response(self, prompt, context=None, conversation_history=None):
        # Implementar geração de resposta
        pass
    
    def get_provider_name(self) -> str:
        return "novo_provider"
    
    def is_available(self) -> bool:
        return True  # Verificar disponibilidade
```

## Integração com Alexa

Para integrar com Alexa, processe as requisições da seguinte forma:

```python
from aura_ia.core.processor import RequestProcessor

processor = RequestProcessor()

async def alexa_handler(event, context):
    # Extrair requisição da Alexa
    user_request = event["request"]["intent"]["slots"]["question"]["value"]
    
    # Processar com Aura IA
    resultado = await processor.process_request(user_request)
    
    # Retornar resposta para Alexa
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": resultado["response"] if resultado["success"] else "Desculpe, ocorreu um erro."
            }
        }
    }
```

## Logs e Monitoramento

Todos os logs são salvos em `logs/interactions.log` (configurável).

### Formato de Log de Interação

```json
{
  "timestamp": "2025-01-15T10:30:00.000000",
  "request": "Qual é a melhor estratégia de investimento?",
  "response": "Para iniciantes, recomendo...",
  "provider": "gemini",
  "metadata": {
    "context": {"user_type": "investor"},
    "has_history": false
  }
}
```

### Formato de Log de Erro

```json
{
  "timestamp": "2025-01-15T10:30:00.000000",
  "error_type": "provider_error",
  "error_message": "API key inválida",
  "details": {
    "provider": "gemini"
  }
}
```

## Testes

Execute os testes unitários:

```bash
pytest tests/
```

Com cobertura:

```bash
pytest --cov=src/aura_ia tests/
```

## Troubleshooting

### Erro: "No AI provider available"

**Causa:** Nenhuma chave de API configurada.

**Solução:** Configure pelo menos uma chave de API (GEMINI_API_KEY ou OPENAI_API_KEY).

### Erro: "Package not installed"

**Causa:** Dependências não instaladas.

**Solução:**
```bash
pip install -r requirements.txt
```

### Provider não funciona

**Verificar:**
1. Chave de API está correta
2. Modelo especificado existe
3. Quota da API não foi excedida
4. Conexão com internet está funcionando

## Performance

- **Latência**: ~1-3 segundos por requisição (dependendo do provedor)
- **Throughput**: Limitado pela API do provedor
- **Memória**: ~50-100MB (variável com histórico de conversa)

## Segurança

⚠️ **IMPORTANTE:**

1. **NUNCA** commite chaves de API no repositório
2. Use variáveis de ambiente ou arquivos de configuração não versionados
3. Adicione `.env` e `config.json` ao `.gitignore`
4. Rotacione chaves regularmente
5. Use diferentes chaves para dev/staging/production

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## Suporte

Para questões e suporte:
- Abra uma issue no GitHub
- Consulte a documentação
- Entre em contato com a equipe

## Roadmap

- [ ] Suporte a mais provedores (Claude, Cohere, etc.)
- [ ] Cache de respostas para otimização
- [ ] Métricas e analytics
- [ ] API REST para integração externa
- [ ] Interface web para testes
- [ ] Suporte a streaming de respostas
- [ ] Fine-tuning de modelos
- [ ] Suporte a multimodalidade (imagens, voz)

## Changelog

### v0.1.0 (2025-01-15)
- ✨ Implementação inicial
- ✅ Suporte a Gemini e GPT
- ✅ Sistema de logging
- ✅ Configuração flexível
- ✅ Processamento assíncrono
- ✅ Documentação completa
