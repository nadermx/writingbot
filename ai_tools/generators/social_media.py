from ai_tools.generators.base import BaseGenerator


class SocialMediaPostGenerator(BaseGenerator):
    slug = 'ai-social-media-post-generator'
    name = 'AI Social Media Post Generator'
    description = 'Generate engaging social media posts tailored for any platform with the right tone and style.'
    category = 'Social Media'
    icon = 'social'
    meta_title = 'Free AI Social Media Post Generator'
    meta_description = 'Create engaging social media posts for Twitter, Facebook, LinkedIn, and more. Choose your platform, tone, and topic.'

    fields = [
        {'name': 'topic', 'label': 'Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What is your post about?'},
        {'name': 'platform', 'label': 'Platform', 'type': 'select', 'required': False, 'options': ['Twitter', 'Facebook', 'LinkedIn', 'Instagram', 'General']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Casual', 'Humorous', 'Inspirational', 'Informative']},
    ]

    system_prompt = (
        'You are a social media expert who crafts viral, engaging posts. Write a social media post '
        'about the given topic. Platform: {platform}. Tone: {tone}. '
        'Respect platform character limits and norms (e.g., concise for Twitter, longer-form for LinkedIn). '
        'Include a compelling hook, clear message, and a call to action where appropriate. '
        'Suggest relevant hashtags at the end.'
    )


class InstagramCaptionGenerator(BaseGenerator):
    slug = 'ai-instagram-caption-generator'
    name = 'AI Instagram Caption Generator'
    description = 'Create scroll-stopping Instagram captions with emojis, hashtags, and calls to action.'
    category = 'Social Media'
    icon = 'instagram'
    meta_title = 'Free AI Instagram Caption Generator'
    meta_description = 'Generate captivating Instagram captions with the perfect mix of personality, emojis, and hashtags.'

    fields = [
        {'name': 'topic', 'label': 'Post Topic or Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your photo, reel, or post topic...'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Fun & Playful', 'Inspirational', 'Informative', 'Aesthetic', 'Witty']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (1-2 lines)', 'Medium (3-5 lines)', 'Long (storytelling)']},
    ]

    system_prompt = (
        'You are an Instagram content strategist. Write an engaging Instagram caption for the given topic. '
        'Tone: {tone}. Length: {length}. '
        'Start with a strong hook to stop the scroll. Use line breaks for readability. '
        'Include a call to action (e.g., save, share, comment). '
        'Add relevant emojis naturally throughout. End with 15-20 relevant hashtags on a separate line.'
    )


class InstagramBioGenerator(BaseGenerator):
    slug = 'ai-instagram-bio-generator'
    name = 'AI Instagram Bio Generator'
    description = 'Craft the perfect Instagram bio that captures your personality or brand in 150 characters.'
    category = 'Social Media'
    icon = 'instagram'
    meta_title = 'Free AI Instagram Bio Generator'
    meta_description = 'Create a standout Instagram bio that captures who you are and what you do in 150 characters.'

    fields = [
        {'name': 'description', 'label': 'About You / Your Brand', 'type': 'textarea', 'required': True, 'placeholder': 'Describe yourself, your brand, or what you do...'},
        {'name': 'style', 'label': 'Style', 'type': 'select', 'required': False, 'options': ['Professional', 'Creative', 'Minimalist', 'Fun & Quirky', 'Bold']},
        {'name': 'include_cta', 'label': 'Call to Action', 'type': 'select', 'required': False, 'options': ['None', 'Link in bio', 'DM for collabs', 'Shop now', 'Follow for more']},
    ]

    system_prompt = (
        'You are a personal branding expert specializing in Instagram. Create 5 Instagram bio options '
        'based on the description provided. Style: {style}. Call to action: {include_cta}. '
        'Each bio must be under 150 characters. Use line breaks, emojis, and special characters creatively. '
        'Make each option distinct in approach. Label them as Option 1 through Option 5.'
    )


class LinkedInSummaryGenerator(BaseGenerator):
    slug = 'ai-linkedin-summary-generator'
    name = 'AI LinkedIn Summary Generator'
    description = 'Write a compelling LinkedIn summary that showcases your professional brand and attracts opportunities.'
    category = 'Social Media'
    icon = 'linkedin'
    meta_title = 'Free AI LinkedIn Summary Generator'
    meta_description = 'Generate a professional LinkedIn summary that highlights your expertise and attracts recruiters.'

    fields = [
        {'name': 'background', 'label': 'Professional Background', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your role, experience, skills, and achievements...'},
        {'name': 'goal', 'label': 'Goal', 'type': 'select', 'required': False, 'options': ['Job Seeking', 'Networking', 'Thought Leadership', 'Business Development', 'General']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Conversational', 'Confident', 'Approachable']},
    ]

    system_prompt = (
        'You are a LinkedIn profile optimization expert. Write a compelling LinkedIn About/Summary section '
        'based on the professional background provided. Goal: {goal}. Tone: {tone}. '
        'Start with a strong opening hook. Highlight key achievements with metrics where possible. '
        'Showcase expertise and unique value proposition. Include relevant keywords for searchability. '
        'End with a call to action. Keep it between 200-300 words. Use short paragraphs for readability.'
    )


class YouTubeDescriptionGenerator(BaseGenerator):
    slug = 'ai-youtube-description-generator'
    name = 'AI YouTube Description Generator'
    description = 'Generate SEO-optimized YouTube video descriptions that boost views and engagement.'
    category = 'Social Media'
    icon = 'youtube'
    meta_title = 'Free AI YouTube Description Generator'
    meta_description = 'Create SEO-optimized YouTube descriptions with timestamps, links, and keywords to boost your video rankings.'

    fields = [
        {'name': 'video_topic', 'label': 'Video Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What is your video about? Include key points covered...'},
        {'name': 'channel_niche', 'label': 'Channel Niche', 'type': 'text', 'required': False, 'placeholder': 'e.g., Tech Reviews, Cooking, Fitness, Gaming'},
        {'name': 'style', 'label': 'Style', 'type': 'select', 'required': False, 'options': ['Educational', 'Entertainment', 'Tutorial', 'Vlog', 'Review']},
    ]

    system_prompt = (
        'You are a YouTube SEO expert and content strategist. Write an optimized YouTube video description '
        'for the given topic. Channel niche: {channel_niche}. Style: {style}. '
        'Structure: Start with 2-3 compelling sentences above the fold (first 150 characters are critical). '
        'Include a detailed summary with relevant keywords, suggested timestamps section, '
        'placeholder links section (social media, related videos), and end with relevant tags/keywords. '
        'Optimize for YouTube search algorithm.'
    )


class TikTokCaptionGenerator(BaseGenerator):
    slug = 'ai-tiktok-caption-generator'
    name = 'AI TikTok Caption Generator'
    description = 'Create catchy TikTok captions that drive engagement, shares, and followers.'
    category = 'Social Media'
    icon = 'tiktok'
    meta_title = 'Free AI TikTok Caption Generator'
    meta_description = 'Generate viral TikTok captions with trending hooks, hashtags, and calls to action.'

    fields = [
        {'name': 'video_topic', 'label': 'Video Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What is your TikTok video about?'},
        {'name': 'vibe', 'label': 'Vibe', 'type': 'select', 'required': False, 'options': ['Funny', 'Relatable', 'Informative', 'Trending', 'Storytelling', 'Edgy']},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'select', 'required': False, 'options': ['Gen Z', 'Millennials', 'General', 'Niche Community']},
    ]

    system_prompt = (
        'You are a TikTok content creator who understands viral trends. Write 5 TikTok caption options '
        'for the given video topic. Vibe: {vibe}. Target audience: {audience}. '
        'Each caption should be punchy and under 150 characters. Use hooks that create curiosity or urgency. '
        'Include relevant trending hashtags (3-5 per caption). '
        'Incorporate TikTok-native language and patterns. Label them as Option 1 through Option 5.'
    )


class CaptionGenerator(BaseGenerator):
    slug = 'ai-caption-generator'
    name = 'AI Caption Generator'
    description = 'Generate creative captions for photos, videos, and social media posts on any platform.'
    category = 'Social Media'
    icon = 'caption'
    meta_title = 'Free AI Caption Generator'
    meta_description = 'Generate creative, engaging captions for any social media platform, photo, or video.'

    fields = [
        {'name': 'content', 'label': 'Content Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your photo, video, or the content you need a caption for...'},
        {'name': 'platform', 'label': 'Platform', 'type': 'select', 'required': False, 'options': ['Instagram', 'Facebook', 'Twitter', 'TikTok', 'Pinterest', 'Any']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Funny', 'Sentimental', 'Professional', 'Inspirational', 'Sarcastic', 'Poetic']},
    ]

    system_prompt = (
        'You are a creative writer specializing in social media captions. Generate 5 unique caption options '
        'for the described content. Platform: {platform}. Tone: {tone}. '
        'Vary the style across options: one short and punchy, one with a question, one storytelling, '
        'one with a quote-style approach, and one with humor or wit. '
        'Respect platform norms and character limits. Label them as Option 1 through Option 5.'
    )


class HashtagGenerator(BaseGenerator):
    slug = 'ai-hashtag-generator'
    name = 'AI Hashtag Generator'
    description = 'Generate relevant, high-performing hashtags to maximize your social media reach and discoverability.'
    category = 'Social Media'
    icon = 'hashtag'
    meta_title = 'Free AI Hashtag Generator'
    meta_description = 'Generate optimized hashtags for Instagram, TikTok, Twitter, and more to boost your reach.'

    fields = [
        {'name': 'topic', 'label': 'Topic or Niche', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your post topic, niche, or content...'},
        {'name': 'platform', 'label': 'Platform', 'type': 'select', 'required': False, 'options': ['Instagram', 'TikTok', 'Twitter', 'LinkedIn', 'General']},
        {'name': 'count', 'label': 'Number of Hashtags', 'type': 'select', 'required': False, 'options': ['10', '15', '20', '30']},
    ]

    system_prompt = (
        'You are a social media marketing expert specializing in hashtag strategy. Generate {count} relevant '
        'hashtags for the given topic. Platform: {platform}. '
        'Organize them into categories: High Volume (popular, broad reach), Medium Volume (niche-specific, '
        'moderate competition), and Low Volume (highly targeted, low competition). '
        'Mix sizes for the best reach strategy. Format each hashtag with the # symbol. '
        'Briefly explain the strategy behind the hashtag mix.'
    )


class ContentIdeaGenerator(BaseGenerator):
    slug = 'ai-content-idea-generator'
    name = 'AI Content Idea Generator'
    description = 'Generate fresh, trending content ideas for your social media channels and content calendar.'
    category = 'Social Media'
    icon = 'idea'
    meta_title = 'Free AI Content Idea Generator'
    meta_description = 'Get fresh social media content ideas tailored to your niche, audience, and platform.'

    fields = [
        {'name': 'niche', 'label': 'Niche or Industry', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your niche, brand, or industry...'},
        {'name': 'platform', 'label': 'Platform', 'type': 'select', 'required': False, 'options': ['Instagram', 'TikTok', 'YouTube', 'Twitter', 'LinkedIn', 'Blog', 'Multi-Platform']},
        {'name': 'content_type', 'label': 'Content Type', 'type': 'select', 'required': False, 'options': ['Posts', 'Reels/Shorts', 'Stories', 'Carousels', 'Videos', 'All Types']},
        {'name': 'count', 'label': 'Number of Ideas', 'type': 'select', 'required': False, 'options': ['10', '15', '20', '30']},
    ]

    system_prompt = (
        'You are a creative social media strategist. Generate {count} content ideas for the given niche. '
        'Platform: {platform}. Content type: {content_type}. '
        'For each idea, provide: a catchy title/hook, brief description of the content, '
        'the format (post, reel, story, etc.), and why it would perform well. '
        'Include a mix of educational, entertaining, engaging, and promotional content. '
        'Organize ideas into content pillars. Make ideas specific and actionable.'
    )


class BioGenerator(BaseGenerator):
    slug = 'ai-bio-generator'
    name = 'AI Bio Generator'
    description = 'Generate professional and personal bios for social media profiles, websites, and portfolios.'
    category = 'Social Media'
    icon = 'bio'
    meta_title = 'Free AI Bio Generator'
    meta_description = 'Create compelling bios for social media, websites, and professional profiles in seconds.'

    fields = [
        {'name': 'about', 'label': 'About You', 'type': 'textarea', 'required': True, 'placeholder': 'Describe who you are, what you do, and your key achievements...'},
        {'name': 'purpose', 'label': 'Purpose', 'type': 'select', 'required': False, 'options': ['Social Media Profile', 'Website/Portfolio', 'Speaker/Conference', 'Author', 'Professional Directory']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Friendly', 'Creative', 'Formal', 'Witty']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (50 words)', 'Medium (100 words)', 'Long (200 words)']},
    ]

    system_prompt = (
        'You are a personal branding expert. Write a compelling bio based on the information provided. '
        'Purpose: {purpose}. Tone: {tone}. Length: {length}. '
        'Highlight key achievements and expertise. Include personality and unique qualities. '
        'Write in the appropriate person (first person for social media, third person for speaker/author bios). '
        'Generate 3 different options with varying approaches. Label them as Option 1 through Option 3.'
    )


class ShortBioGenerator(BaseGenerator):
    slug = 'ai-short-bio-generator'
    name = 'AI Short Bio Generator'
    description = 'Generate concise, impactful short bios perfect for social media profiles and quick introductions.'
    category = 'Social Media'
    icon = 'bio'
    meta_title = 'Free AI Short Bio Generator'
    meta_description = 'Create punchy short bios for Twitter, Instagram, LinkedIn, and other social media profiles.'

    fields = [
        {'name': 'about', 'label': 'About You', 'type': 'textarea', 'required': True, 'placeholder': 'Describe who you are and what you do...'},
        {'name': 'platform', 'label': 'Platform', 'type': 'select', 'required': False, 'options': ['Twitter', 'Instagram', 'LinkedIn', 'TikTok', 'General']},
        {'name': 'style', 'label': 'Style', 'type': 'select', 'required': False, 'options': ['Professional', 'Casual', 'Minimalist', 'Fun', 'Edgy']},
    ]

    system_prompt = (
        'You are a copywriter specializing in micro-copy and personal branding. Write 5 short bio options '
        'for the given description. Platform: {platform}. Style: {style}. '
        'Each bio must be under 160 characters. Use creative formatting: emojis, pipe separators, bullet points, '
        'or line breaks as appropriate. Make each option distinct in tone and structure. '
        'Focus on being memorable and conveying personality quickly. Label them as Option 1 through Option 5.'
    )


SOCIAL_MEDIA_GENERATORS = [
    SocialMediaPostGenerator,
    InstagramCaptionGenerator,
    InstagramBioGenerator,
    LinkedInSummaryGenerator,
    YouTubeDescriptionGenerator,
    TikTokCaptionGenerator,
    CaptionGenerator,
    HashtagGenerator,
    ContentIdeaGenerator,
    BioGenerator,
    ShortBioGenerator,
]
