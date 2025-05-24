const mongoose = require('mongoose');

const ProdutoImagemSchema = new mongoose.Schema({
  nome: String,
  slug: { type: String, unique: true },
  imagem_url: String,
  imagem_fundo_removido_url: String,
  origem: String,
  criado_em: { type: Date, default: Date.now }
});

module.exports = mongoose.model('ProdutoImagem', ProdutoImagemSchema);
