// 일반 스크립트를 사용해 file://에서도 검색과 실행이 동작한다.
(() => {
  'use strict';
  const search = document.querySelector('#search');
  if (search) {
    const cards = [...document.querySelectorAll('.card')];
    const group = document.querySelector('#group');
    const filter = () => {
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
    };
    search.addEventListener('input', filter);
    group.addEventListener('change', filter);
    document.querySelector('#clear').addEventListener('click', () => {
      search.value = ''; group.value = 'all'; filter(); search.focus();
    });
  }

  // 이 함수는 iframe 내부에서만 실행된다. 출력은 HTML이 아닌 텍스트로 표시한다.
  function prepareOutput() {
    const output = document.createElement('pre');
    output.id = 'console-output';
    output.setAttribute('role', 'log');
    output.setAttribute('aria-label', 'console 출력과 오류');
    document.body.append(output);
    const format = value => {
      if (typeof value === 'string') return value;
      if (value instanceof Error) return value.name + ': ' + value.message;
      if (value === undefined) return 'undefined';
      if (typeof value === 'bigint') return String(value) + 'n';
      if (typeof value === 'function' || typeof value === 'symbol') return String(value);
      try { return JSON.stringify(value) ?? String(value); }
      catch { return String(value); }
    };
    const lines = [];
    const write = (level, values) => {
      lines.push('[' + level + '] ' + values.map(format).join(' '));
      if (lines.length > 100) lines.shift();
      output.textContent = lines.join('\n');
    };
    ['log', 'warn', 'error', 'info'].forEach(level => {
      const original = console[level].bind(console);
      console[level] = (...values) => { original(...values); write(level, values); };
    });
    window.addEventListener('error', event => write('error', [event.message]));
    window.addEventListener('unhandledrejection', event => write('error', [event.reason]));
  }

  // JavaScript를 별도 script로 넣어 구문 오류도 먼저 등록한 error 핸들러로 표시한다.
  const script = text => '<script>' + text.replace(/<\/script/gi, '<\\/script') + '</script>';
  const documentCode = (html, js) => '<!doctype html><html lang="ko"><head>'
    + '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    + '<style>body{margin:16px;font:16px/1.7 system-ui,sans-serif;color:#1c3047}'
    + '*{box-sizing:border-box}button,input,select{font:inherit;max-width:100%}'
    + 'button{padding:6px 12px;margin:4px;cursor:pointer}label{display:block;margin:8px 0}'
    + 'pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf2f8;padding:12px;min-height:45px}'
    + ':focus-visible{outline:3px solid #c37a05;outline-offset:3px}</style></head><body>'
    + html + script('(' + prepareOutput.toString() + ')();') + script(js) + '</body></html>';
  document.querySelectorAll('.example').forEach(example => {
    const html = example.querySelector('[data-html]');
    const js = example.querySelector('[data-js]');
    const frame = example.querySelector('iframe');
    const status = example.querySelector('.status');
    const original = { html: html.value, js: js.value };
    const run = () => {
      // allow-same-origin 없이 부모 페이지 DOM과 저장소 접근을 분리한다.
      frame.srcdoc = documentCode(html.value, js.value);
      status.textContent = '실행했습니다. 아래 미리보기에서 결과와 이벤트를 확인하세요.';
    };
    example.querySelector('[data-run]').addEventListener('click', run);
    example.querySelector('[data-reset]').addEventListener('click', () => {
      html.value = original.html; js.value = original.js; run();
      status.textContent = '원본 코드로 초기화했습니다.';
    });
    example.querySelector('[data-width]').addEventListener('change', event => {
      frame.style.width = event.target.value;
    });
    example.querySelector('[data-copy]').addEventListener('click', async () => {
      const content = documentCode(html.value, js.value);
      try {
        await navigator.clipboard.writeText(content);
        status.textContent = '실행 가능한 전체 HTML 예제를 복사했습니다.';
      } catch {
        // file://나 브라우저 권한으로 복사가 막혀도 전체 예제를 수동 복사할 수 있다.
        let fallback = example.querySelector('[data-copy-fallback]');
        if (!fallback) {
          const label = document.createElement('label');
          label.htmlFor = 'copy-fallback'; label.textContent = '전체 예제 수동 복사';
          fallback = document.createElement('textarea');
          fallback.id = 'copy-fallback'; fallback.dataset.copyFallback = '';
          fallback.readOnly = true; fallback.rows = 8;
          example.append(label, fallback);
        }
        fallback.value = content; fallback.focus(); fallback.select();
        status.textContent = '자동 복사가 제한되어 전체 코드를 선택했습니다. Ctrl+C로 복사하세요.';
      }
    });
    run();
  });
})();
