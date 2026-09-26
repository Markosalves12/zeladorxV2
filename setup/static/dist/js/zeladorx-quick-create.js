/*
 * Criação rápida em dropdowns obrigatórios.
 *
 * 1. Formulário de origem: botão "Novo" ao lado do select -> guarda rascunho
 *    no sessionStorage e abre o cadastro relacionado.
 * 2. Cadastro relacionado: abre o modal de criação com "Salvar e voltar".
 * 3. De volta à origem: restaura o rascunho e seleciona o item criado.
 */
(function () {
  'use strict';

  var draftKey = 'zeladorx.quick-create.draft';
  var ignoredNames = ['csrfmiddlewaretoken', 'zx_return', 'zx_field'];

  function readConfig() {
    var node = document.getElementById('zx-quick-create-config');
    if (!node) return null;
    try { return { node: node, data: JSON.parse(node.textContent) }; }
    catch (error) { return null; }
  }

  function currentPath() {
    return window.location.pathname + window.location.search;
  }

  function cleanPath(path) {
    var url = new URL(path, window.location.origin);
    ['zx_created', 'zx_created_label', 'zx_field', 'zx_return', 'zx_quick'].forEach(function (key) {
      url.searchParams.delete(key);
    });
    return url.pathname + url.search;
  }

  function modalOf(form) {
    var modal = form.closest('.modal');
    return modal && modal.id ? modal.id : '';
  }

  function openModal(id) {
    if (!id) return;
    if (window.jQuery && window.jQuery.fn.modal) window.jQuery('#' + id).modal('show');
  }

  function serializeForm(form) {
    var values = {};
    Array.prototype.forEach.call(form.elements, function (element) {
      if (!element.name || ignoredNames.indexOf(element.name) !== -1) return;
      if (element.type === 'file' || element.type === 'submit' || element.type === 'button') return;
      if (element.type === 'checkbox' || element.type === 'radio') {
        if (!values[element.name]) values[element.name] = [];
        if (element.checked) values[element.name].push(element.value);
        return;
      }
      if (element.tagName === 'SELECT' && element.multiple) {
        values[element.name] = Array.prototype.filter.call(element.options, function (option) { return option.selected; })
          .map(function (option) { return option.value; });
        return;
      }
      values[element.name] = element.value;
    });
    return values;
  }

  function restoreForm(form, values) {
    Array.prototype.forEach.call(form.elements, function (element) {
      if (!element.name || !(element.name in values)) return;
      var value = values[element.name];
      if (element.type === 'checkbox' || element.type === 'radio') {
        element.checked = Array.isArray(value) && value.indexOf(element.value) !== -1;
      } else if (element.tagName === 'SELECT' && element.multiple && Array.isArray(value)) {
        Array.prototype.forEach.call(element.options, function (option) { option.selected = value.indexOf(option.value) !== -1; });
      } else if (element.type !== 'file') {
        element.value = value;
      }
    });
  }

  function selectCreated(select, value, label) {
    var match = Array.prototype.find.call(select.options, function (option) { return option.value === value; });
    if (!match && label) {
      match = Array.prototype.find.call(select.options, function (option) { return option.textContent.trim() === label; });
    }
    if (!match) return false;
    select.value = match.value;
    select.dispatchEvent(new Event('change', { bubbles: true }));
    select.classList.add('zx-quick-highlight');
    window.setTimeout(function () { select.classList.remove('zx-quick-highlight'); }, 2600);
    return true;
  }

  function addButtons(form, fields) {
    Object.keys(fields).forEach(function (name) {
      var select = form.querySelector('select[name="' + CSS.escape(name) + '"]');
      if (!select || select.dataset.zxQuick) return;
      select.dataset.zxQuick = '1';

      var wrapper = document.createElement('div');
      wrapper.className = 'zx-quick-field';
      select.parentNode.insertBefore(wrapper, select);
      wrapper.appendChild(select);

      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'zx-quick-add';
      button.title = 'Criar ' + fields[name].label + ' e voltar para este formulário';
      var icon = document.createElement('i');
      icon.className = 'fas fa-plus';
      button.appendChild(icon);
      button.appendChild(document.createTextNode(' Novo'));
      wrapper.appendChild(button);

      button.addEventListener('click', function () {
        var returnTo = cleanPath(currentPath());
        window.sessionStorage.setItem(draftKey, JSON.stringify({
          path: new URL(returnTo, window.location.origin).pathname,
          modal: modalOf(form),
          field: name,
          values: serializeForm(form),
          savedAt: Date.now()
        }));
        var target = new URL(fields[name].url, window.location.origin);
        target.searchParams.set('zx_return', returnTo);
        target.searchParams.set('zx_field', name);
        window.location.href = target.pathname + target.search;
      });
    });
  }

  function hidden(form, name, value) {
    var input = form.querySelector('input[name="' + name + '"]') || document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    if (!input.parentNode) form.appendChild(input);
  }

  function prepareReturnMode(form, returnTo, field) {
    hidden(form, 'zx_return', returnTo);
    hidden(form, 'zx_field', field);

    var banner = document.createElement('div');
    banner.className = 'zx-quick-banner';
    var icon = document.createElement('i');
    icon.className = 'fas fa-reply';
    banner.appendChild(icon);
    banner.appendChild(document.createTextNode('Após salvar, você volta ao formulário anterior com este item selecionado.'));
    var back = document.createElement('a');
    back.href = returnTo;
    back.textContent = 'Cancelar e voltar';
    banner.appendChild(back);
    form.insertBefore(banner, form.firstChild);

    Array.prototype.forEach.call(form.querySelectorAll('button[type="POST"], button[type="submit"], button:not([type])'), function (button) {
      button.innerHTML = '';
      var saveIcon = document.createElement('i');
      saveIcon.className = 'fas fa-check mr-1';
      button.appendChild(saveIcon);
      button.appendChild(document.createTextNode('Salvar e voltar'));
    });

    // Fechar o modal sem salvar também devolve o usuário para a origem.
    var modalId = modalOf(form);
    if (modalId && window.jQuery) {
      window.jQuery('#' + modalId).one('hidden.bs.modal', function () {
        if (!form.dataset.zxSubmitting) window.location.href = returnTo;
      });
    }
    form.addEventListener('submit', function () { form.dataset.zxSubmitting = '1'; });
    openModal(modalId);
  }

  function restoreDraft(form) {
    var params = new URLSearchParams(window.location.search);
    var created = params.get('zx_created');
    if (!created) return;

    var draft = null;
    try { draft = JSON.parse(window.sessionStorage.getItem(draftKey) || 'null'); }
    catch (error) { draft = null; }

    var field = params.get('zx_field') || (draft && draft.field) || '';
    if (draft && draft.path === window.location.pathname) {
      restoreForm(form, draft.values || {});
      openModal(draft.modal);
    }
    window.sessionStorage.removeItem(draftKey);

    var select = field ? form.querySelector('select[name="' + CSS.escape(field) + '"]') : null;
    if (select) selectCreated(select, created, params.get('zx_created_label'));

    window.history.replaceState(null, '', cleanPath(currentPath()) + window.location.hash);
  }

  function initialize() {
    var config = readConfig();
    if (!config) return;
    var form = config.node.closest('form');
    if (!form) return;

    addButtons(form, config.data.fields || {});
    if (config.data.returnTo) prepareReturnMode(form, config.data.returnTo, config.data.returnField || '');
    restoreDraft(form);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize);
  else initialize();
}());
