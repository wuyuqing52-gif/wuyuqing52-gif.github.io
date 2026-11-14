# -*- coding: utf-8 -*-
from pathlib import Path
from html import escape as e
import base64
import json
from review_visuals import render_visual

def render_block(b):
 t=b['type']
 if t=='visual':return render_visual(b['name'])
 if t=='diagram':
  return (f'<figure class="review-diagram" tabindex="0" role="region" aria-label="{e(b["caption"])}">'
          f'<img src="/assets/edition3/{e(b["name"])}.svg" alt="{e(b["caption"])}" loading="lazy"></figure>')
 if t=='media':
  images = []
  for image in b['images']:
   src, label = image['src'], image['label']
   images.append(f'<a href="{e(src)}" data-image-preview data-image-title="{e(label)}" aria-label="放大{e(label)}">'
                 f'<img src="{e(src)}" alt="{e(label)}" loading="lazy" decoding="async"></a>')
  ratio = b.get('ratio', 'auto')
  return (f'<figure class="review-media"><figcaption>{e(b["caption"])}</figcaption>'
          f'<div class="review-media-images" style="--review-media-ratio:{e(ratio)}">'
          + ''.join(images) + '</div></figure>')
 if t=='obstacles':
  items = []
  for index,label in enumerate(b['items'],1):
   asset = Path(__file__).parent / 'dist/assets/edition3' / f'lynx-obstacle-{index}.webp'
   image = base64.b64encode(asset.read_bytes()).decode('ascii')
   items.append(f'<div><img src="data:image/webp;base64,{image}" alt="" width="81" height="81">'
                f'<p>{e(label)}</p></div>')
  return '<div class="review-obstacles">'+''.join(items)+'</div>'
 if t=='image':return '<figure class="review-source-image"><a href="'+e(b['src'])+'" target="_blank" rel="noopener" aria-label="查看原图：'+e(b['caption'])+'"><img src="'+e(b['src'])+'" alt="'+e(b['caption'])+'" loading="lazy"></a><figcaption>'+e(b['caption'])+'</figcaption></figure>'
 if t=='heading':return '<h3 class="review-stage-heading">'+e(b['text'])+'</h3>'
 if t=='paragraph':return '<p>'+e(b['text'])+'</p>'
 if t in ['list','steps']:
  tag='ol' if t=='steps' else 'ul'
  return f'<{tag} class="chapter-list">'+''.join('<li>'+e(i)+'</li>' for i in b['items'])+f'</{tag}>'
 if t=='table':
  return '<div class="chapter-table-wrap" tabindex="0" role="region" aria-label="'+e('、'.join(b['headers']))+'"><table><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(c)+'</td>' for c in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
 if t=='note':return '<aside class="chapter-note"><h3>'+e(b['title'])+'</h3><p>'+e(b['text'])+'</p></aside>'
 if t=='link':return '<a class="primary-button" href="'+e(b['url'])+'" target="_blank" rel="noopener noreferrer">'+e(b['label'])+' <span>↗</span></a>'
 raise ValueError(t)

def render_review_full():
 data=json.loads((Path(__file__).parent/'review-full.json').read_text())
 toc='<nav class="case-contents" aria-label="项目介绍目录"><span class="eyebrow">项目介绍 / CONTENTS</span><ol>'+''.join(f'<li><a href="#review-{i:02}"><span>{i:02}</span>{e(s["title"])}</a></li>' for i,s in enumerate(data['sections'],1))+'</ol></nav>'
 chapters=''.join(f'<section class="case-chapter" id="review-{i:02}" data-case-chapter><div class="chapter-heading"><span>{i:02}</span><h2>{e(s["title"])}</h2></div>'+''.join(render_block(b) for b in s['blocks'])+'</section>' for i,s in enumerate(data['sections'],1))
 return '<div class="case-reading">'+toc+'<article class="case-full-intro" aria-label="AI 走查助手完整项目介绍">'+chapters+'</article></div>'

def render_project_guide(p):
 review=p['slug']=='ai-review'
 items=[]
 flow_map={
  'ai-review':[['设计稿与开发图','AI 扫描与复核','Excel 问题报告'],['对齐输入区域','调整关注与判定','复核真实 / 疑似项'],['手机批量选图','App 与插件同步','网页分析 / 人工对比'],['发送两张图','识别、截图与填表','飞书走查表'],['读取 Figma 稿','分支内生成并修改 UI','提交代码与研发评审']],
  'ip-worldbook':[['作品素材','AI 提炼与组织','可共创的资料库'],['复杂产品关系','Vibe Coding','可交互原型'],['研发代码仓库','绘制与调整页面','可运行的体验']],
  'dual-screen':[['已有主播调研','重新分析认知门槛','提出体验判断'],['实际直播场景','组织场景化引导','理解形态与价值'],['设计发起','产品共创与验证','持续迭代体验']],
  'ai-editor':[['创作上下文','起草与编辑','预览与发布'],['剧情关系','节点与条件表单','结构化编辑'],['AI 起草','人的精修与决策','约束后续生成'],['对话与画布','同步、合并与回退','保留编辑意图']]}
 labels=['走查网站','提示词打磨','应用与插件','走查 Skill','仓库协作修复'] if review else [s[1] for s in p['sections']]
 anchors=[4,4,5,6,7] if review else list(range(1,len(p['sections'])+1))
 tabs=[];panels=[]
 for i,(num,title,body) in enumerate(p['sections']):
  tab=f'guide-tab-{i+1}';panel=f'guide-panel-{i+1}';active=i==0
  tabs.append(f'<button class="guide-tab" type="button" id="{tab}" role="tab" aria-controls="{panel}" aria-selected="{str(active).lower()}" tabindex="{0 if active else -1}"><span>{i+1:02}</span>{e(labels[i])}<b aria-hidden="true">↗</b></button>')
  anchor=f'review-{anchors[i]:02}' if review else f'design-{anchors[i]:02}'
  flow=flow_map[p['slug']][i]
  panels.append(f'<section class="guide-panel" id="{panel}" role="tabpanel" aria-labelledby="{tab}"'+('' if active else ' hidden')+'><span class="guide-stage-label">'+f'阶段 {i+1:02} / {len(p["sections"]):02}</span><h3>{e(title)}</h3><div class="guide-flow" aria-label="阶段流程">'+''.join(f'<span><small>{j+1:02}</small>{e(x)}</span>'+('<i aria-hidden="true">→</i>' if j<2 else '') for j,x in enumerate(flow))+'</div><p>'+e(body)+f'</p><a class="text-link" href="#{anchor}">阅读这一阶段的完整介绍 <span>↓</span></a></section>')
 cta='<a class="guide-tool-link" href="https://ykqtbvy3wr.coze.site/" target="_blank" rel="noopener noreferrer">打开实际网页工具 ↗</a>' if review else '<a class="guide-tool-link" href="#project-intro">阅读项目介绍 ↓</a>'
 return '<section class="project-guide" data-project-guide aria-label="项目互动流程导览"><div class="guide-sidebar"><span class="eyebrow">INTERACTIVE OVERVIEW / 流程导览</span><h2>'+('走查工作流' if review else '设计流程导览')+'</h2><p>选择阶段，查看流程与交付。</p><div role="tablist" aria-label="项目阶段" aria-orientation="vertical">'+''.join(tabs)+'</div>'+cta+'</div><div class="guide-stage">'+''.join(panels)+'</div></section>'
