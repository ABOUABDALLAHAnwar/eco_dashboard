const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    createProxyMiddleware({
      target: 'http://localhost:8001',
      changeOrigin: true,
      cookieDomainRewrite: "",  // ← Chaîne vide : enlève le domain pour que le cookie soit accepté sur localhost:3000
      logLevel: 'debug',  // Tu verras "[HPM] Proxy..." dans le terminal frontend
    })
  );
};