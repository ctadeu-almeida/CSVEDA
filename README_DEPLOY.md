# 🚀 Deploy Rápido - CSVEDA

## ⚡ **Opção Mais Fácil: Streamlit Cloud (GRATUITO)**

### **1. Preparar GitHub**
```bash
git add .
git commit -m "Deploy: CSVEDA pronto para produção"
git push origin main
```

### **2. Deploy**
1. Acesse: https://streamlit.io/cloud
2. "New app" → Selecione seu repositório
3. Main file: `app.py`
4. Clique "Deploy!"

### **3. Configurar API Key**
- Settings → Secrets → Cole:
```toml
GOOGLE_API_KEY = "sua_gemini_api_key_aqui"
```

### **✅ Pronto! URL: `https://csveda-seu-usuario.streamlit.app`**

---

## 🎯 **Alternativa: Render (Mais Robusto)**

1. https://render.com → "New Web Service"
2. Conecte repositório GitHub
3. Build: `pip install -r requirements.txt`
4. Start: `streamlit run app.py --server.port=$PORT --server.headless=true`
5. Environment Variables:
   - `GOOGLE_API_KEY` = sua_api_key
   - `PORT` = 10000

---

## 📱 **Resultado Final**

✅ **Aplicação online com link público**
✅ **Upload de arquivos CSV funcionando**
✅ **Agentes IA com Google Gemini**
✅ **Interface chat WhatsApp-style**
✅ **Análises automáticas de dados**

**🌟 Qualquer pessoa poderá acessar via link e fazer upload de CSV para análise!**