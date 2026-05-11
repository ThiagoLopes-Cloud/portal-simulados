# 📝 Cadastro de Usuário

A tela de cadastro permite a criação de uma nova conta na plataforma SimusLab.

Após o cadastro, o usuário poderá acessar simulados, acompanhar resultados e participar do ranking da plataforma.

---

# 🖼️ Interface da Tela

🚧 Inserir screenshot da tela de cadastro.

Exemplo futuro:

```md
![Tela de Cadastro](../assets/screenshots/register-page.png)
```

---

# 🎯 Objetivo da Página

Permitir que novos estudantes realizem seu cadastro de forma rápida, segura e intuitiva.

---

# 🚀 Como Criar uma Conta

1. Acesse a tela de cadastro.
2. Preencha os dados solicitados.
3. Crie uma senha segura.
4. Confirme sua senha.
5. Clique em **Criar Conta**.

---

# 📋 Campos Disponíveis

## 👤 Nome de Usuário

Campo utilizado para identificação da conta.

### Exemplo:

```txt
joao.silva
```

### Regras:

- letras minúsculas
- números
- pontos

---

## 📧 E-mail

Campo utilizado para comunicação e recuperação de acesso.

### Exemplo:

```txt
usuario@email.com
```

---

## 🔐 Senha

Campo utilizado para autenticação da conta.

### Requisitos recomendados:

- mínimo de 8 caracteres
- letras maiúsculas
- números
- caracteres especiais

---

## 🔁 Confirmar Senha

Campo utilizado para validar a senha digitada anteriormente.

O sistema verifica automaticamente se ambas as senhas coincidem.

---

# 👁️ Visualização de Senha

O ícone de visualização permite:

- exibir senha
- ocultar senha

Essa funcionalidade ajuda a evitar erros de digitação.

---

# 📊 Indicador de Força da Senha

A plataforma analisa automaticamente o nível de segurança da senha digitada.

## Níveis possíveis:

| Nível | Descrição |
|---|---|
| Fraca | Senha insegura |
| Razoável | Segurança intermediária |
| Boa | Boa proteção |
| Forte | Alta segurança |

---

# ✅ Mensagens de Sucesso

Após cadastro realizado corretamente:

```txt
Conta criada com sucesso! Redirecionando para o login...
```

O sistema redireciona automaticamente para a tela de login.

---

# ❌ Mensagens de Erro

## Campos obrigatórios

```txt
Preencha todos os campos.
```

---

## Senhas diferentes

```txt
As senhas não conferem.
```

---

## Falha no cadastro

```txt
Erro ao criar conta. Tente novamente.
```

---

# ⚡ Comportamentos Inteligentes

## Botão de Cadastro

O botão permanece desabilitado enquanto:

- existirem campos vazios
- o sistema estiver processando
- o cadastro tiver sido concluído

---

## Estado de Carregamento

Durante o cadastro o sistema exibe:

```txt
Criando sua conta...
```

junto de um indicador visual de carregamento.

---

# 📱 Responsividade

A tela foi desenvolvida para funcionar em:

- computadores
- tablets
- smartphones

No mobile, os campos de senha são reorganizados automaticamente para melhor usabilidade.

---

# 🛡️ Segurança

A plataforma realiza validações antes do envio dos dados para a API.

As informações são enviadas de forma segura para o sistema de autenticação.

---

# 💡 Boas Práticas

- Utilize um e-mail válido.
- Crie senhas fortes.
- Não compartilhe sua senha.
- Evite senhas fáceis como datas de nascimento.

---

# 🔗 Navegação

## Já possui conta?

O link:

```txt
Fazer login
```

redireciona o usuário para a tela de autenticação.