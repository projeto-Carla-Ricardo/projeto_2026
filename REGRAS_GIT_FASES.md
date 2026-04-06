# Regras de Versionamento por Fases (Instruções para a IA)

Para além do versionamento em Git, o projeto utiliza um sistema de backups/snapshots por pastas para facilitar a avaliação do progresso por parte do professor.

## Regras Ativas:

1. **Desenvolvimento Central:** Todo o desenvolvimento do código será sempre efetuado na raiz do projeto (`PROJETO_2026`).
2. **Estrutura de Pastas de Fases:** Existem 6 pastas criadas na raiz do projeto (`Fase 1`, `Fase 2`, `Fase 3`, `Fase 4`, `Fase 5`, `Fase 6`).
3. **Cópia Cumulativa:** Sempre que todas as tarefas de uma determinada Fase no "Índice de desenvolvimento" do `README.md` forem dadas como concluídas, a IA deve fazer uma **cópia de todo o estado funcional autual da aplicação** (excluindo as próprias pastas `Fase X` e diretórios `.git`, `node_modules`, ambientes virtuais como `.venv`, etc.) para a pasta da Fase correspondente.
4. **Acumulação de Progresso:** O projeto numa fase posterior tem tudo o que foi construído nas fases anteriores.
    *   Exemplo: Se a Fase 2 estiver acabada, a pasta `Fase 2` vai conter o estado final da raiz. A pasta `Fase 2` terá, assim, a implementação correspondente às Fases 1 e 2. O mesmo vale para as seguintes.

> **Ação Periódica Exigida à IA:** Ao ver num prompt que uma fase do projeto foi dada como concluída, ou quando terminar por si, deve fazer um copia para a pasta da fase correspondente e alertar o utilizador. Apenas essa pastas irão ser enviadas para o github para avaliação periodica do professor. 
