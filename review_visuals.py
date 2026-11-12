# -*- coding: utf-8 -*-
from html import escape as e
from pathlib import Path
import re

def icon(name):
 paths={'web':'<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>','spark':'<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z"/>','phone':'<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M10 5h4m-3 14h2"/>','branch':'<circle cx="6" cy="5" r="2"/><circle cx="18" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><path d="M6 7v10m0-4h5a7 7 0 0 0 7-6"/>','layers':'<path d="m12 3 10 6-10 6L2 9l10-6Zm-9 11 9 5 9-5M3 18l9 5 9-5"/>','check':'<path d="m5 12 4 4L19 6"/>'}
 return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[name]+'</svg>'

def node(title,body,num=None,highlight=False):
 return '<li class="rv-node'+(' rv-node-accent' if highlight else '')+'">'+(f'<span class="rv-node-num">{num:02}</span>' if num else '')+'<h4>'+e(title)+'</h4><p>'+e(body)+'</p></li>'

def flow(items,highlight=-1):
 return '<ol class="rv-flow" style="--flow-count:'+str(len(items))+'">'+''.join(node(t,b,i+1,i==highlight) for i,(t,b) in enumerate(items))+'</ol>'

def figure(key,title,body,caption):
 return '<figure class="review-visual rv-'+key+'" id="visual-'+key+'"><header class="rv-heading"><span>PROCESS / '+key.upper()+'</span><h3>'+e(title)+'</h3></header>'+body+'<figcaption>'+e(caption)+'</figcaption></figure>'

def thumb(kind):
 if kind=='form':return '<div class="rv-thumb thumb-form"><i></i><i></i><b></b></div>'
 if kind=='art':return '<div class="rv-thumb thumb-art"><span>✳</span><i></i></div>'
 return '<div class="rv-thumb thumb-board"><i></i><i></i><i></i><i></i></div>'

def evolution():
 items=[('走查网站','设计图与开发图批量对比'),('打磨 PE','调整提示词与走查关注项'),('移动端 + 插件','补齐截图上传与设计图导入'),('走查 Skill 化','AI 识别、截图并填表'),('进入研发仓库','建分支、改 UI、提交代码')]
 return figure('evolution','从走查网站，到 UI 代码修复',flow(items,4)+'<p class="rv-emphasis">工作重心逐步从整理问题，走向直接参与修复。</p>','项目发展顺序：工具开发 → 跨端输入 → Skill → 仓库协作')

def review_modal(x, y, modified=False):
    button = (
        '<rect x="7" y="37" width="40" height="6" rx="2" fill="#a99ace"/>'
        if modified else '<path d="M7 40h16m7 0h17" stroke="#596758" stroke-width="2"/>'
    )
    return (
        f'<g transform="translate({x} {y})">'
        '<rect width="54" height="49" rx="5" fill="#dce6d8"/>'
        '<rect x="21" y="6" width="12" height="12" rx="3" fill="#758d70"/>'
        '<path d="M11 26h32M1 33h52" stroke="#879683" stroke-width="2"/>'
        + button + '</g>'
    )

def review_comparison(include_development=False):
    if include_development:
        return (
            '<rect x="14" y="31" width="45" height="16" rx="4" fill="#3a4a31" stroke="#9db77d"/>'
            '<rect x="63" y="31" width="45" height="16" rx="4" fill="#292d36" stroke="#4d5668"/>'
            '<rect x="112" y="31" width="64" height="16" rx="4" fill="#293527" stroke="#718363" stroke-dasharray="3 2"/>'
            '<g fill="#d0dac9" font-size="9" text-anchor="middle"><text x="36.5" y="42">对比组 1</text>'
            '<text x="85.5" y="42">对比组 2</text><text x="144" y="42">＋ 添加对比组</text></g>'
            '<rect x="14" y="52" width="78" height="49" rx="6" fill="#293527" stroke="#718363"/>'
            '<rect x="98" y="52" width="78" height="49" rx="6" fill="#252733" stroke="#64697e"/>'
            '<g transform="translate(32 57) scale(.78)">' + review_modal(0, 0) + '</g>'
            '<g transform="translate(116 57) scale(.78)">' + review_modal(0, 0, True) + '</g>'
        )
    design = (
        '<g transform="translate(35 46) scale(.67)">' + review_modal(0, 0) + '</g>'
        '<rect x="18" y="80" width="70" height="17" rx="4" fill="#34442b" stroke="#8aa56d"/>'
        '<text x="53" y="92" text-anchor="middle" font-size="9.5" fill="#d3efa9">⌘ / Ctrl + V</text>'
    )
    development = (
        '<path d="M138 59v14m-7-7h14" stroke="#7e869d" stroke-width="1.5"/>'
        '<path d="M126 85h24" stroke="#555d70" stroke-width="2"/>'
    )
    return (
        '<rect x="14" y="32" width="78" height="69" rx="6" fill="#293527" stroke="#718363"/>'
        '<rect x="98" y="32" width="78" height="69" rx="6" fill="#252733" stroke="#64697e"/>'
        '<path d="M20 40h23m61 0h23" stroke="#92a88a" stroke-width="2"/>'
        + design + development
    )

def review_screen(contents):
    return (
        '<div class="rv-screen" aria-hidden="true"><svg viewBox="0 0 190 118" focusable="false">'
        '<rect x="6" y="8" width="178" height="102" rx="8" fill="#181d20" stroke="#4b564d"/>'
        '<path d="M6 24h178" stroke="#414a43"/>'
        '<circle cx="15" cy="16" r="2" fill="#c3f36b"/>'
        '<path d="M22 16h34" stroke="#788678" stroke-width="2" stroke-linecap="round"/>'
        + contents + '</svg></div>'
    )

def web_flow():
    report_preview = (
        '<rect x="14" y="32" width="91" height="69" rx="6" fill="#293527" stroke="#52614d"/>'
        + review_modal(32, 42, True)
        + '<rect x="49" y="46" width="20" height="17" rx="2" fill="#e68f751a" stroke="#f0a186"/>'
        '<rect x="36" y="77" width="45" height="10" rx="2" fill="#e68f751a" stroke="#f0a186"/>'
        '<rect x="112" y="32" width="64" height="69" rx="6" fill="#262c2a" stroke="#48564b"/>'
        '<text x="121" y="46" fill="#d0dac9" font-size="9">问题清单</text>'
        '<path d="M124 57h40m-40 15h34m-34 15h39" stroke="#808e7c" stroke-width="2"/>'
        '<path d="M118 57h2m-2 15h2m-2 15h2" stroke="#efaa8d" stroke-width="3"/>'
    )
    spreadsheet = (
        '<rect x="14" y="32" width="162" height="69" rx="5" fill="#253129" stroke="#576f5b"/>'
        '<path d="M15 50h160M15 66h160M15 83h160M40 33v67m77-67v67" stroke="#516455"/>'
        '<g fill="#d0dac9" font-size="9"><text x="20" y="44">序号</text>'
        '<text x="47" y="44">问题描述</text><text x="126" y="44">标注图</text></g>'
        '<path d="M22 58h7m-7 16h7m-7 17h7M47 58h52m-52 16h41m-41 17h54" stroke="#879f88" stroke-width="2"/>'
        '<path d="M128 57h30m-30 17h30m-30 17h30" stroke="#9ebf86" stroke-width="5" stroke-linecap="round"/>'
    )
    steps = [
        ('上传设计稿', '从 Figma 复制图片，直接粘贴到上传区。也可拖拽或选图。', '剪贴板粘贴 · 免存本地', review_comparison()),
        ('上传开发截图', '把同一区域的开发截图与设计稿并排对比。', '添加对比组 · 一次走查多组', review_comparison(True)),
        ('查看 AI 结果', '对照截图标注和问题清单，人工确认差异并排除误报。', '图上标注 · 人工复核', report_preview),
        ('导出表格', '将问题描述和标注图导出为 Excel，交给开发跟进。', 'Excel 交付 · 图文同表', spreadsheet),
    ]
    panels = ''.join(
        '<li class="rv-story-step">' + review_screen(screen)
        + f'<div class="rv-story-copy"><div class="rv-story-title"><span class="rv-story-number">{i:02}</span>'
        + f'<h4>{e(title)}</h4></div><p>{e(description)}</p>'
        + f'<span class="rv-story-feature">{e(feature)}</span>'
        + '</div></li>'
        for i, (title, description, feature, screen) in enumerate(steps, 1)
    )
    return figure(
        'web-flow', 'AI 扫描差异，设计师确认问题',
        '<ol class="rv-storyboard">' + panels + '</ol>',
        '网页端界面示意 · 从传图、批量对比到问题交付',
    )

def pe():
    rules = [
        ('动态内容拆层', '昵称、头像等动态内容变化不报缺陷，容器和字体样式照常检查。'),
        ('两层几何检查', '用脚本测量模块之间及模块内部的间距，比单靠 AI 目测更精确。'),
        ('测试干扰分流', '识别并过滤测试环境的调试信息，避免将它们误报为界面问题。'),
        ('证据图可交付', '截图保留问题 UI 和周边上下文，配对展示当前效果与预期设计。'),
    ]
    items = ''.join(f'<li><h4>{e(title)}</h4><p>{e(body)}</p></li>' for title, body in rules)
    excerpt = Path(__file__).with_name('review-pe-excerpt.md').read_text(encoding='utf-8').splitlines()

    def highlight(line):
        return ''.join(
            f'<span class="rv-pe-token">{e(part)}</span>' if index % 2 else e(part)
            for index, part in enumerate(re.split(r'(`[^`]+`)', line))
        )

    code = '\n'.join(
        f'<span class="rv-pe-line"><span class="rv-pe-line-num" aria-hidden="true">{index:02}</span>'
        f'<span class="rv-pe-line-text">{highlight(line)}</span></span>'
        for index, line in enumerate(excerpt, 1)
    )
    return (
        '<figure class="review-visual rv-pe" id="visual-pe">'
        '<div class="rv-pe-copy"><header class="rv-heading"><span>REVIEW / DECISION RULES</span>'
        '<h3>四条检查规则</h3></header>'
        f'<ul class="rv-pe-rules">{items}</ul></div>'
        '<div class="rv-pe-snippet"><div class="rv-pe-snippet-bar"><span id="pe-excerpt-label">PE 原文节选</span>'
        '<span aria-hidden="true">MARKDOWN</span></div>'
        f'<pre tabindex="0" aria-labelledby="pe-excerpt-label"><code>{code}</code></pre></div>'
        '</figure>'
    )

def report():
 body='''<div class="rv-browser"><div class="rv-window-bar"><span><i></i><i></i><i></i></span><strong>走查报告</strong><span class="rv-small-pill">示例</span></div><div class="rv-report-layout"><div class="rv-annotated"><div class="rv-annotation-label">标注后的开发截图</div><div class="rv-example-dialog"><span class="rv-product-symbol">✳</span><span class="rv-example-close">×</span><h4>打开游戏，继续体验</h4><p>示例弹窗 / 组件还原走查</p><div class="rv-marked-area" data-visual-mark="layout"><span class="rv-marker">1</span><span class="rv-example-button">打开游戏</span></div><div class="rv-marked-area rv-marked-secondary" data-visual-mark="content"><span class="rv-marker">2</span><span>活动示例素材</span></div><small>暂时退出</small></div></div><div class="rv-issues"><div class="rv-issues-heading"><strong>问题清单</strong><span>标注与描述对应</span></div><div class="rv-issue-filters" role="group" aria-label="查看示例问题"><button type="button" data-issue-filter="all" aria-pressed="true">全部</button><button type="button" data-issue-filter="layout" aria-pressed="false">还原问题</button><button type="button" data-issue-filter="content" aria-pressed="false">疑似差异</button></div><article class="rv-issue" data-visual-issue="layout"><span class="rv-issue-index">1</span><div><b>按钮布局与设计稿存在差异</b><p>对应标注区域，设计师复核后确认。</p><small class="rv-status-confirmed">还原问题 · 待处理</small></div></article><article class="rv-issue" data-visual-issue="content"><span class="rv-issue-index rv-index-muted">2</span><div><b>示例素材与文案不同</b><p>可能属于动态内容，需人工判断。</p><small>疑似差异 · 待复核</small></div></article><div class="rv-export-label">↓ 问题清单 + 标注图 / Excel</div></div></div></div>'''
 return figure('report','让标注截图与问题清单对应起来',body,'界面示意 · 切换问题分类，查看标注与清单的对应关系')

def cross_device():
 body='<div class="rv-sync-root"><div class="rv-sync-source">'+icon('phone')+'<h4>移动端 App</h4><p>Android / iOS<br>相册批选、分享上传</p></div><span class="rv-connector" aria-hidden="true">→</span><div class="rv-sync-account">'+icon('layers')+'<h4>同一账号</h4><p>截图同步<br>衔接多端输入</p></div><span class="rv-connector" aria-hidden="true">→</span><div class="rv-sync-branches"><div><span class="rv-branch-name">网页端</span><p>设计 / 开发对比组 → AI 分析</p><strong>Excel 问题报告 ↗</strong></div><div><span class="rv-branch-name">Figma 插件</span><p>截图同步、导入画板与设计稿</p><strong>插件内 AI 走查 / 手动对比 ↗</strong></div></div></div>'
 return figure('sync','手机采集，网页与 Figma 各取所需',body,'截图同步后，根据走查场景进入网页或 Figma 工作流')

def devices():
 phone='<div class="rv-phone"><div class="rv-phone-top"><span>9:41</span><i></i><span>▰</span></div><div class="rv-upload-header"><small>SHARE / UPLOAD</small><h4>上传截图</h4><p>共 3 张图片</p></div><div class="rv-phone-grid">'+''.join('<div>'+thumb(k)+'<span>✓</span></div>' for k in ['form','art','board'])+'</div><div class="rv-upload-bottom"><small>准备就绪，点击上传</small><div><span>取消</span><b>上传全部（3）</b></div></div></div>'
 plugin='<div class="rv-plugin"><div class="rv-window-bar"><strong>⌘ AI 走查工具</strong><span>×</span></div><div class="rv-plugin-tabs"><span>多组对比</span><b>手机截图</b><span>配置</span></div><div class="rv-plugin-toolbar"><span>手机上传的截图</span><span>↻ 刷新</span></div><div class="rv-import-all">↓ 全部导入 Figma（3 张）</div><div class="rv-plugin-list">'+''.join('<div>'+thumb(k)+f'<span><b>截图 {i+1:02}</b><small>→ 对比组 {i+1}</small></span></div>' for i,k in enumerate(['form','art','board']))+'</div></div>'
 body='<div class="rv-device-pair"><div><span class="rv-device-kicker">01 / 手机 · 批量采集</span>'+phone+'<p class="rv-device-note">从相册选择截图，通过 App 分享上传。</p></div><div><span class="rv-device-kicker">02 / Figma · 同步与导入</span>'+plugin+'<p class="rv-device-note">同步手机截图，批量导入画板并继续走查。</p></div></div>'
 return figure('devices','把截图准备衔接到设计工具里',body,'界面示意 · 以批量上传和截图同步，串联手机与设计工具')

def skill():
 body=flow([('提供两张图','设计图 + 开发图'),('AI 执行走查','识别问题，截取对应区域'),('填入飞书表','问题描述 + 标注截图')],1)+'''<div class="rv-skill-record"><div class="rv-skill-status">'''+icon('check')+'''<div><b>问题记录已整理</b><span>识别 → 截图 → 填表</span></div><small>输出示意</small></div><div class="rv-record-row rv-record-head"><span>问题</span><span>截图</span><span>状态</span></div><div class="rv-record-row"><span>组件容器样式与设计稿不一致</span><span class="rv-mini-crop"><i></i><i></i></span><b>确认问题</b></div><div class="rv-record-row"><span>属性标签颜色需要调整</span><span class="rv-mini-crop"><i></i><i></i></span><b>确认问题</b></div><div class="rv-record-row"><span>动态内容与示例素材存在差异</span><span class="rv-mini-crop"><i></i><i></i></span><small>待复核</small></div></div>'''
 return figure('skill','输入两张图，把问题记录交给 AI',body,'输出示意 · 问题描述、截图和复核状态统一记录')

def repository():
 items=[('接入仓库','访问代码，定位页面与组件'),('建立分支','在独立分支中推进修改'),('D2C 读取设计稿','从 Figma 生成前端代码'),('自行修复 UI','把设计差异转成代码修改'),('提交代码','验证、评审与后续协作')]
 body=flow(items,2)+'''<div class="rv-repo-track"><span>'''+icon('branch')+'''独立分支</span><div class="rv-commit-line"><i></i><span>生成前端</span><i></i><span>调整 UI</span><i></i><span>提交修改</span></div><span class="rv-review-gate">研发验证与评审 ↗</span></div><p class="rv-emphasis">交付物从问题清单，延展为实际界面代码修改。</p>'''
 return figure('repository','进入代码仓库，直接处理 UI 问题',body,'独立分支内修改，提交后继续研发验证与评审')

VISUALS={'evolution':evolution,'web-flow':web_flow,'pe':pe,'report':report,'sync':cross_device,'devices':devices,'skill':skill,'repository':repository}
def render_visual(name):return VISUALS[name]()
