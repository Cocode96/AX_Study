// 서버와 외부 라이브러리 없이 file://에서도 동작한다.
// 검색은 정적 카드의 키워드만 읽는다. 본문은 JavaScript 없이도 열람 가능하다.
(() => {
  const search = document.querySelector('#search');
  if (search) {
    const cards = [...document.querySelectorAll('.topic-card')];
    const buttons = [...document.querySelectorAll('[data-filter]')];
    let group = 'all';
    const topic = document.querySelector('#topic-filter');
    const filter = () => {
      const words = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const match = (group === 'all' || card.dataset.group === group) && (!topic || topic.value === 'all' || card.dataset.topic === topic.value) && words.every(word => card.dataset.search.includes(word));
        card.hidden = !match;
        if (match) count++;
      });
      document.querySelector('#count').textContent = count + '개 항목';
      document.querySelector('#empty').hidden = count !== 0;
    };
    search.addEventListener('input', filter);
    topic?.addEventListener('change', filter);
    buttons.forEach(button => button.addEventListener('click', () => {
      group = button.dataset.filter; if (topic) topic.value = 'all';
      buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      filter();
    }));
    document.querySelector('#clear-search').addEventListener('click', () => {
      search.value = ''; group = 'all'; if (topic) topic.value = 'all';
      buttons.forEach(item => item.setAttribute('aria-pressed', String(item.dataset.filter === 'all')));
      filter(); search.focus();
    });
  }
  // 편집 코드는 same-origin 권한이 없는 sandbox iframe에서만 실행한다.
  // 원본 HTML 파일을 수정하거나 서버에 저장하지 않는다.
  const wrap = code => /<!doctype|<html[\s>]/i.test(code) ? code :
    '<!doctype html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<style>body{margin:16px;font:16px/1.7 sans-serif;color:#182b40}*,*::before,*::after{box-sizing:border-box}button,input,select,textarea{font:inherit}button{cursor:pointer}img{max-width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere}:focus-visible{outline:3px solid #a45200;outline-offset:3px}</style></head><body>' + code + '</body></html>';
  document.querySelectorAll('.example').forEach(example => {
    const frame = example.querySelector('iframe');
    const editor = example.querySelector('textarea');
    const original = editor.value;
    const preset = example.querySelector('[data-preset]');
    preset?.addEventListener('change', () => {
      editor.value = preset.selectedOptions[0].dataset.code;
      frame.srcdoc = wrap(editor.value);
      example.querySelector('.status').textContent = '선택한 값의 코드와 결과를 적용했습니다.';
    });
    example.querySelector('[data-copy]')?.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(editor.value); example.querySelector('.status').textContent = '코드를 복사했습니다.'; }
      catch { editor.focus(); editor.select(); example.querySelector('.status').textContent = '자동 복사가 제한되어 코드를 선택했습니다. Ctrl+C로 복사할 수 있습니다.'; }
    });
    const width = example.querySelector('[data-width]');
    const status = example.querySelector('.status');
    example.querySelector('[data-apply]').addEventListener('click', () => {
      frame.srcdoc = wrap(editor.value);
      status.textContent = '수정한 코드를 적용했습니다. 원본 파일에는 저장되지 않습니다.';
    });
    example.querySelector('[data-reset]').addEventListener('click', () => {
      editor.value = original; frame.srcdoc = wrap(original); if (preset) preset.selectedIndex = 0;
      width.value = 100; frame.style.width = '100%';
      example.querySelector('output').value = '100%';
      status.textContent = '원래 예제와 미리보기 너비로 복원했습니다.';
    });
    width.addEventListener('input', () => {
      frame.style.width = width.value + '%';
      example.querySelector('output').value = width.value + '%';
    });
  });
})();
