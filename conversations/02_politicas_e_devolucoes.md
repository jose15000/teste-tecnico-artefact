# Cenário 2: Informações Gerais e Políticas da Loja

Demonstra a consulta de dados institucionais (endereço e horários) e aplicação de regras de negócio complexas do manual de atendimento (direito de arrependimento, devoluções e frete reverso).

---

### Turno 1

**Cliente:** Qual o endereço e o horário de funcionamento da loja física de vocês em Campo Grande?

> ⚙️ **Tool Call:** `search_policies` com argumentos `{"query":"endereço e horário de funcionamento da loja física em Campo Grande"}`

> 📥 **Tool Result:** `{"total_found": 3, "results": [{"title": "5. Política de Frete e Entregas — 5.1 Entregas na Região Metropolitana de Campo Grande", "content": "5.1 Entregas na Região Metropolitana de Campo Grande \n•​\nFrete grátis para pedidos acima de R$ 500,00. \n•​\nPara pedidos abaixo de R$ 500,00, taxa fixa de R$ 35,00. \n•​\nPrazo de entrega: 1 a 3 dias úteis. \n•​\nEntrega realizada por motoboy próprio. O cliente será contactado por telefone antes da \nentrega."}, {"title": "2. Horário de Funcionamento", "content": "2. Horário de Funcionamento \nO atendimento presencial na loja segue os horários abaixo. O atendimento via WhatsApp segue o \nmesmo horário, com respostas automáticas fora do expediente. \nDia \nHorário \nSegunda a Sexta-feira \n09:00 às 18:00 \nSábado \n09:00 às 13:00 \nDomingo e Feriados \nFechado \n \nEm datas especiais (Black Friday, Aniversário da Loja, Natal), o horário pode ser estendido. \nAlterações serão comunicadas com antecedência nas redes sociais e no atendimento via WhatsApp."}, {"title": "1. Sobre a Empório da Música — 1.2 Dados da Empresa", "content": "1.2 Dados da Empresa \nCampo \nInformação \nRazão Social \nEmpório da Música Instrumentos Musicais Ltda. \nNome Fantasia \nEmpório da Música \nCNPJ \n12.345.678/0001-90 \nEndereço \nRua 14 de Maio, 3200 — Centro, Campo Grande - MS, 79202-333 \nTelefone / WhatsApp \n(67) 3341-4444 \nE-mail \ncontato@empóriodamusica.com.br \nFundação \n2008"}]}`

**Atendente:**

**Endereço da loja física**  
📍 Rua 14 de Maio, 3200 – Centro, Campo Grande – MS, 79202‑333  

**Horário de funcionamento (presencial e WhatsApp)**  
- **Segunda a sexta:** 09:00 – 18:00  
- **Sábado:** 09:00 – 13:00  
- **Domingo e feriados:** fechado  

Em datas especiais (Black Friday, aniversário da loja, Natal) o horário pode ser estendido; avisamos com antecedência nas redes sociais e pelo WhatsApp. 😊

Se precisar de ajuda para escolher um instrumento ou quiser saber sobre algum modelo específico, é só chamar! 🎸🎹🥁

---

### Turno 2

**Cliente:** Me arrependi de uma compra online que recebi ontem, posso devolver meu pedido? Como funciona o frete e o reembolso?

> ⚙️ **Tool Call:** `search_policies` com argumentos `{"query":"política de devolução e reembolso, como funciona o frete de devolução"}`

> 📥 **Tool Result:** `{"total_found": 3, "results": [{"title": "4. Política de Trocas e Devoluções — 4.1 Direito de Arrependimento (Compras Online)", "content": "4.1 Direito de Arrependimento (Compras Online) \n•​\nO cliente pode solicitar a devolução em até 7 (sete) dias corridos após o recebimento do \nproduto, sem necessidade de justificativa. \n•​\nO produto deve estar em sua embalagem original, sem sinais de uso, com todos os \nacessórios e manuais. \n•​\nO reembolso será realizado na mesma forma de pagamento original em até 10 dias úteis. \n•​\nO frete de devolução é por conta da loja em caso de arrependimento."}, {"title": "5. Política de Frete e Entregas — 5.2 Entregas para Outras Cidades", "content": "5.2 Entregas para Outras Cidades \n \n\n\n\nUtilizamos os serviços dos Correios (PAC e SEDEX) e da transportadora Jadlog para envios fora da \nregião metropolitana de Campo Grande. \nModalidade \nPrazo Estimado \nRastreamento \nSeguro \nPAC (Correios) \n5 a 12 dias úteis \nSim \nIncluído \nSEDEX (Correios) \n2 a 5 dias úteis \nSim \nIncluído \nJadlog (.package) \n3 a 8 dias úteis \nSim \nIncluído \n \nO valor do frete é calculado automaticamente com base no CEP de destino, peso e dimensões do \nproduto. Instrumentos de grande porte (baterias acústicas, pianos digitais, contrabaixos) podem exigir \nfrete especial com cotação individual. \nTodos os envios incluem seguro contra extravios e danos durante o transporte. Em caso de avaria, o \ncliente deve recusar o recebimento e entrar em contato imediatamente com a loja."}, {"title": "5. Política de Frete e Entregas — 5.1 Entregas na Região Metropolitana de Campo Grande", "content": "5.1 Entregas na Região Metropolitana de Campo Grande \n•​\nFrete grátis para pedidos acima de R$ 500,00. \n•​\nPara pedidos abaixo de R$ 500,00, taxa fixa de R$ 35,00. \n•​\nPrazo de entrega: 1 a 3 dias úteis. \n•​\nEntrega realizada por motoboy próprio. O cliente será contactado por telefone antes da \nentrega."}]}`

**Atendente:**

**Direito de arrependimento**  
✅ Você tem até **7 dias corridos** após o recebimento do produto para solicitar a devolução, sem precisar justificar.

**Condições para a devolução**  
- O instrumento deve estar na **embalagem original**, sem sinais de uso.  
- Todos os **acessórios, manuais e itens que vieram junto** precisam estar presentes.  

**Frete de devolução**  
- O **custo do frete de volta** (da sua casa até a loja) **é por conta da Empório da Música** quando o motivo é arrependimento.

**Reembolso**  
- O valor será devolvido **na mesma forma de pagamento** utilizada na compra.  
- O prazo para o crédito é de **até 10 dias úteis** após a confirmação de que o item foi recebido em boas condições.

Se precisar iniciar o processo, envie aqui o **número do pedido** e confirme o **telefone cadastrado**. Assim, podemos gerar a solicitação de devolução e encaminhar as instruções de coleta. 🎶  

Qualquer dúvida adicional sobre prazos, documentos ou o procedimento, estou à disposição!

---
