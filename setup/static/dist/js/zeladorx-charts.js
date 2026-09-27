/* ZeladorX — gráficos dos dashboards desenhados no navegador.
 * O servidor envia <div class="zx-plotly" data-figure="{json}">; aqui o
 * plotly.js é carregado uma única vez (cache do navegador) e cada gráfico
 * só é desenhado quando aparece na tela. */
(function () {
  'use strict';
  var PLOTLY_URL = 'https://cdn.plot.ly/plotly-2.35.2.min.js';
  var carregando = null;

  function carregarPlotly() {
    if (window.Plotly) return Promise.resolve(window.Plotly);
    if (carregando) return carregando;
    carregando = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = PLOTLY_URL;
      s.async = true;
      s.onload = function () { resolve(window.Plotly); };
      s.onerror = reject;
      document.head.appendChild(s);
    });
    return carregando;
  }

  function desenhar(el) {
    if (el.dataset.zxRendered) return;
    el.dataset.zxRendered = '1';
    var fig;
    try { fig = JSON.parse(el.dataset.figure); } catch (e) { return; }
    carregarPlotly().then(function (Plotly) {
      var layout = Object.assign({ autosize: true, paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Manrope, sans-serif' } }, fig.layout || {});
      Plotly.newPlot(el, fig.data || [], layout, { responsive: true, displaylogo: false, locale: 'pt-BR' });
    }).catch(function () {
      el.innerHTML = '<p class="text-muted p-3">Não foi possível carregar o gráfico. Verifique a conexão.</p>';
    });
  }

  function iniciar() {
    var els = document.querySelectorAll('.zx-plotly[data-figure]');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) { els.forEach(desenhar); return; }
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { obs.unobserve(en.target); desenhar(en.target); }
      });
    }, { rootMargin: '200px' });
    els.forEach(function (el) { obs.observe(el); });
    // Abas/colapsos: redimensiona gráficos que ficaram visíveis depois.
    document.addEventListener('shown.bs.tab', redimensionar);
    document.addEventListener('click', function () { setTimeout(redimensionar, 350); });
  }

  function redimensionar() {
    if (!window.Plotly) return;
    document.querySelectorAll('.zx-plotly[data-zx-rendered]').forEach(function (el) {
      if (el.offsetParent) window.Plotly.Plots.resize(el);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
