(function () {
  'use strict';

  var storageKey = 'zeladorx.sidebar.open-groups';
  var iconMap = {
    'Relatórios': 'fa-chart-bar',
    'Catálogo de serviços': 'fa-clipboard-list',
    'Serviços agendados': 'fa-calendar-check',
    'Serviços configurados': 'fa-sliders-h',
    'Agendar serviço': 'fa-calendar-plus',
    'Configurar serviço': 'fa-cogs',
    'Unidades': 'fa-building',
    'Gerentes': 'fa-user-tie',
    'Empresas': 'fa-city',
    'Auth': 'fa-user-shield',
    'Dimensionador': 'fa-ruler-combined',
    'Permissões de usuário': 'fa-key',
    'Conf. notificações': 'fa-bell',
    'Solicitações': 'fa-inbox',
    'QR Codes': 'fa-qrcode',
    'Visualizações': 'fa-eye',
    'Dashboards': 'fa-chart-pie'
  };

  function labelOf(link) {
    var paragraph = link.querySelector('p');
    if (!paragraph) return '';
    var clone = paragraph.cloneNode(true);
    Array.prototype.forEach.call(clone.querySelectorAll('i, span'), function (node) { node.remove(); });
    return clone.textContent.replace(/\s+/g, ' ').trim();
  }

  function savedGroups() {
    try { return JSON.parse(window.localStorage.getItem(storageKey) || '[]'); }
    catch (error) { return []; }
  }

  function saveGroups() {
    var open = [];
    document.querySelectorAll('.nav-sidebar > .nav-item.menu-open > .nav-link').forEach(function (link) {
      var label = labelOf(link);
      if (label) open.push(label);
    });
    window.localStorage.setItem(storageKey, JSON.stringify(open));
  }

  function setSectionIcons() {
    document.querySelectorAll('.nav-sidebar > .nav-item > .nav-link').forEach(function (link) {
      var label = labelOf(link);
      var iconClass = iconMap[label];
      var icon = link.querySelector('.nav-icon');
      if (!icon || !iconClass) return;
      icon.className = 'nav-icon fas ' + iconClass;
      link.setAttribute('aria-label', label);
    });
  }

  function markCurrentPage() {
    var currentPath = window.location.pathname.replace(/\/$/, '');
    document.querySelectorAll('.nav-sidebar a.nav-link[href]').forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href || href === '#') return;
      var target;
      try { target = new URL(link.href, window.location.origin).pathname.replace(/\/$/, ''); }
      catch (error) { return; }
      link.classList.remove('active');
      if (target === currentPath) {
        link.classList.add('active');
        var parent = link.closest('.nav-item');
        var group = parent && parent.parentElement ? parent.parentElement.closest('.nav-item') : null;
        if (group) group.classList.add('menu-open');
      }
    });
  }

  function restoreGroups() {
    var open = savedGroups();
    document.querySelectorAll('.nav-sidebar > .nav-item > .nav-link').forEach(function (link) {
      if (open.indexOf(labelOf(link)) !== -1 && link.nextElementSibling) {
        link.parentElement.classList.add('menu-open');
        link.nextElementSibling.style.display = 'block';
      }
    });
  }

  function bindMenuPersistence() {
    document.querySelectorAll('.nav-sidebar > .nav-item > .nav-link').forEach(function (link) {
      if (link.getAttribute('href') === '#') {
        link.addEventListener('click', function (event) {
          event.preventDefault();
          window.setTimeout(saveGroups, 220);
        });
      }
    });
    document.querySelectorAll('.nav-treeview a.nav-link').forEach(function (link) {
      link.addEventListener('click', saveGroups);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    setSectionIcons();
    markCurrentPage();
    restoreGroups();
    bindMenuPersistence();
  });
}());
