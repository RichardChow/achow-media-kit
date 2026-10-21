import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
from cardkit import *
OUT = HERE + '/'
# 示例数据为作者个人实测（Codex vs Claude Code 额度），替换成你自己的真实数据
print(cover(OUT + 'dark-cover.png',
    [[('Codex 100刀', CODEX)], [('vs ', MUTED), ('Claude 20刀', CLAUDE)]],
    '同样 20 刀中档推理，消耗差 5 倍以上｜我的实测',
    kicker='> GPT-6 Astra vs Opus 5.5 · 5h 额度',
    title_size=118,
    term_lines=[('$ run kline --agent codex', TEXT2),
                ('31 / 81 根 · 5h 额度已到上限', CODEX),
                ('$ run kline --agent claude', TEXT2),
                ('8 个交易日 · 5h 用量 16%', CLAUDE),
                ('$_', TEXT2)]))
print(compare_card(OUT + 'dark-compare.png',
    [('Codex', CODEX), (' vs ', MUTED), ('Claude Code', CLAUDE), (' 额度实测', WHITE)],
    '> 同样 20 刀/月 · 中档推理',
    [{'name': 'Codex Plus', 'color': CODEX, 'spec': ['GPT-6 Astra · 中档', '$20 / 月']},
     {'name': 'Claude Code Pro', 'color': CLAUDE, 'spec': ['Opus 5.5 · 中档', '$20 / 月']}],
    [{'title': '做 PPT', 'subtitle': '占 5 小时额度',
      'rows': [{'side': 0, 'label': 'Codex 做一份', 'value': '至少 50%', 'pct': 50, 'note': '同事做一份：一次吃掉 80%'},
               {'side': 0, 'label': 'Codex 小改一次', 'value': '20–30%', 'pct': (20, 30)},
               {'side': 1, 'label': 'Claude 改 6 版', 'value': '共 25%', 'pct': 25}]},
     {'title': 'K 线工作流', 'subtitle': '一天 81 根 · 占 5 小时额度',
      'rows': [{'side': 0, 'label': 'Codex', 'value': '到上限', 'pct': 100,
                'note': '只跑了 31 根，一天都没跑完'},
               {'side': 1, 'label': 'Claude Code', 'value': '16%', 'pct': 16,
                'note': '1:40–3:02 跑完 8 个交易日，当前 5 小时用量 16%'}]}],
    '个人实测，方法不严谨'))

# light theme
print(cover(OUT + 'light-cover.png',
    [[('Codex 100刀', CODEX)], [('vs ', MUTED), ('Claude 20刀', CLAUDE)]],
    '同样 20 刀中档推理，消耗差 5 倍以上｜我的实测',
    kicker='> GPT-6 Astra vs Opus 5.5 · 5h 额度',
    footer=['Codex Plus', 'Claude Code Pro', 'K 线工作流 81 根/天'],
    theme='light'))
print(compare_card(OUT + 'light-compare.png',
    [('Codex', CODEX), (' vs ', MUTED), ('Claude Code', CLAUDE), (' 额度实测', WHITE)],
    '> 同样 20 刀/月 · 中档推理',
    [{'name': 'Codex Plus', 'color': CODEX, 'spec': ['GPT-6 Astra · 中档', '$20 / 月']},
     {'name': 'Claude Code Pro', 'color': CLAUDE, 'spec': ['Opus 5.5 · 中档', '$20 / 月']}],
    [{'title': '做 PPT', 'subtitle': '占 5 小时额度',
      'rows': [{'side': 0, 'label': 'Codex 做一份', 'value': '至少 50%', 'pct': 50, 'note': '同事做一份：一次吃掉 80%'},
               {'side': 0, 'label': 'Codex 小改一次', 'value': '20–30%', 'pct': (20, 30)},
               {'side': 1, 'label': 'Claude 改 6 版', 'value': '共 25%', 'pct': 25}]},
     {'title': 'K 线工作流', 'subtitle': '一天 81 根 · 占 5 小时额度',
      'rows': [{'side': 0, 'label': 'Codex', 'value': '到上限', 'pct': 100,
                'note': '只跑了 31 根，一天都没跑完'},
               {'side': 1, 'label': 'Claude Code', 'value': '16%', 'pct': 16,
                'note': '1:40–3:02 跑完 8 个交易日，当前 5 小时用量 16%'}]}],
    '个人实测，方法不严谨', theme='light'))
