# 01 — HTTPX PR #3442

## Caso

Reprodução e comparação de uma correção do projeto open source HTTPX relacionada à configuração SSL/TLS quando `verify=False` é utilizado junto com um certificado de cliente (`cert`).

- Projeto: `encode/httpx`
- Issue relacionada: `#3441`
- Pull Request oficial: `#3442` — `Fix verify=False, cert=... case.`
- Commit funcional oficial: `b1c39523ae3b5d6a3b8c3e49b0feca21242db2c9`
- Merge commit: `89599a9`

## Resultado resumido

A investigação identificou um `return` antecipado no ramo `verify=False` de `create_ssl_context`. Esse retorno impedia que o fluxo alcançasse o bloco responsável por carregar o certificado de cliente.

A solução produzida removeu esse retorno antecipado e adicionou um teste de regressão. A solução oficial realizou a mesma correção funcional no código de produção, mas atualizou o changelog em vez de adicionar teste nessa PR.

Classificação final: **CORRETO, MAS DIFERENTE**.

## Arquivos

- `AGENT_DIARY.md` — investigação completa, testes e comparação.
- `diffs/AGENT_SOLUTION.diff` — patch produzido para o exercício.
- `diffs/OFFICIAL_PR3442.diff` — patch oficial usado na comparação.
- `evidencias/httpx/_config.py` — arquivo de produção após a correção.
- `evidencias/tests/test_config.py` — arquivo de testes contendo o teste de regressão adicionado.

## Resultado de teste registrado

```text
Antes: 1 failed
Depois: 1 passed
```

A suíte completa não foi executada no ambiente utilizado por falta das dependências de desenvolvimento `trustme` e `trio` e indisponibilidade de rede para instalá-las.

## Observação metodológica

O material recebido para esta execução não continha o histórico `.git` e já possuía a forma corrigida de `create_ssl_context`. Para documentar o exercício, o estado defeituoso anterior à correção foi reconstruído a partir do diff oficial da PR. Essa limitação está registrada também no diário para manter rastreabilidade.
