/*
 * ZeladorX - Relatórios PDF montados no navegador
 *
 * Intercepta os links "Relatório simples" / "Relatório com checklist" dos
 * relatórios PDF de jardinagem e limpeza predial. Em vez de esperar o servidor
 * desenhar o PDF, busca os dados (mesma URL com ?formato=json), monta o arquivo
 * aqui com pdfmake e baixa automaticamente.
 * Se algo falhar, cai no PDF gerado pelo servidor (link original).
 */
(function () {
  'use strict';

  var LINK_PDF = /\/exportar-relatorio-de-serivos-.*-pdf(-with-checklist)?\//i;
  var FOTO_LADO_MAX = 800;
  var DOWNLOADS_SIMULTANEOS = 6;

  var CORES_STATUS = {
    'Em andamento': ['#008000', '#FFFFFF'],
    'Cancelado': ['#808080', '#FFFFFF'],
    'Concluido': ['#020d3f', '#FFFFFF']
  };

  var CORES_GRAFICO = {
    'Concluido': '#020d3f',
    'Próximo': '#e0b800',
    'Atrasado': '#d62828',
    'Agendado': '#14a0b6',
    'Em andamento': '#008000'
  };

  var scriptBase = (function () {
    var atual = document.currentScript && document.currentScript.src;
    return atual ? atual.replace(/zeladorx-relatorio-pdf\.js.*$/, '') : '/static/dist/js/';
  })();

  // ------------------------------------------------------------------ utilidades
  function carregarScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error('Falha ao carregar ' + src)); };
      document.head.appendChild(s);
    });
  }

  var pdfMakePronto = null;
  function carregarPdfMake() {
    if (window.pdfMake && window.pdfMake.vfs) return Promise.resolve(window.pdfMake);
    if (!pdfMakePronto) {
      pdfMakePronto = carregarScript(scriptBase + 'vendor/pdfmake.min.js')
        .then(function () { return carregarScript(scriptBase + 'vendor/vfs_fonts.js'); })
        .then(function () { return window.pdfMake; });
    }
    return pdfMakePronto;
  }

  function comFormatoJson(href) {
    var url = new URL(href, window.location.origin);
    url.searchParams.set('formato', 'json');
    return url.toString();
  }

  // ---------------------------------------------------------------- aviso na tela
  var aviso = null;
  function mostrarAviso(texto) {
    if (!aviso) {
      aviso = document.createElement('div');
      aviso.setAttribute('role', 'status');
      aviso.style.cssText = 'position:fixed;right:24px;bottom:24px;z-index:3000;background:#0f172a;' +
        'color:#fff;padding:14px 18px;border-radius:14px;box-shadow:0 12px 30px rgba(15,23,42,.35);' +
        'font:500 14px Manrope,system-ui,sans-serif;max-width:320px;display:flex;gap:10px;align-items:center';
      document.body.appendChild(aviso);
    }
    aviso.innerHTML = '<i class="fas fa-file-pdf"></i><span></span>';
    aviso.querySelector('span').textContent = texto;
    aviso.style.display = 'flex';
  }
  function esconderAviso() { if (aviso) aviso.style.display = 'none'; }

  // --------------------------------------------------------------------- imagens
  var cacheImagens = {};

  function imagemParaDataUrl(url) {
    if (!url) return Promise.resolve(null);
    if (cacheImagens[url]) return cacheImagens[url];
    cacheImagens[url] = fetch(url, { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.blob(); })
      .then(function (blob) {
        return new Promise(function (resolve, reject) {
          var img = new Image();
          var objUrl = URL.createObjectURL(blob);
          img.onload = function () {
            var escala = Math.min(1, FOTO_LADO_MAX / Math.max(img.width, img.height));
            var canvas = document.createElement('canvas');
            canvas.width = Math.max(1, Math.round(img.width * escala));
            canvas.height = Math.max(1, Math.round(img.height * escala));
            var ctx = canvas.getContext('2d');
            ctx.fillStyle = '#FFFFFF';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            URL.revokeObjectURL(objUrl);
            resolve({ data: canvas.toDataURL('image/jpeg', 0.75), w: canvas.width, h: canvas.height });
          };
          img.onerror = function () { URL.revokeObjectURL(objUrl); reject(new Error('imagem inválida')); };
          img.src = objUrl;
        });
      })
      .catch(function () { return null; });
    return cacheImagens[url];
  }

  function baixarImagens(urls, aoProgredir) {
    var lista = Array.from(new Set(urls.filter(Boolean)));
    var feitos = 0;
    var i = 0;
    function proximo() {
      if (i >= lista.length) return Promise.resolve();
      var url = lista[i++];
      return imagemParaDataUrl(url).then(function () {
        feitos += 1;
        aoProgredir(feitos, lista.length);
        return proximo();
      });
    }
    var trabalhadores = [];
    for (var k = 0; k < Math.min(DOWNLOADS_SIMULTANEOS, lista.length); k++) trabalhadores.push(proximo());
    return Promise.all(trabalhadores);
  }

  // --------------------------------------------------------------------- gráficos
  function agrupar(servicos, chave, porLista) {
    var grupos = {};
    servicos.forEach(function (s) {
      var nomes = porLista ? chave(s) : [chave(s)];
      if (!nomes || !nomes.length) nomes = ['Não informado'];
      nomes.forEach(function (nome) {
        nome = nome || 'Não informado';
        if (!grupos[nome]) grupos[nome] = { area: 0, qtd: 0 };
        grupos[nome].area += Number(s.area.dimensao || 0);
        grupos[nome].qtd += 1;
      });
    });
    return Object.keys(grupos).map(function (k) { return { nome: k, area: grupos[k].area, qtd: grupos[k].qtd }; })
      .sort(function (a, b) { return b.area - a.area; })
      .slice(0, 15);
  }

  function desenharGrafico(titulo, itens, campo, cor) {
    var largura = 1000;
    var linha = 34;
    var altura = 80 + itens.length * linha;
    var canvas = document.createElement('canvas');
    canvas.width = largura;
    canvas.height = altura;
    var ctx = canvas.getContext('2d');
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, largura, altura);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 24px sans-serif';
    ctx.fillText(titulo, 20, 38);

    var max = Math.max.apply(null, itens.map(function (i) { return i[campo]; }).concat([1]));
    var inicioBarra = 330;
    var larguraBarra = largura - inicioBarra - 120;
    ctx.font = '18px sans-serif';
    itens.forEach(function (item, idx) {
      var y = 70 + idx * linha;
      var rotulo = item.nome.length > 32 ? item.nome.slice(0, 31) + '…' : item.nome;
      ctx.fillStyle = '#334155';
      ctx.textAlign = 'right';
      ctx.fillText(rotulo, inicioBarra - 12, y + 18);
      ctx.fillStyle = cor;
      var w = Math.max(2, (item[campo] / max) * larguraBarra);
      ctx.fillRect(inicioBarra, y + 2, w, linha - 10);
      ctx.fillStyle = '#0f172a';
      ctx.textAlign = 'left';
      var valor = campo === 'area' ? item.area.toLocaleString('pt-BR', { maximumFractionDigits: 0 }) + ' m²' : String(item.qtd);
      ctx.fillText(valor, inicioBarra + w + 8, y + 18);
    });
    return { image: canvas.toDataURL('image/png'), width: 515, margin: [0, 0, 0, 14] };
  }

  function graficosDoGrupo(servicos, rotuloStatus, setor) {
    var cor = CORES_GRAFICO[rotuloStatus] || '#020d3f';
    var dimensoes = [];
    if (setor === 'jardinagem') {
      dimensoes.push(['Tipo de Terreno', function (s) { return s.area.terreno; }, false]);
      dimensoes.push(['Tipo de Vegetação', function (s) { return s.area.vegetacao; }, false]);
    }
    dimensoes.push(['localidade', function (s) { return s.area.localidade; }, false]);
    dimensoes.push([setor === 'jardinagem' ? 'área verde' : 'área', function (s) { return s.area.nome; }, false]);
    if (setor === 'jardinagem') dimensoes.push(['colaborador', function (s) { return s.colaboradores; }, true]);
    dimensoes.push(['serviço', function (s) { return s.servicos; }, true]);

    var saida = [];
    dimensoes.forEach(function (d) {
      var itens = agrupar(servicos, d[1], d[2]);
      if (!itens.length) return;
      saida.push(desenharGrafico('Área Total por ' + d[0] + ' (' + rotuloStatus + ')', itens, 'area', cor));
      saida.push(desenharGrafico('Quantidade de serviços por ' + d[0] + ' (' + rotuloStatus + ')', itens, 'qtd', cor));
    });
    return saida;
  }

  // ----------------------------------------------------------------- documento
  function corDoStatus(s) {
    if (CORES_STATUS[s.status]) return { texto: s.status, fundo: CORES_STATUS[s.status][0], cor: CORES_STATUS[s.status][1] };
    var d = s.dias_diferenca;
    if (d === null || d === undefined) return null;
    if (d < 0) return { texto: s.novo_status, fundo: '#ff0000', cor: '#FFFFFF' };
    if (d <= 7) return { texto: s.novo_status, fundo: '#ffff00', cor: '#000000' };
    return { texto: s.novo_status, fundo: '#14a0b6', cor: '#FFFFFF' };
  }

  function blocoImagem(titulo, url, dados, extras) {
    var img = cacheImagensResolvidas[url] || cacheImagensResolvidas[dados.imagem_padrao];
    var conteudo = [{ text: titulo, style: 'fotoTitulo' }];
    (extras || []).forEach(function (e) { conteudo.push(e); });
    if (img) conteudo.push({ image: img.data, fit: [240, 220], margin: [0, 4, 0, 0] });
    else conteudo.push({ text: 'Imagem indisponível', style: 'suave' });
    return { stack: conteudo, margin: [0, 0, 0, 12], unbreakable: true };
  }

  function grade(blocos) {
    var linhas = [];
    for (var i = 0; i < blocos.length; i += 2) {
      linhas.push({ columns: [blocos[i], blocos[i + 1] || { text: '' }], columnGap: 20 });
    }
    return linhas;
  }

  function tabela(cabecalho, linhas, larguras) {
    return {
      table: {
        headerRows: 1,
        widths: larguras,
        body: [cabecalho.map(function (h) { return { text: h, style: 'th' }; })].concat(linhas)
      },
      layout: {
        fillColor: function (i) { return i === 0 ? '#e6e6e6' : (i % 2 === 0 ? '#f2f2f2' : null); },
        hLineColor: '#d0d5dd', vLineColor: '#d0d5dd'
      },
      fontSize: 8,
      margin: [0, 4, 0, 14]
    };
  }

  function statusChecklist(status) {
    var fundo = status === 'Pendente' ? '#f6be04' : (status === 'Concluído' ? '#008000' : null);
    return fundo ? { text: status, fillColor: fundo, color: status === 'Concluído' ? '#FFFFFF' : '#000000' } : status || '-';
  }

  var cacheImagensResolvidas = {};

  function blocoServico(s, dados) {
    var st = corDoStatus(s);
    var conteudo = [];
    conteudo.push({
      text: [
        { text: 'Descrição: ' + s.descricao + ' (Agendamento.Id: ' + s.id + ') ', bold: true },
        st ? { text: ' ' + st.texto + ' ', background: st.fundo, color: st.cor, bold: true } : ''
      ],
      margin: [0, 0, 0, 8]
    });
    conteudo.push({
      stack: [
        'Data de Início: ' + (s.inicio || '-'),
        'Data de Conclusão: ' + (s.conclusao || 'Não concluído'),
        'Área atendida: ' + (s.area.nome || '-'),
        'Tamanho da área atendida: ' + (s.area.nome ? s.area.dimensao : '-') + ' M²',
        'Serviços Escalados: ' + (s.servicos.join(', ') || '-')
      ].concat(dados.setor === 'jardinagem' ? ['Colaboradores Escalados: ' + (s.colaboradores.join(', ') || '-')] : []),
      lineHeight: 1.35,
      margin: [0, 0, 0, 10]
    });

    // Fotos
    var fotos = [];
    if (dados.setor === 'jardinagem') {
      fotos.push(blocoImagem('Na solicitação', s.foto_solicitacao, dados));
      if (dados.com_checklist) {
        s.checklists.forEach(function (c) {
          fotos.push(blocoImagem('Descrição: ' + c.descricao, c.foto, dados, [
            { text: [{ text: 'Status: ' }, statusChecklist(c.status)], fontSize: 8 },
            { text: 'Atualizado em: ' + (c.atualizado_em || '-'), fontSize: 8 }
          ]));
        });
      }
      fotos.push(blocoImagem('Na entrega', s.foto_entrega, dados));
    } else {
      s.execucoes.forEach(function (e) { fotos.push(blocoImagem('Na entrega', e.foto_entrega, dados)); });
      if (dados.com_checklist) {
        s.checklists.forEach(function (c) {
          fotos.push(blocoImagem('Descrição: ' + c.descricao, c.foto, dados, [
            { text: [{ text: 'Status: ' }, statusChecklist(c.status)], fontSize: 8 },
            { text: 'Atualizado em: ' + (c.atualizado_em || '-'), fontSize: 8 }
          ]));
        });
      }
    }
    conteudo = conteudo.concat(grade(fotos));

    if (s.execucoes.length) {
      conteudo.push({ text: 'Dados de Execução:', bold: true, margin: [0, 6, 0, 0] });
      conteudo.push(tabela(
        ['Agendamento.Id', 'Colaboradores.Nome', 'DataHoraChegada', 'DataHoraRetorno', 'TempoEmAtividade'],
        s.execucoes.map(function (e) { return [String(s.id), e.colaborador, e.chegada || '-', e.retorno || '-', e.tempo || '-']; }),
        [70, '*', 85, 85, 80]
      ));
    }

    if (dados.com_checklist && s.checklists.length) {
      conteudo.push({ text: 'Dados do Checklist:', bold: true });
      conteudo.push(tabela(
        ['Agendamento.Id', 'Agendamento.Descrição', 'Checklist.Descrição', 'Checklist.AtualizadoEm', 'Checklist.Status'],
        s.checklists.map(function (c) { return [String(s.id), s.descricao, c.descricao, c.atualizado_em || '-', statusChecklist(c.status)]; }),
        [60, '*', '*', 85, 65]
      ));
    }
    return conteudo;
  }

  function montarDocumento(dados, logo) {
    var conteudo = [];
    dados.servicos.forEach(function (s, idx) {
      var bloco = blocoServico(s, dados);
      if (idx > 0) bloco[0].pageBreak = 'before';
      conteudo = conteudo.concat(bloco);
    });

    if (dados.servicos.length) {
      var concluido = dados.status.indexOf('Concluido') !== -1;
      var graficos = [];
      if (concluido) {
        graficos.push({ text: 'Volume de serviços prestados', style: 'secao' });
        graficos = graficos.concat(graficosDoGrupo(dados.servicos.filter(function (s) { return s.status === 'Concluido'; }), 'Concluido', dados.setor));
      } else {
        graficos.push({ text: 'Volume de serviços Agendados', style: 'secao' });
        ['Próximo', 'Atrasado', 'Agendado', 'Em andamento'].forEach(function (rotulo) {
          var grupo = dados.servicos.filter(function (s) { return s.novo_status === rotulo; });
          if (grupo.length) graficos = graficos.concat(graficosDoGrupo(grupo, rotulo, dados.setor));
        });
      }
      graficos[0].pageBreak = 'before';
      conteudo = conteudo.concat(graficos);
    } else {
      conteudo.push({ text: 'Nenhum serviço encontrado para os filtros escolhidos.', style: 'suave', margin: [0, 30, 0, 0] });
    }

    conteudo.push({ text: 'zeladorX', alignment: 'center', margin: [0, 30, 0, 0], color: '#64748b' });

    return {
      pageSize: 'LETTER',
      pageMargins: [50, logo ? 110 : 70, 50, 50],
      info: { title: 'Relatório de Serviços - ZeladorX' },
      header: function () {
        var cab = [];
        if (logo) cab.push({ image: logo.data, fit: [160, 50], alignment: 'center', margin: [0, 18, 0, 4] });
        cab.push({ text: 'Relatório de Serviços', alignment: 'center', bold: true, fontSize: 14, margin: [0, logo ? 0 : 28, 0, 0] });
        return { stack: cab };
      },
      footer: function (atual, total) {
        return { text: 'Gerado em ' + dados.gerado_em + '  •  Página ' + atual + ' de ' + total, alignment: 'center', fontSize: 8, color: '#64748b', margin: [0, 18, 0, 0] };
      },
      content: conteudo,
      defaultStyle: { fontSize: 10 },
      styles: {
        th: { bold: true, fontSize: 8 },
        fotoTitulo: { fontSize: 9, bold: true },
        suave: { color: '#64748b', fontSize: 9 },
        secao: { fontSize: 13, bold: true, margin: [0, 0, 0, 12] }
      }
    };
  }

  // --------------------------------------------------------------------- fluxo
  function gerar(href) {
    mostrarAviso('Buscando os dados do relatório…');
    var dados;
    return Promise.all([
      fetch(comFormatoJson(href), { credentials: 'same-origin', headers: { Accept: 'application/json' } })
        .then(function (r) {
          var tipo = r.headers.get('content-type') || '';
          if (!r.ok || tipo.indexOf('application/json') === -1) throw new Error('resposta inesperada');
          return r.json();
        }),
      carregarPdfMake()
    ]).then(function (res) {
      dados = res[0];
      var urls = [dados.logo, dados.imagem_padrao];
      dados.servicos.forEach(function (s) {
        urls.push(s.foto_solicitacao, s.foto_entrega);
        s.execucoes.forEach(function (e) { urls.push(e.foto_entrega); });
        if (dados.com_checklist) s.checklists.forEach(function (c) { urls.push(c.foto); });
      });
      mostrarAviso('Carregando fotos…');
      return baixarImagens(urls, function (feitos, total) {
        mostrarAviso('Carregando fotos (' + feitos + ' de ' + total + ')…');
      }).then(function () {
        var todas = Array.from(new Set(urls.filter(Boolean)));
        return Promise.all(todas.map(function (u) {
          return imagemParaDataUrl(u).then(function (img) { if (img) cacheImagensResolvidas[u] = img; });
        }));
      });
    }).then(function () {
      mostrarAviso('Montando o PDF (' + dados.servicos.length + ' serviços)…');
      var doc = montarDocumento(dados, cacheImagensResolvidas[dados.logo]);
      var nome = 'relatorio de servicos ' + dados.status.join(',') + ' ' + Date.now() + '.pdf';
      return new Promise(function (resolve) {
        window.pdfMake.createPdf(doc).download(nome, resolve);
      });
    }).then(function () {
      mostrarAviso('Relatório baixado.');
      setTimeout(esconderAviso, 2500);
    });
  }

  var emAndamento = false;
  document.addEventListener('click', function (evento) {
    var link = evento.target.closest && evento.target.closest('a[href]');
    if (!link || !LINK_PDF.test(link.getAttribute('href') || '')) return;
    if (evento.ctrlKey || evento.metaKey || evento.shiftKey) return;
    evento.preventDefault();
    if (emAndamento) return;
    emAndamento = true;
    var href = link.href;
    gerar(href).catch(function (erro) {
      console.warn('[ZeladorX] PDF no navegador falhou, usando o servidor:', erro);
      mostrarAviso('Gerando pelo servidor…');
      setTimeout(esconderAviso, 4000);
      window.location.href = href;
    }).then(function () { emAndamento = false; });
  });
})();
