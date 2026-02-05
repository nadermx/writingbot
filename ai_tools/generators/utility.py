from ai_tools.generators.base import BaseGenerator


class PromptGenerator(BaseGenerator):
    slug = 'ai-prompt-generator'
    name = 'AI Prompt Generator'
    description = 'Generate effective prompts for ChatGPT, Claude, and other AI assistants.'
    category = 'General Utility'
    icon = 'prompt'
    meta_title = 'Free AI Prompt Generator'
    meta_description = 'Generate effective prompts for ChatGPT, Claude, and other AI tools to get better results.'

    fields = [
        {'name': 'goal', 'label': 'What Do You Want the AI to Do?', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the task or output you want from the AI...'},
        {'name': 'ai_tool', 'label': 'Target AI Tool', 'type': 'select', 'required': False, 'options': ['ChatGPT', 'Claude', 'Gemini', 'Midjourney', 'DALL-E', 'Stable Diffusion', 'General']},
        {'name': 'detail_level', 'label': 'Detail Level', 'type': 'select', 'required': False, 'options': ['Simple', 'Detailed', 'Expert-Level']},
        {'name': 'num_prompts', 'label': 'Number of Prompts', 'type': 'select', 'required': False, 'options': ['1', '3', '5']},
    ]

    system_prompt = (
        'You are an expert prompt engineer. Generate {num_prompts} effective prompt(s) that a user can copy '
        'and paste into {ai_tool} to achieve their goal. Detail level: {detail_level}. '
        'Each prompt should include clear instructions, context, desired format, and constraints. '
        'Use prompt engineering best practices: role assignment, step-by-step instructions, '
        'and output formatting. Label each prompt option clearly.'
    )


class RandomPromptGenerator(BaseGenerator):
    slug = 'ai-random-prompt-generator'
    name = 'AI Random Prompt Generator'
    description = 'Generate random, creative prompts for brainstorming, practice, or experimentation.'
    category = 'General Utility'
    icon = 'random'
    meta_title = 'Free AI Random Prompt Generator'
    meta_description = 'Generate random creative prompts for brainstorming, writing practice, and AI experimentation.'

    fields = [
        {'name': 'category', 'label': 'Category', 'type': 'select', 'required': False, 'options': ['Any', 'Creative Writing', 'Business', 'Technology', 'Philosophy', 'Science', 'Art & Design', 'Education']},
        {'name': 'difficulty', 'label': 'Difficulty', 'type': 'select', 'required': False, 'options': ['Easy', 'Medium', 'Challenging', 'Expert']},
        {'name': 'num_prompts', 'label': 'Number of Prompts', 'type': 'select', 'required': False, 'options': ['1', '3', '5', '10']},
    ]

    system_prompt = (
        'You are a creative brainstorming assistant. Generate {num_prompts} random, unique prompt(s) '
        'for the user to explore. Category: {category}. Difficulty: {difficulty}. '
        'Each prompt should be thought-provoking, specific enough to act on, and inspire creative thinking. '
        'Vary the formats: questions, scenarios, challenges, and what-if hypotheticals. '
        'Number each prompt.'
    )


class WritingPromptGenerator(BaseGenerator):
    slug = 'ai-writing-prompt-generator'
    name = 'AI Writing Prompt Generator'
    description = 'Generate inspiring writing prompts for fiction, nonfiction, poetry, and journaling.'
    category = 'General Utility'
    icon = 'writing'
    meta_title = 'Free AI Writing Prompt Generator'
    meta_description = 'Generate inspiring writing prompts for fiction, nonfiction, poetry, and journaling.'

    fields = [
        {'name': 'genre', 'label': 'Genre', 'type': 'select', 'required': False, 'options': ['Fiction', 'Nonfiction', 'Poetry', 'Journal Entry', 'Fantasy', 'Sci-Fi', 'Mystery', 'Romance', 'Horror', 'Literary']},
        {'name': 'theme', 'label': 'Theme (optional)', 'type': 'text', 'required': False, 'placeholder': 'e.g., loss, adventure, identity, technology'},
        {'name': 'num_prompts', 'label': 'Number of Prompts', 'type': 'select', 'required': False, 'options': ['1', '3', '5', '10']},
    ]

    system_prompt = (
        'You are a creative writing coach. Generate {num_prompts} inspiring writing prompt(s). '
        'Genre: {genre}. Theme: {theme}. '
        'Each prompt should spark the imagination and give the writer a clear starting point. '
        'Include a mix of opening lines, scenarios, character sketches, and situational setups. '
        'Make each prompt vivid and emotionally engaging. Number each prompt.'
    )


class InspirationalQuoteGenerator(BaseGenerator):
    slug = 'ai-inspirational-quote-generator'
    name = 'AI Inspirational Quote Generator'
    description = 'Generate original inspirational quotes for motivation, social media, or presentations.'
    category = 'General Utility'
    icon = 'quote'
    meta_title = 'Free AI Inspirational Quote Generator'
    meta_description = 'Generate original inspirational quotes for motivation, social media, and presentations.'

    fields = [
        {'name': 'theme', 'label': 'Theme', 'type': 'text', 'required': True, 'placeholder': 'e.g., perseverance, leadership, creativity, growth'},
        {'name': 'style', 'label': 'Style', 'type': 'select', 'required': False, 'options': ['Motivational', 'Philosophical', 'Poetic', 'Humorous', 'Stoic', 'Modern']},
        {'name': 'num_quotes', 'label': 'Number of Quotes', 'type': 'select', 'required': False, 'options': ['3', '5', '10', '15']},
    ]

    system_prompt = (
        'You are a gifted writer creating original inspirational quotes. Generate {num_quotes} original '
        'quotes on the given theme. Style: {style}. '
        'Each quote should be concise (1-3 sentences), memorable, and thought-provoking. '
        'Use vivid metaphors, strong verbs, and universal truths. '
        'These must be original compositions, not existing quotes. Number each quote.'
    )


class RandomQuoteGenerator(BaseGenerator):
    slug = 'ai-random-quote-generator'
    name = 'AI Random Quote Generator'
    description = 'Generate random original quotes on diverse topics for daily inspiration.'
    category = 'General Utility'
    icon = 'quote'
    meta_title = 'Free AI Random Quote Generator'
    meta_description = 'Generate random original quotes on diverse topics for daily inspiration and reflection.'

    fields = [
        {'name': 'mood', 'label': 'Mood', 'type': 'select', 'required': False, 'options': ['Any', 'Uplifting', 'Reflective', 'Empowering', 'Calming', 'Energizing', 'Humorous']},
        {'name': 'audience', 'label': 'Audience', 'type': 'select', 'required': False, 'options': ['General', 'Entrepreneurs', 'Students', 'Leaders', 'Creatives', 'Athletes']},
        {'name': 'num_quotes', 'label': 'Number of Quotes', 'type': 'select', 'required': False, 'options': ['3', '5', '10']},
    ]

    system_prompt = (
        'You are a creative quote writer. Generate {num_quotes} random original quotes covering diverse topics. '
        'Mood: {mood}. Audience: {audience}. '
        'Each quote should be on a different subject, concise, and impactful. '
        'Span topics like success, love, wisdom, courage, change, and happiness. '
        'These must be original compositions. Number each quote with its topic in parentheses.'
    )


class AcronymGenerator(BaseGenerator):
    slug = 'ai-acronym-generator'
    name = 'AI Acronym Generator'
    description = 'Generate meaningful acronyms from phrases or create backronyms from existing letters.'
    category = 'General Utility'
    icon = 'acronym'
    meta_title = 'Free AI Acronym Generator'
    meta_description = 'Generate meaningful acronyms from phrases or create backronyms from existing letters.'

    fields = [
        {'name': 'input_text', 'label': 'Phrase or Letters', 'type': 'textarea', 'required': True, 'placeholder': 'Enter a phrase to abbreviate, or letters to expand into an acronym...'},
        {'name': 'mode', 'label': 'Mode', 'type': 'select', 'required': False, 'options': ['Create Acronym (from phrase)', 'Create Backronym (from letters)', 'Both']},
        {'name': 'context', 'label': 'Context or Industry', 'type': 'text', 'required': False, 'placeholder': 'e.g., healthcare, technology, education'},
    ]

    system_prompt = (
        'You are a creative naming and branding specialist. {mode} for the given input. '
        'Context: {context}. '
        'If creating an acronym: generate 5 catchy, memorable abbreviations from the phrase. '
        'If creating a backronym: generate 5 meaningful expansions for each letter. '
        'Each option should be easy to remember, relevant to the context, and professional. '
        'Explain why each option works. Number each option.'
    )


class CaseStudyGenerator(BaseGenerator):
    slug = 'ai-case-study-generator'
    name = 'AI Case Study Generator'
    description = 'Generate professional case studies with problem, solution, and results sections.'
    category = 'General Utility'
    icon = 'case-study'
    meta_title = 'Free AI Case Study Generator'
    meta_description = 'Generate professional case studies with problem, solution, and measurable results.'

    fields = [
        {'name': 'subject', 'label': 'Company or Project', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the company, project, or scenario...'},
        {'name': 'industry', 'label': 'Industry', 'type': 'text', 'required': False, 'placeholder': 'e.g., SaaS, Healthcare, E-commerce'},
        {'name': 'focus', 'label': 'Key Focus', 'type': 'select', 'required': False, 'options': ['Business Growth', 'Cost Reduction', 'Customer Success', 'Digital Transformation', 'Process Improvement', 'Product Launch']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (500 words)', 'Standard (1000 words)', 'Detailed (1500 words)']},
    ]

    system_prompt = (
        'You are a professional case study writer. Write a compelling case study for the given subject. '
        'Industry: {industry}. Focus area: {focus}. Target length: {length}. '
        'Structure with: Executive Summary, Background/Challenge, Solution/Approach, '
        'Implementation, Results (with metrics), and Key Takeaways. '
        'Use specific details, data points, and a narrative that demonstrates clear value.'
    )


class StoryboardGenerator(BaseGenerator):
    slug = 'ai-storyboard-generator'
    name = 'AI Storyboard Generator'
    description = 'Generate detailed storyboards for videos, presentations, ads, and animations.'
    category = 'General Utility'
    icon = 'storyboard'
    meta_title = 'Free AI Storyboard Generator'
    meta_description = 'Generate detailed storyboards for videos, presentations, ads, and animations.'

    fields = [
        {'name': 'concept', 'label': 'Video/Story Concept', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your video, ad, or story concept...'},
        {'name': 'format', 'label': 'Format', 'type': 'select', 'required': False, 'options': ['YouTube Video', 'Commercial/Ad', 'Short Film', 'Explainer Video', 'Social Media Reel', 'Presentation']},
        {'name': 'num_scenes', 'label': 'Number of Scenes', 'type': 'select', 'required': False, 'options': ['5', '8', '10', '15', '20']},
    ]

    system_prompt = (
        'You are a professional storyboard artist and video strategist. Create a detailed storyboard '
        'for the given concept. Format: {format}. Number of scenes: {num_scenes}. '
        'For each scene include: Scene Number, Visual Description (what the viewer sees), '
        'Action/Movement, Dialogue/Voiceover, Audio/Music Notes, and Duration Estimate. '
        'Ensure a clear narrative arc with a hook, development, and conclusion.'
    )


class APIDocumentationGenerator(BaseGenerator):
    slug = 'ai-api-documentation-generator'
    name = 'AI API Documentation Generator'
    description = 'Generate clear, developer-friendly API documentation with endpoints and examples.'
    category = 'General Utility'
    icon = 'api'
    meta_title = 'Free AI API Documentation Generator'
    meta_description = 'Generate clear, developer-friendly API documentation with endpoints, parameters, and examples.'

    fields = [
        {'name': 'api_description', 'label': 'API Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your API, its purpose, and key endpoints...'},
        {'name': 'auth_type', 'label': 'Authentication Type', 'type': 'select', 'required': False, 'options': ['API Key', 'OAuth 2.0', 'Bearer Token', 'Basic Auth', 'None']},
        {'name': 'format', 'label': 'Documentation Format', 'type': 'select', 'required': False, 'options': ['REST API', 'GraphQL', 'WebSocket', 'General']},
    ]

    system_prompt = (
        'You are a senior technical writer specializing in API documentation. Generate comprehensive '
        'documentation for the described API. Authentication: {auth_type}. Format: {format}. '
        'Include: Overview, Authentication setup, Base URL, Endpoints (with HTTP methods, parameters, '
        'request/response examples in JSON), Error codes, Rate limits, and a Getting Started guide. '
        'Use clean formatting with code blocks for examples.'
    )


class ProductNameGenerator(BaseGenerator):
    slug = 'ai-product-name-generator'
    name = 'AI Product Name Generator'
    description = 'Generate creative, memorable product names for apps, tools, and consumer goods.'
    category = 'General Utility'
    icon = 'product'
    meta_title = 'Free AI Product Name Generator'
    meta_description = 'Generate creative, memorable product names for apps, tools, and consumer goods.'

    fields = [
        {'name': 'product_description', 'label': 'Product Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your product, its features, and target market...'},
        {'name': 'style', 'label': 'Naming Style', 'type': 'select', 'required': False, 'options': ['Modern/Tech', 'Playful', 'Professional', 'Minimalist', 'Descriptive', 'Abstract']},
        {'name': 'industry', 'label': 'Industry', 'type': 'text', 'required': False, 'placeholder': 'e.g., FinTech, Health & Wellness, Food'},
        {'name': 'num_names', 'label': 'Number of Names', 'type': 'select', 'required': False, 'options': ['5', '10', '15', '20']},
    ]

    system_prompt = (
        'You are a creative branding specialist and naming expert. Generate {num_names} product name ideas '
        'for the described product. Style: {style}. Industry: {industry}. '
        'Each name should be: memorable, easy to pronounce, suitable for a domain name, and evocative of '
        'the product\'s value. Include a brief explanation of why each name works. '
        'Mix approaches: compound words, invented words, metaphors, and abbreviations. Number each option.'
    )


class BusinessNameGenerator(BaseGenerator):
    slug = 'ai-business-name-generator'
    name = 'AI Business Name Generator'
    description = 'Generate professional, brandable business names for startups and companies.'
    category = 'General Utility'
    icon = 'business'
    meta_title = 'Free AI Business Name Generator'
    meta_description = 'Generate professional, brandable business names for startups, agencies, and companies.'

    fields = [
        {'name': 'business_description', 'label': 'Business Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your business, services, and target market...'},
        {'name': 'style', 'label': 'Naming Style', 'type': 'select', 'required': False, 'options': ['Professional', 'Creative', 'Modern', 'Classic', 'Techy', 'Friendly']},
        {'name': 'industry', 'label': 'Industry', 'type': 'text', 'required': False, 'placeholder': 'e.g., Consulting, E-commerce, SaaS'},
        {'name': 'num_names', 'label': 'Number of Names', 'type': 'select', 'required': False, 'options': ['5', '10', '15', '20']},
    ]

    system_prompt = (
        'You are an expert branding consultant and business naming specialist. Generate {num_names} business '
        'name ideas. Style: {style}. Industry: {industry}. '
        'Each name should be: professional, memorable, easy to spell, domain-friendly, and reflective of '
        'the business\'s values and market. Include a brief rationale for each name. '
        'Consider: real words, portmanteaus, acronyms, invented words, and metaphorical names. '
        'Number each option.'
    )


UTILITY_GENERATORS = [
    PromptGenerator,
    RandomPromptGenerator,
    WritingPromptGenerator,
    InspirationalQuoteGenerator,
    RandomQuoteGenerator,
    AcronymGenerator,
    CaseStudyGenerator,
    StoryboardGenerator,
    APIDocumentationGenerator,
    ProductNameGenerator,
    BusinessNameGenerator,
]
