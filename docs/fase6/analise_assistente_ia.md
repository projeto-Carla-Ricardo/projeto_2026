# Análise Crítica — Eficácia do Assistente IA

## 1. Introdução

O assistente IA do IALO utiliza o modelo **Gemini 3.1 Flash Lite Preview** da Google para fornecer apoio conversacional durante o preenchimento do questionário de diagnóstico. Esta análise avalia a eficácia, limitações e oportunidades de melhoria.

## 2. Funcionalidades Implementadas

| Funcionalidade | Estado | Qualidade |
|----------------|--------|-----------|
| Explicação de conceitos técnicos | ✅ | Alta |
| Contextualização por pergunta | ✅ | Média-Alta |
| Linguagem acessível (sem jargão) | ✅ | Alta |
| Exemplos práticos por setor | ✅ | Média |
| Deteção de contradições | ⚠️ | Básica |
| Sugestão de respostas | ✅ | Média |

## 3. Pontos Fortes

### 3.1 System Prompt Especializado
O system prompt foi cuidadosamente desenhado para contextualizar o modelo como consultor de transformação digital para PME portuguesas, resultando em respostas relevantes e culturalmente adequadas.

### 3.2 Contextualização
O assistente recebe informação sobre a pergunta atual do questionário, permitindo respostas específicas e úteis em vez de genéricas.

### 3.3 Acessibilidade Linguística
O modelo Gemini demonstra boa capacidade de comunicar em português de Portugal com tom acessível, evitando termos técnicos quando possível.

### 3.4 Custo-Eficácia
O modelo `gemini-3.1-flash-lite-preview` oferece um bom equilíbrio entre velocidade de resposta e qualidade, sendo adequado para o caso de uso conversacional.

## 4. Limitações Identificadas

### 4.1 Deteção de Contradições
A capacidade de detetar contradições entre respostas é limitada. O modelo não tem acesso direto ao histórico de todas as respostas anteriores, apenas ao contexto da pergunta atual.

**Melhoria sugerida:** Incluir um resumo das respostas anteriores no contexto enviado ao modelo.

### 4.2 Especificidade Setorial
As respostas podem ser genéricas quando o setor da empresa não é explicitamente mencionado na conversa.

**Melhoria sugerida:** Incluir automaticamente o setor e perfil da empresa no contexto de cada mensagem.

### 4.3 Dependência de Conectividade
O assistente requer ligação à internet e uma API key válida. Em caso de falha, o utilizador fica sem assistência.

**Melhoria sugerida:** Implementar respostas pré-definidas como fallback offline.

### 4.4 Consistência entre Sessões
O histórico de conversação é mantido apenas em memória durante a sessão. Ao reiniciar o servidor, o contexto é perdido.

**Melhoria sugerida:** Persistir o histórico de conversação na base de dados.

### 4.5 Validação de Respostas
O modelo pode ocasionalmente sugerir respostas que não correspondem exatamente às opções disponíveis.

**Melhoria sugerida:** Enviar as opções de resposta ao modelo como parte do contexto.

## 5. Métricas de Avaliação

### 5.1 Critérios de Qualidade

| Critério | Peso | Avaliação |
|----------|------|-----------|
| Relevância da resposta | 30% | ⭐⭐⭐⭐ (4/5) |
| Clareza da linguagem | 25% | ⭐⭐⭐⭐⭐ (5/5) |
| Adequação cultural | 15% | ⭐⭐⭐⭐ (4/5) |
| Tempo de resposta | 15% | ⭐⭐⭐⭐⭐ (5/5) |
| Precisão técnica | 15% | ⭐⭐⭐⭐ (4/5) |
| **Média ponderada** | | **4.3/5** |

### 5.2 Cenários de Teste

| Cenário | Resultado |
|---------|-----------|
| "O que significa maturidade digital?" | ✅ Resposta clara e contextualizada |
| "O que é um ERP?" | ✅ Explicação simples com exemplos |
| "Devo responder 3 ou 4 nesta pergunta?" | ⚠️ Ajuda, mas pode ser vago |
| "Contradição: disse que usa Excel mas agora diz que não usa computador" | ⚠️ Nem sempre deteta |

## 6. Recomendações Futuras

1. **RAG (Retrieval-Augmented Generation)**: Integrar base de conhecimento do Framework IALO para respostas mais precisas
2. **Fine-tuning**: Treinar com dados específicos de PME portuguesas
3. **Feedback loop**: Implementar botões de "útil/não útil" para melhorar continuamente
4. **Multi-modal**: Permitir upload de documentos para análise contextual
5. **Análise de sentimento**: Detetar frustração do utilizador e adaptar o tom

## 7. Conclusão

O assistente IA cumpre o seu objetivo principal de tornar o questionário mais acessível e intuitivo para utilizadores sem formação técnica. A integração com o Gemini é funcional e o custo-benefício é positivo. As limitações identificadas são maioritariamente incrementais e podem ser abordadas em versões futuras.

**Classificação global: 4.3/5 — Bom, com espaço claro para evolução.**
