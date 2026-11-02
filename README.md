# Plano de estudo PPComp 2027

Ambiente de estudo pessoal para a seleção do Mestrado Profissional em Computação Aplicada (Ifes Campus Serra, Edital 25/2026, prova em 04/02/2027). Projeto pessoal, sem vínculo com o Ifes.

## O que tem

- `agenda/`: o site estático (abra `agenda/index.html`). Tem as abas Análise da prova, Plano de estudo, Mapa mental, Semanas (14 páginas, 95 dias), Simulados A a E, Inglês, Temas e Técnicas. O progresso fica salvo no `localStorage` do navegador.
- `plano-ppcomp-2027.html`: a análise estratégica completa (edital, provas antigas, previsão de questões). No deploy ela fica em `/plano.html`.
- `gen/`: os geradores em Python que montam o site.

## Regerar o site

```bash
python3 gen/gen.py gen gen/data.json            # 95 dias do plano
python3 gen/sim_gen.py gen gen/sims.json        # banco de simulados A–E
python3 -I gen/verify.py gen/sims.json          # confere os gabaritos (executa o código e as tabelas-verdade)
python3 gen/build.py                            # escreve agenda/
```

## Deploy

O `Dockerfile` serve `agenda/` com nginx na porta 80:

```bash
docker build -t planoestudo . && docker run -p 8080:80 planoestudo
```

Em produção roda atrás do Traefik (rede `coolify`) com `docker compose up -d --build`. Para atualizar o site publicado: `git pull && docker compose up -d --build` na pasta do repositório no servidor.

Livros, provas e o edital ficam fora do repositório, pelo `.gitignore`.
