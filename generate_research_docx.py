"""
Alfaaz Recruit — Research Foundation document generator.
Run: python generate_research_docx.py
Output: Alfaaz_Research_Foundation.docx
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

DOC = Document()

# ---------- Styles ----------
styles = DOC.styles
normal = styles['Normal']
normal.font.name = 'Calibri'
normal.font.size = Pt(11)

def h1(text):
    p = DOC.add_heading(text, level=1)
    return p

def h2(text):
    return DOC.add_heading(text, level=2)

def h3(text):
    return DOC.add_heading(text, level=3)

def para(text, bold=False):
    p = DOC.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    return p

def bullet(text):
    return DOC.add_paragraph(text, style='List Bullet')

def table(headers, rows):
    t = DOC.add_table(rows=1, cols=len(headers))
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.bold = True
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
    return t

# ---------- Title page ----------
title = DOC.add_heading('Alfaaz Recruit', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub = DOC.add_paragraph('Research Foundation for the Seven Parameters')
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.runs[0].font.size = Pt(14)
sub.runs[0].italic = True
meta = DOC.add_paragraph('Meta-analytic evidence, SJT mapping, and GBA mapping')
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.runs[0].font.size = Pt(11)

DOC.add_page_break()

# ---------- Section 1 ----------
h1('1. Purpose')
para(
    'This document consolidates the meta-analytic evidence supporting each of the seven Alfaaz '
    'parameters, maps each parameter to its Situational Judgment Test (SJT) scenario, and identifies '
    'the closest validated Game-Based Assessment (GBA) analogue. It is the research foundation for '
    'the Alfaaz Recruit battery.'
)
para(
    'The evidence base prioritizes meta-analytic and systematic-review findings over single studies. '
    'Where an exact GBA model exists for a parameter, it is cited. Where it does not, the closest '
    'validated analogue from adjacent constructs is identified and adapted.'
)

# ---------- Section 2 ----------
h1('2. The Seven Parameters')
para(
    'The seven parameters were selected because each satisfies three conditions: (1) meta-analytic '
    'evidence links it to volunteer-relevant outcomes, (2) the construct is behaviorally observable '
    'through game telemetry, and (3) the construct maps onto something Alfaaz actually needs from '
    'its volunteers.'
)
table(
    ['#', 'Parameter', 'Primary Meta-Analytic Source', 'Effect Size'],
    [
        ['1', 'Empathy', 'Yin & Wang (2023), 62 studies, N=71,310', 'r = .32 (cognitive), .30 (affective)'],
        ['2', 'Conscientiousness', 'Barrick & Mount (1991); Wilmot & Ones (2022)', 'ρ = .19 with performance'],
        ['3', 'Collaborative Spirit', 'Torka et al. (2021), N=320,632', 'Coordination → team performance'],
        ['4', 'Emotional Agility', 'Emotion regulation meta-analysis (2023), 549 effects', 'ρ = .22 with cognitive empathy'],
        ['5', 'Curiosity', 'Tang et al. (2022), 24 studies', 'r = .53 with interest (distinct construct)'],
        ['6', 'Creative Initiative', 'Da Costa et al. (2015), 7 meta-analyses', 'r = .27 divergent thinking'],
        ['7', 'Motivation', 'Forner et al. (2024), 117 studies', 'Intrinsic motivation predicts retention'],
    ]
)

# ---------- Parameter templates ----------
PARAMETERS = [
    {
        'name': 'Empathy',
        'meta': [
            'Yin & Wang (2023): meta-analysis of 62 studies, 146 samples, 71,310 participants. '
            'Prosocial behavior correlates positively with cognitive empathy (r = .32) and '
            'affective empathy (r = .30).',
            'Eisenberg & Miller (1987): high-empathy individuals are more sensitive to others\' distress '
            'and more likely to act to alleviate it.',
            'Separate meta-analysis: empathy is positively associated with charitable giving (r = .25, p < .001), '
            'though volunteering may be less purely empathically motivated because it provides direct payoffs.',
        ],
        'sjt': (
            'SJT scenarios S1, S2, S4, S5, S6. The candidate chooses between options that trade off '
            'interpersonal accommodation against task efficiency, rule-following, or creative pivots. '
            'Empathy keys are assigned when the option prioritizes understanding or responding to '
            'another person\'s state.'
        ),
        'gba': (
            'Yuzu Module 1 (Active-Empathic Listening) — a gamified questionnaire inspired by the '
            'Active-Empathic Listening Scale (AELS). Convergent validity evaluated against AELS. '
            'Key finding: cognitive empathy is more consistently measurable than affective empathy in GBA.'
        ),
        'game': (
            'The Frequency (F1, F2). The player tunes a signal slider. A simulated producer sends subtle '
            'text cues. The optimum and the producer\'s comfort zone differ. Behavioral target: cue detection, '
            'contextual calibration, clarification-seeking under ambiguity.'
        ),
    },
    {
        'name': 'Conscientiousness',
        'meta': [
            'Barrick & Mount (1991): meta-analysis of 57 studies. Conscientiousness is positively related '
            'to job performance across occupations.',
            'Wilmot & Ones (2022): synthesis of 50+ meta-analyses. Conscientiousness yields the strongest '
            'effect (ρ = 0.19) among Big Five traits for performance.',
            'Lodi-Smith & Roberts (2007): investment in volunteer roles is positively related to '
            'agreeableness, conscientiousness, and emotional stability.',
        ],
        'sjt': (
            'SJT scenarios S1, S2, S3, S7. The candidate chooses between rule-consistent, methodical '
            'options and alternatives that prioritize relational or creative responses.'
        ),
        'gba': (
            'Ventura & Shute (2013): game-based persistence assessment in Physics Playground. '
            'Validated against an existing persistence measure; predicted learning after controlling for '
            'gender, video game experience, pretest knowledge, and enjoyment. Shute & colleagues also '
            'developed stealth assessments for conscientiousness in Newton\'s Playground.'
        ),
        'game': (
            'The Archive (A1, A2). The player sorts art items using complex overlapping rules with an '
            'on-demand rule guide. Behavioral target: rule adherence, exception precision, verification, '
            'error correction.'
        ),
    },
    {
        'name': 'Collaborative Spirit',
        'meta': [
            'Torka et al. (2021): meta-analysis of 622 effect sizes, N=320,632. Effort gains or losses '
            'depend on dispensability and social comparison.',
            'Team orientation meta-analysis (2022): 39 articles, 210 effects. Positively related to '
            'communication, coordination, cooperation, trust, and team performance.',
        ],
        'sjt': (
            'SJT scenarios S1, S2, S3, S4, S5, S6, S7. Collaborative keys are assigned when the option '
            'involves consultation, adjustment to a partner\'s state, or collective problem-solving.'
        ),
        'gba': (
            'Collaborative Siege Task (Guo et al., 2026): 298 participants, real-time strategy game with '
            'asymmetric roles and ill-structured problems. Demonstrated hierarchical factor structure, '
            'satisfactory item difficulty and discrimination, and criterion-related validity against peer '
            'assessment. No sex, major, or role bias found.'
        ),
        'game': (
            'The Shared Canvas (C1, C2). Player and simulated partner paint a mural. Partner moves '
            'erratically; player can share paint. Behavioral target: need-sensitive cooperation, pacing '
            'coordination, response to partner state.'
        ),
    },
    {
        'name': 'Emotional Agility',
        'meta': [
            'Emotion regulation meta-analysis (2023): 549 effect sizes from 58 samples. Adaptive emotion '
            'regulation positively related to cognitive empathy (ρ = .22) and compassion (ρ = .19), '
            'negatively related to empathic distress (ρ = –.12).',
            'Aldao, Nolen-Hoeksema, & Schweizer (2010): systematic differences between adaptive and '
            'maladaptive emotion-regulation strategies.',
        ],
        'sjt': (
            'SJT scenarios S3, S5, S7. Emotional agility keys are assigned when the option involves '
            'calm adaptation, de-escalation, or recovery from a disruptive moment.'
        ),
        'gba': (
            'REThink (David et al., 2024): 110 children and adolescents completed the REThink game-based '
            'assessment. Statistically significant positive associations between game scores and emotion '
            'regulation scales. Predictive validity demonstrated via negative associations with '
            'emotional/behavioral problems. Internal consistency acceptable.'
        ),
        'game': (
            'The Shifting Grid (E1, E2). Fast sorting task with an unfair disruption (rule reversal or '
            'UI glitch). Behavioral target: recovery trials, perseverative errors, cadence stability.'
        ),
    },
    {
        'name': 'Curiosity',
        'meta': [
            'Tang et al. (2022): meta-analysis of 24 studies (31 effect sizes). Curiosity correlates with '
            'interest at r = .53, but is a distinct construct specifically linked to knowledge-gap closure.',
            'Wilson (2024): review of curiosity and information-seeking. Curiosity is functionally distinct '
            'from interest and specifically linked to closing knowledge gaps.',
        ],
        'sjt': (
            'SJT scenarios S3, S4, S5, S6. Curiosity keys are assigned when the option involves information '
            'seeking, question asking, or learning about an unfamiliar situation.'
        ),
        'gba': (
            'Questions Worlds (Tor & Gordon, 2020): digital question-asking assessment. Extracts question '
            'breadth, depth, specificity. Total question specificity in the last presented world was a '
            'significant predictor of teacher-rated curiosity — external validation from a source other '
            'than self-report.'
        ),
        'game': (
            'The Hidden Gallery (Q1, Q2). Node-map navigation with optional doors containing non-instrumental '
            'information. Behavioral target: doors opened, depth of inspection, persistence after empty '
            'discoveries.'
        ),
    },
    {
        'name': 'Creative Initiative',
        'meta': [
            'Da Costa et al. (2015): second-order meta-analysis of 7 meta-analyses. Creativity correlates '
            'with emotional intelligence (r = .31), divergent thinking (r = .27), openness (r = .22), '
            'and intrinsic motivation (r = .20).',
        ],
        'sjt': (
            'SJT scenarios S1, S2, S3, S5, S6, S7. Creative Initiative keys are assigned when the option '
            'involves reframing, unconventional solutions, or experimentation with limited resources.'
        ),
        'gba': (
            'CREA (Rafner et al., 2023): 408 participants — the largest game-based validation study to date. '
            'Demonstrated convergent and discriminant validity for crea.tiles with respect to standard '
            'tests, correlations r = .1 to .4.'
        ),
        'game': (
            'The Broken Tool (CR1, CR3). Physics sandbox with multiple valid solution families. Behavioral '
            'target: strategy diversity, feedback-driven changes, useful iteration.'
        ),
    },
    {
        'name': 'Motivation',
        'meta': [
            'Forner et al. (2024): systematic review and meta-analysis of volunteer turnover, 117 studies. '
            'Intrinsic motivation consistently predicts retention.',
            'VFI meta-analysis: N = 38,327. Volunteer motivators predict satisfaction, commitment, and '
            'intention to continue.',
        ],
        'sjt': (
            'SJT scenario S7. Motivation keys are assigned when the option involves honoring commitment '
            'or sustained effort beyond the minimum.'
        ),
        'gba': (
            'Ventura & Shute (2013): persistence GBA. The persistence measure was validated against an '
            'existing measure and predicted learning after controlling for gender, video game experience, '
            'and pretest knowledge.'
        ),
        'game': (
            'The Repetition (M1, M2). Stamping flyers beyond the mandatory minimum. Behavioral target: '
            'extra units completed, time after minimum, cadence degradation, resumed after pause.'
        ),
    },
]

# ---------- Section 3 ----------
h1('3. Parameter-by-Parameter Evidence')
for p in PARAMETERS:
    h2(p['name'])
    h3('Meta-analytic evidence')
    for m in p['meta']:
        bullet(m)
    h3('SJT mapping')
    para(p['sjt'])
    h3('Validated GBA analogue')
    para(p['gba'])
    h3('Alfaaz game')
    para(p['game'])

# ---------- Section 4 ----------
h1('4. Validation Pathway')
para(
    'A game-based assessment can be said to predict a parameter when three conditions are met:'
)
bullet('Convergent validity: r ≥ .25–.30 between game features and the SJT parameter.')
bullet('Discriminant validity: game features correlate more strongly with their target parameter '
       'than with any other parameter.')
bullet('Criterion validity: game features correlate with real-world outcomes (reliability, teamwork, '
       'retention, initiative) after controlling for the SJT.')
para(
    'Until all three are met, game features are descriptive behavioral evidence, not predictions.'
)

h2('Phase 1 — Content validity (immediate)')
para(
    '3–5 expert reviewers (psychometrician, volunteer coordinator, game designer, lived-experience '
    'volunteer) rate each game on mechanic-construct alignment, confound risk, scoring defensibility, '
    'and fairness.'
)

h2('Phase 2 — Convergent and discriminant validity (N ≥ 200)')
para(
    'Administer the battery alongside validated self-report measures: IRI (empathy), HEXACO or BFI '
    '(conscientiousness), SYMLOG (collaboration), ERQ or REThink (emotional agility), CEI-II (curiosity), '
    'Alternative Uses Task or CREA (creativity), VFI (motivation).'
)

h2('Phase 3 — Criterion validity (N ≥ 100 volunteers, 6 months)')
para(
    'Correlate game features with attendance, task completion, supervisor reliability ratings, peer '
    'teamwork ratings, retention, and initiative ratings.'
)

h2('Phase 4 — Fairness audit (N ≥ 500)')
para(
    'Test measurement invariance across device, input method, age, education, and language. Compute '
    'differential item functioning for each feature.'
)

# ---------- Section 5 ----------
h1('5. References')
REFS = [
    'Aldao, A., Nolen-Hoeksema, S., & Schweizer, S. (2010). Emotion-regulation strategies across '
    'psychopathology: A meta-analytic review. Clinical Psychology Review, 30(2), 217–237.',
    'Auer, E. M., Mersy, G., Marin, S., Blaik, J., & Landers, R. N. (2021). Using machine learning to '
    'model trace behavioral data from a game-based assessment. International Journal of Selection and '
    'Assessment, 30(1), 82–100.',
    'Barrick, M. R., & Mount, M. K. (1991). The Big Five personality dimensions and job performance: '
    'A meta-analysis. Personnel Psychology, 44(1), 1–26.',
    'Da Costa, S., Páez, D., Sánchez, F., Garaigordobil, M., & Gondim, S. (2015). Personal factors of '
    'creativity: A second order meta-analysis. Revista de Psicología del Trabajo y de las Organizaciones, '
    '31(3), 165–173.',
    'David, O. A., Tomoiagã, C., & Fodor, L. A. (2024). Gamified assessment of emotion-regulation '
    'abilities in youths: Validation of the REThink online game-based assessment system. Games for '
    'Health Journal, 13(3).',
    'Eisenberg, N., & Miller, P. A. (1987). The relation of empathy to prosocial and related behaviors. '
    'Psychological Bulletin, 101(1), 91–119.',
    'Forner, V. W., et al. (2024). STEMming the tide: New perspectives on careers and turnover. Journal '
    'of Organizational Behavior.',
    'Guo, S., Xu, Y., Yang, X., Chen, Y., Li, X., & Tian, X. (2026). A theory-driven game-based '
    'assessment of collaborative problem-solving. Journal of Intelligence, 14(9), 197.',
    'Lodi-Smith, J., & Roberts, B. W. (2007). Social investment and personality: A meta-analysis of the '
    'relationship of personality traits to investment in work, family, religion, and volunteerism. '
    'Personality and Social Psychology Review, 11(1), 68–86.',
    'Rafner, J., et al. (2023). Towards game-based assessment of creative thinking. Creativity Research '
    'Journal, 35(4), 763–782.',
    'Shute, V. J. (2011). Stealth assessment in computer-based games to support learning. In S. Tobias '
    '& J. D. Fletcher (Eds.), Computer games and instruction. Information Age Publishing.',
    'Tang, X., Renninger, K. A., Hidi, S., & Murayama, K. (2022). The differences and similarities '
    'between curiosity and interest: Meta-analysis and network analyses. Learning and Instruction, 80, '
    '101628.',
    'Tor, N., & Gordon, G. (2020). Digital interactive quantitative curiosity assessment tool: Questions '
    'worlds. International Journal of Information and Education Technology, 10(8), 614–621.',
    'Torka, A.-K., Mazei, J., & Hüffmeier, J. (2021). Together, everyone achieves more—or, less? An '
    'interdisciplinary meta-analysis on effort gains and losses in teams. Psychological Bulletin, 147(5), '
    '504–534.',
    'Ventura, M., & Shute, V. (2013). The validity of a game-based assessment of persistence. Computers '
    'in Human Behavior, 29(6), 2568–2572.',
    'Wilmot, M. P., & Ones, D. S. (2022). Big five personality traits and performance: A quantitative '
    'synthesis of 50+ meta-analyses. Journal of Personality, 90(4), 559–573.',
    'Yin, Y., & Wang, Y. (2023). Is empathy associated with more prosocial behaviour? A meta-analysis. '
    'Asian Journal of Social Psychology, 26, 3–22.',
]
for ref in REFS:
    p = DOC.add_paragraph(ref)
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.first_line_indent = Inches(-0.3)

# ---------- Save ----------
DOC.save('Alfaaz_Research_Foundation.docx')
print('Wrote Alfaaz_Research_Foundation.docx')