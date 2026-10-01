// catalog.json을 정적 HTML로 만든다. 런타임에는 Node나 fetch가 필요 없다.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname,'..');
const {groups,entries} = JSON.parse(fs.readFileSync(path.join(root,'data/catalog.json'),'utf8'));
const escape = value => String(value).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const pad=n=>String(n).padStart(2,'0');
const icon='<span class="brand-icon" aria-hidden="true">JS</span>';
const footer=`<footer class="site-footer"><span>AX STUDY / JavaScript Reference</span><span>설치 없이 읽고, 수정하고, 실행하기</span></footer>`;
function page(title,sidebar,body,prefix=''){
 return `<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="JavaScript 기초부터 DOM과 이벤트까지, 키워드 설명과 비교 가능한 실행 예제"><title>${escape(title)} | JavaScript 참고서</title><link rel="stylesheet" href="${prefix}assets/reference.css"><script defer src="${prefix}assets/reference.js"></script></head>
<body><a class="skip" href="#content">본문으로 이동</a>
<header class="site-header"><a class="brand" href="${prefix}index.html">${icon}<span>JavaScript <strong>참고서</strong></span></a><nav aria-label="참고 자료"><a href="${prefix}index.html">키워드 찾기</a><a href="${prefix}README.md">사용 안내</a><a href="${prefix}../../07_frontend_basic/html-css-reference/index.html">HTML / CSS ↗</a></nav></header>
<div class="layout"><aside class="sidebar">${sidebar}</aside><main id="content">${body}${footer}</main></div>
</body></html>\n`;
}
const groupNames=groups.map(g=>g.replace('이벤트 등록과 제어','등록과 이벤트 흐름').replace('입력과 브라우저 이벤트','입력과 브라우저'));
const topics=groups.map((g,i)=>`<a href="#group-${i}"><span class="nav-number">${pad(i+1)}</span>${escape(groupNames[i])}<span class="nav-count">${entries.filter(e=>e.group===i).length}</span></a>`).join('\n');
const side=`<p class="side-label">REFERENCE INDEX</p><details class="topic-nav" open><summary>주제별 탐색</summary><nav aria-label="주제별 탐색">${topics}</nav></details><div class="side-note"><span class="status-dot"></span>오프라인 실행 가능<p>파일을 열면 바로 사용할 수 있다. 원문 링크는 인터넷 연결이 필요하다.</p></div>`;
const card=(e,i)=>`<article class="card" data-group="${e.group}" data-search="${escape([e.name,e.desc,e.note,e.syntax,e.use,e.input,e.result,e.pitfall].join(' ').toLowerCase())}"><div class="card-meta"><span>${(e.kind!=='language' && e.group>=6)?'BROWSER API':'JAVASCRIPT'}</span><span>${pad(i+1)}</span></div><h3><a href="entries/${e.id}.html">${escape(e.name)}</a></h3><p>${escape(e.desc)}</p><div class="card-bottom"><span>기본 + 비교 예제</span><span aria-hidden="true">↗</span></div></article>`;
const indexBody=`<section class="hero"><div><p class="eyebrow"><span class="status-dot"></span>코드 옆에 두고 쓰는 참고서</p><h1>찾고, 바꾸고,<br><span>동작을 확인한다.</span></h1><p class="lead">JavaScript 기초부터 DOM, 이벤트와 AJAX까지.<br>문법 설명과 실행 결과를 한 화면에서 비교한다.</p><div class="hero-stats"><div><strong>${entries.length}</strong><span>키워드</span></div><div><strong>${entries.length*2}</strong><span>실행 예제</span></div><div><strong>${groups.length}</strong><span>주제</span></div></div></div><div class="hero-code"><div class="code-heading"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span><span>click-event.js</span></div><pre><code><span class="code-comment">// 버튼을 누르면 문구를 변경한다.</span>
<span class="code-keyword">const</span> button = document.<span class="code-function">querySelector</span>(<span class="code-string">'#button'</span>);

button.<span class="code-function">addEventListener</span>(<span class="code-string">'click'</span>, () =&gt; {
  button.textContent = <span class="code-string">'실행 완료'</span>;
});</code></pre><a href="entries/add-event-listener.html">이 예제를 직접 실행하기 <span aria-hidden="true">→</span></a></div></section>
<section class="search-panel" aria-label="키워드 검색"><div class="search-row"><div class="search-field"><label for="search">어떤 키워드를 찾고 있나요?</label><div class="search-input"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="map, 버블링, 반환값, 입력, 배열" autocomplete="off"><kbd aria-hidden="true">/</kbd></div></div><div class="select-field"><label for="group">주제 범위</label><select id="group"><option value="all">모든 주제</option>${groups.map((g,i)=>`<option value="${i}">${escape(g)}</option>`).join('')}</select></div><button id="clear" class="button quiet" type="button">초기화</button></div><div class="search-footer"><p id="count" role="status">${entries.length}개 항목</p><div class="quick-search" aria-label="빠른 검색"><span>바로 찾기</span>${['배열','함수','이벤트','AJAX'].map(word=>`<button type="button" data-query="${word}">${word}</button>`).join('')}</div></div><noscript>검색과 실행에는 JavaScript가 필요하다. 아래 링크, 설명과 코드 원문은 계속 읽을 수 있다.</noscript></section>
<div id="empty" class="empty-state" hidden><h2>찾는 항목이 없습니다.</h2><p>영문 키워드나 짧은 한글 개념으로 다시 검색하세요.</p><button type="button" data-clear>검색 초기화</button></div>
${groups.map((g,i)=>`<section class="group-section" id="group-${i}" aria-labelledby="heading-${i}"><div class="section-heading"><div><p class="eyebrow">CHAPTER ${pad(i+1)}</p><h2 id="heading-${i}">${escape(g)}</h2></div><span>${entries.filter(e=>e.group===i).length}개 항목</span></div><div class="grid">${entries.filter(e=>e.group===i).map(e=>card(e,entries.indexOf(e))).join('\n')}</div></section>`).join('\n')}
<section class="scope-note"><h2>이번 참고서의 범위</h2><p>변수와 함수, Promise와 async/await 같은 JavaScript 언어 문법을 DOM, 이벤트, fetch 같은 브라우저 API와 구분해 다룬다. AJAX의 부분 갱신 예제는 오프라인에서도 동작한다. 모듈과 저장소 API는 이번 범위에 포함하지 않는다.</p><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide">MDN JavaScript Guide ↗</a></section>`;
fs.writeFileSync(path.join(root,'index.html'),page('키워드 찾기',side,indexBody));

const relatedIds={
 'const':['let','array','spread-rest'], 'let':['const','scope','closure'],
 'map':['foreach','filter','arrow','spread-rest'], 'foreach':['map','for-of','callback'],
 'filter':['find','map','equality'], 'find':['filter','nullish','equality'],
 'callback':['function','arrow','add-event-listener'], 'this':['arrow','event-object','function'],
 'query-selector':['query-selector-all','dom-ready','text-content'],
 'propagation':['event-object','stop-propagation','prevent-default','delegation'],
 'stop-propagation':['propagation','prevent-default','event-object'],
 'prevent-default':['submit','stop-propagation','listener-options'],
 'delegation':['event-object','traversal','create-element','propagation'],
 'event-object':['add-event-listener','propagation','delegation'],
 'submit':['prevent-default','input-change','keyboard'],
 'listener-options':['add-event-listener','remove-event-listener','prevent-default'],
 'input-change':['conversion','submit','keyboard'], 'keyboard':['input-change','click','submit']
 ,'ajax':['fetch','async-await','request-state','http-errors'],
 'promise':['async-await','event-loop','callback'],
 'async-await':['promise','fetch','try-catch','event-loop'],
 'fetch':['response-json','http-errors','abort-request','ajax'],
 'response-json':['fetch','json','http-errors'],
 'http-errors':['fetch','response-json','try-catch'],
 'abort-request':['request-state','fetch','listener-options'],
 'request-state':['abort-request','async-await','ajax']
};
const editor=(type,value)=>`<div class="editor-panel" data-editor="${type}"><label class="sr-only" for="${type==='js'?'javascript':'html'}">${type==='js'?'JavaScript':'HTML / CSS'}</label><div class="code-editor"><pre class="line-numbers" aria-hidden="true" data-lines="${type}">1</pre><textarea id="${type==='js'?'javascript':'html'}" data-${type} spellcheck="false" wrap="off" rows="14">${escape(value)}</textarea></div></div>`;
fs.mkdirSync(path.join(root,'entries'),{recursive:true});
entries.forEach((e,index)=>{
 const samples=[{title:'기본 예제',code:e.code,html:e.html,expected:e.expected},e.alternate];
 const related=(relatedIds[e.id]||entries.filter(x=>x.group===e.group&&x!==e).slice(0,4).map(x=>x.id)).map(id=>entries.find(x=>x.id===id));
 const sideEntry=`<a class="back-link" href="../index.html">← 전체 키워드</a><p class="side-label">${escape(groups[e.group])}</p><nav class="entry-toc" aria-label="이 페이지 목차"><a href="#overview">01 핵심 이해</a><a href="#syntax">02 문법과 값</a><a href="#playground">03 실행과 비교</a><a href="#pitfalls">04 자주 헷갈리는 점</a><a href="#related">05 연결해서 보기</a></nav><div class="side-note"><span class="status-dot"></span>${(e.kind!=='language' && e.group>=6)?'브라우저 API':'JavaScript 언어'}<p>${(e.kind!=='language' && e.group>=6)?'DOM과 이벤트는 브라우저가 제공하는 기능이다.':'변수와 연산, 함수는 JavaScript 자체의 기능이다.'}</p></div>`;
 const eventDiagram=e.id==='propagation'?`<div class="event-flow" aria-label="이벤트 전파 순서"><div><span>01 CAPTURE</span><strong>조상 → 대상</strong><p>부모 capture 핸들러</p></div><span aria-hidden="true">→</span><div><span>02 TARGET</span><strong>실제 발생 요소</strong><p>대상 capture와 bubble 핸들러</p></div><span aria-hidden="true">→</span><div><span>03 BUBBLE</span><strong>대상 → 조상</strong><p>부모 bubble 핸들러</p></div></div>`:'';
 const networkExample = e.id==='ajax' ? `<section class="doc-section"><p class="eyebrow">실제 서버에 연결할 때</p><h2>같은 흐름에서 요청 URL을 바꾼다</h2><p class="network-note">위 기본 예제의 data URL은 브라우저 내부 데이터다. 실제 서버 요청은 HTTP로 열린 페이지에서 아래처럼 API URL을 사용한다. 아래 코드는 서버 연결용 참고 코드이며 자동 실행하지 않는다. API는 [{"name":"HTML"}, {"name":"JavaScript"}] 형태의 JSON 배열을 반환한다고 가정한다.</p><pre class="syntax"><code>${escape(`async function loadFromServer() {
  const response = await fetch('/api/items');
  if (!response.ok) throw new Error('HTTP ' + response.status);
  const items = await response.json();
  const nodes = items.map(item => {
    const li = document.createElement('li');
    li.textContent = item.name;
    return li;
  });
  document.querySelector('#list').replaceChildren(...nodes);
}
loadFromServer().catch(error => {
  document.querySelector('#status').textContent = error.message;
});`)}</code></pre><p class="network-note">실제 API 주소와 응답 구조를 확인해 맞춘다. 다른 출처의 서버에는 서버 측 CORS 허용이 필요하다. mode: 'no-cors'로 JSON을 읽을 수 있게 되는 것은 아니다.</p></section>` : '';
 const body=`<nav class="breadcrumbs" aria-label="현재 위치"><a href="../index.html">JavaScript</a><span aria-hidden="true">/</span><a href="../index.html#group-${e.group}">${escape(groups[e.group])}</a></nav>
<header class="entry-heading"><p class="eyebrow">${(e.kind!=='language' && e.group>=6)?'BROWSER API':'JAVASCRIPT'} / ${pad(index+1)}</p><h1>${escape(e.name)}</h1><p class="lead">${escape(e.desc)}</p><div class="tags"><span>주석 있는 예제</span><span>기본 / 비교 2가지</span><a href="${e.source}" target="_blank" rel="noopener">MDN 원문 ↗</a></div></header>
<section id="overview" class="overview"><div class="overview-primary"><p class="eyebrow">이럴 때 사용한다</p><h2>${escape(e.use)}</h2><p>${escape(e.note)}</p></div><div class="overview-secondary"><p class="eyebrow">먼저 구분할 것</p><p>${escape(e.pitfall)}</p></div></section>
<section id="syntax" class="doc-section"><div class="section-heading"><div><p class="eyebrow">01 / SYNTAX</p><h2>문법과 값의 흐름</h2></div></div><pre class="syntax"><code>${escape(e.syntax)}</code></pre><dl class="contract"><div><dt>입력 / 조건</dt><dd>${escape(e.input)}</dd></div><div><dt>결과 / 반환값</dt><dd>${escape(e.result)}</dd></div><div><dt>원본 / 상태 변경</dt><dd>${escape(e.mutation)}</dd></div></dl>${eventDiagram}</section>
<section id="playground" class="example doc-section"><div class="section-heading"><div><p class="eyebrow">02 / PLAYGROUND</p><h2>코드와 결과를 함께 보기</h2></div><span class="live-pill"><span class="status-dot"></span>브라우저 실행</span></div><div class="sample-bar"><label for="preset">예제 선택</label><select id="preset" data-preset>${samples.map((s,i)=>`<option value="${i}" data-code="${escape(s.code)}" data-html="${escape(s.html)}" data-expected="${escape(s.expected)}">${escape(s.title)}</option>`).join('')}</select><span class="sample-note">비교 예제에서 경계 조건과 차이를 확인한다.</span></div>
<div class="playground-grid"><div class="editor-column"><div class="pane-header"><div class="editor-tabs" role="group" aria-label="편집할 코드"><button type="button" data-tab="js" aria-pressed="true">JavaScript</button><button type="button" data-tab="html" aria-pressed="false">HTML / CSS</button></div><span data-dirty class="dirty-badge">원본</span></div>${editor('js',e.code)}${editor('html',e.html)}<div class="editor-toolbar"><button type="button" class="button primary" data-run>▶ 실행 <kbd>Ctrl ↵</kbd></button><button type="button" class="button subtle" data-reset>원본으로 초기화</button><button type="button" class="button subtle" data-copy>전체 예제 복사</button></div></div><div class="result-column"><div class="pane-header"><h3>실행 결과</h3><label class="width-control" for="width">폭 <select id="width" data-width><option value="100%">자동</option><option value="360px">360px</option></select></label></div><div class="frame-wrap"><iframe title="${escape(e.name)} 실행 결과" sandbox="allow-scripts allow-forms"></iframe></div></div></div>
<p class="status" role="status"></p><div class="expected"><strong>기대 결과</strong><p data-expected>${escape(e.expected)}</p></div><p class="playground-help">${e.html?'버튼, 입력 등은 오른쪽 미리보기에서 직접 조작한다.':'console 출력은 오른쪽 결과 창에 표시된다.'} 수정 후 실행하거나 Ctrl+Enter를 누른다. 수정 내용은 파일에 자동 저장되지 않는다.</p><noscript>아래 비교 예제 코드는 JavaScript를 켜지 않아도 읽을 수 있다.</noscript><details class="alternate-source"><summary>비교 예제 원문: ${escape(e.alternate.title)}</summary>${e.alternate.html?`<h3>HTML / CSS</h3><pre><code>${escape(e.alternate.html)}</code></pre>`:''}<h3>JavaScript</h3><pre><code>${escape(e.alternate.code)}</code></pre><p>기대 결과: ${escape(e.alternate.expected)}</p></details></section>
${networkExample}<section id="pitfalls" class="doc-section pitfall-section"><p class="eyebrow">03 / TROUBLESHOOTING</p><h2>이 항목에서 자주 헷갈리는 점</h2><p>${escape(e.pitfall)}</p><details><summary>오류 메시지로 확인할 위치</summary><dl class="error-guide"><div><dt>ReferenceError</dt><dd>이름 오타, 선언 위치와 선언 전 접근을 확인한다.</dd></div><div><dt>TypeError</dt><dd>null이나 undefined인지, 해당 타입에서 호출 가능한 메서드인지 확인한다.</dd></div><div><dt>SyntaxError</dt><dd>괄호, 따옴표, 쉼표와 문법을 확인한다. 구문 오류는 예제 실행 전에 표시된다.</dd></div></dl></details></section>
<section id="related" class="doc-section"><p class="eyebrow">04 / CONNECTIONS</p><h2>연결해서 보기</h2><div class="related-grid">${related.map(x=>`<a class="related-card" href="${x.id}.html"><strong>${escape(x.name)}</strong><span>${escape(x.desc)}</span><span aria-hidden="true">→</span></a>`).join('')}</div></section><nav class="page-turn" aria-label="앞뒤 키워드">${index?`<a href="${entries[index-1].id}.html"><small>이전 키워드</small><strong>← ${escape(entries[index-1].name)}</strong></a>`:'<span></span>'}${index+1<entries.length?`<a href="${entries[index+1].id}.html"><small>다음 키워드</small><strong>${escape(entries[index+1].name)} →</strong></a>`:''}</nav>`;
 fs.writeFileSync(path.join(root,'entries',e.id+'.html'),page(e.name,sideEntry,body,'../'));
});
console.log(`Built ${entries.length} entries / ${entries.length*2} examples`);
