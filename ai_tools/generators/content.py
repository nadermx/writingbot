from ai_tools.generators.base import BaseGenerator


class BlogWriter(BaseGenerator):
    slug = 'ai-blog-writer'
    name = 'AI Blog Writer'
    description = 'Generate engaging, well-structured blog posts on any topic with SEO-friendly formatting.'
    category = 'Content & SEO'
    icon = 'blog'
    meta_title = 'Free AI Blog Writer'
    meta_description = 'Generate engaging blog posts on any topic. Choose your tone, length, and style for SEO-optimized content.'

    fields = [
        {'name': 'topic', 'label': 'Blog Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Enter your blog topic or title idea...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (400 words)', 'Medium (800 words)', 'Long (1200 words)', 'Extended (2000 words)']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Conversational', 'Professional', 'Informative', 'Persuasive', 'Entertaining']},
        {'name': 'keywords', 'label': 'Target Keywords', 'type': 'text', 'required': False, 'placeholder': 'e.g., productivity tips, remote work, time management'},
    ]

    system_prompt = (
        'You are an expert blog writer and content strategist. Write an engaging, well-structured blog post '
        'on the given topic. Target length: {length}. Tone: {tone}. Target keywords: {keywords}. '
        'Include a compelling introduction with a hook, clear subheadings (H2/H3), actionable insights, '
        'and a conclusion with a call to action. Optimize naturally for SEO without keyword stuffing.'
    )


class ArticleWriter(BaseGenerator):
    slug = 'ai-article-writer'
    name = 'AI Article Writer'
    description = 'Generate polished, publication-ready articles with proper structure and depth.'
    category = 'Content & SEO'
    icon = 'article'
    meta_title = 'Free AI Article Writer'
    meta_description = 'Generate publication-ready articles on any topic with proper structure and in-depth analysis.'

    fields = [
        {'name': 'topic', 'label': 'Article Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Enter your article topic or headline...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (500 words)', 'Medium (1000 words)', 'Long (1500 words)', 'Feature (2500 words)']},
        {'name': 'style', 'label': 'Article Style', 'type': 'select', 'required': False, 'options': ['News', 'Feature', 'Opinion', 'How-To', 'Explainer', 'Interview']},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'e.g., tech professionals, small business owners'},
    ]

    system_prompt = (
        'You are an experienced journalist and article writer. Write a polished, publication-ready article '
        'on the given topic. Target length: {length}. Style: {style}. Target audience: {audience}. '
        'Include a strong lead paragraph, well-researched body sections with clear transitions, '
        'relevant examples or data points, and a compelling conclusion. Maintain journalistic standards.'
    )


class ContentGenerator(BaseGenerator):
    slug = 'ai-content-generator'
    name = 'AI Content Generator'
    description = 'Generate versatile content for websites, marketing, social media, and more.'
    category = 'Content & SEO'
    icon = 'content'
    meta_title = 'Free AI Content Generator'
    meta_description = 'Generate high-quality content for websites, marketing campaigns, social media, and more.'

    fields = [
        {'name': 'topic', 'label': 'Content Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the content you need...'},
        {'name': 'content_type', 'label': 'Content Type', 'type': 'select', 'required': False, 'options': ['Website Copy', 'Marketing Copy', 'Social Media Post', 'Newsletter', 'Product Description', 'Landing Page']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Casual', 'Friendly', 'Authoritative', 'Playful', 'Urgent']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (100 words)', 'Medium (300 words)', 'Long (600 words)', 'Extended (1000 words)']},
    ]

    system_prompt = (
        'You are a versatile content creator and copywriter. Generate high-quality content on the given topic. '
        'Content type: {content_type}. Tone: {tone}. Target length: {length}. '
        'Write engaging, purposeful content tailored to the specified format. Include clear messaging, '
        'appropriate formatting for the content type, and a strong value proposition where applicable.'
    )


class ParagraphGenerator(BaseGenerator):
    slug = 'ai-paragraph-generator'
    name = 'AI Paragraph Generator'
    description = 'Generate well-crafted paragraphs on any topic with your desired tone and style.'
    category = 'Content & SEO'
    icon = 'paragraph'
    meta_title = 'Free AI Paragraph Generator'
    meta_description = 'Generate well-crafted paragraphs on any topic instantly. Choose your tone and length.'

    fields = [
        {'name': 'topic', 'label': 'Paragraph Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What should the paragraph be about?'},
        {'name': 'num_paragraphs', 'label': 'Number of Paragraphs', 'type': 'select', 'required': False, 'options': ['1', '2', '3', '5']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Neutral', 'Formal', 'Casual', 'Descriptive', 'Persuasive', 'Narrative']},
    ]

    system_prompt = (
        'You are an expert writer. Generate {num_paragraphs} well-crafted paragraph(s) on the given topic. '
        'Tone: {tone}. Each paragraph should have a clear topic sentence, supporting details, '
        'and a smooth closing. Use varied sentence structures and precise language. '
        'Ensure each paragraph is cohesive and flows naturally.'
    )


class SentenceGenerator(BaseGenerator):
    slug = 'ai-sentence-generator'
    name = 'AI Sentence Generator'
    description = 'Generate clear, polished sentences on any topic for essays, stories, or content.'
    category = 'Content & SEO'
    icon = 'sentence'
    meta_title = 'Free AI Sentence Generator'
    meta_description = 'Generate clear, polished sentences on any topic. Perfect for essays, stories, and content creation.'

    fields = [
        {'name': 'topic', 'label': 'Topic or Context', 'type': 'textarea', 'required': True, 'placeholder': 'Enter a topic or context for the sentences...'},
        {'name': 'num_sentences', 'label': 'Number of Sentences', 'type': 'select', 'required': False, 'options': ['1', '3', '5', '10']},
        {'name': 'style', 'label': 'Sentence Style', 'type': 'select', 'required': False, 'options': ['Simple', 'Complex', 'Compound', 'Descriptive', 'Persuasive', 'Creative']},
    ]

    system_prompt = (
        'You are an expert language craftsperson. Generate {num_sentences} well-constructed sentence(s) '
        'on the given topic. Style: {style}. Each sentence should be grammatically perfect, clear, '
        'and impactful. Vary sentence openings and structures. Number each sentence for clarity.'
    )


class TextGenerator(BaseGenerator):
    slug = 'ai-text-generator'
    name = 'AI Text Generator'
    description = 'Generate custom text for any purpose with flexible length and formatting options.'
    category = 'Content & SEO'
    icon = 'text'
    meta_title = 'Free AI Text Generator'
    meta_description = 'Generate custom text for any purpose. Flexible length, tone, and formatting options.'

    fields = [
        {'name': 'prompt', 'label': 'What to Write', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the text you need generated...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Brief (50 words)', 'Short (150 words)', 'Medium (300 words)', 'Long (600 words)']},
        {'name': 'format', 'label': 'Format', 'type': 'select', 'required': False, 'options': ['Plain Text', 'Bullet Points', 'Numbered List', 'Formatted with Headings']},
    ]

    system_prompt = (
        'You are a versatile text generator. Generate text based on the given instructions. '
        'Target length: {length}. Format: {format}. '
        'Write clear, well-organized text that directly addresses the request. '
        'Adapt your tone and style to suit the context of the request.'
    )


class OutlineGenerator(BaseGenerator):
    slug = 'ai-outline-generator'
    name = 'AI Outline Generator'
    description = 'Generate structured outlines for blog posts, articles, presentations, and more.'
    category = 'Content & SEO'
    icon = 'outline'
    meta_title = 'Free AI Outline Generator'
    meta_description = 'Generate structured outlines for blog posts, articles, and presentations instantly.'

    fields = [
        {'name': 'topic', 'label': 'Topic', 'type': 'textarea', 'required': True, 'placeholder': 'Enter the topic you want to outline...'},
        {'name': 'outline_type', 'label': 'Outline Type', 'type': 'select', 'required': False, 'options': ['Blog Post', 'Article', 'Presentation', 'Report', 'Book Chapter', 'Course Module']},
        {'name': 'depth', 'label': 'Detail Level', 'type': 'select', 'required': False, 'options': ['Basic (main points)', 'Detailed (sub-points)', 'Comprehensive (full notes)']},
    ]

    system_prompt = (
        'You are an expert content strategist and outliner. Create a well-structured outline for the given topic. '
        'Type: {outline_type}. Detail level: {depth}. '
        'Use Roman numerals for main sections, letters for sub-points, and numbers for supporting details. '
        'Include an introduction, logically ordered main sections, and a conclusion. '
        'Each point should be clear and actionable.'
    )


class ListicleGenerator(BaseGenerator):
    slug = 'ai-listicle-generator'
    name = 'AI Listicle Generator'
    description = 'Generate engaging list-format articles with numbered items and descriptions.'
    category = 'Content & SEO'
    icon = 'list'
    meta_title = 'Free AI Listicle Generator'
    meta_description = 'Generate engaging listicle articles with numbered items and detailed descriptions.'

    fields = [
        {'name': 'topic', 'label': 'Listicle Topic', 'type': 'textarea', 'required': True, 'placeholder': 'e.g., Best productivity tools for remote teams'},
        {'name': 'num_items', 'label': 'Number of Items', 'type': 'select', 'required': False, 'options': ['5', '7', '10', '15', '20']},
        {'name': 'style', 'label': 'Description Style', 'type': 'select', 'required': False, 'options': ['Brief (1-2 sentences)', 'Medium (short paragraph)', 'Detailed (full paragraph)']},
    ]

    system_prompt = (
        'You are an expert content writer specializing in listicle-format articles. Generate a listicle '
        'on the given topic with {num_items} items. Description style: {style}. '
        'Include an engaging introduction, numbered items each with a bold title and description, '
        'and a brief conclusion. Make each item informative and distinct from the others.'
    )


class FAQGenerator(BaseGenerator):
    slug = 'ai-faq-generator'
    name = 'AI FAQ Generator'
    description = 'Generate comprehensive FAQ sections with relevant questions and clear answers.'
    category = 'Content & SEO'
    icon = 'faq'
    meta_title = 'Free AI FAQ Generator'
    meta_description = 'Generate comprehensive FAQ sections with relevant questions and clear answers for any topic.'

    fields = [
        {'name': 'topic', 'label': 'Topic or Business', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your topic, product, or business...'},
        {'name': 'num_questions', 'label': 'Number of FAQs', 'type': 'select', 'required': False, 'options': ['5', '8', '10', '15', '20']},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'e.g., new customers, students, developers'},
    ]

    system_prompt = (
        'You are an expert content writer and customer experience specialist. Generate a comprehensive '
        'FAQ section with {num_questions} questions and answers on the given topic. '
        'Target audience: {audience}. Each Q&A should address a genuine concern the audience would have. '
        'Format with clear Q: and A: labels. Keep answers concise but thorough. '
        'Order questions from most common to more specific.'
    )


class MetaDescriptionGenerator(BaseGenerator):
    slug = 'ai-meta-description-generator'
    name = 'AI Meta Description Generator'
    description = 'Generate SEO-optimized meta descriptions that improve click-through rates.'
    category = 'Content & SEO'
    icon = 'meta'
    meta_title = 'Free AI Meta Description Generator'
    meta_description = 'Generate SEO-optimized meta descriptions that boost click-through rates from search results.'

    fields = [
        {'name': 'page_topic', 'label': 'Page Topic or Title', 'type': 'textarea', 'required': True, 'placeholder': 'Enter the page title or describe the page content...'},
        {'name': 'keywords', 'label': 'Target Keywords', 'type': 'text', 'required': False, 'placeholder': 'e.g., best running shoes, marathon training'},
        {'name': 'num_options', 'label': 'Number of Options', 'type': 'select', 'required': False, 'options': ['3', '5', '8']},
    ]

    system_prompt = (
        'You are an SEO specialist and meta description expert. Generate {num_options} unique meta description '
        'options for the given page. Target keywords: {keywords}. '
        'Each meta description must be between 150-160 characters, include a call to action, '
        'naturally incorporate target keywords, and entice users to click. '
        'Label each option with its character count.'
    )


class TitleGenerator(BaseGenerator):
    slug = 'ai-title-generator'
    name = 'AI Title Generator'
    description = 'Generate compelling titles for blog posts, articles, videos, and other content.'
    category = 'Content & SEO'
    icon = 'title'
    meta_title = 'Free AI Title Generator'
    meta_description = 'Generate compelling, click-worthy titles for blog posts, articles, videos, and more.'

    fields = [
        {'name': 'topic', 'label': 'Content Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What is your content about?'},
        {'name': 'content_type', 'label': 'Content Type', 'type': 'select', 'required': False, 'options': ['Blog Post', 'Article', 'YouTube Video', 'Podcast Episode', 'Newsletter', 'Landing Page']},
        {'name': 'style', 'label': 'Title Style', 'type': 'select', 'required': False, 'options': ['How-To', 'Listicle', 'Question', 'Provocative', 'Direct', 'Curiosity Gap']},
        {'name': 'num_options', 'label': 'Number of Options', 'type': 'select', 'required': False, 'options': ['5', '10', '15']},
    ]

    system_prompt = (
        'You are a headline copywriter and content strategist. Generate {num_options} compelling title options '
        'for the given topic. Content type: {content_type}. Style: {style}. '
        'Each title should be attention-grabbing, clear, and optimized for clicks. '
        'Vary the approaches: use numbers, power words, questions, and emotional triggers. '
        'Keep titles under 70 characters for SEO. Number each option.'
    )


class HeadlineGenerator(BaseGenerator):
    slug = 'ai-headline-generator'
    name = 'AI Headline Generator'
    description = 'Generate powerful, attention-grabbing headlines for ads, articles, and campaigns.'
    category = 'Content & SEO'
    icon = 'headline'
    meta_title = 'Free AI Headline Generator'
    meta_description = 'Generate powerful, attention-grabbing headlines for ads, articles, and marketing campaigns.'

    fields = [
        {'name': 'topic', 'label': 'Topic or Product', 'type': 'textarea', 'required': True, 'placeholder': 'What are you writing a headline for?'},
        {'name': 'purpose', 'label': 'Purpose', 'type': 'select', 'required': False, 'options': ['News Article', 'Advertisement', 'Email Subject Line', 'Social Media', 'Landing Page', 'Press Release']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Bold', 'Professional', 'Witty', 'Urgent', 'Inspirational', 'Informative']},
        {'name': 'num_options', 'label': 'Number of Options', 'type': 'select', 'required': False, 'options': ['5', '10', '15']},
    ]

    system_prompt = (
        'You are an expert copywriter specializing in headlines. Generate {num_options} powerful headline '
        'options for the given topic. Purpose: {purpose}. Tone: {tone}. '
        'Apply proven headline formulas: benefit-driven, curiosity-inducing, specific numbers, '
        'emotional triggers, and urgency. Each headline should be concise and impactful. '
        'Number each option.'
    )


class SEODescriptionGenerator(BaseGenerator):
    slug = 'ai-seo-description-generator'
    name = 'AI SEO Description Generator'
    description = 'Generate SEO-optimized descriptions for products, pages, and business listings.'
    category = 'Content & SEO'
    icon = 'seo'
    meta_title = 'Free AI SEO Description Generator'
    meta_description = 'Generate SEO-optimized descriptions for products, web pages, and business listings.'

    fields = [
        {'name': 'subject', 'label': 'Subject to Describe', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the product, page, or business...'},
        {'name': 'description_type', 'label': 'Description Type', 'type': 'select', 'required': False, 'options': ['Product Description', 'Page Description', 'Business Listing', 'Category Page', 'Service Description']},
        {'name': 'keywords', 'label': 'Target Keywords', 'type': 'text', 'required': False, 'placeholder': 'e.g., organic skincare, natural moisturizer'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (50 words)', 'Medium (100 words)', 'Long (200 words)', 'Extended (300 words)']},
    ]

    system_prompt = (
        'You are an SEO copywriting expert. Write an SEO-optimized description for the given subject. '
        'Type: {description_type}. Target keywords: {keywords}. Length: {length}. '
        'Naturally incorporate target keywords without stuffing. Write compelling, benefit-focused copy '
        'that appeals to both search engines and human readers. Include a subtle call to action. '
        'Use clear, scannable formatting appropriate for the description type.'
    )


CONTENT_GENERATORS = [
    BlogWriter,
    ArticleWriter,
    ContentGenerator,
    ParagraphGenerator,
    SentenceGenerator,
    TextGenerator,
    OutlineGenerator,
    ListicleGenerator,
    FAQGenerator,
    MetaDescriptionGenerator,
    TitleGenerator,
    HeadlineGenerator,
    SEODescriptionGenerator,
]
