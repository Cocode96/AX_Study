// 외부 라이브러리, fetch와 서버 없이 file://에서 작동한다.
(() => {
  'use strict';
  const search = document.querySelector('#search');
  const topicNav = document.querySelector('.topic-nav');
  if (topicNav) {
    const breakpoint = matchMedia('(max-width: 900px)');
    const resizeNav = () => { topicNav.open = !breakpoint.matches; };
    breakpoint.addEventListener('change', resizeNav); resizeNav();
  }
  if (search) {
    const cards = [...document.querySelectorAll('.card')];
    const group = document.querySelector('#group');
    const filter = (updateUrl = true) => {
      const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        card.hidden = !((group.value === 'all' || group.value === card.dataset.group)
          && words.every(word => card.dataset.search.includes(word)));
        if (!card.hidden) count++;
      });
      document.querySelectorAll('.group-section').forEach(section => {
        section.hidden = ![...section.querySelectorAll('.card')].some(card => !card.hidden);
      });
      document.querySelector('#count').textContent = count + '개 항목';
      document.querySelector('#empty').hidden = count !== 0;
      if (updateUrl) {
        const url = new URL(location.href);
        search.value.trim() ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
        group.value !== 'all' ? url.searchParams.set('topic', group.value) : url.searchParams.delete('topic');
        // 일부 file:// 브라우저의 History 제약은 검색 기능에 영향을 주지 않는다.
        try { history.replaceState(null, '', url); } catch { /* 현재 화면의 검색은 유지 */ }
      }
    };
    const restore = () => {
      const url = new URL(location.href);
      search.value = url.searchParams.get('q') || '';
      const value = url.searchParams.get('topic') || 'all';
      group.value = [...group.options].some(option => option.value === value) ? value : 'all';
      filter(false);
    };
    const clear = () => { search.value = ''; group.value = 'all'; filter(); search.focus(); };
    search.addEventListener('input', () => filter());
    group.addEventListener('change', () => filter());
    document.querySelector('#clear').addEventListener('click', clear);
    document.querySelector('[data-clear]').addEventListener('click', clear);
    document.querySelectorAll('[data-query]').forEach(button => button.addEventListener('click', () => {
      search.value = button.dataset.query; group.value = 'all'; filter(); search.focus();
    }));
    document.addEventListener('keydown', event => {
      const editing = event.target.matches('input,textarea,select,[contenteditable="true"]');
      if (event.key === '/' && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
        event.preventDefault(); search.focus();
      }
      if (event.key === 'Escape' && event.target === search) clear();
    });
    window.addEventListener('popstate', restore); restore();
  }

  // 이 함수는 격리된 iframe 안에서 실행되며 출력 내용을 텍스트로만 표시한다.
  function prepareOutput(lineOffset) {
    const section = document.createElement('section');
    section.className = 'ref-console';
    const header = document.createElement('header');
    const title = document.createElement('strong'); title.textContent = 'CONSOLE';
    const count = document.createElement('span'); count.textContent = '0개 출력';
    const clear = document.createElement('button'); clear.type = 'button'; clear.id = 'clear-output';
    clear.textContent = '출력 지우기';
    header.append(title, count, clear);
    const empty = document.createElement('p'); empty.className = 'ref-empty';
    empty.textContent = '아직 출력이 없습니다. 버튼이나 입력을 조작해 보세요.';
    const output = document.createElement('pre'); output.id = 'console-output';
    output.setAttribute('role', 'log'); output.setAttribute('aria-label', 'console 출력과 오류');
    output.setAttribute('aria-live', 'polite');
    section.append(header, empty, output); document.body.append(section);
    const format = value => {
      if (typeof value === 'string') return value;
      if (typeof value === 'number') return Object.is(value, -0) ? '-0' : String(value);
      if (value instanceof Error) return value.name + ': ' + value.message;
      if (value === undefined) return 'undefined';
      if (typeof value === 'bigint') return String(value) + 'n';
      if (typeof value === 'function' || typeof value === 'symbol') return String(value);
      if (value instanceof Element) return '<' + value.tagName.toLowerCase() + (value.id ? '#' + value.id : '') + '>';
      try {
        const seen = new WeakSet();
        return JSON.stringify(value, (key, item) => {
          if (typeof item === 'bigint') return String(item) + 'n';
          if (item && typeof item === 'object') {
            if (seen.has(item)) return '[이미 표시한 참조]';
            seen.add(item);
          }
          return item;
        }) ?? String(value);
      } catch { return String(value); }
    };
    const lines = [];
    const write = (level, values) => {
      lines.push({level, text: '[' + level + '] ' + values.map(format).join(' ')});
      if (lines.length > 100) lines.shift();
      output.replaceChildren();
      lines.forEach((line, index) => {
        const item = document.createElement('span'); item.className = 'ref-line ref-' + line.level;
        item.textContent = line.text + (index < lines.length - 1 ? '\n' : '');
        output.append(item);
      });
      empty.hidden = lines.length !== 0; count.textContent = lines.length + '개 출력';
    };
    clear.addEventListener('click', () => {
      lines.length = 0; output.replaceChildren(); empty.hidden = false; count.textContent = '0개 출력';
    });
    ['log', 'warn', 'error', 'info'].forEach(level => {
      const original = console[level].bind(console);
      console[level] = (...values) => { original(...values); write(level, values); };
    });
    window.addEventListener('error', event => {
      const line = event.lineno - lineOffset;
      write('error', [event.message + (line > 0 ? ' (JavaScript ' + line + '행)' : '')]);
    });
    window.addEventListener('unhandledrejection', event => write('error', [event.reason]));
  }
  const script = text => '<script>\n' + text.replace(/<\/script/gi, '<\\/script') + '\n</script>\n';
  const documentCode = (html, js) => {
    const base = '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
      + '<meta name="viewport" content="width=device-width,initial-scale=1">'
      + '<style>body{margin:14px;font:13px/1.8 system-ui,sans-serif;color:#203b32}*{box-sizing:border-box}'
      + 'button,input,select{font:inherit;max-width:100%}button{border:1px solid #b7d3c2;border-radius:6px;background:#edf6ef;color:#24563f;padding:6px 10px;margin:3px;cursor:pointer}'
      + 'input:not([type=checkbox]){padding:6px 8px;border:1px solid #b7d3c2;border-radius:5px}'
      + 'label{display:block;margin:8px 0}p{margin:8px 0}h4{margin:12px 0 6px}'
      + ':focus-visible{outline:3px solid #bd7405;outline-offset:3px}'
      + '.ref-console{margin-top:18px;border-radius:8px;overflow:hidden;background:#182b2d;color:#dceae1}'
      + '.ref-console>header{display:flex;gap:10px;align-items:center;padding:10px 12px;border-bottom:1px solid #ffffff12}'
      + '.ref-console strong{font:10px Consolas,monospace;letter-spacing:1px;color:#adcabd}'
      + '.ref-console header span{font-size:9px;color:#adcabd;margin-left:auto}'
      + '.ref-console header button{font-size:9px;padding:2px 6px;background:transparent;color:#c3d9cd;border-color:#527269;margin:0}'
      + '#console-output{margin:0;padding:12px 14px;font:12px/1.85 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;min-height:40px}'
      + '.ref-warn{color:#edd284}.ref-error{color:#ffb8ae}.ref-info{color:#9ce0d9}.ref-empty{font-size:10px;color:#a5bfb3;padding:12px;margin:0}'
      + '[hidden]{display:none!important}</style></head><body>\n' + html + '\n';
    const bootstrap = '(' + prepareOutput.toString() + ')(LINE_OFFSET);';
    const before = base + script(bootstrap);
    const offset = before.split('\n').length;
    return base + script(bootstrap.replace('LINE_OFFSET', String(offset))) + script(js) + '</body></html>';
  };
  document.querySelectorAll('.example').forEach(example => {
    const html = example.querySelector('textarea[data-html]');
    const js = example.querySelector('[data-js]');
    const frame = example.querySelector('iframe');
    const status = example.querySelector('.status');
    const preset = example.querySelector('[data-preset]');
    const badge = example.querySelector('[data-dirty]');
    let lastRun = { html: html.value, js: js.value };
    const lineNumbers = () => [html, js].forEach(editor => {
      const type = editor === js ? 'js' : 'html';
      const gutter = example.querySelector('[data-lines="' + type + '"]');
      gutter.textContent = Array.from({length: editor.value.split('\n').length}, (_, i) => i + 1).join('\n');
      gutter.scrollTop = editor.scrollTop;
    });
    const dirty = () => {
      const changed = html.value !== lastRun.html || js.value !== lastRun.js;
      badge.dataset.state = changed ? 'dirty' : 'clean';
      badge.textContent = changed ? '실행 전 변경' : '실행 내용';
      if (changed) status.textContent = '코드가 변경되었습니다. 실행하면 결과에 반영됩니다.';
      lineNumbers();
    };
    const tab = type => {
      example.querySelectorAll('[data-editor]').forEach(panel => { panel.hidden = panel.dataset.editor !== type; });
      example.querySelectorAll('[data-tab]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.tab === type)));
      lineNumbers();
    };
    const run = () => {
      // allow-same-origin 없이 부모 문서, 저장소와 예제 상태를 분리한다.
      frame.srcdoc = documentCode(html.value, js.value);
      lastRun = { html: html.value, js: js.value }; dirty();
      status.textContent = '실행했습니다. 결과 창에서 출력과 UI 동작을 확인하세요.';
    };
    const loadSample = () => {
      const option = preset.selectedOptions[0];
      js.value = option.dataset.code; html.value = option.dataset.html;
      example.querySelector('p[data-expected]').textContent = option.dataset.expected;
      run(); tab('js');
    };
    example.querySelectorAll('[data-tab]').forEach(button => button.addEventListener('click', () => tab(button.dataset.tab)));
    for (const editor of [html, js]) {
      editor.addEventListener('input', dirty); editor.addEventListener('scroll', lineNumbers);
      editor.addEventListener('keydown', event => {
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && !event.isComposing) {
          event.preventDefault(); run();
        }
      });
    }
    preset.addEventListener('change', loadSample);
    example.querySelector('[data-run]').addEventListener('click', run);
    example.querySelector('[data-reset]').addEventListener('click', () => {
      loadSample(); status.textContent = '선택한 예제의 원본 코드로 초기화했습니다.';
    });
    example.querySelector('[data-width]').addEventListener('change', event => { frame.style.width = event.target.value; });
    example.querySelector('[data-copy]').addEventListener('click', async () => {
      const content = documentCode(html.value, js.value);
      try {
        await navigator.clipboard.writeText(content);
        status.textContent = '실행 가능한 전체 HTML 예제를 복사했습니다.';
      } catch {
        let fallback = example.querySelector('[data-copy-fallback]');
        if (!fallback) {
          const label = document.createElement('label'); label.className = 'copy-label';
          label.htmlFor = 'copy-fallback'; label.textContent = '전체 예제 수동 복사';
          fallback = document.createElement('textarea'); fallback.id = 'copy-fallback';
          fallback.dataset.copyFallback = ''; fallback.readOnly = true; fallback.rows = 8;
          fallback.className = 'copy-fallback'; example.append(label, fallback);
        }
        fallback.value = content; fallback.focus(); fallback.select();
        status.textContent = '자동 복사가 제한되어 전체 코드를 선택했습니다. Ctrl+C로 복사하세요.';
      }
    });
    run(); tab('js');
  });
})();
