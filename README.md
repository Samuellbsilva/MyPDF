# 📄 API de Análise e Resumo de PDFs

Este projeto é uma API construída com Flask que permite:

- 📤 Fazer upload de arquivos PDF  
- 📚 Extrair o texto desses arquivos  
- ✂️ Gerar um resumo automatizado  
- 📊 Analisar o conteúdo e fornecer insights estruturados  

A aplicação utiliza a biblioteca **Aspose.PDF** para processamento de arquivos e integra-se com a **API da Hugging Face** para realizar tarefas de Processamento de Linguagem Natural (NLP).

---

## 🚀 Funcionalidades

| Rota                 | Descrição                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `/api/extrairtxt`    | Extrai o texto completo de um PDF enviado                                 |
| `/api/resumirpdf`    | Resume automaticamente o conteúdo textual do PDF com Hugging Face         |
| `/api/analisarpdf`   | Analisa o conteúdo do PDF e retorna insights estruturados   
