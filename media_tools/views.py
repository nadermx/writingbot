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
            {'q': 'What resolution and quality can I expect from the generated art?', 'a': 'The prompts are optimized for high-resolution output. When used with tools like Midjourney or DALL-E 3, you can generate art at up to 4K resolution suitable for printing and gallery display.'},
            {'q': 'Can I use AI-generated art for commercial purposes?', 'a': 'The prompts themselves are free to use. Commercial usage rights for the final images depend on the AI image generator you use — Midjourney, DALL-E, and Stable Diffusion each have their own licensing terms.'},
            {'q': 'How does this compare to prompting Midjourney or DALL-E directly?', 'a': 'Our tool generates expertly crafted prompts that incorporate artistic terminology, composition rules, and style-specific keywords. This produces significantly better results than writing prompts from scratch without prompt engineering knowledge.'},
            {'q': 'What customization options are available for art prompts?', 'a': 'You can choose from 8 art styles, specify your subject matter in detail, and use the additional notes field for color preferences, mood, composition, or references to specific artists and art movements.'},
            {'q': 'What are some tips for getting the best AI art results?', 'a': 'Be specific about your subject, mention the mood or atmosphere you want, reference art movements or artists for style guidance, and use the additional notes field to specify details like color palette, time of day, or composition preferences.'},
            {'q': 'What file formats will my AI art be in?', 'a': 'The output format depends on the AI image generator you use. DALL-E outputs PNG files, Midjourney provides JPG and PNG, and Stable Diffusion supports PNG, JPG, and WebP. Our prompts work with any output format.'},
            {'q': 'Is the AI Art Generator free to use?', 'a': 'Yes, the basic art prompt generator is free with daily usage limits. Premium subscribers get unlimited generations and access to enhanced AI prompts for more detailed and creative results.'},
            {'q': 'Can I generate multiple art variations at once?', 'a': 'Each generation produces one detailed prompt. You can quickly generate multiple prompts by adjusting your description or changing the style selection, then use each prompt in your preferred AI image tool for variations.'},
            {'q': 'Does the AI Art Generator work on mobile devices?', 'a': 'Yes, the generator is fully responsive and works on smartphones and tablets. Create art prompts on the go and copy them to use with any AI image tool later.'},
            {'q': 'Is my art description kept private?', 'a': 'Yes, your descriptions and generated prompts are not stored or shared. Each generation is processed in real time and the data is not retained after delivery.'},
            {'q': 'How fast are art prompts generated?', 'a': 'Art prompts are generated in just a few seconds. The AI analyzes your description and instantly crafts a detailed, style-optimized prompt ready for use.'},
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
            {'q': 'What output quality can I expect for poster designs?', 'a': 'Prompts are crafted for high-resolution output at 300 DPI or higher, ensuring sharp text and imagery suitable for large-format printing up to billboard size.'},
            {'q': 'Can I use these poster designs commercially?', 'a': 'Yes, the prompts are designed for commercial use including event marketing, advertising campaigns, and retail promotions. Final image licensing depends on your chosen AI image generator.'},
            {'q': 'Do the prompts work with Stable Diffusion and DALL-E?', 'a': 'Absolutely. The poster prompts are optimized for all major AI image generators including Stable Diffusion, DALL-E 3, Midjourney, and Adobe Firefly.'},
            {'q': 'Can I customize the layout and typography suggestions?', 'a': 'Yes, use the additional notes field to specify headline fonts, text placement preferences, layout orientation, and any specific design elements you need included.'},
            {'q': 'What tips help create better poster designs?', 'a': 'Include the event type and audience, specify a color mood, mention whether it is portrait or landscape, and describe the key visual element or focal point you want featured.'},
            {'q': 'What file format should I save my poster in?', 'a': 'For print posters, export as high-resolution PDF or TIFF with CMYK colors. For digital posters, PNG or JPG at 72-150 DPI works well for screens and social media sharing.'},
            {'q': 'Is the AI Poster Generator free?', 'a': 'Yes, you can generate poster design prompts for free with daily limits. Premium subscribers enjoy unlimited generations and enhanced prompt detail powered by advanced AI models.'},
            {'q': 'Can I generate multiple poster concepts for A/B testing?', 'a': 'Yes, run multiple generations with slightly different descriptions or styles to get varied poster concepts, then test which resonates best with your audience.'},
            {'q': 'Does the poster generator work on phones and tablets?', 'a': 'Yes, the tool is fully responsive. Design poster prompts from any device and copy them to your preferred AI image generator or design application.'},
            {'q': 'Are my poster descriptions stored or shared?', 'a': 'No. Your descriptions and generated prompts are processed in real time and are not stored, logged, or shared with any third party.'},
            {'q': 'How quickly are poster prompts generated?', 'a': 'Poster prompts are generated in seconds. The AI instantly analyzes your description and creates a comprehensive design brief including layout, typography, and visual direction.'},
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
            {'q': 'What resolution should I use for flyer designs?', 'a': 'For print flyers, aim for 300 DPI at your target size. For digital flyers shared on social media or email, 150 DPI or 1080px wide is sufficient for crisp display on all screens.'},
            {'q': 'Can I use these flyer designs for commercial marketing?', 'a': 'Yes, the prompts are specifically designed for commercial marketing use including business promotions, event advertising, real estate listings, and retail sales campaigns.'},
            {'q': 'Do the prompts work with DALL-E and Stable Diffusion for flyers?', 'a': 'Yes, all flyer prompts are compatible with DALL-E 3, Midjourney, Stable Diffusion, and other AI image generators. The prompts include layout and typography guidance that translates across platforms.'},
            {'q': 'What customization options do I have for flyer layouts?', 'a': 'You can specify single or double-sided, portrait or landscape orientation, content sections like contact info and CTA placement, brand colors, logo positioning, and specific imagery requirements.'},
            {'q': 'What are some best practices for effective flyer design?', 'a': 'Lead with a strong headline, use one clear call-to-action, keep text concise, include contact information prominently, use high-contrast colors for readability, and leave enough white space to avoid clutter.'},
            {'q': 'What file format is best for printing flyers?', 'a': 'Export as PDF with CMYK color mode and 3mm bleed for professional printing. For home printing, high-resolution PNG or JPG at 300 DPI works well. Digital flyers should be PNG or JPG at 72-150 DPI.'},
            {'q': 'Is the flyer generator free to use?', 'a': 'Yes, you can create flyer design prompts for free with daily usage limits. Premium users get unlimited generations and enhanced prompts with more detailed layout and marketing copy suggestions.'},
            {'q': 'Can I generate flyers in bulk for a marketing campaign?', 'a': 'You can generate multiple flyer concepts quickly by running successive prompts with different descriptions or styles. Each prompt produces a unique design concept tailored to your specifications.'},
            {'q': 'Can I design flyers on my phone?', 'a': 'Yes, the flyer generator is mobile-friendly and works seamlessly on smartphones and tablets. Create your flyer prompts anywhere, then use them with your preferred design tool.'},
            {'q': 'Is my flyer content kept confidential?', 'a': 'Yes, all your descriptions and business information entered into the generator are processed in real time and not stored, ensuring your marketing content remains private.'},
            {'q': 'How fast does the flyer prompt generator work?', 'a': 'Flyer prompts are generated in just a few seconds, giving you a complete design brief with layout suggestions, color guidance, typography recommendations, and visual direction.'},
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
            {'q': 'What resolution do thumbnail prompts target?', 'a': 'Prompts are optimized for standard thumbnail sizes including 1280x720 for blog headers, 1200x630 for social media link previews, and 1080x1080 for square social posts, all at high resolution.'},
            {'q': 'Can I use these thumbnails for commercial content?', 'a': 'Yes, the prompts are designed for commercial blog posts, marketing content, social media campaigns, and professional publications. Usage rights for the final images depend on your AI image generator.'},
            {'q': 'Do the prompts work with Midjourney and DALL-E for thumbnails?', 'a': 'Yes, all thumbnail prompts are crafted to produce excellent results with Midjourney, DALL-E 3, Stable Diffusion, and other popular AI image generation tools.'},
            {'q': 'What customization options are available for thumbnails?', 'a': 'Choose from 6 visual styles, specify your topic and mood, add brand colors and fonts in the additional notes, and describe specific visual elements or imagery you want featured.'},
            {'q': 'What tips help create thumbnails that get more clicks?', 'a': 'Use bold contrasting colors, include a clear focal point, keep compositions simple and uncluttered, use faces or emotional imagery when relevant, and ensure the thumbnail reads well at small sizes.'},
            {'q': 'What file format is best for blog and social media thumbnails?', 'a': 'PNG offers the best quality for thumbnails with text overlays and sharp edges. JPG works well for photographic thumbnails. WebP provides smaller file sizes for faster web loading.'},
            {'q': 'Is the thumbnail generator free?', 'a': 'Yes, the basic thumbnail prompt generator is free with daily usage limits. Premium subscribers get unlimited access and enhanced AI-powered prompts for more polished, detailed thumbnail concepts.'},
            {'q': 'Can I generate a batch of thumbnails for content planning?', 'a': 'You can quickly generate multiple thumbnail prompts by running successive generations with different topics. This is ideal for planning blog series, social media calendars, or content batches.'},
            {'q': 'Does the thumbnail generator work on mobile?', 'a': 'Yes, the tool is fully responsive and works on any device. Generate thumbnail prompts from your phone or tablet while on the go, then create the images when you are back at your desk.'},
            {'q': 'Are my thumbnail descriptions private?', 'a': 'Yes, your content topics and descriptions are not stored or shared. All data is processed in real time and discarded after the prompt is delivered to you.'},
            {'q': 'How quickly are thumbnail prompts created?', 'a': 'Thumbnail prompts are generated in just a few seconds. You get a complete visual brief including composition, color scheme, focal point, and style direction almost instantly.'},
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
            {'q': 'What resolution are YouTube thumbnail prompts optimized for?', 'a': 'All prompts target the official YouTube thumbnail resolution of 1280x720 pixels at 16:9 aspect ratio, ensuring your thumbnails display perfectly across desktop, mobile, and TV screens.'},
            {'q': 'Can I use these thumbnails commercially on monetized channels?', 'a': 'Yes, the prompts are designed for commercial YouTube channels. The final thumbnail image licensing depends on the AI tool you use — Midjourney and DALL-E both allow commercial use of generated images.'},
            {'q': 'How do these prompts compare to using Canva or Photoshop for thumbnails?', 'a': 'Our AI generates concept-level prompts optimized for click-through rates, incorporating proven YouTube design patterns. You can use the generated images as a base and add text overlays in Canva or Photoshop for the final thumbnail.'},
            {'q': 'Can I customize thumbnails for different video niches?', 'a': 'Yes, choose from 8 niche-specific styles including reaction, tutorial, gaming, tech review, vlog, educational, dramatic, and before-and-after. Each style follows the visual conventions that perform best in that niche.'},
            {'q': 'What are the best tips for high-CTR YouTube thumbnails?', 'a': 'Use expressive facial expressions, limit text to 3-5 bold words, create contrast between foreground and background, use bright saturated colors, and ensure the image tells a story that creates curiosity.'},
            {'q': 'What file format should I save YouTube thumbnails in?', 'a': 'YouTube accepts JPG, GIF, and PNG formats under 2MB. PNG is recommended for thumbnails with text overlays for the sharpest quality. JPG works well for photographic thumbnails at smaller file sizes.'},
            {'q': 'Is the YouTube Thumbnail Maker free?', 'a': 'Yes, you can generate YouTube thumbnail prompts for free with daily limits. Premium subscribers get unlimited generations and access to enhanced prompts that incorporate advanced CTR optimization techniques.'},
            {'q': 'Can I create thumbnails for an entire video series?', 'a': 'Yes, describe your series branding in the additional notes to generate consistent thumbnail concepts. Run multiple prompts for different episodes while maintaining a cohesive visual identity across your channel.'},
            {'q': 'Can I make YouTube thumbnails on my phone?', 'a': 'Yes, the tool works on mobile devices. Generate thumbnail prompts on your phone, copy the prompt to your AI image app, and create thumbnails without needing a desktop computer.'},
            {'q': 'Is my video content description kept private?', 'a': 'Yes, your video descriptions and channel details are processed in real time and are never stored, logged, or shared. Your content strategy remains completely confidential.'},
            {'q': 'How fast does the YouTube thumbnail generator work?', 'a': 'Thumbnail prompts are generated in seconds. You get a detailed prompt including facial expressions, color palette, composition, and text overlay zones ready to paste into any AI image generator.'},
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
            {'q': 'What sizes and resolutions do the icon prompts support?', 'a': 'Prompts are designed for scalable output from 16x16 favicons up to 1024x1024 app store icons. The descriptions emphasize clean edges and readable details at every size.'},
            {'q': 'Can I use generated icons commercially in my app or website?', 'a': 'Yes, the prompts are designed for commercial use in apps, websites, and software products. Final icon licensing depends on the AI image generator you use to create the actual icons.'},
            {'q': 'How do these icon prompts work with Midjourney and Stable Diffusion?', 'a': 'The prompts include specific terms for clean icon rendering, transparent or solid backgrounds, and consistent line weights that produce excellent results in Midjourney, DALL-E, and Stable Diffusion.'},
            {'q': 'Can I customize icons to match my design system?', 'a': 'Yes, specify your design system (Material Design, iOS Human Interface, Fluent Design) in the additional notes along with stroke weight, corner radius, and color palette for consistent results.'},
            {'q': 'What are best practices for creating effective icons?', 'a': 'Keep designs simple and recognizable, use consistent stroke weights, test readability at small sizes, maintain optical balance, and stick to a limited color palette. Our prompts incorporate all these principles automatically.'},
            {'q': 'What file format should I use for icons?', 'a': 'SVG is ideal for scalable web icons. PNG with transparency works for app icons and UI elements. ICO format is needed for favicons. Use the AI-generated image as a reference and recreate in vector format for production use.'},
            {'q': 'Is the AI Icon Generator free?', 'a': 'Yes, the basic icon prompt generator is free with daily usage limits. Premium users get unlimited generations and enhanced prompts with more detailed specifications for professional icon design projects.'},
            {'q': 'Can I generate a complete icon set at once?', 'a': 'Generate individual icons one at a time while specifying a consistent theme and style in each prompt. This approach lets you build a cohesive icon set with matching visual weight and proportions.'},
            {'q': 'Does the icon generator work on mobile devices?', 'a': 'Yes, the tool is fully responsive. Generate icon design prompts from any smartphone or tablet, then use the prompts with your preferred AI image generator or design application.'},
            {'q': 'Are my icon descriptions kept private?', 'a': 'Yes, all descriptions and generated prompts are processed in real time and not stored. Your app concepts and design ideas remain completely confidential.'},
            {'q': 'How quickly are icon prompts generated?', 'a': 'Icon prompts are generated in seconds, providing detailed specifications for style, line weight, color, background, and scalability considerations instantly.'},
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
            {'q': 'What resolution and quality do mockup prompts target?', 'a': 'Prompts are crafted for photorealistic, high-resolution output suitable for client presentations, portfolio pieces, and marketing materials at print-quality resolution.'},
            {'q': 'Can I use these mockups for commercial projects and client work?', 'a': 'Yes, the mockup prompts are designed for professional and commercial use including pitch decks, marketing campaigns, e-commerce listings, and portfolio showcases. Image licensing depends on your AI generator.'},
            {'q': 'Do mockup prompts work well with DALL-E and Midjourney?', 'a': 'Yes, the prompts are optimized for photorealistic rendering in DALL-E 3, Midjourney, and Stable Diffusion. They include specific lighting, material, and perspective details that produce convincing product mockups.'},
            {'q': 'What customization options are available for mockups?', 'a': 'Choose from 8 mockup types including device screens, packaging, apparel, print materials, billboards, lifestyle scenes, minimal floating, and studio shots. Add specific environment, lighting, and angle details in additional notes.'},
            {'q': 'What tips help create more realistic product mockups?', 'a': 'Describe the exact product and environment clearly, specify the camera angle and distance, mention realistic lighting conditions, include surface textures and materials, and reference specific settings like an office desk or cafe table.'},
            {'q': 'What file format works best for mockup presentations?', 'a': 'PNG offers the best quality for mockups with transparency needs. High-resolution JPG works well for presentation decks. For web use, WebP provides excellent quality at smaller file sizes.'},
            {'q': 'Is the AI Mockup Generator free?', 'a': 'Yes, you can generate mockup prompts for free with daily limits. Premium subscribers get unlimited generations and access to enhanced prompts with more detailed scene composition and material specifications.'},
            {'q': 'Can I generate mockups for multiple products in a product line?', 'a': 'Generate individual mockup prompts for each product while maintaining consistent styling by specifying the same environment, lighting, and brand elements across prompts for a cohesive product line presentation.'},
            {'q': 'Can I create mockups from my phone or tablet?', 'a': 'Yes, the mockup generator is fully responsive and works on all devices. Create mockup prompts on the go and use them with any AI image generator when you are ready.'},
            {'q': 'Is my product information kept confidential?', 'a': 'Yes, all product descriptions and mockup details are processed in real time and never stored or shared. Your unreleased product concepts and designs remain completely private.'},
            {'q': 'How fast are mockup prompts generated?', 'a': 'Mockup prompts are generated in seconds, delivering a comprehensive brief including product placement, lighting setup, camera angle, environment details, and material rendering specifications.'},
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
            {'q': 'What resolution and print quality can I expect from illustrations?', 'a': 'Prompts are optimized for high-resolution output suitable for print at 300 DPI. When used with Midjourney or DALL-E 3, illustrations can be generated at resolutions ideal for books, magazines, and large prints.'},
            {'q': 'Can I use AI-generated illustrations commercially in publications?', 'a': "Yes, the prompts are designed for commercial use in children\'s books, editorial publications, marketing materials, and digital content. Final licensing depends on the AI generator you use to create the images."},
            {'q': 'How do illustration prompts perform in Midjourney versus Stable Diffusion?', 'a': 'Both produce excellent results. Midjourney tends to excel at artistic and editorial styles, while Stable Diffusion offers more control over fine details. The prompts are structured to work optimally across both platforms.'},
            {'q': 'What customization options are there for illustration style?', 'a': 'Choose from 8 illustration styles, specify color palettes, shading techniques, line weight preferences, and subject matter. Use additional notes for art direction like mood boards, reference artists, or specific compositional requirements.'},
            {'q': 'What tips help create better book and editorial illustrations?', 'a': "For children\'s books, describe character emotions and scene action clearly. For editorial work, focus on the conceptual metaphor. Always specify the intended audience and mention if text space is needed within the illustration."},
            {'q': 'What file format is best for illustrations?', 'a': 'PNG preserves quality and supports transparency for layered compositions. TIFF is preferred for print publications. For web use, high-quality JPG or WebP offers good quality at reduced file sizes.'},
            {'q': 'Is the AI Illustration Generator free?', 'a': 'Yes, the basic generator is free with daily usage limits. Premium users get unlimited generations and enhanced prompts with richer artistic direction, detailed color palettes, and advanced composition guidance.'},
            {'q': 'Can I generate a series of illustrations with consistent characters?', 'a': 'Yes, describe your character in detail consistently across prompts and specify the same art style. Include character reference details in every generation to maintain visual continuity across a series.'},
            {'q': 'Does the illustration generator work on mobile?', 'a': 'Yes, the tool is fully responsive and works perfectly on smartphones and tablets. Create illustration prompts anywhere and use them with your preferred AI image tool at your convenience.'},
            {'q': 'Are my illustration concepts kept private?', 'a': "Yes, all descriptions including book plots, character details, and creative concepts are processed in real time and never stored. Your unpublished ideas and intellectual property remain confidential."},
            {'q': 'How quickly are illustration prompts generated?', 'a': 'Illustration prompts are ready in seconds, providing comprehensive artistic direction including style, color palette, composition, lighting, character details, and mood guidance.'},
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
            {'q': 'What resolution and output quality do design prompts target?', 'a': 'Prompts are optimized for professional output at print-ready resolution (300 DPI). The generated designs work at any scale from social media graphics to large-format marketing banners.'},
            {'q': 'Can I use the generated designs for commercial branding projects?', 'a': 'Yes, the prompts are specifically crafted for commercial branding, marketing, and corporate communications. Usage rights for AI-generated images depend on the platform you use to render them.'},
            {'q': 'How do design prompts compare to using Canva or Adobe Express?', 'a': 'Our AI generates unique, concept-level design directions rather than template-based designs. Use the prompts with AI image generators for original visuals, then refine in Canva, Photoshop, or Figma for final production.'},
            {'q': 'What customization options do I have for graphic design prompts?', 'a': 'Choose from 8 design styles, specify your brand guidelines, target audience, and intended use case. Add brand colors, font preferences, layout direction, and specific design element requirements in the additional notes.'},
            {'q': 'What are best practices for creating effective brand designs?', 'a': 'Maintain consistency across all materials, use a limited color palette, establish clear visual hierarchy, ensure designs work in both color and grayscale, and test readability at various sizes from business cards to billboards.'},
            {'q': 'What file format should I use for marketing designs?', 'a': 'PDF is standard for print materials. PNG works best for digital graphics with transparency. SVG is ideal for logos and scalable elements. JPG suits photographic marketing content for web use.'},
            {'q': 'Is the AI Design Generator free?', 'a': 'Yes, the basic design prompt generator is free with daily limits. Premium subscribers get unlimited generations and enhanced prompts with deeper design system guidance and brand strategy recommendations.'},
            {'q': 'Can I generate an entire brand identity suite?', 'a': 'Generate prompts for individual brand elements (logo, business cards, social media templates, letterheads) while specifying consistent brand guidelines across each prompt to build a cohesive identity system.'},
            {'q': 'Can I use the design generator on my phone?', 'a': 'Yes, the tool is fully responsive and works on all mobile devices. Create design briefs from anywhere and export the prompts to your preferred design application or AI image generator.'},
            {'q': 'Are my brand details and design briefs kept private?', 'a': 'Yes, all brand information, design descriptions, and generated prompts are processed in real time and never stored or shared. Your brand strategy and creative direction remain confidential.'},
            {'q': 'How fast are graphic design prompts generated?', 'a': 'Design prompts are created in seconds, delivering a complete design brief with style direction, color recommendations, typography guidance, layout principles, and visual hierarchy specifications.'},
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
            {'q': 'What resolution and quality do product image prompts target?', 'a': 'Prompts target high-resolution product photography suitable for Amazon (2000x2000px minimum), Shopify, and other e-commerce platforms. The descriptions emphasize sharp detail and professional studio-quality lighting.'},
            {'q': 'Can I use these product images for commercial e-commerce listings?', 'a': 'Yes, the prompts are specifically designed for commercial product photography. They follow marketplace guidelines for Amazon, Etsy, Shopify, and other platforms. Image licensing depends on your AI generator.'},
            {'q': 'How do product image prompts perform in DALL-E versus Midjourney?', 'a': 'DALL-E 3 excels at clean white-background product shots, while Midjourney produces stunning lifestyle and hero shots. The prompts work well with both, and Stable Diffusion offers additional control over lighting and materials.'},
            {'q': 'What customization options are available for product photography?', 'a': 'Choose from 8 photography styles including white background, lifestyle, flat lay, hero shot, detail close-up, group shots, studio, and outdoor. Specify lighting, angles, props, and surface materials in the additional notes.'},
            {'q': 'What tips help create better product images?', 'a': 'Describe the exact product material and finish, specify the lighting direction and intensity, mention the surface or background texture, include props that suggest lifestyle context, and always reference the intended marketplace requirements.'},
            {'q': 'What file format is best for e-commerce product images?', 'a': 'PNG is ideal for product images requiring transparency or white backgrounds. High-quality JPG at 85-95% works for most marketplaces. Amazon requires JPEG or PNG at minimum 1000x1000 pixels with pure white backgrounds.'},
            {'q': 'Is the Product Image Generator free?', 'a': 'Yes, you can generate product photography prompts for free with daily limits. Premium users get unlimited generations and enhanced prompts with advanced lighting setups and marketplace-specific optimization.'},
            {'q': 'Can I generate images for an entire product catalog?', 'a': 'Yes, generate prompts for each product while maintaining consistent lighting and styling by specifying the same studio setup across prompts. This creates a professional, cohesive look across your entire product line.'},
            {'q': 'Can I create product images from my phone?', 'a': 'Yes, the tool works perfectly on mobile devices. Generate product photography prompts anywhere, ideal for capturing product ideas on the go and creating listings from your smartphone.'},
            {'q': 'Is my product information kept confidential?', 'a': 'Yes, all product details and descriptions are processed in real time and never stored or shared. Your unreleased products, pricing strategies, and business details remain completely private.'},
            {'q': 'How fast are product image prompts generated?', 'a': 'Product image prompts are ready in seconds, providing complete photography direction including lighting setup, camera angle, background, props, and post-processing style recommendations.'},
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
            {'q': 'What resolution and quality can I expect from avatar prompts?', 'a': 'Prompts target high-resolution square output (512x512 to 1024x1024) that scales down cleanly to thumbnail sizes. The designs maintain clarity and recognizability even at small circular crop sizes used on most platforms.'},
            {'q': 'Can I use generated avatars commercially for my brand or product?', 'a': 'Yes, the prompts are designed for commercial use including brand mascots, team profiles, app user defaults, and marketing materials. Image usage rights depend on the AI generator you use.'},
            {'q': 'How do avatar prompts work with Midjourney and DALL-E?', 'a': 'Both produce excellent avatar results. Midjourney excels at artistic and anime styles, while DALL-E 3 is strong with cartoon and realistic styles. Stable Diffusion offers the most control for pixel art and specific character details.'},
            {'q': 'What customization options are available for avatars?', 'a': 'Choose from 8 styles including cartoon, anime, pixel art, 3D rendered, painted, professional headshot, chibi, and memoji-style. Specify hair, clothing, accessories, expressions, and background elements in your description.'},
            {'q': 'What tips help create distinctive, memorable avatars?', 'a': 'Focus on one or two defining visual features, use bold color choices, keep backgrounds simple, ensure the face or focal element is centered, and choose a style that matches the platform where the avatar will be displayed.'},
            {'q': 'What file format should I use for avatars?', 'a': 'PNG with transparency is best for avatars that need to work on various backgrounds. JPG works for simple backgrounds. Most platforms accept both formats, with recommended sizes between 400x400 and 1000x1000 pixels.'},
            {'q': 'Is the AI Avatar Generator free?', 'a': 'Yes, the basic avatar prompt generator is free with daily usage limits. Premium subscribers get unlimited generations and enhanced prompts with more detailed character specifications and style nuances.'},
            {'q': 'Can I create a set of matching avatars for my team or community?', 'a': 'Yes, specify a consistent style, color scheme, and theme across multiple generations. Describe the shared visual elements in each prompt to create a cohesive set with individual personality for each avatar.'},
            {'q': 'Does the avatar generator work on mobile devices?', 'a': 'Yes, the tool is fully responsive. Generate avatar prompts from your phone or tablet, perfect for quickly creating profile pictures or updating your social media presence on the go.'},
            {'q': 'Is my avatar description kept private?', 'a': 'Yes, all descriptions and personal preferences are processed in real time and never stored or shared. Your identity details and creative concepts remain completely confidential.'},
            {'q': 'How quickly are avatar prompts generated?', 'a': 'Avatar prompts are ready in just a few seconds, providing detailed character descriptions including style, features, expression, accessories, color palette, and background specifications.'},
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
            {'q': 'What resolution do portrait prompts target?', 'a': 'Prompts are optimized for high-resolution portrait output, typically targeting 2048x2048 or larger. This ensures fine detail in facial features, skin texture, and lighting effects suitable for printing and digital display.'},
            {'q': 'Can I use AI-generated portraits for commercial projects?', 'a': 'Yes, the prompts are suitable for commercial use including editorial publications, marketing campaigns, book covers, and album artwork. Check your AI image generator licensing for specific commercial usage terms.'},
            {'q': 'How do portrait prompts compare between Midjourney, DALL-E, and Stable Diffusion?', 'a': 'Midjourney produces stunning artistic and editorial portraits. DALL-E 3 excels at photorealistic results with accurate facial details. Stable Diffusion with fine-tuned models offers the most control over specific portrait styles and features.'},
            {'q': 'What customization options are available for portraits?', 'a': 'Choose from 8 styles including photorealistic, oil painting, watercolor, charcoal, pop art, renaissance, film noir, and fashion editorial. Specify lighting, mood, background, clothing, and specific facial expressions in your description.'},
            {'q': 'What tips help create more compelling portraits?', 'a': 'Describe the subject\'s emotion and personality, specify the lighting direction and quality, mention the background context, include details about clothing and accessories, and reference a specific artistic era or photographer for style guidance.'},
            {'q': 'What file format works best for portrait images?', 'a': 'PNG preserves the most detail for portraits with fine textures and subtle lighting. High-quality JPG (90%+) works well for web display and social media. TIFF is recommended for print-quality portrait reproductions.'},
            {'q': 'Is the AI Portrait Generator free?', 'a': 'Yes, portrait prompt generation is free with daily limits. Premium users get unlimited generations and access to enhanced prompts with advanced lighting techniques, more detailed composition guidance, and deeper artistic direction.'},
            {'q': 'Can I generate a series of portraits in a consistent style?', 'a': 'Yes, specify the same artistic style, lighting setup, and color palette across multiple prompts. Describe common elements like background treatment and composition to create a visually unified portrait series.'},
            {'q': 'Does the portrait generator work on mobile devices?', 'a': 'Yes, the tool is fully responsive and works seamlessly on smartphones and tablets. Create portrait prompts anywhere and use them with your preferred AI image generator at any time.'},
            {'q': 'Are my portrait descriptions kept private?', 'a': 'Yes, all descriptions are processed in real time and never stored or shared. Your creative concepts and personal details remain completely confidential.'},
            {'q': 'How fast are portrait prompts generated?', 'a': 'Portrait prompts are ready in seconds, delivering a comprehensive brief covering subject description, lighting setup, artistic style, color palette, composition, mood, and background direction.'},
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
            {'q': 'What is the maximum resolution I can generate wallpapers at?', 'a': 'Prompts are optimized for 4K (3840x2160) and even 8K (7680x4320) resolution wallpapers. Ultrawide monitor formats (3440x1440, 5120x2160) and mobile resolutions (1080x1920, 1440x3200) are also supported.'},
            {'q': 'Can I use generated wallpapers commercially or redistribute them?', 'a': 'Yes, you can use the wallpapers for personal and commercial purposes such as app defaults, website backgrounds, and digital products. Redistribution rights depend on the AI image generator licensing terms.'},
            {'q': 'How do wallpaper prompts perform in Midjourney versus Stable Diffusion?', 'a': 'Midjourney excels at artistic, fantasy, and abstract wallpapers with stunning color depth. Stable Diffusion is excellent for photorealistic landscapes and custom resolutions. DALL-E 3 produces clean, detailed wallpapers in any style.'},
            {'q': 'What customization options are there for wallpaper designs?', 'a': 'Choose from 8 themes including nature, abstract, space, minimal, cyberpunk, fantasy, gradient, and dark moody. Specify exact resolution, color dominance, subject placement, and icon-friendly zones in the additional notes.'},
            {'q': 'What tips help create the best desktop wallpapers?', 'a': 'Keep the center and right side relatively uncluttered for desktop icons, use subtle rather than busy patterns, choose colors that do not strain the eyes over long viewing, and specify whether you want a light or dark theme to match your system.'},
            {'q': 'What file format is best for wallpapers?', 'a': 'PNG offers the best quality for wallpapers with sharp details and gradients. High-quality JPG (90%+) provides smaller file sizes with minimal quality loss. For OLED screens, use deep blacks in PNG format for best display results.'},
            {'q': 'Is the wallpaper generator free?', 'a': 'Yes, basic wallpaper prompt generation is free with daily limits. Premium users get unlimited generations and enhanced prompts optimized for specific monitor resolutions and advanced composition techniques.'},
            {'q': 'Can I generate a matching set of wallpapers for all my devices?', 'a': 'Yes, generate prompts for the same theme at different aspect ratios — 16:9 for desktop, 9:16 for mobile, 21:9 for ultrawide. The AI maintains visual consistency across orientations while optimizing composition for each format.'},
            {'q': 'Does the wallpaper generator work on mobile?', 'a': 'Yes, the tool is fully responsive. Generate wallpaper prompts from your phone or tablet and use any AI image generator to create the wallpaper directly on your mobile device.'},
            {'q': 'Are my wallpaper descriptions private?', 'a': 'Yes, all descriptions and preferences are processed in real time and never stored. Your creative themes and generated prompts remain completely confidential.'},
            {'q': 'How fast are wallpaper prompts generated?', 'a': 'Wallpaper prompts are ready in seconds, providing complete details on composition, color palette, resolution optimization, subject placement, and icon-friendly zone positioning.'},
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
            {'q': 'What resolution and quality do background prompts support?', 'a': 'Prompts target high-resolution output suitable for any screen size from mobile (1080x1920) to 4K monitors (3840x2160) and beyond. For web backgrounds, seamless tiling at any resolution is supported through specific prompt guidance.'},
            {'q': 'Can I use generated backgrounds commercially for websites and apps?', 'a': 'Yes, the prompts are designed for commercial use in websites, applications, presentations, video production, and marketing materials. Image licensing terms depend on the AI generator you use.'},
            {'q': 'How do background prompts work with DALL-E, Midjourney, and Stable Diffusion?', 'a': 'All three produce excellent backgrounds. DALL-E 3 excels at clean gradients and bokeh effects. Midjourney creates stunning abstract and textured backgrounds. Stable Diffusion is ideal for seamless tileable patterns and custom dimensions.'},
            {'q': 'What customization options are available for backgrounds?', 'a': 'Choose from 8 styles including gradient, abstract, textured, bokeh, pattern-based, nature, minimal, and dark theme. Specify exact colors, opacity levels, blur intensity, and content placement zones in the additional notes.'},
            {'q': 'What are best practices for creating effective backgrounds?', 'a': 'Ensure the background does not compete with foreground content, use subtle gradients rather than harsh transitions, maintain enough contrast for text readability, keep key visual elements away from edges, and test on both light and dark displays.'},
            {'q': 'What file format is best for different background uses?', 'a': 'PNG is ideal for backgrounds with transparency or gradients. JPG works for photographic backgrounds at smaller file sizes. SVG or WebP is optimal for web backgrounds needing fast load times. Use CSS-friendly dimensions for website backgrounds.'},
            {'q': 'Is the AI Background Generator free?', 'a': 'Yes, background prompt generation is free with daily usage limits. Premium subscribers get unlimited generations and enhanced prompts with advanced layering, color harmony, and seamless tiling optimization.'},
            {'q': 'Can I generate a set of matching backgrounds for a project?', 'a': 'Yes, describe your color scheme and style consistently across multiple prompts to create a cohesive background set. This is ideal for presentation slide decks, website sections, or multi-page marketing materials.'},
            {'q': 'Can I generate backgrounds on mobile devices?', 'a': 'Yes, the tool is fully responsive and works on any smartphone or tablet. Generate background prompts on the go for your Zoom calls, presentations, social media posts, or web projects.'},
            {'q': 'Are my background descriptions kept private?', 'a': 'Yes, all descriptions and generated prompts are processed in real time and never stored or shared. Your design specifications and project details remain completely confidential.'},
            {'q': 'How fast are background prompts generated?', 'a': 'Background prompts are ready in seconds, providing comprehensive specifications for color palette, pattern style, blur effects, content placement zones, and seamless tiling guidance.'},
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
            {'q': 'What resolution and quality can I expect?', 'a': 'Prompts are optimized for high-resolution output at 300 DPI, suitable for both web display and print use.'},
            {'q': 'Can I use the infographics commercially?', 'a': 'Yes, all generated infographic prompts produce original designs you can use for business presentations, marketing materials, and client deliverables.'},
            {'q': 'Do the prompts work with Midjourney and DALL-E?', 'a': 'Absolutely. The prompts are crafted to work with Midjourney, DALL-E 3, Stable Diffusion, and other popular AI image generators.'},
            {'q': 'Can I customize the color scheme and branding?', 'a': 'Yes, specify your brand colors, fonts, and logo placement in the description for a fully branded infographic design.'},
            {'q': 'What are some tips for better infographic results?', 'a': 'Include specific data points, choose a clear visual hierarchy, limit text to key statistics, and specify a consistent color palette for best results.'},
            {'q': 'What file formats will my infographic be in?', 'a': 'The AI image generator you use will determine the output format, typically PNG or JPG. Our prompts are optimized for crisp vector-style rendering.'},
            {'q': 'Is the infographic generator free to use?', 'a': 'Free users can generate infographic prompts with daily limits. Premium users get unlimited generations and enhanced prompt detail.'},
            {'q': 'Can I generate multiple infographics in a batch?', 'a': 'You can generate prompts one at a time, each tailored to different data sets or topics. Premium users enjoy higher daily limits for batch workflows.'},
            {'q': 'Does the infographic generator work on mobile devices?', 'a': 'Yes, the tool is fully responsive and works on smartphones and tablets. You can create infographic prompts on the go from any browser.'},
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
            {'q': 'What resolution should my book cover be?', 'a': 'For print books, 300 DPI at 6x9 inches is standard. For e-books, Amazon recommends 2560x1600 pixels. Prompts account for both formats.'},
            {'q': 'Can I use the book cover for commercial self-publishing?', 'a': 'Yes, the generated prompts create original cover designs suitable for Amazon KDP, IngramSpark, and other self-publishing platforms.'},
            {'q': 'Which AI tools produce the best book covers from these prompts?', 'a': 'Midjourney v5+ and DALL-E 3 excel at book cover generation. Stable Diffusion SDXL also produces excellent results with the right models.'},
            {'q': 'Can I include title text and author name in the design?', 'a': 'Prompts include space for typography placement. For best results, add text in a design tool like Canva or Photoshop after generating the artwork.'},
            {'q': 'What makes a book cover sell well online?', 'a': 'High contrast, readable at thumbnail size, genre-appropriate imagery, and a clear focal point. Our prompts incorporate all of these best practices.'},
            {'q': 'What file format should I use for my book cover?', 'a': 'Use PNG for maximum quality when uploading to publishing platforms. JPG works for e-book-only covers where file size matters.'},
            {'q': 'Is the book cover generator free?', 'a': 'Free users can generate a limited number of book cover prompts daily. Premium users get unlimited generations with more detailed, genre-optimized prompts.'},
            {'q': 'Can I generate covers for a book series?', 'a': 'Yes, describe your series theme and visual identity to generate consistent cover designs across multiple books in a series.'},
            {'q': 'How fast are book cover prompts generated?', 'a': 'Prompts are generated in seconds. The total time depends on which AI image generator you use to render the final cover artwork.'},
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
            {'q': 'What resolution works best for packaging design?', 'a': 'For print-ready packaging, 300 DPI is essential. Prompts are structured to generate high-detail artwork suitable for production-quality output.'},
            {'q': 'Can I use these packaging designs commercially?', 'a': 'Yes, generated prompts create original designs you can use for real product packaging, retail shelves, and e-commerce listings.'},
            {'q': 'Which AI image generators work best for packaging design?', 'a': 'Midjourney excels at realistic product mockups. DALL-E 3 handles text integration well. Stable Diffusion SDXL is great for iterating on design variations.'},
            {'q': 'Can I specify materials like kraft paper or metallic finishes?', 'a': 'Yes, include material preferences like matte, glossy, kraft paper, foil stamping, or embossed textures in your description for accurate design prompts.'},
            {'q': 'What are best practices for packaging design prompts?', 'a': 'Specify your product type, target audience, shelf placement, and brand personality. Include color preferences and mention any regulatory label areas needed.'},
            {'q': 'What file formats are best for packaging design?', 'a': 'PNG for initial concepts, then move to vector formats (AI, SVG) for production. Our prompts generate artwork suitable for conversion to print-ready files.'},
            {'q': 'Is the packaging design generator free?', 'a': 'Free users can generate packaging design prompts with daily limits. Premium users unlock unlimited generations and more detailed material-specific prompts.'},
            {'q': 'Can I generate packaging for multiple products at once?', 'a': 'Generate prompts one product at a time for best results. Describe your product line theme to maintain visual consistency across your entire range.'},
            {'q': 'Does the tool work well on mobile for quick concepts?', 'a': 'Yes, the packaging design generator is fully responsive. Quickly generate concept prompts on your phone and refine them later on desktop.'},
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
            {'q': 'What quality and resolution do I need for streaming platforms?', 'a': 'Spotify and Apple Music require at least 3000x3000 pixels at 72 DPI in sRGB color space. Our prompts are designed to produce artwork at this standard.'},
            {'q': 'Can I use the album artwork commercially on streaming services?', 'a': 'Yes, the prompts generate original artwork concepts you can use for Spotify, Apple Music, Bandcamp, SoundCloud, and all distribution platforms.'},
            {'q': 'Which AI tool creates the best album covers?', 'a': 'Midjourney produces the most visually striking album art. DALL-E 3 handles conceptual imagery well. Both work excellently with our genre-optimized prompts.'},
            {'q': 'Can I match the artwork to my existing visual brand?', 'a': 'Yes, describe your color palette, visual style, mood, and existing branding elements to get artwork that fits your artist identity.'},
            {'q': 'What makes great album cover artwork?', 'a': 'Strong focal imagery, genre-appropriate aesthetics, readability at small sizes, and a mood that matches your music. Avoid overly complex compositions that lose impact at thumbnail size.'},
            {'q': 'What file format should I upload to distributors?', 'a': 'Most distributors require JPG or PNG, 3000x3000 pixels minimum. PNG preserves quality best. DistroKid, TuneCore, and CD Baby all accept both formats.'},
            {'q': 'Is the album cover generator free for independent artists?', 'a': 'Free users can generate album cover prompts with daily limits. Premium plans offer unlimited generations, perfect for artists releasing multiple singles and EPs.'},
            {'q': 'Can I create matching artwork for an entire album or EP?', 'a': 'Yes, describe your album theme and visual direction to generate a cohesive series of artworks for singles, the full album, and promotional materials.'},
            {'q': 'How does this compare to hiring a graphic designer?', 'a': 'Our tool generates prompts in seconds for free, versus days and hundreds of dollars for a designer. It is ideal for independent artists, demos, and rapid iteration before finalizing with a professional.'},
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
            {'q': 'What resolution do I need for a tattoo stencil?', 'a': 'For stencil printing, 300 DPI at actual tattoo size works best. Our prompts generate clean line work that transfers well to thermal stencil paper.'},
            {'q': 'Can I use these tattoo designs at a real tattoo shop?', 'a': 'Yes, bring the generated design to your tattoo artist as a reference or starting point. Most artists appreciate detailed reference imagery for custom work.'},
            {'q': 'Which AI tool renders tattoo designs best?', 'a': 'Midjourney excels at realistic tattoo renders on skin. Stable Diffusion with tattoo-specific models produces excellent line art. DALL-E 3 handles watercolor and abstract styles well.'},
            {'q': 'Can I combine multiple tattoo styles in one design?', 'a': 'Yes, describe your desired style mix such as geometric with watercolor splashes or Japanese with neo-traditional elements for unique fusion designs.'},
            {'q': 'What should I include in my tattoo description for best results?', 'a': 'Specify style, body placement, size, key symbols or imagery, color vs black and grey, and any meaningful elements you want incorporated into the design.'},
            {'q': 'What file format works best for sharing with my tattoo artist?', 'a': 'PNG with a white or transparent background is ideal. High-contrast black line work on white is easiest for tattoo artists to work from and create stencils.'},
            {'q': 'Is the tattoo design generator free?', 'a': 'Free users can generate tattoo design prompts with daily limits. Premium users get unlimited generations and more detailed style-specific prompts.'},
            {'q': 'Can I generate a full sleeve or large piece concept?', 'a': 'Yes, describe your full sleeve theme, flow direction, and key elements. The generator creates cohesive compositions that wrap naturally around the body.'},
            {'q': 'Is my tattoo design idea kept private?', 'a': 'Yes, your descriptions and generated prompts are not shared publicly. Your custom tattoo concepts remain private to your account.'},
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
            {'q': 'What resolution and scaling options are available for pixel art?', 'a': 'Pixel art is resolution-independent and scales perfectly using nearest-neighbor interpolation. A 32x32 sprite can be cleanly scaled to 256x256 or larger without blur.'},
            {'q': 'Can I use the pixel art commercially in my indie game?', 'a': 'Yes, all generated pixel art prompts produce original designs. You own the rights to artwork created from these prompts for commercial game releases.'},
            {'q': 'Which AI generator handles pixel art best?', 'a': 'Stable Diffusion with pixel art LoRA models produces the most authentic results. Midjourney can create pixel art with style parameters. DALL-E 3 handles simple sprites well.'},
            {'q': 'Can I customize the exact number of colors in my palette?', 'a': 'Yes, specify exact color counts like 4-color Game Boy palette, 16-color NES palette, or any custom limit. This ensures authentic retro aesthetics.'},
            {'q': 'What tips help create better pixel art with AI?', 'a': 'Specify the exact grid size, mention "pixel art" and "sprite" explicitly, reference a specific era (8-bit, 16-bit), and keep designs simple with clear silhouettes for small sprites.'},
            {'q': 'What file format is best for pixel art?', 'a': 'PNG is the standard for pixel art as it uses lossless compression and preserves every pixel perfectly. Never use JPG for pixel art as it introduces compression artifacts.'},
            {'q': 'Is the pixel art generator free for hobbyists?', 'a': 'Free users can generate pixel art prompts daily with usage limits. Premium plans offer unlimited generations, ideal for game developers creating full sprite sheets.'},
            {'q': 'Can I generate animation frames or sprite sheets?', 'a': 'Describe your animation sequence such as walk cycle, attack animation, or idle animation. Generate individual frames and assemble them into sprite sheets in your game engine.'},
            {'q': 'How does this compare to drawing pixel art manually?', 'a': 'Manual pixel art offers precise control but takes hours per sprite. Our generator creates detailed prompts in seconds, perfect for rapid prototyping and concept exploration before manual refinement.'},
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
            {'q': 'What resolution do I need for fabric printing?', 'a': 'For fabric printing, 300 DPI at the tile repeat size is standard. A single tile at 2000x2000 pixels works well for most print-on-demand fabric services.'},
            {'q': 'Can I sell products with these patterns commercially?', 'a': 'Yes, the prompts generate original pattern designs. You can use them for fabric, wallpaper, merchandise, and any commercial product line.'},
            {'q': 'Which AI tool creates the best seamless patterns?', 'a': 'Midjourney with the --tile parameter creates excellent seamless patterns. Stable Diffusion with tiling models also produces great results. DALL-E 3 works for simpler repeats.'},
            {'q': 'Can I specify exact colors to match my brand?', 'a': 'Yes, include hex codes, Pantone references, or descriptive color names in your prompt. You can also specify a limited color palette for screen printing.'},
            {'q': 'What makes a pattern design tile seamlessly?', 'a': 'Edges must match perfectly on all sides. Our prompts specify seamless tiling explicitly. For best results, test the output by repeating it in a grid before production.'},
            {'q': 'What file format works best for pattern tiles?', 'a': 'PNG for digital use and design work. TIFF for print production. SVG if you need vector-based patterns. Our prompts produce artwork suitable for all formats.'},
            {'q': 'Is the pattern generator free to use?', 'a': 'Free users can generate pattern prompts with daily limits. Premium users get unlimited generations and access to more detailed pattern-specific prompt enhancements.'},
            {'q': 'Can I create matching pattern variations for a collection?', 'a': 'Yes, describe your theme and request coordinating patterns such as a hero print, a secondary pattern, and a simple blender to build a cohesive textile collection.'},
            {'q': 'Does the tool handle complex pattern types like half-drop repeats?', 'a': 'Yes, specify repeat types such as straight repeat, half-drop, brick, mirror, or rotational symmetry in your description for precise pattern engineering.'},
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
            {'q': 'What quality level can I achieve with the 3D model prompts?', 'a': 'Prompts support everything from real-time game assets to photorealistic product renders. Specify your target quality and polygon budget for optimized results.'},
            {'q': 'Can I use these 3D concepts for commercial projects?', 'a': 'Yes, all prompts generate original 3D model concepts suitable for commercial games, architectural visualization, product renders, and client work.'},
            {'q': 'Which AI tools can generate 3D models from these prompts?', 'a': 'Use prompts with Midjourney or DALL-E for 2D concept art, then model in Blender. For direct 3D generation, tools like Meshy, Tripo3D, and Shap-E work with our descriptions.'},
            {'q': 'Can I specify polygon count and topology requirements?', 'a': 'Yes, include target poly counts, subdivision levels, and topology preferences. Specify "low-poly game-ready" or "high-poly sculpt" for appropriate detail levels.'},
            {'q': 'What are best practices for 3D model prompt writing?', 'a': 'Specify the viewing angle, lighting environment, material types, scale reference, and intended use case. Include technical requirements like poly budget and texture resolution.'},
            {'q': 'What output format should I target for 3D models?', 'a': 'FBX and OBJ are universal. glTF is ideal for web and real-time. USD works for film pipelines. Our prompts describe models compatible with all standard 3D formats.'},
            {'q': 'Is the 3D model generator free?', 'a': 'Free users can generate 3D model prompts with daily limits. Premium users get unlimited generations with additional technical details for professional production workflows.'},
            {'q': 'Can I generate prompts for an entire 3D scene?', 'a': 'Yes, describe complete scenes with multiple objects, environment details, lighting rigs, and atmospheric effects for comprehensive scene composition prompts.'},
            {'q': 'How fast are the 3D model prompts generated?', 'a': 'Prompts are generated in seconds. The actual 3D modeling or rendering time depends on your chosen software and hardware. Prompts help you skip the concept phase entirely.'},
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
            {'q': 'What resolution works best for storyboard panels?', 'a': 'Standard storyboard frames are 16:9 or 2.39:1 aspect ratio. 1920x1080 pixels per panel is ideal for presentation-quality storyboards.'},
            {'q': 'Can I use the storyboards for a professional film production?', 'a': 'Yes, the prompts create industry-standard storyboard concepts suitable for pitching to studios, planning shoots, and coordinating with cinematographers and crew.'},
            {'q': 'Which AI tool renders storyboard panels best?', 'a': 'Midjourney excels at cinematic compositions. DALL-E 3 handles specific scene descriptions well. Stable Diffusion with film-style models produces consistent character looks across panels.'},
            {'q': 'Can I maintain consistent characters across panels?', 'a': 'Describe your characters with specific details like clothing, hair, and features. For AI generation, use consistent character descriptions or seed values to maintain visual continuity.'},
            {'q': 'What should I include for effective storyboard prompts?', 'a': 'Specify shot type, camera angle, character positions, action direction, lighting mood, and any important props. Include transitions like cut, dissolve, or pan between panels.'},
            {'q': 'What file format is best for sharing storyboards?', 'a': 'PNG for individual panels, PDF for compiled storyboard sheets. Many production teams also use dedicated storyboard software that accepts standard image imports.'},
            {'q': 'Is the storyboard generator free for student filmmakers?', 'a': 'Free users can generate storyboard prompts with daily limits. Premium plans offer unlimited generations, perfect for full film and animation pre-production workflows.'},
            {'q': 'Can I generate storyboards for animation projects?', 'a': 'Yes, select the Animation style for prompts optimized for animated productions including key poses, motion arcs, and timing notes for each panel.'},
            {'q': 'How does this compare to hand-drawing storyboards?', 'a': 'AI-generated storyboard panels take seconds versus hours of hand-drawing. Perfect for rapid visualization, pitch decks, and early pre-production before committing to a dedicated storyboard artist.'},
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
            {'q': 'What resolution should my fantasy map be?', 'a': 'For detailed world maps, aim for at least 4000x3000 pixels. Battle maps for VTTs work best at 140 pixels per grid square. Our prompts support all scales.'},
            {'q': 'Can I use the fantasy maps commercially in my published novel or game?', 'a': 'Yes, the prompts generate original map designs. You can use the resulting artwork in published novels, RPG sourcebooks, video games, and other commercial projects.'},
            {'q': 'Which AI generator creates the best fantasy maps?', 'a': 'Midjourney produces stunning illustrated maps with rich detail. Stable Diffusion with map-specific models offers great control. DALL-E 3 handles simpler regional maps well.'},
            {'q': 'Can I customize the geographic features and landmarks?', 'a': 'Yes, specify exact geography including mountain ranges, rivers, forests, deserts, coastlines, cities, ruins, and any landmarks important to your world lore.'},
            {'q': 'What tips help create the best fantasy maps?', 'a': 'Define your continent shape, place mountains first as they determine river flow, add forests and settlements logically, and specify the map era and technology level for authentic cartographic style.'},
            {'q': 'What file format works best for fantasy maps?', 'a': 'PNG for digital use and virtual tabletops. High-resolution JPG for print. For Roll20 and Foundry VTT, PNG under 10MB with grid alignment works best.'},
            {'q': 'Is the fantasy map generator free for hobbyist worldbuilders?', 'a': 'Free users can generate fantasy map prompts with daily limits. Premium users get unlimited generations for building entire world atlases and campaign settings.'},
            {'q': 'Can I generate maps at different scales?', 'a': 'Yes, create world maps, continent maps, regional maps, city maps, dungeon maps, and battle maps. Specify the scale and scope in your description.'},
            {'q': 'How does this compare to dedicated map-making tools like Inkarnate?', 'a': 'Our generator creates unique, artistic map concepts in seconds. Tools like Inkarnate offer precise placement control. Many creators use our prompts for inspiration and then refine in dedicated map editors.'},
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
            {'q': 'What resolution works best for cartoon artwork?', 'a': 'For digital use, 2048x2048 pixels is a great starting point. For print materials like merchandise, aim for 300 DPI at the final print size.'},
            {'q': 'Can I use cartoon artwork commercially for my brand?', 'a': 'Yes, all generated prompts produce original cartoon designs. Use them for mascots, marketing materials, merchandise, social media, and brand identity.'},
            {'q': 'Which AI tool creates the best cartoon art?', 'a': 'Midjourney excels at Pixar-style 3D cartoons and stylized characters. DALL-E 3 handles specific character descriptions accurately. Stable Diffusion with anime models dominates chibi and anime styles.'},
            {'q': 'Can I maintain a consistent character across multiple images?', 'a': 'Describe your character with precise details such as outfit, hairstyle, colors, and proportions. Use the same description base across prompts for visual consistency.'},
            {'q': 'What makes a cartoon character design memorable?', 'a': 'Strong silhouette, distinctive features, limited color palette, exaggerated proportions, and clear personality expression. Our prompts incorporate these classic animation design principles.'},
            {'q': 'What file format is best for cartoon artwork?', 'a': 'PNG with transparency for characters and stickers. JPG for full-scene illustrations. SVG if you trace the artwork to vector format for scalable logos and mascots.'},
            {'q': 'Is the cartoon generator free?', 'a': 'Free users can generate cartoon prompts with daily limits. Premium users get unlimited generations and enhanced style-specific prompt details for professional-quality results.'},
            {'q': 'Can I generate cartoon artwork on my phone?', 'a': 'Yes, the cartoon generator is fully responsive and works on all mobile devices. Create character concepts and cartoon illustrations from any smartphone or tablet browser.'},
            {'q': 'How fast can I generate cartoon character concepts?', 'a': 'Prompts are generated in just a few seconds. This makes it incredibly fast to explore different character designs, styles, and expressions before committing to a final concept.'},
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
            {'q': 'What resolution should comic book art be?', 'a': 'Standard comic pages are 6.625x10.25 inches at 300 DPI for print. For webcomics, 800-1200 pixels wide at 72 DPI is ideal for screen reading.'},
            {'q': 'Can I use the comic art commercially for publishing?', 'a': 'Yes, the prompts generate original comic art concepts. You can use the resulting artwork for self-published comics, webcomics, graphic novels, and print-on-demand.'},
            {'q': 'Which AI generator produces the best comic book art?', 'a': 'Midjourney creates stunning Western comic styles and dynamic poses. Stable Diffusion with anime models dominates manga generation. DALL-E 3 handles specific scene compositions well.'},
            {'q': 'Can I specify panel layouts and page composition?', 'a': 'Yes, describe your desired panel layout such as six-panel grid, splash page, two-page spread, or dynamic angled panels. Include reading flow direction for manga-style right-to-left layouts.'},
            {'q': 'What tips help create better comic art with AI?', 'a': 'Specify the exact camera angle, character poses, facial expressions, and lighting for each panel. Reference specific comic art styles or artists for consistent visual tone throughout your project.'},
            {'q': 'What file format is standard for comic publishing?', 'a': 'TIFF or PNG at 300 DPI for print comics. PNG or JPG for webcomics. CBZ/CBR archives for digital comic distribution platforms like ComiXology.'},
            {'q': 'Is the comic generator free for indie creators?', 'a': 'Free users can generate comic art prompts with daily limits. Premium plans offer unlimited generations, ideal for creators producing full issues and serialized webcomics.'},
            {'q': 'Can I generate multiple panels with consistent characters?', 'a': 'Describe your characters with detailed physical traits, costumes, and distinguishing features. Reuse these descriptions across panel prompts to maintain visual consistency throughout your comic.'},
            {'q': 'How does this compare to commissioning a comic artist?', 'a': 'AI-generated comic art concepts take seconds and cost nothing versus weeks and hundreds of dollars per page from a professional. It is perfect for rapid prototyping, pitch materials, and indie creators on a budget.'},
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
            {'q': 'What level of detail can I expect in the designs?', 'a': 'Prompts include articulation points, sculpt details, paint applications, and accessory specifications. You control the detail level from simple vinyl toys to highly detailed collectibles.'},
            {'q': 'Can I use these designs to manufacture real action figures?', 'a': 'Yes, the prompts generate original toy design concepts suitable for prototyping, 3D printing, and pitching to manufacturers for commercial production.'},
            {'q': 'Which AI tool renders action figure concepts best?', 'a': 'Midjourney excels at photorealistic toy renders and packaging mockups. DALL-E 3 handles specific accessory details well. Stable Diffusion produces great stylized toy concepts.'},
            {'q': 'Can I specify articulation and joint details?', 'a': 'Yes, describe the number of articulation points, joint types like ball joints or swivel hinges, and posability requirements for your action figure design.'},
            {'q': 'What makes a great action figure design prompt?', 'a': 'Specify the scale, art style, character pose, key accessories, number of interchangeable parts, packaging type, and target audience such as collectors versus children for best results.'},
            {'q': 'What file format works best for toy design concepts?', 'a': 'PNG for 2D concept art and turnaround sheets. For 3D printing prototypes, use the concept art as reference to model in ZBrush or Blender and export as STL.'},
            {'q': 'Is the action figure generator free?', 'a': 'Free users can generate action figure design prompts with daily limits. Premium users get unlimited generations with enhanced detail for professional toy design workflows.'},
            {'q': 'Can I design a full toy line with multiple figures?', 'a': 'Yes, describe your toy line theme, shared design elements, and individual character variations to generate a cohesive collection of action figure concepts.'},
            {'q': 'Are my action figure design ideas kept private?', 'a': 'Yes, your toy design descriptions and generated prompts are private to your account. Your original character concepts and intellectual property remain confidential.'},
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
        'url': '/image-converter/',
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
        'url': '/tools/ai-image-generator/',
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


class ImageToolsIndex(View):
    """Renders the image tools index page listing all image/AI tools."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        tools = [t for t in MEDIA_TOOLS if t.get('category') in ('image', 'ai')]
        return render(request, 'media-tools/image-tools-index.html', {
            'title': f'Free Online Image Tools | {config.PROJECT_NAME}',
            'description': 'AI image generators, background remover, image converter, and 30+ creative design tools. All free.',
            'page': 'image-tools',
            'g': g,
            'tools': tools,
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
