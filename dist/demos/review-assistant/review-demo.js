(() => {
 const root=document.querySelector('.review-demo'); if(!root)return;
 const $=s=>root.querySelector(s), $$=s=>[...root.querySelectorAll(s)];
 const base='/demos/review-assistant/';
 const issues=[
  {id:1,title:'底部操作由横向改为纵向',kind:'明确差异',description:'设计稿的“直接退出 / 打开游戏”为并列双按钮；开发截图为上下排列，操作层级与布局发生变化。',box:[4,62,92,35]},
  {id:2,title:'主按钮的颜色与样式不一致',kind:'明确差异',description:'设计稿采用白底深色文字；开发截图采用红色圆角填充与白色文字，需核对按钮规范。',box:[7,64,86,18]},
  {id:3,title:'游戏图标素材不同',kind:'待确认',description:'赛车图标替换为活动主题图。可能属于动态内容，需核对是否为同一游戏与场景，不直接判为还原错误。',box:[39,10,22,26]},
  {id:4,title:'左上角新增悬浮标识',kind:'待确认',description:'开发截图包含蓝色“息流”标识，设计稿未出现。需确认其是否为录屏、宿主或调试环境附加元素。',box:[18,0,19,19]}
 ];
 const prompt='图1是设计稿，图2是开发还原截图，帮我走查并记录走查文档';
 let mode='web',timers=[],epoch=0,webDone=false,skillDone=false,selected=1,showSuspected=false;
 const cancel=()=>{epoch++;timers.forEach(clearTimeout);timers=[];};
 const later=(fn,ms)=>{const e=epoch;timers.push(setTimeout(()=>{if(e===epoch)fn();},ms));};
 const escape=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function table(){return `<table class="rd-mini-table"><thead><tr><th>编号</th><th>问题</th><th>判断</th></tr></thead><tbody>${issues.map(i=>`<tr><td>0${i.id}</td><td>${i.title}</td><td>${i.kind}</td></tr>`).join('')}</tbody></table>`;}
 function boxes(){return issues.filter(i=>i.id<=2||showSuspected).map(i=>`<span class="rd-box ${i.id>2?'suspected':''} ${selected===i.id?'selected':''}" style="left:${i.box[0]}%;top:${i.box[1]}%;width:${i.box[2]}%;height:${i.box[3]}%"><b>${i.id}</b></span>`).join('');}
 function syncReport(){const grid=$('.rd-report-grid'),col=$('.rd-image-column');if(!grid||$('.rd-report').hidden||mode!=='web')return;const width=Math.min(col.clientWidth,innerWidth<=650?170:grid.clientHeight*900/788);root.style.setProperty('--rd-result-width',width+'px');root.style.setProperty('--rd-result-height',width*788/900+'px');}
 new ResizeObserver(()=>requestAnimationFrame(syncReport)).observe($('.rd-stage'));
 function renderReport(){requestAnimationFrame(syncReport);
  $('.rd-report').innerHTML=`<div class="rd-report-header"><strong>走查报告 <small>固定示例</small></strong><small>2 条明确差异 · 2 条待确认</small></div><div class="rd-report-grid"><div class="rd-image-column"><div class="rd-annotated"><img src="${base}development.png" alt="开发截图及问题区域标注">${boxes()}</div></div><div class="rd-issues">${issues.map(i=>`<button type="button" class="rd-issue ${i.id>2?'suspected':''} ${i.id===selected?'selected':''}" data-issue="${i.id}"><small>${i.kind} / 0${i.id}</small><strong> ${i.title}</strong><p>${i.description}</p></button>`).join('')}</div></div>`;
 }
 function restoreWeb(){ $('.rd-group').hidden=webDone;$('.rd-web-footer').hidden=webDone;requestAnimationFrame(syncReport);$('.rd-progress').hidden=true;$('.rd-inputs').hidden=webDone;$('.rd-report').hidden=!webDone;$('.rd-run').disabled=false;$('.rd-run').textContent=webDone?'↻ 重新走查':'✧ AI 走查';$('.rd-ready').textContent='● 就绪'; }
 function switchMode(next){if($('.rd-skill-progress'))resetSkill();cancel();mode=next;restoreWeb();$('.rd-composer button[type=submit]').disabled=skillDone;$('.rd-composer textarea').disabled=skillDone;$('.rd-skill-progress')?.remove();$$('[data-mode]').forEach(b=>{const on=b.dataset.mode===mode;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;});$('#rd-web').hidden=mode!=='web';$('#rd-skill').hidden=mode!=='skill';}
 function resetSkill(){skillDone=false;$('.rd-composer').classList.remove('is-sent');$('.rd-messages').innerHTML='<div class="rd-welcome"><span>从一句指令，到一份走查记录。</span><p>对比设计稿与开发截图，识别差异并整理问题。</p></div>';$('#rd-prompt').value=prompt;$('#rd-prompt').rows=2;$('#rd-prompt').placeholder='输入走查指令…';$('.rd-composer button[type=submit]').disabled=false;$('#rd-prompt').disabled=false;}
 function reset(){cancel();webDone=false;selected=1;showSuspected=false;resetSkill();$('.rd-report').innerHTML='';restoreWeb();}
 function runWeb(){cancel();$('.rd-web-footer').hidden=false;$('.rd-group').hidden=false;$('.rd-run').disabled=true;$('.rd-ready').textContent='◌ 分析中';$('.rd-inputs').hidden=false;$('.rd-report').hidden=true;$('.rd-progress').hidden=false;const stages=['对齐设计稿与开发截图','识别布局与视觉差异','区分真实问题与待确认内容'];const progress=n=>{$('.rd-progress').innerHTML=`${stages[n]}… <small>模拟执行 ${n+1}/3</small><progress value="${(n+1)*30}" max="100"></progress>`;};progress(0);later(()=>progress(1),650);later(()=>progress(2),1300);later(()=>{webDone=true;renderReport();restoreWeb();$('.rd-ready').textContent='● 已完成';},2000);}
 function runSkill(e){e.preventDefault();if(skillDone||!$('#rd-prompt').value.trim())return;cancel();const sentPrompt=$('#rd-prompt').value.trim();const attachments=$('.rd-attachments').outerHTML;$('#rd-prompt').value='';$('#rd-prompt').rows=1;$('#rd-prompt').placeholder='正在走查…';$('.rd-composer').classList.add('is-sent');$('.rd-composer button[type=submit]').disabled=true;$('#rd-prompt').disabled=true;$('.rd-messages').innerHTML=`<div class="rd-bubble user">${attachments}${escape(sentPrompt)}</div><div class="rd-bubble assistant rd-skill-progress" role="status"><strong>正在执行走查 Skill</strong><ol><li>对比默认设计稿与开发截图…</li></ol></div>`;later(()=>{$('.rd-skill-progress ol').innerHTML='<li>已识别布局与按钮样式差异</li><li>正在整理问题与待确认内容…</li>';},800);later(()=>{skillDone=true;$('#rd-prompt').placeholder='已发送，重置后可再次体验';$('.rd-skill-progress').outerHTML=`<div class="rd-bubble assistant"><strong>已生成「游戏弹窗设计验收」示例走查表</strong><p>共 4 条记录：2 条明确差异，2 条待确认。已整理问题描述与对应区域，供人工复核。</p>${table()}<p>以上为固定示例，未调用 AI，也未写入飞书。</p></div>`;$('.rd-messages').scrollTop=$('.rd-messages').scrollHeight;},1900);}
 const dialog=$('.rd-dialog');
 function openDialog(title,content){$('.rd-dialog-head strong').textContent=title;$('.rd-dialog-body').innerHTML=content;dialog.showModal();}
 root.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.mode)switchMode(b.dataset.mode);if(b.classList.contains('rd-reset'))reset();if(b.classList.contains('rd-run'))runWeb();if(b.dataset.image){const design=b.dataset.image==='design';openDialog(design?'默认素材 / 设计稿':'默认素材 / 开发截图',`<img src="${base}${design?'design':'development'}.png" alt="${design?'设计稿':'开发截图'}原图">`);}if(b.dataset.issue){selected=Number(b.dataset.issue);if(selected>2)showSuspected=true;const scroll=$('.rd-issues').scrollTop;renderReport();$('.rd-issues').scrollTop=scroll;$('.rd-issue[data-issue="'+selected+'"]').focus({preventScroll:true});} });
 $('.rd-modes').addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(e.key)){e.preventDefault();switchMode(e.key==='Home'?'web':e.key==='End'?'skill':mode==='web'?'skill':'web');$('[data-mode="'+mode+'"]').focus();}});

 $('.rd-composer').addEventListener('submit',runSkill);$('#rd-prompt').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();$('.rd-composer').requestSubmit();}});
 $('.rd-dialog-head button').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
})();
