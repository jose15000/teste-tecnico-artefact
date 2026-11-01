# Cenário 3: Status de Pedido e Rastreamento Seguro

Demonstra a checagem de pedidos com verificação prévia do telefone do comprador para resguardo de privacidade e emissão do código de rastreio dos correios.

---

### Turno 1

**Cliente:** Boa tarde! Gostaria de saber o status do meu pedido número 8.

**Atendente:**

Boa tarde! Tudo bem? 😊

Para consultar o status do seu pedido **n.º 8**, preciso confirmar o telefone cadastrado no pedido. Você poderia me informar o número de telefone associado, por favor? (Formato: (67) xxxx‑xxxx)

---

### Turno 2

**Cliente:** Meu telefone cadastrado é (67) 99654-7821.

> ⚙️ **Tool Call:** `get_order_status` com argumentos `{"customer_phone":"(67) 99654-7821","order_id":8}`

> 📥 **Tool Result:** `{"order_id": 8, "customer_name": "Ana Carolina Ferreira", "order_date": "2026-02-15", "status": "shipped", "total_brl": 349.9, "payment_method": "debit", "tracking_code": "BRJL5544332BR", "estimated_delivery": "2026-02-28", "notes": null, "items": [{"name": "Kala KA-C Concert Mogno", "quantity": 1}]}`

**Atendente:**

Obrigada, Ana! 🙏

📦 **Seu pedido n.º 8 está com o status:** **“enviado”**.  
- **Código de rastreamento:** *BRJL5544332BR*  
- **Previsão de entrega:** **28/02/2026**  

Se precisar de mais alguma informação ou quiser acompanhar o rastreamento, é só me chamar. Estou à disposição! 🎶

---
