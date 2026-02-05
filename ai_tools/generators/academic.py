from ai_tools.generators.base import BaseGenerator


class EssayWriter(BaseGenerator):
    slug = 'ai-essay-writer'
    name = 'AI Essay Writer'
    description = 'Generate well-structured essays on any topic with proper introductions, body paragraphs, and conclusions.'
    category = 'Academic Writing'
    icon = 'essay'
    meta_title = 'Free AI Essay Writer'
    meta_description = 'Generate well-structured essays on any topic. Choose your length, style, and academic level.'

    fields = [
        {'name': 'topic', 'label': 'Essay Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Enter your essay topic or prompt...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (300 words)', 'Medium (500 words)', 'Long (800 words)', 'Extended (1200 words)']},
        {'name': 'level', 'label': 'Academic Level', 'type': 'select', 'required': False, 'options': ['High School', 'Undergraduate', 'Graduate', 'Professional']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Formal', 'Analytical', 'Persuasive', 'Narrative', 'Expository']},
    ]

    system_prompt = (
        'You are an expert academic essay writer. Write a well-structured essay on the given topic. '
        'Target length: {length}. Academic level: {level}. Tone: {tone}. '
        'Include a clear thesis statement, well-organized body paragraphs with evidence and analysis, '
        'and a strong conclusion. Use proper transitions between paragraphs.'
    )


class EssayOutlineGenerator(BaseGenerator):
    slug = 'ai-essay-outline-generator'
    name = 'AI Essay Outline Generator'
    description = 'Create detailed essay outlines with thesis statements, main arguments, and supporting points.'
    category = 'Academic Writing'
    icon = 'outline'
    meta_title = 'Free AI Essay Outline Generator'
    meta_description = 'Generate detailed essay outlines with thesis statements and organized arguments.'

    fields = [
        {'name': 'topic', 'label': 'Essay Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Enter your essay topic...'},
        {'name': 'num_points', 'label': 'Number of Main Points', 'type': 'select', 'required': False, 'options': ['3', '4', '5', '6']},
        {'name': 'level', 'label': 'Academic Level', 'type': 'select', 'required': False, 'options': ['High School', 'Undergraduate', 'Graduate']},
    ]

    system_prompt = (
        'You are an expert academic writing assistant. Create a detailed essay outline for the given topic. '
        'Include {num_points} main points. Academic level: {level}. '
        'Structure: I. Introduction (with thesis statement), II-IV. Body paragraphs (each with topic sentence, '
        'supporting evidence, and analysis), V. Conclusion. Use Roman numerals and letters for sub-points.'
    )


class ThesisStatementGenerator(BaseGenerator):
    slug = 'ai-thesis-statement-generator'
    name = 'AI Thesis Statement Generator'
    description = 'Generate strong, arguable thesis statements for essays and research papers.'
    category = 'Academic Writing'
    icon = 'thesis'
    meta_title = 'Free AI Thesis Statement Generator'
    meta_description = 'Create strong thesis statements for essays and research papers instantly.'

    fields = [
        {'name': 'topic', 'label': 'Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What is your paper about?'},
        {'name': 'position', 'label': 'Your Position/Argument', 'type': 'textarea', 'required': False, 'placeholder': 'What do you want to argue? (optional)'},
        {'name': 'type', 'label': 'Essay Type', 'type': 'select', 'required': False, 'options': ['Argumentative', 'Analytical', 'Expository', 'Compare & Contrast', 'Cause & Effect']},
    ]

    system_prompt = (
        'You are an expert at crafting thesis statements. Generate 3 strong, specific, and arguable thesis '
        'statements for the given topic. Essay type: {type}. Position: {position}. '
        'Each thesis should be 1-2 sentences, take a clear stance, and preview the main arguments. '
        'Label them as Option 1, Option 2, Option 3.'
    )


class ResearchPaperWriter(BaseGenerator):
    slug = 'ai-research-paper-writer'
    name = 'AI Research Paper Writer'
    description = 'Generate structured research paper drafts with proper academic formatting.'
    category = 'Academic Writing'
    icon = 'research'
    meta_title = 'Free AI Research Paper Writer'
    meta_description = 'Generate research paper drafts with proper structure and academic formatting.'

    fields = [
        {'name': 'topic', 'label': 'Research Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Enter your research topic...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (500 words)', 'Medium (1000 words)', 'Long (1500 words)']},
        {'name': 'field', 'label': 'Academic Field', 'type': 'text', 'required': False, 'placeholder': 'e.g., Psychology, Biology, History'},
    ]

    system_prompt = (
        'You are an expert academic researcher. Write a research paper draft on the given topic. '
        'Target length: {length}. Academic field: {field}. '
        'Include: Abstract, Introduction (with research question), Literature Review context, '
        'Methodology overview, Discussion/Analysis, and Conclusion. Use formal academic language.'
    )


class LiteratureReviewGenerator(BaseGenerator):
    slug = 'ai-literature-review-generator'
    name = 'AI Literature Review Generator'
    description = 'Generate structured literature review sections for research papers.'
    category = 'Academic Writing'
    icon = 'review'
    meta_title = 'Free AI Literature Review Generator'
    meta_description = 'Generate literature review sections with thematic organization and analysis.'

    fields = [
        {'name': 'topic', 'label': 'Research Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Enter your research topic...'},
        {'name': 'key_themes', 'label': 'Key Themes/Areas', 'type': 'textarea', 'required': False, 'placeholder': 'List key themes to cover (one per line)'},
        {'name': 'field', 'label': 'Academic Field', 'type': 'text', 'required': False, 'placeholder': 'e.g., Education, Computer Science'},
    ]

    system_prompt = (
        'You are an expert academic writer specializing in literature reviews. Write a literature review '
        'section for the given research topic. Field: {field}. Key themes: {key_themes}. '
        'Organize thematically, synthesize sources, identify gaps in existing research, '
        'and use formal academic language. Include placeholder citations in (Author, Year) format.'
    )


class ConclusionWriter(BaseGenerator):
    slug = 'ai-conclusion-writer'
    name = 'AI Conclusion Writer'
    description = 'Generate strong conclusions that summarize arguments and provide closure.'
    category = 'Academic Writing'
    icon = 'conclusion'
    meta_title = 'Free AI Conclusion Writer'
    meta_description = 'Generate strong essay and paper conclusions that tie everything together.'

    fields = [
        {'name': 'content', 'label': 'Essay/Paper Content', 'type': 'textarea', 'required': True, 'placeholder': 'Paste your essay or paper content...'},
        {'name': 'type', 'label': 'Type', 'type': 'select', 'required': False, 'options': ['Essay Conclusion', 'Research Paper Conclusion', 'Report Conclusion']},
    ]

    system_prompt = (
        'You are an expert academic writer. Write a strong conclusion for the following content. '
        'Type: {type}. The conclusion should: restate the thesis/main argument in fresh words, '
        'summarize key points, discuss broader implications, and end with a thought-provoking final statement. '
        'Do NOT introduce new arguments.'
    )


class AbstractGenerator(BaseGenerator):
    slug = 'ai-abstract-generator'
    name = 'AI Abstract Generator'
    description = 'Generate concise abstracts for research papers and academic articles.'
    category = 'Academic Writing'
    icon = 'abstract'
    meta_title = 'Free AI Abstract Generator'
    meta_description = 'Generate concise, well-structured abstracts for research papers and articles.'

    fields = [
        {'name': 'content', 'label': 'Paper Content', 'type': 'textarea', 'required': True, 'placeholder': 'Paste your paper content or describe your research...'},
        {'name': 'word_limit', 'label': 'Word Limit', 'type': 'select', 'required': False, 'options': ['150 words', '200 words', '250 words', '300 words']},
    ]

    system_prompt = (
        'You are an expert at writing academic abstracts. Write a concise abstract for the following '
        'research content. Target: {word_limit}. Include: purpose/objective, methodology, key findings, '
        'and conclusions. Use past tense for methods and results, present tense for conclusions.'
    )


class AnnotatedBibliographyGenerator(BaseGenerator):
    slug = 'ai-annotated-bibliography-generator'
    name = 'AI Annotated Bibliography Generator'
    description = 'Generate annotated bibliography entries with summaries and evaluations.'
    category = 'Academic Writing'
    icon = 'bibliography'
    meta_title = 'Free AI Annotated Bibliography Generator'
    meta_description = 'Create annotated bibliography entries with summaries and critical evaluations.'

    fields = [
        {'name': 'source', 'label': 'Source Information', 'type': 'textarea', 'required': True, 'placeholder': 'Enter source details (title, author, URL, or description)...'},
        {'name': 'style', 'label': 'Citation Style', 'type': 'select', 'required': False, 'options': ['APA 7th', 'MLA 9th', 'Chicago', 'Harvard']},
        {'name': 'focus', 'label': 'Research Focus', 'type': 'text', 'required': False, 'placeholder': 'What aspect of the source is relevant to your research?'},
    ]

    system_prompt = (
        'You are an expert at creating annotated bibliographies. Generate an annotated bibliography entry '
        'for the given source. Citation style: {style}. Research focus: {focus}. '
        'Include: a properly formatted citation, a 150-word annotation with a summary of the source, '
        'an evaluation of its credibility and usefulness, and how it relates to the research topic.'
    )


class DiscussionPostGenerator(BaseGenerator):
    slug = 'ai-discussion-post-generator'
    name = 'AI Discussion Post Generator'
    description = 'Generate thoughtful discussion board posts for online courses.'
    category = 'Academic Writing'
    icon = 'discussion'
    meta_title = 'Free AI Discussion Post Generator'
    meta_description = 'Generate thoughtful discussion board posts for online courses and forums.'

    fields = [
        {'name': 'prompt', 'label': 'Discussion Prompt', 'type': 'textarea', 'required': True, 'placeholder': 'Enter the discussion prompt or question...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (150 words)', 'Medium (250 words)', 'Long (400 words)']},
        {'name': 'level', 'label': 'Course Level', 'type': 'select', 'required': False, 'options': ['Undergraduate', 'Graduate', 'Professional']},
    ]

    system_prompt = (
        'You are a thoughtful student writing a discussion board post. Respond to the given prompt. '
        'Target length: {length}. Course level: {level}. '
        'Include a clear position, supporting evidence or examples, engage with the topic critically, '
        'and end with a question to encourage further discussion. Use first person where appropriate.'
    )


ACADEMIC_GENERATORS = [
    EssayWriter,
    EssayOutlineGenerator,
    ThesisStatementGenerator,
    ResearchPaperWriter,
    LiteratureReviewGenerator,
    ConclusionWriter,
    AbstractGenerator,
    AnnotatedBibliographyGenerator,
    DiscussionPostGenerator,
]
