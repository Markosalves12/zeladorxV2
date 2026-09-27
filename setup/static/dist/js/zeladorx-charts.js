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
      var styles = window.getComputedStyle(document.documentElement);
      var textColor = styles.getPropertyValue('--zx-text').trim() || '#202124';
      var mutedColor = styles.getPropertyValue('--zx-muted').trim() || '#68707C';
      var borderColor = styles.getPropertyValue('--zx-border').trim() || '#DFE3EB';
      var primaryColor = styles.getPropertyValue('--zx-primary').trim() || '#0B57D0';
      var successColor = styles.getPropertyValue('--zx-success').trim() || '#137333';
      var warningColor = styles.getPropertyValue('--zx-warning').trim() || '#F9AB00';
      var dangerColor = styles.getPropertyValue('--zx-danger').trim() || '#B3261E';
      var layout = Object.assign({
        autosize: true,
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        colorway: [primaryColor, successColor, warningColor, dangerColor, '#0097A7', '#7B61A8'],
        font: { family: 'Manrope, sans-serif', color: textColor, size: 12 },
        hoverlabel: { bgcolor: textColor, bordercolor: textColor, font: { color: '#FFFFFF' } },
        margin: { l: 54, r: 18, t: 48, b: 48 }
      }, fig.layout || {});
      layout.font = Object.assign({ family: 'Manrope, sans-serif', color: textColor, size: 12 }, layout.font || {});
      layout.title = Object.assign({ font: { family: 'Sora, sans-serif', color: textColor, size: 15 }, x: 0.01, xanchor: 'left' }, layout.title || {});
      layout.margin = Object.assign({ l: 54, r: 18, t: 48, b: 48 }, layout.margin || {});
      layout.xaxis = Object.assign({ gridcolor: borderColor, zerolinecolor: borderColor, tickfont: { color: mutedColor }, automargin: true }, layout.xaxis || {});
      layout.yaxis = Object.assign({ gridcolor: borderColor, zerolinecolor: borderColor, tickfont: { color: mutedColor }, automargin: true }, layout.yaxis || {});
      Plotly.newPlot(el, fig.data || [], layout, {
        responsive: true,
        displaylogo: false,
        locale: 'pt-BR',
        modeBarButtonsToRemove: ['select2d', 'lasso2d', 'autoScale2d']
      });
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
