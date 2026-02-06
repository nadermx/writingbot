import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from media_tools.services import (
    ImageService, VoiceService, QRService, AIImageService,
    TranscriptionService, LogoService, CharacterService,
    WordCloudService, BannerService, PresentationService,
    ImageToolService,
)
import config

logger = logging.getLogger('app')


# ---- AI Image Tool Definitions (27 tools) ----

IMAGE_TOOLS = {
    'art-generator': {
        'name': 'AI Art Generator',
        'h1': 'AI Art Generator',
        'subtitle': 'Transform your ideas into stunning artwork with AI-optimized prompts for any art style.',
        'meta_title': 'AI Art Generator - Create Art Prompts',
        'meta_description': 'Generate detailed AI art prompts for paintings, digital art, and illustrations. Free online art prompt generator.',
        'placeholder': 'e.g. A mystical forest with bioluminescent trees and a hidden waterfall...',
        'style_options': {
            'oil-painting': 'Oil Painting',
            'watercolor': 'Watercolor',
            'digital-art': 'Digital Art',
            'acrylic': 'Acrylic',
            'pencil-sketch': 'Pencil Sketch',
            'mixed-media': 'Mixed Media',
            'impressionist': 'Impressionist',
            'abstract': 'Abstract',
        },
        'features': [
            {'title': 'Any Art Style', 'desc': 'Generate prompts for oil paintings, watercolors, digital art, and more.'},
            {'title': 'Gallery-Quality', 'desc': 'Prompts optimized for composition, lighting, and artistic detail.'},
            {'title': 'Instant Results', 'desc': 'Get detailed art prompts in seconds, ready for any AI image generator.'},
        ],
        'faqs': [
            {'q': 'What art styles are supported?', 'a': 'Our AI Art Generator supports all major art styles including oil painting, watercolor, digital art, pencil sketch, impressionism, surrealism, abstract, and many more.'},
            {'q': 'Can I use the prompts with any AI image generator?', 'a': 'Yes! The generated prompts work with DALL-E, Midjourney, Stable Diffusion, and any other AI image generation tool.'},
            {'q': 'How detailed are the generated prompts?', 'a': 'Each prompt includes specifics about style, medium, composition, color palette, lighting, mood, and artistic technique for the best results.'},
        ],
    },
    'poster-generator': {
        'name': 'AI Poster Generator',
        'h1': 'AI Poster Generator',
        'subtitle': 'Design eye-catching posters with AI-generated layouts, typography, and visual concepts.',
        'meta_title': 'AI Poster Generator - Create Poster Designs',
        'meta_description': 'Generate professional poster design prompts with AI. Perfect for events, movies, concerts, and marketing.',
        'placeholder': 'e.g. A retro-style music festival poster for a summer jazz event...',
        'style_options': {
            'modern': 'Modern & Clean',
            'retro': 'Retro & Vintage',
            'minimalist': 'Minimalist',
            'grunge': 'Grunge & Textured',
            'typographic': 'Typography-Focused',
            'photographic': 'Photo-Based',
            'illustrated': 'Illustrated',
            'swiss': 'Swiss/International Style',
        },
        'features': [
            {'title': 'Print-Ready Concepts', 'desc': 'Prompts include dimensions, margins, and layout details for real printing.'},
            {'title': 'Typography Focus', 'desc': 'Detailed guidance on headline placement, font styles, and text hierarchy.'},
            {'title': 'Event & Marketing', 'desc': 'Optimized for concert posters, movie posters, event flyers, and ads.'},
        ],
        'faqs': [
            {'q': 'What sizes are supported?', 'a': 'Prompts are optimized for standard poster sizes including A3, A2, 18x24", 24x36", and custom dimensions.'},
            {'q': 'Can I specify my brand colors?', 'a': 'Yes, use the additional notes field to specify your brand colors, fonts, and any specific requirements.'},
            {'q': 'Are the designs print-ready?', 'a': 'The prompts include print-ready considerations like bleed area, safe zones, and CMYK color guidance.'},
        ],
    },
    'flyer-generator': {
        'name': 'AI Flyer Generator',
        'h1': 'AI Flyer Generator',
        'subtitle': 'Create professional flyer designs with AI for events, promotions, and business marketing.',
        'meta_title': 'AI Flyer Generator - Design Flyers with AI',
        'meta_description': 'Generate professional flyer design concepts with AI. Perfect for events, sales, and marketing campaigns.',
        'placeholder': 'e.g. A grand opening flyer for a new Italian restaurant with a warm, inviting feel...',
        'style_options': {
            'corporate': 'Corporate & Professional',
            'fun': 'Fun & Colorful',
            'elegant': 'Elegant & Sophisticated',
            'bold': 'Bold & Eye-Catching',
            'clean': 'Clean & Modern',
            'handmade': 'Handmade & Organic',
        },
        'features': [
            {'title': 'Marketing-Optimized', 'desc': 'CTA placement, contact info zones, and conversion-focused layouts.'},
            {'title': 'Multiple Formats', 'desc': 'A4, letter, half-page, and tri-fold flyer design support.'},
            {'title': 'Brand-Ready', 'desc': 'Easily incorporate your brand colors, logo placement, and messaging.'},
        ],
        'faqs': [
            {'q': 'What flyer formats are supported?', 'a': 'The generator supports A4, US Letter, half-page, tri-fold, and custom size flyer designs.'},
            {'q': 'Can I generate double-sided flyer designs?', 'a': 'Yes, specify "double-sided" in the additional notes to get front and back design concepts.'},
            {'q': 'Is this suitable for digital flyers?', 'a': 'Absolutely! The prompts work for both print flyers and digital social media flyers.'},
        ],
    },
    'thumbnail-generator': {
        'name': 'AI Thumbnail Generator',
        'h1': 'AI Thumbnail Generator',
        'subtitle': 'Generate attention-grabbing thumbnails for blogs, articles, and social media content.',
        'meta_title': 'AI Thumbnail Generator - Create Thumbnails',
        'meta_description': 'Generate eye-catching thumbnail designs with AI for blogs, social media, and digital content.',
        'placeholder': 'e.g. A vibrant tech blog thumbnail about the future of AI in healthcare...',
        'style_options': {
            'bold': 'Bold & Vibrant',
            'minimal': 'Minimal & Clean',
            'dark': 'Dark & Dramatic',
            'bright': 'Bright & Cheerful',
            'professional': 'Professional',
            'artistic': 'Artistic & Creative',
        },
        'features': [
            {'title': 'Click-Worthy', 'desc': 'Prompts designed for maximum visual impact and click-through rates.'},
            {'title': 'Platform-Optimized', 'desc': 'Works for blog headers, social media, and article featured images.'},
            {'title': 'Brand Consistent', 'desc': 'Maintain visual consistency across your content thumbnails.'},
        ],
        'faqs': [
            {'q': 'What platforms are these optimized for?', 'a': 'Thumbnails work great for blogs, Medium, LinkedIn articles, Twitter/X posts, and general social media.'},
            {'q': 'What aspect ratios are used?', 'a': 'Prompts are optimized for 16:9 (landscape) and 1:1 (square) which are the most common thumbnail formats.'},
            {'q': 'Can I generate thumbnails for a series?', 'a': 'Yes, specify your series theme in the description to get consistent visual styling across thumbnails.'},
        ],
    },
    'youtube-thumbnail': {
        'name': 'AI YouTube Thumbnail Maker',
        'h1': 'AI YouTube Thumbnail Maker',
        'subtitle': 'Create click-worthy YouTube thumbnails that boost views and engagement.',
        'meta_title': 'AI YouTube Thumbnail Maker - Boost Your CTR',
        'meta_description': 'Generate high-CTR YouTube thumbnail designs with AI. Optimized for clicks, views, and subscriber growth.',
        'placeholder': 'e.g. A shocking reaction thumbnail for a video about trying the world\'s spiciest food...',
        'style_options': {
            'reaction': 'Reaction / Expressive',
            'tutorial': 'Tutorial / How-To',
            'vlog': 'Vlog / Lifestyle',
            'gaming': 'Gaming',
            'tech-review': 'Tech Review',
            'educational': 'Educational',
            'dramatic': 'Dramatic / Cinematic',
            'before-after': 'Before & After',
        },
        'features': [
            {'title': 'High CTR Design', 'desc': 'Prompts use proven YouTube thumbnail formulas that drive clicks.'},
            {'title': '1280x720 Optimized', 'desc': 'Perfect dimensions and composition for YouTube\'s thumbnail format.'},
            {'title': 'Text Overlay Zones', 'desc': 'Clear areas designated for bold overlay text that reads at any size.'},
        ],
        'faqs': [
            {'q': 'What makes a good YouTube thumbnail?', 'a': 'Expressive faces, bold contrasting colors, large readable text, and a clear focal point. Our AI incorporates all these elements.'},
            {'q': 'What is the correct YouTube thumbnail size?', 'a': 'YouTube thumbnails are 1280x720 pixels (16:9 aspect ratio). All prompts are optimized for this exact size.'},
            {'q': 'Can I match my channel\'s branding?', 'a': 'Yes, specify your channel colors and style in the additional notes for consistent branding across thumbnails.'},
        ],
    },
    'icon-generator': {
        'name': 'AI Icon Generator',
        'h1': 'AI Icon Generator',
        'subtitle': 'Design clean, scalable icons for apps, websites, and UI with AI assistance.',
        'meta_title': 'AI Icon Generator - Create Custom Icons',
        'meta_description': 'Generate professional icon designs with AI. Clean, scalable icons for apps, websites, and user interfaces.',
        'placeholder': 'e.g. A settings gear icon with a modern, rounded design for a mobile app...',
        'style_options': {
            'flat': 'Flat Design',
            'outlined': 'Outlined / Line',
            'filled': 'Filled / Solid',
            'gradient': 'Gradient',
            'glyph': 'Glyph / Monochrome',
            'duotone': 'Duotone',
            '3d': '3D / Isometric',
            'hand-drawn': 'Hand-Drawn',
        },
        'features': [
            {'title': 'Pixel-Perfect', 'desc': 'Icons designed for crisp rendering at any size from 16px to 512px.'},
            {'title': 'Design System Ready', 'desc': 'Consistent with Material Design, iOS, and Fluent design systems.'},
            {'title': 'Multi-Size Export', 'desc': 'Prompts consider scalability for favicons, app icons, and UI elements.'},
        ],
        'faqs': [
            {'q': 'What icon styles are available?', 'a': 'Flat, outlined, filled, gradient, glyph, duotone, 3D isometric, and hand-drawn styles.'},
            {'q': 'Can I generate app store icons?', 'a': 'Yes! Specify "app store icon" for prompts optimized for iOS App Store and Google Play guidelines.'},
            {'q': 'Are the icons consistent in a set?', 'a': 'Describe your icon set theme to get consistent stroke weight, style, and proportions across icons.'},
        ],
    },
    'mockup-generator': {
        'name': 'AI Mockup Generator',
        'h1': 'AI Mockup Generator',
        'subtitle': 'Create photorealistic product mockups and device presentations with AI.',
        'meta_title': 'AI Mockup Generator - Product Mockups',
        'meta_description': 'Generate professional product mockup designs with AI. Device screens, packaging, apparel, and more.',
        'placeholder': 'e.g. A sleek iPhone mockup showing a fitness app on a marble desk with plants...',
        'style_options': {
            'device': 'Device / Screen',
            'packaging': 'Packaging / Box',
            'apparel': 'Apparel / T-Shirt',
            'print': 'Print / Stationery',
            'environment': 'Environmental / Billboard',
            'lifestyle': 'Lifestyle Scene',
            'minimal': 'Minimal / Floating',
            'studio': 'Studio Shot',
        },
        'features': [
            {'title': 'Photorealistic Quality', 'desc': 'Studio-quality lighting and material rendering for believable mockups.'},
            {'title': 'Multiple Product Types', 'desc': 'Phones, laptops, packaging, apparel, billboards, and print materials.'},
            {'title': 'Presentation-Ready', 'desc': 'Perfect for pitch decks, portfolios, and client presentations.'},
        ],
        'faqs': [
            {'q': 'What products can I create mockups for?', 'a': 'Phones, tablets, laptops, packaging, t-shirts, mugs, billboards, business cards, and virtually any product.'},
            {'q': 'Can I specify the environment?', 'a': 'Yes! Describe the setting (office desk, coffee shop, outdoor, studio) for contextual mockups.'},
            {'q': 'Are these suitable for client presentations?', 'a': 'Absolutely. The prompts produce professional, presentation-quality mockup concepts.'},
        ],
    },
    'illustration-generator': {
        'name': 'AI Illustration Generator',
        'h1': 'AI Illustration Generator',
        'subtitle': 'Create beautiful illustrations for books, articles, presentations, and creative projects.',
        'meta_title': 'AI Illustration Generator - Custom Illustrations',
        'meta_description': 'Generate detailed illustration prompts with AI for editorial, children\'s books, and creative projects.',
        'placeholder': 'e.g. A whimsical children\'s book illustration of a fox reading under a mushroom...',
        'style_options': {
            'editorial': 'Editorial / Magazine',
            'childrens': 'Children\'s Book',
            'botanical': 'Botanical / Nature',
            'fashion': 'Fashion',
            'technical': 'Technical / Scientific',
            'fantasy': 'Fantasy',
            'flat': 'Flat / Vector',
            'hand-drawn': 'Hand-Drawn / Sketchy',
        },
        'features': [
            {'title': 'Story-Driven', 'desc': 'Illustrations with narrative depth, character, and emotional resonance.'},
            {'title': 'Style Versatility', 'desc': 'From editorial to children\'s books to technical illustrations.'},
            {'title': 'Print & Digital', 'desc': 'Prompts suited for both print publications and digital platforms.'},
        ],
        'faqs': [
            {'q': 'What illustration styles are available?', 'a': 'Editorial, children\'s book, botanical, fashion, technical, fantasy, flat vector, and hand-drawn styles.'},
            {'q': 'Can I use these for book projects?', 'a': 'Yes! The prompts are perfect for children\'s books, novel covers, and editorial illustrations.'},
            {'q': 'Do prompts include color guidance?', 'a': 'Every prompt includes specific color palette suggestions and shading techniques for the chosen style.'},
        ],
    },
    'design-generator': {
        'name': 'AI Design Generator',
        'h1': 'AI Design Generator',
        'subtitle': 'Generate professional graphic designs for branding, marketing, and visual communication.',
        'meta_title': 'AI Design Generator - Graphic Design Prompts',
        'meta_description': 'Generate professional graphic design prompts with AI for branding, marketing materials, and visual content.',
        'placeholder': 'e.g. A modern brand identity design for a sustainable coffee company...',
        'style_options': {
            'modern': 'Modern & Minimal',
            'corporate': 'Corporate & Professional',
            'creative': 'Creative & Artistic',
            'retro': 'Retro & Nostalgic',
            'brutalist': 'Brutalist',
            'geometric': 'Geometric',
            'organic': 'Organic & Natural',
            'tech': 'Tech & Futuristic',
        },
        'features': [
            {'title': 'Design Principles', 'desc': 'Prompts built on balance, contrast, alignment, and visual hierarchy.'},
            {'title': 'Brand-Focused', 'desc': 'Perfect for brand identity, marketing collateral, and visual systems.'},
            {'title': 'Trend-Aware', 'desc': 'Incorporates current graphic design trends and best practices.'},
        ],
        'faqs': [
            {'q': 'What types of designs can I generate?', 'a': 'Brand identities, social media graphics, marketing materials, infographics, presentation decks, and more.'},
            {'q': 'Can I specify brand guidelines?', 'a': 'Yes, include your brand colors, fonts, and style guide in the description for on-brand results.'},
            {'q': 'Are prompts suitable for professional use?', 'a': 'Absolutely. The prompts follow professional design principles and industry standards.'},
        ],
    },
    'product-image-generator': {
        'name': 'AI Product Image Generator',
        'h1': 'AI Product Image Generator',
        'subtitle': 'Create stunning e-commerce product images and commercial photography prompts.',
        'meta_title': 'AI Product Image Generator - E-Commerce Photos',
        'meta_description': 'Generate professional product photography prompts with AI for e-commerce, catalogs, and marketing.',
        'placeholder': 'e.g. A luxury watch photographed on a black velvet surface with dramatic side lighting...',
        'style_options': {
            'white-bg': 'White Background (Amazon-style)',
            'lifestyle': 'Lifestyle / In-Context',
            'flat-lay': 'Flat Lay',
            'hero': 'Hero Shot',
            'detail': 'Detail / Close-Up',
            'group': 'Group / Collection',
            'studio': 'Studio Professional',
            'outdoor': 'Outdoor / Natural',
        },
        'features': [
            {'title': 'E-Commerce Ready', 'desc': 'Optimized for Amazon, Shopify, and marketplace listing requirements.'},
            {'title': 'Studio Lighting', 'desc': 'Professional lighting setups for perfect product shots.'},
            {'title': 'Multiple Angles', 'desc': 'Get prompt concepts for hero shots, detail views, and lifestyle contexts.'},
        ],
        'faqs': [
            {'q': 'Does this work for Amazon product images?', 'a': 'Yes! Select "White Background" style for Amazon-compliant product image prompts with proper lighting.'},
            {'q': 'Can I generate lifestyle product shots?', 'a': 'Absolutely. Choose "Lifestyle" style and describe the context for in-environment product photography prompts.'},
            {'q': 'What products work best?', 'a': 'Any physical product: electronics, clothing, food, cosmetics, jewelry, furniture, and more.'},
        ],
    },
    'avatar-generator': {
        'name': 'AI Avatar Generator',
        'h1': 'AI Avatar Generator',
        'subtitle': 'Create unique, personalized avatars for social media, gaming, and professional profiles.',
        'meta_title': 'AI Avatar Generator - Custom Profile Pictures',
        'meta_description': 'Generate unique avatar designs with AI for social media, gaming profiles, and professional use.',
        'placeholder': 'e.g. A cyberpunk-style avatar with neon blue hair and glowing eyes...',
        'style_options': {
            'cartoon': 'Cartoon',
            'anime': 'Anime / Manga',
            'pixel': 'Pixel Art',
            '3d': '3D Rendered',
            'painted': 'Painted / Artistic',
            'professional': 'Professional / Headshot',
            'chibi': 'Chibi / Cute',
            'memoji': 'Memoji-Style',
        },
        'features': [
            {'title': 'Unique Identity', 'desc': 'Create distinctive avatars that stand out on any platform.'},
            {'title': 'Multi-Platform', 'desc': 'Optimized for circular and square crops used across social media.'},
            {'title': 'Style Variety', 'desc': 'From cute cartoon to professional portrait-style avatars.'},
        ],
        'faqs': [
            {'q': 'What platforms are these avatars for?', 'a': 'Works for all platforms: Twitter/X, Discord, Twitch, LinkedIn, Instagram, gaming profiles, and more.'},
            {'q': 'Can I create matching avatars for a team?', 'a': 'Yes! Describe a consistent style and theme to generate matching team or brand avatars.'},
            {'q': 'What sizes work best?', 'a': 'Avatars are designed to look great at both thumbnail (32px) and full-size (512px+) display.'},
        ],
    },
    'portrait-generator': {
        'name': 'AI Portrait Generator',
        'h1': 'AI Portrait Generator',
        'subtitle': 'Generate stunning portrait prompts with professional lighting, composition, and artistic detail.',
        'meta_title': 'AI Portrait Generator - Artistic Portraits',
        'meta_description': 'Generate professional portrait prompts with AI for photorealistic and artistic portrait creation.',
        'placeholder': 'e.g. A dramatic black and white portrait of an elderly musician with weathered hands...',
        'style_options': {
            'photorealistic': 'Photorealistic',
            'oil-painting': 'Oil Painting',
            'watercolor': 'Watercolor',
            'charcoal': 'Charcoal / Pencil',
            'pop-art': 'Pop Art',
            'renaissance': 'Renaissance',
            'noir': 'Film Noir',
            'fashion': 'Fashion / Editorial',
        },
        'features': [
            {'title': 'Lighting Mastery', 'desc': 'Rembrandt, butterfly, split, and rim lighting techniques.'},
            {'title': 'Emotional Depth', 'desc': 'Prompts that capture personality, emotion, and character.'},
            {'title': 'Artistic Styles', 'desc': 'From photorealistic to oil painting to pop art portraits.'},
        ],
        'faqs': [
            {'q': 'What lighting styles are included?', 'a': 'Rembrandt, butterfly, split, rim, broad, and short lighting. The AI selects the best for your description.'},
            {'q': 'Can I create self-portraits?', 'a': 'Describe your desired look and the AI generates detailed prompts for self-portrait creation.'},
            {'q': 'What artistic styles work for portraits?', 'a': 'Photorealistic, oil painting, watercolor, charcoal, pop art, renaissance, and more.'},
        ],
    },
    'wallpaper-generator': {
        'name': 'AI Wallpaper Generator',
        'h1': 'AI Wallpaper Generator',
        'subtitle': 'Create breathtaking desktop and mobile wallpapers with AI-generated prompts.',
        'meta_title': 'AI Wallpaper Generator - HD Wallpapers',
        'meta_description': 'Generate stunning desktop and mobile wallpaper designs with AI. 4K quality prompts for any theme.',
        'placeholder': 'e.g. A serene Japanese zen garden at dawn with cherry blossoms and koi pond...',
        'style_options': {
            'nature': 'Nature & Landscape',
            'abstract': 'Abstract & Geometric',
            'space': 'Space & Cosmic',
            'minimal': 'Minimal & Clean',
            'cyberpunk': 'Cyberpunk / Neon',
            'fantasy': 'Fantasy / Magical',
            'gradient': 'Gradient & Color',
            'dark': 'Dark & Moody',
        },
        'features': [
            {'title': '4K/8K Ready', 'desc': 'Prompts optimized for ultra-high resolution wallpaper output.'},
            {'title': 'Desktop & Mobile', 'desc': 'Support for landscape (16:9) and portrait (9:16) aspect ratios.'},
            {'title': 'Icon-Friendly', 'desc': 'Compositions designed with clean areas for desktop icons and widgets.'},
        ],
        'faqs': [
            {'q': 'What resolutions are supported?', 'a': 'Prompts target 4K (3840x2160), ultrawide (3440x1440), and mobile (1080x1920) wallpaper resolutions.'},
            {'q': 'Will the wallpaper have space for icons?', 'a': 'Yes! Prompts include clean areas suitable for desktop icons and widgets without visual clutter.'},
            {'q': 'Can I create matching desktop and mobile wallpapers?', 'a': 'Describe your theme once and use different aspect ratio settings for matching desktop and mobile versions.'},
        ],
    },
    'background-generator': {
        'name': 'AI Background Generator',
        'h1': 'AI Background Generator',
        'subtitle': 'Generate versatile backgrounds for presentations, websites, videos, and graphic design.',
        'meta_title': 'AI Background Generator - Custom Backgrounds',
        'meta_description': 'Generate professional background designs with AI for websites, presentations, videos, and social media.',
        'placeholder': 'e.g. A soft gradient background with floating geometric shapes for a tech presentation...',
        'style_options': {
            'gradient': 'Gradient & Color',
            'abstract': 'Abstract',
            'textured': 'Textured',
            'bokeh': 'Bokeh / Blur',
            'pattern': 'Pattern-Based',
            'nature': 'Nature / Photo',
            'minimal': 'Minimal',
            'dark': 'Dark Theme',
        },
        'features': [
            {'title': 'Non-Distracting', 'desc': 'Designed to complement content without competing for attention.'},
            {'title': 'Multi-Purpose', 'desc': 'Perfect for websites, slides, Zoom backgrounds, and social media.'},
            {'title': 'Seamless Options', 'desc': 'Tileable patterns for websites and repeating background needs.'},
        ],
        'faqs': [
            {'q': 'What are these backgrounds used for?', 'a': 'Websites, presentations, Zoom/Teams backgrounds, social media posts, video production, and graphic design projects.'},
            {'q': 'Can I get seamlessly tileable backgrounds?', 'a': 'Yes, specify "seamless" or "tileable" in your description for repeating pattern backgrounds.'},
            {'q': 'Are transparent backgrounds supported?', 'a': 'Describe a background with specific elements and use the result as an overlay or base layer in your design tool.'},
        ],
    },
    'infographic-generator': {
        'name': 'AI Infographic Generator',
        'h1': 'AI Infographic Generator',
        'subtitle': 'Create visually compelling infographics and data visualization layouts with AI.',
        'meta_title': 'AI Infographic Generator - Data Visualization',
        'meta_description': 'Generate professional infographic design prompts with AI. Data visualization, timelines, and process flows.',
        'placeholder': 'e.g. An infographic showing the history of space exploration with a timeline layout...',
        'style_options': {
            'timeline': 'Timeline',
            'comparison': 'Comparison / Versus',
            'process': 'Process / How-To',
            'statistical': 'Statistical / Data',
            'list': 'List / Top 10',
            'geographic': 'Geographic / Map',
            'hierarchical': 'Hierarchical / Org Chart',
            'flowchart': 'Flowchart',
        },
        'features': [
            {'title': 'Data-Driven Design', 'desc': 'Charts, graphs, icons, and statistic callouts for clear data storytelling.'},
            {'title': 'Visual Hierarchy', 'desc': 'Clear flow from top to bottom with color-coded sections and numbered steps.'},
            {'title': 'Shareable Format', 'desc': 'Vertical scrolling format perfect for social media sharing and blog embedding.'},
        ],
        'faqs': [
            {'q': 'What types of infographics can I create?', 'a': 'Timelines, comparisons, process flows, statistical dashboards, lists, maps, org charts, and flowcharts.'},
            {'q': 'Can I specify my data points?', 'a': 'Yes, include your actual data and statistics in the description for a tailored infographic layout.'},
            {'q': 'What dimensions are infographics?', 'a': 'Standard infographic width is 800-1200px with variable height. Prompts are optimized for vertical scrolling.'},
        ],
    },
    'book-cover-generator': {
        'name': 'AI Book Cover Generator',
        'h1': 'AI Book Cover Generator',
        'subtitle': 'Design professional book covers that stand out on shelves and in online stores.',
        'meta_title': 'AI Book Cover Generator - Professional Covers',
        'meta_description': 'Generate stunning book cover designs with AI. Optimized for Amazon, bookstores, and self-publishing.',
        'placeholder': 'e.g. A dark fantasy book cover for a novel about a witch in a haunted Victorian mansion...',
        'style_options': {
            'thriller': 'Thriller / Mystery',
            'romance': 'Romance',
            'scifi': 'Sci-Fi / Fantasy',
            'literary': 'Literary Fiction',
            'nonfiction': 'Non-Fiction / Business',
            'horror': 'Horror / Dark',
            'childrens': 'Children\'s / Middle Grade',
            'memoir': 'Memoir / Biography',
        },
        'features': [
            {'title': 'Genre-Optimized', 'desc': 'Covers designed for thriller, romance, sci-fi, and other genre conventions.'},
            {'title': 'Thumbnail-Ready', 'desc': 'Designs that look great at Amazon thumbnail size and full print size.'},
            {'title': 'Print & E-Book', 'desc': 'Covers with spine, back cover, and e-book front cover considerations.'},
        ],
        'faqs': [
            {'q': 'What book genres are supported?', 'a': 'All genres: thriller, romance, sci-fi, fantasy, literary fiction, non-fiction, horror, children\'s, memoir, and more.'},
            {'q': 'Will it look good on Amazon?', 'a': 'Yes! Prompts are optimized for thumbnail readability, which is critical for Amazon and online bookstore sales.'},
            {'q': 'Does it include spine and back cover?', 'a': 'Full wrap designs include front cover, spine, and back cover for print-on-demand services.'},
        ],
    },
    'packaging-design-generator': {
        'name': 'AI Packaging Design Generator',
        'h1': 'AI Packaging Design Generator',
        'subtitle': 'Create stunning product packaging designs that grab attention on retail shelves.',
        'meta_title': 'AI Packaging Design Generator - Product Packaging',
        'meta_description': 'Generate professional packaging designs with AI for products, retail, and e-commerce brands.',
        'placeholder': 'e.g. Eco-friendly packaging for an organic skincare line with minimalist botanical design...',
        'style_options': {
            'minimalist': 'Minimalist',
            'luxury': 'Luxury / Premium',
            'eco': 'Eco-Friendly / Sustainable',
            'playful': 'Playful / Colorful',
            'vintage': 'Vintage / Artisanal',
            'modern': 'Modern / Clean',
            'bold': 'Bold / Maximalist',
            'craft': 'Craft / Handmade',
        },
        'features': [
            {'title': 'Shelf Appeal', 'desc': 'Designs optimized to stand out on retail shelves from viewing distance.'},
            {'title': '3D Visualization', 'desc': 'Prompts include 3D structure, die-cut, and material considerations.'},
            {'title': 'Brand Identity', 'desc': 'Integrate your brand elements for consistent product line packaging.'},
        ],
        'faqs': [
            {'q': 'What package types are supported?', 'a': 'Boxes, bottles, bags, cans, tubes, sachets, pouches, and custom packaging shapes.'},
            {'q': 'Can I design for a product line?', 'a': 'Yes, describe your product line for consistent packaging across multiple SKUs.'},
            {'q': 'Are the designs production-ready?', 'a': 'Prompts include material considerations and die-cut awareness for real-world production.'},
        ],
    },
    'album-cover-generator': {
        'name': 'AI Album Cover Generator',
        'h1': 'AI Album Cover Generator',
        'subtitle': 'Design iconic album artwork that captures the essence of your music.',
        'meta_title': 'AI Album Cover Generator - Music Artwork',
        'meta_description': 'Generate iconic album cover designs with AI. Perfect for singles, EPs, albums, and playlist covers.',
        'placeholder': 'e.g. An ethereal, dreamy album cover for an indie folk EP about stargazing...',
        'style_options': {
            'photography': 'Photography-Based',
            'illustrated': 'Illustrated / Drawn',
            'abstract': 'Abstract / Conceptual',
            'collage': 'Collage / Mixed Media',
            'minimalist': 'Minimalist / Typography',
            'retro': 'Retro / Vinyl Era',
            'psychedelic': 'Psychedelic',
            'dark': 'Dark / Gritty',
        },
        'features': [
            {'title': 'Genre-Specific', 'desc': 'Aesthetics matched to hip-hop, rock, electronic, indie, and classical.'},
            {'title': 'Streaming-Optimized', 'desc': 'Square 3000x3000px format for Spotify, Apple Music, and all platforms.'},
            {'title': 'Iconic Design', 'desc': 'Memorable, distinctive artwork that defines your musical identity.'},
        ],
        'faqs': [
            {'q': 'What music genres work best?', 'a': 'All genres: hip-hop, rock, pop, electronic, classical, jazz, indie, metal, R&B, country, and more.'},
            {'q': 'What size should album covers be?', 'a': 'The standard is 3000x3000 pixels (square). All prompts are optimized for this format.'},
            {'q': 'Can I use this for single artwork too?', 'a': 'Yes! Works for single covers, EP artwork, album covers, and playlist cover images.'},
        ],
    },
    'tattoo-generator': {
        'name': 'AI Tattoo Generator',
        'h1': 'AI Tattoo Generator',
        'subtitle': 'Design unique, meaningful tattoo concepts with AI in any style you choose.',
        'meta_title': 'AI Tattoo Generator - Custom Tattoo Designs',
        'meta_description': 'Generate custom tattoo design prompts with AI. Traditional, Japanese, blackwork, watercolor, and more styles.',
        'placeholder': 'e.g. A Japanese-style dragon wrapping around the forearm with cherry blossom accents...',
        'style_options': {
            'traditional': 'Traditional / Old School',
            'neo-trad': 'Neo-Traditional',
            'japanese': 'Japanese / Irezumi',
            'blackwork': 'Blackwork',
            'watercolor': 'Watercolor',
            'geometric': 'Geometric / Sacred',
            'realistic': 'Realistic / Portrait',
            'minimalist': 'Minimalist / Fine Line',
        },
        'features': [
            {'title': 'Body Placement', 'desc': 'Designs flow with body contours for arm, back, chest, and leg.'},
            {'title': 'Aging Considered', 'desc': 'Line weights and details designed to age well over time.'},
            {'title': 'Stencil-Ready', 'desc': 'Clean outlines suitable for direct tattoo stencil transfer.'},
        ],
        'faqs': [
            {'q': 'What tattoo styles are available?', 'a': 'Traditional, neo-traditional, Japanese, blackwork, watercolor, geometric, realistic, minimalist, dotwork, and tribal.'},
            {'q': 'Can I specify body placement?', 'a': 'Yes! Specify arm, leg, back, chest, shoulder, or any body part for placement-optimized designs.'},
            {'q': 'Will the design age well as a tattoo?', 'a': 'Prompts consider line weight and detail density to ensure the design looks great for years to come.'},
        ],
    },
    'pixel-art-generator': {
        'name': 'AI Pixel Art Generator',
        'h1': 'AI Pixel Art Generator',
        'subtitle': 'Create retro-inspired pixel art for games, avatars, and nostalgic digital creations.',
        'meta_title': 'AI Pixel Art Generator - Retro Pixel Art',
        'meta_description': 'Generate detailed pixel art prompts with AI. Perfect for indie games, avatars, and retro-style artwork.',
        'placeholder': 'e.g. A 32x32 pixel art knight character with silver armor and a glowing blue sword...',
        'style_options': {
            'nes': 'NES / 8-bit',
            'snes': 'SNES / 16-bit',
            'gameboy': 'Game Boy',
            'modern': 'Modern Pixel Art',
            'isometric': 'Isometric',
            'top-down': 'Top-Down RPG',
            'platformer': 'Platformer / Side-Scroll',
            'ui': 'UI / Icons',
        },
        'features': [
            {'title': 'Authentic Retro', 'desc': 'Faithful to NES, SNES, and Game Boy color palette limitations.'},
            {'title': 'Game-Ready', 'desc': 'Sprite designs ready for game development and animation frames.'},
            {'title': 'Precise Grids', 'desc': 'Exact pixel grid sizes from 16x16 to 128x128 with clean edges.'},
        ],
        'faqs': [
            {'q': 'What pixel art sizes are supported?', 'a': '16x16, 32x32, 48x48, 64x64, 96x96, and 128x128 pixel grids, plus larger custom sizes.'},
            {'q': 'Can I specify a color palette?', 'a': 'Yes! Choose retro palettes (NES, SNES, Game Boy) or specify custom color limitations.'},
            {'q': 'Is this suitable for game development?', 'a': 'Absolutely. Prompts include sprite-ready considerations for both static and animated pixel art.'},
        ],
    },
    'pattern-generator': {
        'name': 'AI Pattern Generator',
        'h1': 'AI Pattern Generator',
        'subtitle': 'Design seamless repeating patterns for fabrics, wallpapers, and digital surfaces.',
        'meta_title': 'AI Pattern Generator - Seamless Patterns',
        'meta_description': 'Generate seamless repeating patterns with AI for textiles, wallpapers, and digital design.',
        'placeholder': 'e.g. A tropical botanical pattern with monstera leaves and exotic flowers on dark background...',
        'style_options': {
            'botanical': 'Botanical / Floral',
            'geometric': 'Geometric',
            'abstract': 'Abstract',
            'ethnic': 'Ethnic / Tribal',
            'art-deco': 'Art Deco',
            'minimal': 'Minimal / Simple',
            'retro': 'Retro / 70s',
            'damask': 'Damask / Ornamental',
        },
        'features': [
            {'title': 'Seamless Repeat', 'desc': 'Patterns designed for perfect seamless tiling in any direction.'},
            {'title': 'Multi-Application', 'desc': 'For fabric, wallpaper, wrapping paper, and digital backgrounds.'},
            {'title': 'Color Cohesion', 'desc': 'Harmonious color palettes that work across the full pattern repeat.'},
        ],
        'faqs': [
            {'q': 'Are the patterns seamlessly tileable?', 'a': 'Yes, all prompts are specifically designed for seamless repeat patterns that tile perfectly.'},
            {'q': 'What can I use the patterns for?', 'a': 'Fabric printing, wallpaper, wrapping paper, website backgrounds, product packaging, and more.'},
            {'q': 'Can I control the pattern density?', 'a': 'Specify "dense" or "sparse" in your description, or use additional notes to control motif spacing.'},
        ],
    },
    '3d-model-generator': {
        'name': 'AI 3D Model Generator',
        'h1': 'AI 3D Model Generator',
        'subtitle': 'Generate detailed 3D model and render prompts for visualization and game assets.',
        'meta_title': 'AI 3D Model Generator - 3D Visualization',
        'meta_description': 'Generate professional 3D model and render prompts with AI for games, architecture, and product visualization.',
        'placeholder': 'e.g. A low-poly 3D model of a cozy cabin in the woods with warm interior lighting...',
        'style_options': {
            'low-poly': 'Low Poly',
            'high-poly': 'High Poly / Realistic',
            'sculpted': 'Sculpted / ZBrush',
            'isometric': 'Isometric',
            'architectural': 'Architectural',
            'character': 'Character Model',
            'product': 'Product Visualization',
            'stylized': 'Stylized / Cartoon 3D',
        },
        'features': [
            {'title': 'Render-Quality', 'desc': 'Prompts for Blender, Unreal Engine, and Octane render quality output.'},
            {'title': 'Material Detail', 'desc': 'PBR material properties: metallic, roughness, subsurface scattering.'},
            {'title': 'Multiple Use Cases', 'desc': 'For game assets, architectural viz, product renders, and art.'},
        ],
        'faqs': [
            {'q': 'What render engines are these optimized for?', 'a': 'Prompts work with Blender Cycles, Unreal Engine, Octane, V-Ray, and any standard PBR renderer.'},
            {'q': 'Can I generate game-ready 3D prompts?', 'a': 'Yes! Select "Low Poly" or "Stylized" for game-optimized 3D model concepts.'},
            {'q': 'Do prompts include material information?', 'a': 'Every prompt includes PBR material properties, lighting setup, and camera angle recommendations.'},
        ],
    },
    'storyboard-generator': {
        'name': 'AI Storyboard Generator',
        'h1': 'AI Storyboard Generator',
        'subtitle': 'Create professional storyboard panels for film, animation, and advertising projects.',
        'meta_title': 'AI Storyboard Generator - Film Storyboards',
        'meta_description': 'Generate professional storyboard panel prompts with AI for films, animations, and video projects.',
        'placeholder': 'e.g. A dramatic chase scene through a neon-lit alley with rain reflecting city lights...',
        'style_options': {
            'film': 'Film / Live Action',
            'animation': 'Animation',
            'commercial': 'Commercial / Ad',
            'music-video': 'Music Video',
            'rough': 'Rough / Thumbnail',
            'clean': 'Clean / Presentation',
            'comic-style': 'Comic Book Style',
            'cinematic': 'Cinematic / Widescreen',
        },
        'features': [
            {'title': 'Cinematic Composition', 'desc': 'Camera angles, shot types, and framing following film language.'},
            {'title': 'Sequential Clarity', 'desc': 'Panels that clearly communicate action, motion, and story flow.'},
            {'title': 'Production-Ready', 'desc': 'Standard storyboard formats for film, animation, and advertising.'},
        ],
        'faqs': [
            {'q': 'What are storyboards used for?', 'a': 'Pre-production planning for films, animations, commercials, music videos, and any visual storytelling project.'},
            {'q': 'Can I generate a full sequence?', 'a': 'Describe your scene and specify multiple panels for a complete storyboard sequence.'},
            {'q': 'What camera terminology is used?', 'a': 'Prompts include wide shots, close-ups, POV, Dutch angles, tracking shots, and other cinematic terms.'},
        ],
    },
    'fantasy-map-generator': {
        'name': 'AI Fantasy Map Generator',
        'h1': 'AI Fantasy Map Generator',
        'subtitle': 'Create immersive fantasy world maps for RPGs, novels, and world-building projects.',
        'meta_title': 'AI Fantasy Map Generator - World Building Maps',
        'meta_description': 'Generate detailed fantasy world maps with AI for D&D, novels, RPGs, and creative world-building.',
        'placeholder': 'e.g. A continent map for a high fantasy world with mountain ranges, ancient forests, and a central kingdom...',
        'style_options': {
            'tolkien': 'Tolkien / Classic',
            'medieval': 'Medieval Cartography',
            'pirate': 'Pirate / Treasure Map',
            'political': 'Political / Borders',
            'terrain': 'Terrain / Topographic',
            'artistic': 'Artistic / Illustrated',
            'old-world': 'Old World / Parchment',
            'digital': 'Digital / Modern',
        },
        'features': [
            {'title': 'Rich Geography', 'desc': 'Mountains, forests, rivers, coastlines, deserts, and settlements.'},
            {'title': 'World-Building', 'desc': 'Maps that support deep narrative and RPG campaign development.'},
            {'title': 'Authentic Style', 'desc': 'Parchment textures, compass roses, and classic cartographic elements.'},
        ],
        'faqs': [
            {'q': 'What map styles are available?', 'a': 'Tolkien-style, medieval cartography, pirate/treasure maps, political borders, terrain, and artistic illustrated maps.'},
            {'q': 'Can I use this for D&D campaigns?', 'a': 'Absolutely! Perfect for Dungeons & Dragons, Pathfinder, and any tabletop RPG world-building.'},
            {'q': 'Will it include place names?', 'a': 'Prompts include areas for labels. Specify your place names in the description for accurate placement.'},
        ],
    },
    'cartoon-generator': {
        'name': 'AI Cartoon Generator',
        'h1': 'AI Cartoon Generator',
        'subtitle': 'Create fun, expressive cartoon artwork in any style from chibi to classic animation.',
        'meta_title': 'AI Cartoon Generator - Cartoon Art',
        'meta_description': 'Generate cartoon art prompts with AI. From cute chibi to classic animation styles. Fun and expressive.',
        'placeholder': 'e.g. A playful cartoon cat chef cooking in a tiny kitchen with oversized utensils...',
        'style_options': {
            'classic': 'Classic Cartoon',
            'anime': 'Anime-Influenced',
            'pixar': 'Pixar / 3D Cartoon',
            'newspaper': 'Newspaper Strip',
            'chibi': 'Chibi / Kawaii',
            'adult': 'Adult Animation',
            'rubber-hose': 'Rubber Hose (1930s)',
            'modern': 'Modern / Flat',
        },
        'features': [
            {'title': 'Character Appeal', 'desc': 'Designs with the Disney "appeal" principle for lovable characters.'},
            {'title': 'Expressive Faces', 'desc': 'Exaggerated features and emotions that bring cartoons to life.'},
            {'title': 'Any Style', 'desc': 'From vintage rubber hose to modern flat design cartoons.'},
        ],
        'faqs': [
            {'q': 'What cartoon styles are available?', 'a': 'Classic, anime, Pixar-style 3D, newspaper strip, chibi/kawaii, adult animation, rubber hose, and modern flat styles.'},
            {'q': 'Can I create cartoon versions of real things?', 'a': 'Yes! Describe any subject and choose a cartoon style to get a fun, cartoonified version.'},
            {'q': 'Is this good for mascot design?', 'a': 'Perfect for mascot design! Include brand details for a character that represents your brand personality.'},
        ],
    },
    'comic-generator': {
        'name': 'AI Comic Generator',
        'h1': 'AI Comic Generator',
        'subtitle': 'Create dynamic comic book art with AI-optimized prompts for panels, covers, and spreads.',
        'meta_title': 'AI Comic Generator - Comic Book Art',
        'meta_description': 'Generate comic book art prompts with AI for superhero, manga, indie, and webcomic styles.',
        'placeholder': 'e.g. A dynamic superhero landing pose with a cityscape background and dramatic lighting...',
        'style_options': {
            'superhero': 'Superhero / DC-Marvel',
            'manga': 'Manga',
            'indie': 'Indie / Alternative',
            'webcomic': 'Webcomic',
            'graphic-novel': 'Graphic Novel',
            'noir': 'Noir / Crime',
            'action': 'Action / Shonen',
            'slice-of-life': 'Slice of Life',
        },
        'features': [
            {'title': 'Dynamic Poses', 'desc': 'Action-packed compositions with dramatic perspective and motion.'},
            {'title': 'Panel-Ready', 'desc': 'Art designed for comic panel layouts with speech bubble areas.'},
            {'title': 'Ink & Color', 'desc': 'Halftone dots, speed lines, and classic comic coloring techniques.'},
        ],
        'faqs': [
            {'q': 'What comic styles are supported?', 'a': 'Superhero, manga, indie, webcomic, graphic novel, noir, action/shonen, and slice-of-life styles.'},
            {'q': 'Can I create full comic pages?', 'a': 'Describe your page layout for multi-panel page compositions, splash pages, and spread designs.'},
            {'q': 'Does it support manga style?', 'a': 'Yes! Full manga support including panel flow, screen tones, speed lines, and Japanese comic aesthetics.'},
        ],
    },
    'action-figure-generator': {
        'name': 'AI Action Figure Generator',
        'h1': 'AI Action Figure Generator',
        'subtitle': 'Design collectible action figure concepts with detailed accessories and packaging.',
        'meta_title': 'AI Action Figure Generator - Toy Design',
        'meta_description': 'Generate action figure and toy design concepts with AI. Articulation, accessories, and packaging.',
        'placeholder': 'e.g. A 6-inch cyberpunk samurai action figure with interchangeable hands and a neon katana...',
        'style_options': {
            'realistic': 'Realistic / Detailed',
            'stylized': 'Stylized / Cartoon',
            'vintage': 'Vintage / Retro',
            'designer': 'Designer / Art Toy',
            'miniature': 'Miniature / Tabletop',
            'plush': 'Plush / Soft Toy',
            'bobblehead': 'Bobblehead / Funko',
            'model-kit': 'Model Kit / Gunpla',
        },
        'features': [
            {'title': 'Articulation Design', 'desc': 'Detailed joint and articulation point planning for posability.'},
            {'title': 'Accessories', 'desc': 'Weapons, interchangeable parts, bases, and display stands.'},
            {'title': 'Packaging Concept', 'desc': 'Blister card and box art design for retail presentation.'},
        ],
        'faqs': [
            {'q': 'What scales are supported?', 'a': '3.75-inch, 6-inch, 12-inch, and custom scales. Specify your preferred scale in the description.'},
            {'q': 'Can I design the packaging too?', 'a': 'Yes! Prompts include blister card, window box, and packaging artwork concepts.'},
            {'q': 'Is this for original characters or fan art?', 'a': 'Both! Design original action figure concepts or describe existing characters for collectible concepts.'},
        ],
    },
}


# Registry of all media tools
MEDIA_TOOLS = [
    {
        'slug': 'image-converter',
        'name': 'Image Converter',
        'description': 'Convert images between JPG, PNG, WebP, GIF, BMP, and more.',
        'category': 'image',
        'icon': 'image',
        'url': '/converter-tools/',
    },
    {
        'slug': 'background-remover',
        'name': 'Background Remover',
        'description': 'Remove backgrounds from images instantly with AI.',
        'category': 'image',
        'icon': 'bg-remove',
        'url': '/background-remover/',
    },
    {
        'slug': 'ai-image-generator',
        'name': 'AI Image Generator',
        'description': 'Generate image prompts with AI to create stunning visuals.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/image-tools/',
    },
    {
        'slug': 'qr-code-generator',
        'name': 'QR Code Generator',
        'description': 'Create custom QR codes for URLs, text, and more.',
        'category': 'utility',
        'icon': 'qr',
        'url': '/tools/qr-code-generator/',
    },
    {
        'slug': 'ai-voice-generator',
        'name': 'AI Voice Generator',
        'description': 'Convert text to natural-sounding speech with multiple voices.',
        'category': 'audio',
        'icon': 'voice',
        'url': '/tools/ai-voice-generator/',
    },
    {
        'slug': 'transcription',
        'name': 'Transcription (Speech to Text)',
        'description': 'Upload audio files and extract text using AI-powered transcription.',
        'category': 'audio',
        'icon': 'transcription',
        'url': '/tools/transcription/',
    },
    {
        'slug': 'logo-generator',
        'name': 'AI Logo Generator',
        'description': 'Generate professional logo design concepts and AI prompts for your brand.',
        'category': 'ai',
        'icon': 'logo',
        'url': '/tools/logo-generator/',
    },
    {
        'slug': 'character-generator',
        'name': 'AI Character Generator',
        'description': 'Create detailed character designs with AI for games, stories, and art.',
        'category': 'ai',
        'icon': 'character',
        'url': '/tools/character-generator/',
    },
    {
        'slug': 'word-cloud',
        'name': 'Word Cloud Generator',
        'description': 'Turn any text into a beautiful word cloud image. Free and instant.',
        'category': 'utility',
        'icon': 'wordcloud',
        'url': '/tools/word-cloud/',
    },
    {
        'slug': 'banner-generator',
        'name': 'AI Banner Generator',
        'description': 'Create banner ad designs with AI for social media and display ads.',
        'category': 'ai',
        'icon': 'banner',
        'url': '/tools/banner-generator/',
    },
    {
        'slug': 'presentation-maker',
        'name': 'AI Presentation Maker',
        'description': 'Generate complete slide-by-slide presentations with AI in seconds.',
        'category': 'ai',
        'icon': 'presentation',
        'url': '/tools/presentation-maker/',
    },
    {
        'slug': 'art-generator',
        'name': 'AI Art Generator',
        'description': 'Transform ideas into stunning artwork prompts for any art style.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/art-generator/',
    },
    {
        'slug': 'poster-generator',
        'name': 'AI Poster Generator',
        'description': 'Design eye-catching posters with AI-generated layouts and concepts.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/poster-generator/',
    },
    {
        'slug': 'flyer-generator',
        'name': 'AI Flyer Generator',
        'description': 'Create professional flyer designs for events and promotions.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/flyer-generator/',
    },
    {
        'slug': 'thumbnail-generator',
        'name': 'AI Thumbnail Generator',
        'description': 'Generate attention-grabbing thumbnails for blogs and social media.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/thumbnail-generator/',
    },
    {
        'slug': 'youtube-thumbnail',
        'name': 'AI YouTube Thumbnail Maker',
        'description': 'Create click-worthy YouTube thumbnails that boost views.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/youtube-thumbnail/',
    },
    {
        'slug': 'icon-generator',
        'name': 'AI Icon Generator',
        'description': 'Design clean, scalable icons for apps, websites, and UI.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/icon-generator/',
    },
    {
        'slug': 'mockup-generator',
        'name': 'AI Mockup Generator',
        'description': 'Create photorealistic product mockups and device presentations.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/mockup-generator/',
    },
    {
        'slug': 'illustration-generator',
        'name': 'AI Illustration Generator',
        'description': 'Create beautiful illustrations for books, articles, and projects.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/illustration-generator/',
    },
    {
        'slug': 'design-generator',
        'name': 'AI Design Generator',
        'description': 'Generate professional graphic designs for branding and marketing.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/design-generator/',
    },
    {
        'slug': 'product-image-generator',
        'name': 'AI Product Image Generator',
        'description': 'Create stunning e-commerce product images and photography prompts.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/product-image-generator/',
    },
    {
        'slug': 'avatar-generator',
        'name': 'AI Avatar Generator',
        'description': 'Create unique avatars for social media, gaming, and profiles.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/avatar-generator/',
    },
    {
        'slug': 'portrait-generator',
        'name': 'AI Portrait Generator',
        'description': 'Generate stunning portrait prompts with professional artistic detail.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/portrait-generator/',
    },
    {
        'slug': 'wallpaper-generator',
        'name': 'AI Wallpaper Generator',
        'description': 'Create breathtaking desktop and mobile wallpapers with AI.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/wallpaper-generator/',
    },
    {
        'slug': 'background-generator',
        'name': 'AI Background Generator',
        'description': 'Generate versatile backgrounds for presentations and websites.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/background-generator/',
    },
    {
        'slug': 'infographic-generator',
        'name': 'AI Infographic Generator',
        'description': 'Create visually compelling infographics and data visualizations.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/infographic-generator/',
    },
    {
        'slug': 'book-cover-generator',
        'name': 'AI Book Cover Generator',
        'description': 'Design professional book covers for any genre.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/book-cover-generator/',
    },
    {
        'slug': 'packaging-design-generator',
        'name': 'AI Packaging Design Generator',
        'description': 'Create stunning product packaging designs for retail.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/packaging-design-generator/',
    },
    {
        'slug': 'album-cover-generator',
        'name': 'AI Album Cover Generator',
        'description': 'Design iconic album artwork for your music.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/album-cover-generator/',
    },
    {
        'slug': 'tattoo-generator',
        'name': 'AI Tattoo Generator',
        'description': 'Design unique tattoo concepts in any style.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/tattoo-generator/',
    },
    {
        'slug': 'pixel-art-generator',
        'name': 'AI Pixel Art Generator',
        'description': 'Create retro-inspired pixel art for games and avatars.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/pixel-art-generator/',
    },
    {
        'slug': 'pattern-generator',
        'name': 'AI Pattern Generator',
        'description': 'Design seamless repeating patterns for fabrics and surfaces.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/pattern-generator/',
    },
    {
        'slug': '3d-model-generator',
        'name': 'AI 3D Model Generator',
        'description': 'Generate detailed 3D model and render prompts.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/3d-model-generator/',
    },
    {
        'slug': 'storyboard-generator',
        'name': 'AI Storyboard Generator',
        'description': 'Create professional storyboard panels for film and animation.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/storyboard-generator/',
    },
    {
        'slug': 'fantasy-map-generator',
        'name': 'AI Fantasy Map Generator',
        'description': 'Create immersive fantasy world maps for RPGs and novels.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/fantasy-map-generator/',
    },
    {
        'slug': 'cartoon-generator',
        'name': 'AI Cartoon Generator',
        'description': 'Create fun, expressive cartoon artwork in any style.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/cartoon-generator/',
    },
    {
        'slug': 'comic-generator',
        'name': 'AI Comic Generator',
        'description': 'Create dynamic comic book art for panels, covers, and spreads.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/comic-generator/',
    },
    {
        'slug': 'action-figure-generator',
        'name': 'AI Action Figure Generator',
        'description': 'Design collectible action figure concepts with accessories.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/tools/action-figure-generator/',
    },
]


class MediaToolsIndex(View):
    """Renders the media tools index page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/index.html', {
            'title': f'Free Online Media Tools | {config.PROJECT_NAME}',
            'description': 'Free online image converter, background remover, QR code generator, and AI voice tools.',
            'page': 'media-tools',
            'g': g,
            'tools': MEDIA_TOOLS,
        })


class ImageConverterPage(View):
    """Image converter tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Image Converter | {config.PROJECT_NAME}',
            'description': 'Convert images between JPG, PNG, WebP, GIF, BMP, TIFF, and ICO. Free online tool, no installation required.',
            'page': 'image-converter',
            'g': g,
            'tool_type': 'image-converter',
            'tool_name': 'Image Converter',
            'tool_description': 'Convert your images to any format. Supports JPG, PNG, WebP, GIF, BMP, TIFF, and ICO.',
            'accept': 'image/*',
            'formats': list(ImageService.SUPPORTED_FORMATS.keys()),
        })


class BackgroundRemoverPage(View):
    """Background remover tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Background Remover | {config.PROJECT_NAME}',
            'description': 'Remove backgrounds from images instantly using AI. Free online tool.',
            'page': 'background-remover',
            'g': g,
            'tool_type': 'background-remover',
            'tool_name': 'Background Remover',
            'tool_description': 'Upload an image and instantly remove its background using AI.',
            'accept': 'image/*',
        })


class AIImageGeneratorPage(View):
    """AI image prompt generator page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Image Generator | {config.PROJECT_NAME}',
            'description': 'Generate detailed AI image prompts from simple descriptions.',
            'page': 'ai-image-generator',
            'g': g,
            'tool_type': 'ai-image-generator',
            'tool_name': 'AI Image Generator',
            'tool_description': 'Describe what you want and get a detailed, optimized prompt for AI image generation.',
            'accept': '',
        })


class QRCodePage(View):
    """QR code generator page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free QR Code Generator | {config.PROJECT_NAME}',
            'description': 'Create custom QR codes for URLs, text, WiFi, and more. Free online QR code maker.',
            'page': 'qr-code-generator',
            'g': g,
            'tool_type': 'qr-code',
            'tool_name': 'QR Code Generator',
            'tool_description': 'Generate custom QR codes with your choice of colors and error correction level.',
            'accept': '',
        })


class VoiceGeneratorPage(View):
    """AI voice generator page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Voice Generator - Text to Speech | {config.PROJECT_NAME}',
            'description': 'Convert text to natural-sounding speech. Choose from 6 AI voices. Free online text-to-speech.',
            'page': 'ai-voice-generator',
            'g': g,
            'tool_type': 'voice-generator',
            'tool_name': 'AI Voice Generator',
            'tool_description': 'Convert text to natural-sounding speech with multiple AI voices.',
            'accept': '',
            'voices': VoiceService.VOICES,
        })


class TranscriptionPage(View):
    """Transcription (speech-to-text) tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Audio Transcription - Speech to Text | {config.PROJECT_NAME}',
            'description': 'Convert audio files to text with AI-powered transcription. Supports MP3, WAV, OGG, FLAC, and more.',
            'page': 'transcription',
            'g': g,
            'tool_type': 'transcription',
            'tool_name': 'Transcription (Speech to Text)',
            'tool_description': 'Upload an audio file and get an accurate text transcription using AI.',
            'accept': 'audio/*,.mp3,.wav,.ogg,.flac,.m4a,.webm',
        })


class LogoGeneratorPage(View):
    """AI logo generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Logo Generator | {config.PROJECT_NAME}',
            'description': 'Generate professional logo design concepts and AI-ready prompts for your brand identity.',
            'page': 'logo-generator',
            'g': g,
            'tool_type': 'logo-generator',
            'tool_name': 'AI Logo Generator',
            'tool_description': 'Enter your business details and get a detailed logo design brief with AI image generation prompts.',
            'accept': '',
            'logo_styles': LogoService.STYLES,
        })


class CharacterGeneratorPage(View):
    """AI character generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Character Generator | {config.PROJECT_NAME}',
            'description': 'Create detailed character designs with AI for games, stories, animation, and concept art.',
            'page': 'character-generator',
            'g': g,
            'tool_type': 'character-generator',
            'tool_name': 'AI Character Generator',
            'tool_description': 'Describe your character and get a complete character sheet with AI image generation prompts.',
            'accept': '',
            'character_styles': CharacterService.STYLES,
        })


class WordCloudPage(View):
    """Word cloud generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Word Cloud Generator | {config.PROJECT_NAME}',
            'description': 'Create beautiful word cloud images from any text. Free online word cloud maker.',
            'page': 'word-cloud',
            'g': g,
            'tool_type': 'word-cloud',
            'tool_name': 'Word Cloud Generator',
            'tool_description': 'Paste your text and generate a stunning word cloud image instantly.',
            'accept': '',
            'colormaps': WordCloudService.COLORMAPS,
        })


class BannerGeneratorPage(View):
    """AI banner generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Banner Generator | {config.PROJECT_NAME}',
            'description': 'Generate professional banner ad designs with AI for social media and display advertising.',
            'page': 'banner-generator',
            'g': g,
            'tool_type': 'banner-generator',
            'tool_name': 'AI Banner Generator',
            'tool_description': 'Enter your banner details and get a complete design brief with AI image generation prompts.',
            'accept': '',
            'banner_sizes': BannerService.SIZES,
        })


class PresentationMakerPage(View):
    """AI presentation maker tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Presentation Maker | {config.PROJECT_NAME}',
            'description': 'Generate complete slide-by-slide presentations with AI. Free online presentation creator.',
            'page': 'presentation-maker',
            'g': g,
            'tool_type': 'presentation-maker',
            'tool_name': 'AI Presentation Maker',
            'tool_description': 'Enter your topic and get a complete presentation with slide content, speaker notes, and visual suggestions.',
            'accept': '',
            'presentation_styles': PresentationService.STYLES,
        })


class AIImageToolPage(View):
    """Generic page view for all 27 AI image tools.

    Each URL sets tool_key, then this view looks up the tool config
    from IMAGE_TOOLS and renders the shared template.
    """
    tool_key = None

    def get(self, request):
        tool = IMAGE_TOOLS.get(self.tool_key)
        if not tool:
            from django.http import Http404
            raise Http404

        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/ai-image-tool.html', {
            'title': f'{tool["meta_title"]} | {config.PROJECT_NAME}',
            'description': tool['meta_description'],
            'page': self.tool_key,
            'g': g,
            'tool_key': self.tool_key,
            'tool_name': tool['name'],
            'tool_h1': tool['h1'],
            'tool_subtitle': tool['subtitle'],
            'placeholder': tool['placeholder'],
            'style_options': tool['style_options'],
            'features': tool['features'],
            'faqs': tool['faqs'],
        })


# ---- API Views ----

class AIImageToolAPI(APIView):
    """POST /api/media/image-tool/ - Generate AI image prompt for any tool type."""

    def post(self, request):
        tool_key = request.data.get('tool_key', '').strip()
        description = request.data.get('description', '').strip()
        style = request.data.get('style', '').strip()
        additional = request.data.get('additional', '').strip()

        if not tool_key or tool_key not in IMAGE_TOOLS:
            return Response(
                {'error': 'Invalid tool type.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not description:
            return Response(
                {'error': 'Please enter a description.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = ImageToolService.generate_prompt(
            tool_key, description, style, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'prompt': result})


class ImageConvertAPI(APIView):
    """POST /api/media/convert-image/ - Convert image format."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        target_format = request.data.get('format', 'png')
        quality = int(request.data.get('quality', 90))

        if not file:
            return Response(
                {'error': 'Please upload an image file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = ImageService.convert(file, target_format, quality)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content_types = {
            'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
            'gif': 'image/gif', 'bmp': 'image/bmp', 'webp': 'image/webp',
            'tiff': 'image/tiff', 'ico': 'image/x-icon',
        }
        ct = content_types.get(target_format.lower(), 'application/octet-stream')

        response = HttpResponse(output.read(), content_type=ct)
        response['Content-Disposition'] = f'attachment; filename="converted.{target_format}"'
        return response


class BackgroundRemoveAPI(APIView):
    """POST /api/media/remove-bg/ - Remove image background."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {'error': 'Please upload an image file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = ImageService.remove_background(file)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="no-background.png"'
        return response


class QRCodeAPI(APIView):
    """POST /api/media/qr-code/ - Generate QR code."""

    def post(self, request):
        data = request.data.get('data', '').strip()
        size = int(request.data.get('size', 300))
        color = request.data.get('color', '#000000')
        bg_color = request.data.get('bg_color', '#FFFFFF')
        error_correction = request.data.get('error_correction', 'M')

        if not data:
            return Response(
                {'error': 'Please enter data to encode.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = QRService.generate_qr(data, size, color, bg_color, error_correction)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        return response


class VoiceGenerateAPI(APIView):
    """POST /api/media/text-to-speech/ - Generate speech audio."""

    def post(self, request):
        text = request.data.get('text', '').strip()
        voice = request.data.get('voice', 'alloy')
        speed = float(request.data.get('speed', 1.0))

        if not text:
            return Response(
                {'error': 'Please enter some text to convert.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = VoiceService.text_to_speech(text, voice, speed)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
        return response


class AIImagePromptAPI(APIView):
    """POST /api/media/ai-image/ - Generate AI image prompt."""

    def post(self, request):
        description = request.data.get('description', '').strip()

        if not description:
            return Response(
                {'error': 'Please enter an image description.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        prompt, error = AIImageService.generate_image_prompt(description, use_premium=is_premium)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'prompt': prompt})


class TranscribeAPI(APIView):
    """POST /api/media/transcribe/ - Transcribe audio to text."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {'error': 'Please upload an audio file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result, error = TranscriptionService.transcribe(file)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class LogoGenerateAPI(APIView):
    """POST /api/media/logo/ - Generate logo design prompt."""

    def post(self, request):
        business_name = request.data.get('business_name', '').strip()
        industry = request.data.get('industry', '').strip()
        style = request.data.get('style', 'modern')
        colors = request.data.get('colors', '').strip()
        additional = request.data.get('additional', '').strip()

        if not business_name:
            return Response(
                {'error': 'Please enter a business name.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = LogoService.generate_logo_prompt(
            business_name, industry, style, colors, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class CharacterGenerateAPI(APIView):
    """POST /api/media/character/ - Generate character description."""

    def post(self, request):
        name = request.data.get('name', '').strip()
        traits = request.data.get('traits', '').strip()
        style = request.data.get('style', 'concept')
        gender = request.data.get('gender', '').strip()
        age = request.data.get('age', '').strip()
        additional = request.data.get('additional', '').strip()

        if not traits:
            return Response(
                {'error': 'Please describe your character traits or features.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = CharacterService.generate_character(
            name, traits, style, gender, age, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class WordCloudAPI(APIView):
    """POST /api/media/word-cloud/ - Generate word cloud image."""

    def post(self, request):
        text = request.data.get('text', '').strip()
        width = int(request.data.get('width', 800))
        height = int(request.data.get('height', 400))
        bg_color = request.data.get('bg_color', 'white')
        colormap = request.data.get('colormap', 'viridis')
        max_words = int(request.data.get('max_words', 200))

        if not text:
            return Response(
                {'error': 'Please enter some text.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = WordCloudService.generate_word_cloud(
            text, width, height, bg_color, colormap, max_words
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="wordcloud.png"'
        return response


class BannerGenerateAPI(APIView):
    """POST /api/media/banner/ - Generate banner design prompt."""

    def post(self, request):
        title = request.data.get('title', '').strip()
        subtitle = request.data.get('subtitle', '').strip()
        cta = request.data.get('cta', '').strip()
        size = request.data.get('size', '1200x628')
        style = request.data.get('style', '').strip()
        brand_colors = request.data.get('brand_colors', '').strip()
        additional = request.data.get('additional', '').strip()

        if not title:
            return Response(
                {'error': 'Please enter a banner title.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = BannerService.generate_banner(
            title, subtitle, cta, size, style, brand_colors, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class PresentationGenerateAPI(APIView):
    """POST /api/media/presentation/ - Generate presentation content."""

    def post(self, request):
        topic = request.data.get('topic', '').strip()
        num_slides = int(request.data.get('num_slides', 10))
        style = request.data.get('style', 'professional')
        audience = request.data.get('audience', '').strip()
        additional = request.data.get('additional', '').strip()

        if not topic:
            return Response(
                {'error': 'Please enter a presentation topic.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = PresentationService.generate_presentation(
            topic, num_slides, style, audience, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})
