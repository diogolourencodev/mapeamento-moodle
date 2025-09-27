## 📌 Visão Geral

Este script realiza login automático no Moodle da **Universidade de Vassouras** e percorre perfis de usuários a partir de um intervalo de IDs, coletando nomes válidos.
Os dados extraídos são armazenados em arquivos locais (`usuarios.json` e `invalidos.txt`) para evitar repetição de consultas.

---

## ⚙️ Pré-requisitos

Antes de executar, garanta que possui:

* **Python 3.8+**
* As bibliotecas:

  ```bash
  pip install requests beautifulsoup4
  ```
* Arquivo `usuarios.json` no diretório raiz (pode ser vazio, ex: `{}`).

---

## 📂 Estrutura de Arquivos

* `script.py` → código principal.
* `usuarios.json` → armazena os IDs válidos e nomes coletados.
* `invalidos.txt` → lista de IDs que retornaram como “usuário inválido”.

---

## 🔑 Configuração

No início do código, defina suas credenciais:

```python
LOGIN = "SEU_LOGIN_AQUI"
PASSWORD = "SUA_SENHA_AQUI"
```

---

## ▶️ Como Executar

1. Certifique-se de que o arquivo `usuarios.json` existe:

   ```bash
   echo "{}" > usuarios.json
   ```
2. Execute o script:

   ```bash
   python3 mapeamento.py
   ```

Durante a execução, o programa exibirá logs em tempo real, indicando:

* `SAVE` → usuário encontrado e salvo.
* `SKIP` → usuário inválido ou já coletado.
* `ERR` → erro de requisição ou parsing.
* `FAIL` → elemento da página não encontrado.

---

## 📝 Saída

* Exemplo de entrada válida em `usuarios.json`:

  ```json
  {
      "2131001": "Fulano da Silva",
      "2131002": "Maria Oliveira"
  }
  ```

* Exemplo de `invalidos.txt`:

  ```
  2131003
  2131004
  ```

---

## ⚠️ Aviso Importante

Este código **acessa sistemas institucionais com autenticação**.

⚠️ Use **apenas em ambiente controlado, com autorização explícita**.

O uso indevido pode violar **políticas de uso** da instituição e **leis vigentes**.
