from ai_tools.generators.base import BaseGenerator


class AdCopyGenerator(BaseGenerator):
    slug = 'ai-ad-copy-generator'
    name = 'AI Ad Copy Generator'
    description = 'Generate compelling ad copy that drives clicks, conversions, and sales across any platform.'
    category = 'Marketing & Sales'
    icon = 'ad'
    meta_title = 'Free AI Ad Copy Generator'
    meta_description = 'Create high-converting ad copy for Google Ads, Facebook, Instagram, and LinkedIn in seconds.'

    fields = [
        {'name': 'product', 'label': 'Product/Service', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your product or service and its key benefits...'},
        {'name': 'platform', 'label': 'Platform', 'type': 'select', 'required': False, 'options': ['Google Ads', 'Facebook', 'Instagram', 'LinkedIn']},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'e.g., Small business owners, Parents, Tech enthusiasts'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Casual', 'Urgent', 'Playful']},
    ]

    system_prompt = (
        'You are an expert advertising copywriter. Write compelling ad copy for {platform}. '
        'Target audience: {audience}. Tone: {tone}. '
        'Follow platform-specific best practices for character limits and formatting. '
        'Include a strong headline, persuasive body copy, and a clear call to action. '
        'Provide 3 variations of the ad copy.'
    )


class SalesPitchGenerator(BaseGenerator):
    slug = 'ai-sales-pitch-generator'
    name = 'AI Sales Pitch Generator'
    description = 'Create persuasive sales pitches that highlight value propositions and close deals.'
    category = 'Marketing & Sales'
    icon = 'pitch'
    meta_title = 'Free AI Sales Pitch Generator'
    meta_description = 'Generate persuasive sales pitches that win clients and close deals faster.'

    fields = [
        {'name': 'product', 'label': 'Product/Service', 'type': 'textarea', 'required': True, 'placeholder': 'Describe what you are selling and its key benefits...'},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'e.g., C-suite executives, IT managers, Retailers'},
        {'name': 'format', 'label': 'Pitch Format', 'type': 'select', 'required': False, 'options': ['Elevator Pitch', '1-Minute Pitch', 'Full Presentation', 'Cold Call Script']},
    ]

    system_prompt = (
        'You are an expert sales strategist. Create a compelling {format} for the described product or service. '
        'Target audience: {audience}. '
        'Structure the pitch with a hook, problem statement, solution, key benefits, social proof, '
        'and a strong closing with call to action. Use persuasive, confident language.'
    )


class SalesEmailGenerator(BaseGenerator):
    slug = 'ai-sales-email-generator'
    name = 'AI Sales Email Generator'
    description = 'Generate effective sales emails that get opened, read, and responded to.'
    category = 'Marketing & Sales'
    icon = 'email'
    meta_title = 'Free AI Sales Email Generator'
    meta_description = 'Create sales emails that get responses and drive conversions.'

    fields = [
        {'name': 'product', 'label': 'Product/Service', 'type': 'textarea', 'required': True, 'placeholder': 'Describe what you are selling...'},
        {'name': 'recipient', 'label': 'Recipient Role', 'type': 'text', 'required': False, 'placeholder': 'e.g., Marketing Director, CEO, Procurement Manager'},
        {'name': 'email_type', 'label': 'Email Type', 'type': 'select', 'required': False, 'options': ['Cold Outreach', 'Follow-up', 'Demo Request', 'Proposal']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Friendly', 'Consultative', 'Direct']},
    ]

    system_prompt = (
        'You are an expert sales email copywriter. Write a {email_type} sales email. '
        'Recipient role: {recipient}. Tone: {tone}. '
        'Include a compelling subject line, personalized opening, clear value proposition, '
        'social proof or credibility, and a specific call to action. Keep it concise and scannable.'
    )


class MarketingEmailGenerator(BaseGenerator):
    slug = 'ai-marketing-email-generator'
    name = 'AI Marketing Email Generator'
    description = 'Create engaging marketing emails that build brand awareness and drive action.'
    category = 'Marketing & Sales'
    icon = 'email'
    meta_title = 'Free AI Marketing Email Generator'
    meta_description = 'Generate engaging marketing emails that boost open rates and drive conversions.'

    fields = [
        {'name': 'topic', 'label': 'Email Topic/Campaign', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the campaign, announcement, or message...'},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'e.g., Existing customers, Newsletter subscribers'},
        {'name': 'email_type', 'label': 'Email Type', 'type': 'select', 'required': False, 'options': ['Newsletter', 'Announcement', 'Drip Campaign', 'Re-engagement', 'Welcome Email']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Friendly', 'Excited', 'Informative']},
    ]

    system_prompt = (
        'You are an expert email marketer. Write a {email_type} marketing email. '
        'Audience: {audience}. Tone: {tone}. '
        'Include an attention-grabbing subject line, preview text, compelling header, '
        'well-structured body with clear value, and a prominent call to action. '
        'Optimize for readability and engagement.'
    )


class ProductDescriptionGenerator(BaseGenerator):
    slug = 'ai-product-description-generator'
    name = 'AI Product Description Generator'
    description = 'Write compelling product descriptions that highlight benefits and drive purchases.'
    category = 'Marketing & Sales'
    icon = 'product'
    meta_title = 'Free AI Product Description Generator'
    meta_description = 'Create persuasive product descriptions that boost sales and conversions.'

    fields = [
        {'name': 'product', 'label': 'Product Details', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the product, its features, and target customer...'},
        {'name': 'platform', 'label': 'Platform', 'type': 'select', 'required': False, 'options': ['E-commerce Website', 'Amazon', 'Shopify', 'Etsy', 'Social Media']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Luxurious', 'Casual', 'Technical', 'Fun']},
    ]

    system_prompt = (
        'You are an expert e-commerce copywriter. Write a compelling product description for {platform}. '
        'Tone: {tone}. '
        'Include a captivating headline, benefit-driven opening, key features as bullet points, '
        'sensory and emotional language, and a subtle call to action. '
        'Optimize for both customers and search engines.'
    )


class DiscountPromotionGenerator(BaseGenerator):
    slug = 'ai-discount-promotion-generator'
    name = 'AI Discount Promotion Generator'
    description = 'Create attention-grabbing discount and sale promotions that drive urgency and conversions.'
    category = 'Marketing & Sales'
    icon = 'discount'
    meta_title = 'Free AI Discount Promotion Generator'
    meta_description = 'Generate compelling discount and sale promotions that create urgency and boost sales.'

    fields = [
        {'name': 'offer', 'label': 'Offer Details', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the discount, sale, or special offer...'},
        {'name': 'channel', 'label': 'Channel', 'type': 'select', 'required': False, 'options': ['Email', 'Social Media', 'Website Banner', 'SMS', 'Print']},
        {'name': 'urgency', 'label': 'Urgency Level', 'type': 'select', 'required': False, 'options': ['Limited Time', 'Flash Sale', 'Seasonal', 'Ongoing']},
    ]

    system_prompt = (
        'You are an expert promotional copywriter. Create a compelling discount promotion for {channel}. '
        'Urgency level: {urgency}. '
        'Write attention-grabbing copy that clearly communicates the offer, creates urgency, '
        'highlights the value to the customer, and includes a strong call to action. '
        'Include a headline, body copy, and terms/conditions if relevant.'
    )


class ProductPromotionGenerator(BaseGenerator):
    slug = 'ai-product-promotion-generator'
    name = 'AI Product Promotion Generator'
    description = 'Generate product promotion copy that showcases features and drives interest.'
    category = 'Marketing & Sales'
    icon = 'promotion'
    meta_title = 'Free AI Product Promotion Generator'
    meta_description = 'Create compelling product promotion copy that drives interest and sales.'

    fields = [
        {'name': 'product', 'label': 'Product Details', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the product and what makes it special...'},
        {'name': 'channel', 'label': 'Channel', 'type': 'select', 'required': False, 'options': ['Social Media', 'Email', 'Blog Post', 'Press Release', 'Video Script']},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'e.g., Tech enthusiasts, Fitness lovers, Parents'},
    ]

    system_prompt = (
        'You are an expert product marketer. Write a compelling product promotion for {channel}. '
        'Target audience: {audience}. '
        'Highlight the unique selling points, key benefits, and competitive advantages. '
        'Use engaging language that resonates with the target audience and includes a clear call to action.'
    )


class EventPromotionGenerator(BaseGenerator):
    slug = 'ai-event-promotion-generator'
    name = 'AI Event Promotion Generator'
    description = 'Create exciting event promotion copy that drives registrations and attendance.'
    category = 'Marketing & Sales'
    icon = 'event'
    meta_title = 'Free AI Event Promotion Generator'
    meta_description = 'Generate event promotion copy that drives registrations and builds excitement.'

    fields = [
        {'name': 'event', 'label': 'Event Details', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the event, date, location, speakers, and highlights...'},
        {'name': 'event_type', 'label': 'Event Type', 'type': 'select', 'required': False, 'options': ['Conference', 'Webinar', 'Workshop', 'Product Launch', 'Networking', 'Fundraiser']},
        {'name': 'channel', 'label': 'Channel', 'type': 'select', 'required': False, 'options': ['Email', 'Social Media', 'Website', 'Flyer', 'Press Release']},
    ]

    system_prompt = (
        'You are an expert event marketer. Write compelling {event_type} promotion copy for {channel}. '
        'Build excitement around the event, highlight key speakers or activities, '
        'communicate the value of attending, include essential details (date, time, location), '
        'and provide a clear registration call to action. Create a sense of urgency.'
    )


class SloganGenerator(BaseGenerator):
    slug = 'ai-slogan-generator'
    name = 'AI Slogan Generator'
    description = 'Generate memorable slogans that capture your brand essence and stick in minds.'
    category = 'Marketing & Sales'
    icon = 'slogan'
    meta_title = 'Free AI Slogan Generator'
    meta_description = 'Create catchy, memorable slogans that capture your brand identity.'

    fields = [
        {'name': 'brand', 'label': 'Brand/Product', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your brand, product, or service and its core values...'},
        {'name': 'style', 'label': 'Style', 'type': 'select', 'required': False, 'options': ['Catchy', 'Inspirational', 'Humorous', 'Bold', 'Elegant']},
        {'name': 'industry', 'label': 'Industry', 'type': 'text', 'required': False, 'placeholder': 'e.g., Technology, Food, Fashion, Health'},
    ]

    system_prompt = (
        'You are an expert brand strategist and copywriter. Generate 10 creative slogans. '
        'Style: {style}. Industry: {industry}. '
        'Each slogan should be concise (under 10 words), memorable, and capture the brand essence. '
        'Include a mix of approaches: benefit-driven, emotional, aspirational, and clever wordplay. '
        'Briefly explain why each slogan works.'
    )


class TaglineGenerator(BaseGenerator):
    slug = 'ai-tagline-generator'
    name = 'AI Tagline Generator'
    description = 'Create powerful taglines that define your brand and resonate with your audience.'
    category = 'Marketing & Sales'
    icon = 'tagline'
    meta_title = 'Free AI Tagline Generator'
    meta_description = 'Generate powerful brand taglines that resonate with your target audience.'

    fields = [
        {'name': 'brand', 'label': 'Brand Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your brand, mission, and target audience...'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Friendly', 'Bold', 'Witty', 'Sophisticated']},
        {'name': 'keywords', 'label': 'Key Words/Themes', 'type': 'text', 'required': False, 'placeholder': 'e.g., innovation, trust, quality, speed'},
    ]

    system_prompt = (
        'You are an expert branding strategist. Generate 10 distinctive taglines. '
        'Tone: {tone}. Key themes: {keywords}. '
        'Each tagline should be 3-8 words, easily memorable, and convey the brand promise. '
        'Focus on emotional connection, differentiation, and lasting impact. '
        'Briefly explain the strategy behind each tagline.'
    )


class PressReleaseGenerator(BaseGenerator):
    slug = 'ai-press-release-generator'
    name = 'AI Press Release Generator'
    description = 'Generate professional press releases that get media coverage and attention.'
    category = 'Marketing & Sales'
    icon = 'press'
    meta_title = 'Free AI Press Release Generator'
    meta_description = 'Create professional press releases formatted for media distribution.'

    fields = [
        {'name': 'announcement', 'label': 'Announcement', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the news, event, product launch, or announcement...'},
        {'name': 'company', 'label': 'Company Name', 'type': 'text', 'required': True, 'placeholder': 'Your company or organization name'},
        {'name': 'pr_type', 'label': 'Release Type', 'type': 'select', 'required': False, 'options': ['Product Launch', 'Partnership', 'Funding', 'Award', 'Event', 'General News']},
        {'name': 'contact', 'label': 'Contact Info', 'type': 'text', 'required': False, 'placeholder': 'e.g., press@company.com'},
    ]

    system_prompt = (
        'You are an expert PR writer. Write a professional {pr_type} press release for {company}. '
        'Contact: {contact}. '
        'Follow standard press release format: headline, dateline, lead paragraph (who, what, when, where, why), '
        'supporting details, quotes from stakeholders, boilerplate "About" section, and media contact info. '
        'Write in AP style with a newsworthy, objective tone.'
    )


class LandingPageCopyGenerator(BaseGenerator):
    slug = 'ai-landing-page-copy-generator'
    name = 'AI Landing Page Copy Generator'
    description = 'Create high-converting landing page copy with compelling headlines and CTAs.'
    category = 'Marketing & Sales'
    icon = 'landing'
    meta_title = 'Free AI Landing Page Copy Generator'
    meta_description = 'Generate high-converting landing page copy with headlines, benefits, and CTAs.'

    fields = [
        {'name': 'product', 'label': 'Product/Service', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the product, service, or offer for the landing page...'},
        {'name': 'goal', 'label': 'Conversion Goal', 'type': 'select', 'required': False, 'options': ['Sign Up', 'Purchase', 'Download', 'Book a Demo', 'Get a Quote', 'Subscribe']},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'e.g., SaaS buyers, Freelancers, Enterprise teams'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Conversational', 'Bold', 'Minimalist']},
    ]

    system_prompt = (
        'You are an expert conversion copywriter. Write landing page copy optimized for {goal} conversions. '
        'Target audience: {audience}. Tone: {tone}. '
        'Include: a powerful headline and subheadline, hero section copy, 3-4 benefit sections with headers, '
        'social proof section, FAQ section, and multiple call-to-action blocks. '
        'Focus on benefits over features, use power words, and create urgency.'
    )


MARKETING_GENERATORS = [
    AdCopyGenerator,
    SalesPitchGenerator,
    SalesEmailGenerator,
    MarketingEmailGenerator,
    ProductDescriptionGenerator,
    DiscountPromotionGenerator,
    ProductPromotionGenerator,
    EventPromotionGenerator,
    SloganGenerator,
    TaglineGenerator,
    PressReleaseGenerator,
    LandingPageCopyGenerator,
]
