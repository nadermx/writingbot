from ai_tools.generators.base import BaseGenerator


class StoryGenerator(BaseGenerator):
    slug = 'ai-story-generator'
    name = 'AI Story Generator'
    description = 'Generate captivating stories with compelling characters, vivid settings, and engaging plots.'
    category = 'Creative Writing'
    icon = 'story'
    meta_title = 'Free AI Story Generator'
    meta_description = 'Generate captivating stories with compelling characters and engaging plots. Choose your genre, length, and style.'

    fields = [
        {'name': 'premise', 'label': 'Story Premise', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your story idea or premise...'},
        {'name': 'genre', 'label': 'Genre', 'type': 'select', 'required': False, 'options': ['Fantasy', 'Science Fiction', 'Mystery', 'Thriller', 'Romance', 'Adventure', 'Historical Fiction', 'Literary Fiction']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Flash Fiction (500 words)', 'Short (1000 words)', 'Medium (2000 words)', 'Long (3000 words)']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Dramatic', 'Humorous', 'Dark', 'Lighthearted', 'Suspenseful', 'Whimsical', 'Melancholic']},
    ]

    system_prompt = (
        'You are a master storyteller and creative fiction writer. Write a compelling story based on the given premise. '
        'Genre: {genre}. Target length: {length}. Tone: {tone}. '
        'Include vivid descriptions, well-developed characters, natural dialogue, and a satisfying narrative arc '
        'with a clear beginning, rising action, climax, and resolution.'
    )


class ShortStoryGenerator(BaseGenerator):
    slug = 'ai-short-story-generator'
    name = 'AI Short Story Generator'
    description = 'Create complete short stories with focused narratives, tight pacing, and impactful endings.'
    category = 'Creative Writing'
    icon = 'short-story'
    meta_title = 'Free AI Short Story Generator'
    meta_description = 'Create complete short stories with focused narratives and impactful endings.'

    fields = [
        {'name': 'concept', 'label': 'Story Concept', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the core concept or conflict of your short story...'},
        {'name': 'setting', 'label': 'Setting', 'type': 'text', 'required': False, 'placeholder': 'e.g., A small coastal town in the 1960s'},
        {'name': 'pov', 'label': 'Point of View', 'type': 'select', 'required': False, 'options': ['First Person', 'Third Person Limited', 'Third Person Omniscient', 'Second Person']},
        {'name': 'theme', 'label': 'Theme', 'type': 'select', 'required': False, 'options': ['Love & Loss', 'Coming of Age', 'Redemption', 'Identity', 'Survival', 'Justice', 'Freedom', 'Betrayal']},
    ]

    system_prompt = (
        'You are an acclaimed short story writer. Write a complete short story (1000-1500 words) based on the concept. '
        'Setting: {setting}. Point of view: {pov}. Theme: {theme}. '
        'Focus on tight pacing, a single central conflict, vivid sensory details, and a memorable ending. '
        'Every sentence should serve the story. Show, do not tell.'
    )


class RomanceStoryGenerator(BaseGenerator):
    slug = 'ai-romance-story-generator'
    name = 'AI Romance Story Generator'
    description = 'Generate heartfelt romance stories with chemistry, tension, and emotional depth.'
    category = 'Creative Writing'
    icon = 'romance'
    meta_title = 'Free AI Romance Story Generator'
    meta_description = 'Generate heartfelt romance stories with chemistry, tension, and emotional depth.'

    fields = [
        {'name': 'scenario', 'label': 'Romance Scenario', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the romantic scenario or how the characters meet...'},
        {'name': 'subgenre', 'label': 'Subgenre', 'type': 'select', 'required': False, 'options': ['Contemporary', 'Historical', 'Paranormal', 'Romantic Comedy', 'Second Chance', 'Enemies to Lovers', 'Friends to Lovers', 'Slow Burn']},
        {'name': 'heat_level', 'label': 'Heat Level', 'type': 'select', 'required': False, 'options': ['Sweet (No explicit content)', 'Warm (Mild romance)', 'Steamy (Fade to black)']},
        {'name': 'setting', 'label': 'Setting', 'type': 'text', 'required': False, 'placeholder': 'e.g., A Parisian bakery, A mountain lodge'},
    ]

    system_prompt = (
        'You are a talented romance writer. Write a captivating romance story based on the scenario. '
        'Subgenre: {subgenre}. Heat level: {heat_level}. Setting: {setting}. '
        'Focus on emotional connection, natural chemistry between characters, meaningful dialogue, '
        'romantic tension, and character development. Build toward a satisfying romantic payoff.'
    )


class HorrorStoryGenerator(BaseGenerator):
    slug = 'ai-horror-story-generator'
    name = 'AI Horror Story Generator'
    description = 'Generate spine-chilling horror stories with atmospheric dread and terrifying twists.'
    category = 'Creative Writing'
    icon = 'horror'
    meta_title = 'Free AI Horror Story Generator'
    meta_description = 'Generate spine-chilling horror stories with atmospheric dread and terrifying twists.'

    fields = [
        {'name': 'premise', 'label': 'Horror Premise', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the horror scenario or what terrifying thing happens...'},
        {'name': 'subgenre', 'label': 'Subgenre', 'type': 'select', 'required': False, 'options': ['Psychological Horror', 'Supernatural', 'Gothic', 'Cosmic Horror', 'Slasher', 'Folk Horror', 'Body Horror', 'Haunted House']},
        {'name': 'atmosphere', 'label': 'Atmosphere', 'type': 'select', 'required': False, 'options': ['Creeping Dread', 'Intense Terror', 'Eerie & Unsettling', 'Dark & Oppressive', 'Paranoid & Claustrophobic']},
    ]

    system_prompt = (
        'You are a master of horror fiction. Write a terrifying horror story based on the premise. '
        'Subgenre: {subgenre}. Atmosphere: {atmosphere}. '
        'Build tension gradually through atmosphere, sensory detail, and pacing. Use foreshadowing, '
        'unreliable perceptions, and the fear of the unknown. Let dread simmer before the reveal. '
        'End with a twist or lingering sense of unease.'
    )


class StoryPromptGenerator(BaseGenerator):
    slug = 'ai-story-prompt-generator'
    name = 'AI Story Prompt Generator'
    description = 'Generate creative and inspiring story prompts to spark your imagination and overcome writer\'s block.'
    category = 'Creative Writing'
    icon = 'prompt'
    meta_title = 'Free AI Story Prompt Generator'
    meta_description = 'Generate creative story prompts to spark your imagination and overcome writer\'s block.'

    fields = [
        {'name': 'preferences', 'label': 'Preferences or Themes', 'type': 'textarea', 'required': True, 'placeholder': 'Describe any themes, genres, or elements you want in the prompts...'},
        {'name': 'genre', 'label': 'Genre', 'type': 'select', 'required': False, 'options': ['Any Genre', 'Fantasy', 'Science Fiction', 'Mystery', 'Horror', 'Romance', 'Literary Fiction', 'Historical Fiction', 'Thriller']},
        {'name': 'count', 'label': 'Number of Prompts', 'type': 'select', 'required': False, 'options': ['3 prompts', '5 prompts', '10 prompts']},
    ]

    system_prompt = (
        'You are a creative writing coach who specializes in generating inspiring story prompts. '
        'Generate {count} unique, creative story prompts based on the user\'s preferences. '
        'Genre focus: {genre}. '
        'Each prompt should include a compelling hook, an interesting character, a setting, and a conflict or mystery. '
        'Make each prompt distinct and detailed enough to spark a full story, but open-ended enough for creative freedom. '
        'Number each prompt clearly.'
    )


class StoryStarterGenerator(BaseGenerator):
    slug = 'ai-story-starter-generator'
    name = 'AI Story Starter Generator'
    description = 'Generate gripping opening paragraphs that hook readers from the first sentence.'
    category = 'Creative Writing'
    icon = 'starter'
    meta_title = 'Free AI Story Starter Generator'
    meta_description = 'Generate gripping opening paragraphs that hook readers from the very first sentence.'

    fields = [
        {'name': 'idea', 'label': 'Story Idea', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your story idea or the world you want to start in...'},
        {'name': 'genre', 'label': 'Genre', 'type': 'select', 'required': False, 'options': ['Fantasy', 'Science Fiction', 'Mystery', 'Horror', 'Romance', 'Thriller', 'Literary Fiction', 'Adventure']},
        {'name': 'style', 'label': 'Opening Style', 'type': 'select', 'required': False, 'options': ['Action Opening', 'Dialogue Opening', 'Description Opening', 'Mystery/Question Opening', 'In Medias Res', 'Character Introduction']},
    ]

    system_prompt = (
        'You are an expert fiction writer who specializes in crafting irresistible story openings. '
        'Generate 3 different opening paragraphs (each 100-200 words) based on the story idea. '
        'Genre: {genre}. Style: {style}. '
        'Each opening should hook the reader immediately, establish voice and tone, hint at conflict, '
        'and make the reader desperate to know what happens next. Label them as Option 1, Option 2, Option 3.'
    )


class PlotGenerator(BaseGenerator):
    slug = 'ai-plot-generator'
    name = 'AI Plot Generator'
    description = 'Generate detailed plot outlines with story structure, turning points, and character arcs.'
    category = 'Creative Writing'
    icon = 'plot'
    meta_title = 'Free AI Plot Generator'
    meta_description = 'Generate detailed plot outlines with story structure, turning points, and character arcs.'

    fields = [
        {'name': 'concept', 'label': 'Story Concept', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your story concept, main characters, or central conflict...'},
        {'name': 'structure', 'label': 'Plot Structure', 'type': 'select', 'required': False, 'options': ['Three-Act Structure', 'Hero\'s Journey', 'Save the Cat', 'Five-Act Structure', 'Freytag\'s Pyramid']},
        {'name': 'genre', 'label': 'Genre', 'type': 'select', 'required': False, 'options': ['Fantasy', 'Science Fiction', 'Mystery', 'Thriller', 'Romance', 'Horror', 'Adventure', 'Literary Fiction']},
        {'name': 'complexity', 'label': 'Plot Complexity', 'type': 'select', 'required': False, 'options': ['Simple (Single plotline)', 'Moderate (Main + subplot)', 'Complex (Multiple interweaving plots)']},
    ]

    system_prompt = (
        'You are a story structure expert and plot architect. Create a detailed plot outline for the given concept. '
        'Structure: {structure}. Genre: {genre}. Complexity: {complexity}. '
        'Include: premise, main characters with motivations, inciting incident, key turning points, '
        'rising action beats, climax, resolution, and character arcs. '
        'Organize the outline according to the chosen structure with clear act/stage labels.'
    )


class CharacterNameGenerator(BaseGenerator):
    slug = 'ai-character-name-generator'
    name = 'AI Character Name Generator'
    description = 'Generate unique, memorable character names that fit your story\'s genre, setting, and tone.'
    category = 'Creative Writing'
    icon = 'character'
    meta_title = 'Free AI Character Name Generator'
    meta_description = 'Generate unique character names that fit your story\'s genre, setting, and tone.'

    fields = [
        {'name': 'description', 'label': 'Character Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the character (personality, role, background, species, etc.)...'},
        {'name': 'genre', 'label': 'Genre/Setting', 'type': 'select', 'required': False, 'options': ['Fantasy/Medieval', 'Science Fiction/Futuristic', 'Contemporary/Modern', 'Historical', 'Mythology', 'Anime/Manga', 'Video Game', 'Superhero']},
        {'name': 'style', 'label': 'Name Style', 'type': 'select', 'required': False, 'options': ['Realistic', 'Exotic/Unique', 'Symbolic (meaning-based)', 'Elegant', 'Tough/Gritty', 'Whimsical/Fun']},
        {'name': 'count', 'label': 'Number of Names', 'type': 'select', 'required': False, 'options': ['5 names', '10 names', '15 names', '20 names']},
    ]

    system_prompt = (
        'You are an expert at creating memorable character names for fiction. Generate {count} unique character names '
        'based on the description. Genre/Setting: {genre}. Name style: {style}. '
        'For each name, provide: the full name, a pronunciation guide if needed, the meaning or origin, '
        'and a brief note on why it suits the character. Organize them in a numbered list.'
    )


class DialogueGenerator(BaseGenerator):
    slug = 'ai-dialogue-generator'
    name = 'AI Dialogue Generator'
    description = 'Generate natural, character-driven dialogue that reveals personality and advances the story.'
    category = 'Creative Writing'
    icon = 'dialogue'
    meta_title = 'Free AI Dialogue Generator'
    meta_description = 'Generate natural, character-driven dialogue that reveals personality and advances the story.'

    fields = [
        {'name': 'scene', 'label': 'Scene Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the scene, characters involved, and what they are discussing...'},
        {'name': 'mood', 'label': 'Mood', 'type': 'select', 'required': False, 'options': ['Tense/Confrontational', 'Romantic/Intimate', 'Humorous/Witty', 'Emotional/Vulnerable', 'Casual/Friendly', 'Mysterious/Cryptic', 'Professional/Formal']},
        {'name': 'format', 'label': 'Format', 'type': 'select', 'required': False, 'options': ['Dialogue with action beats', 'Pure dialogue only', 'Screenplay format', 'Dialogue with internal thoughts']},
    ]

    system_prompt = (
        'You are a master dialogue writer. Write a compelling dialogue scene based on the description. '
        'Mood: {mood}. Format: {format}. '
        'Make each character\'s voice distinct and recognizable. Use subtext and implied meaning. '
        'Include natural speech patterns, interruptions, and pauses where appropriate. '
        'The dialogue should reveal character, create tension or emotion, and move the story forward.'
    )


class PoetryGenerator(BaseGenerator):
    slug = 'ai-poetry-generator'
    name = 'AI Poetry Generator'
    description = 'Generate beautiful poems in various forms with vivid imagery and emotional resonance.'
    category = 'Creative Writing'
    icon = 'poetry'
    meta_title = 'Free AI Poetry Generator'
    meta_description = 'Generate beautiful poems in various forms with vivid imagery and emotional resonance.'

    fields = [
        {'name': 'subject', 'label': 'Subject or Theme', 'type': 'textarea', 'required': True, 'placeholder': 'What should the poem be about? Describe the theme, emotion, or imagery...'},
        {'name': 'form', 'label': 'Poetry Form', 'type': 'select', 'required': False, 'options': ['Free Verse', 'Sonnet', 'Haiku', 'Limerick', 'Ballad', 'Ode', 'Villanelle', 'Acrostic', 'Rhyming Couplets']},
        {'name': 'mood', 'label': 'Mood', 'type': 'select', 'required': False, 'options': ['Romantic', 'Melancholic', 'Joyful', 'Reflective', 'Dark', 'Hopeful', 'Nostalgic', 'Fierce']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (4-8 lines)', 'Medium (12-20 lines)', 'Long (24-40 lines)']},
    ]

    system_prompt = (
        'You are a gifted poet with mastery of all poetic forms. Write a poem on the given subject. '
        'Form: {form}. Mood: {mood}. Length: {length}. '
        'Use vivid imagery, strong metaphors, and precise word choices. Pay attention to rhythm, sound, '
        'and line breaks. If a structured form is chosen, follow its rules faithfully (meter, rhyme scheme, etc.). '
        'The poem should evoke genuine emotion and offer a fresh perspective.'
    )


class SongLyricsGenerator(BaseGenerator):
    slug = 'ai-song-lyrics-generator'
    name = 'AI Song Lyrics Generator'
    description = 'Generate original song lyrics with verses, choruses, and bridges in your chosen style.'
    category = 'Creative Writing'
    icon = 'lyrics'
    meta_title = 'Free AI Song Lyrics Generator'
    meta_description = 'Generate original song lyrics with verses, choruses, and bridges in your chosen style.'

    fields = [
        {'name': 'topic', 'label': 'Song Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What should the song be about? Describe the story, emotion, or message...'},
        {'name': 'genre', 'label': 'Music Genre', 'type': 'select', 'required': False, 'options': ['Pop', 'Rock', 'Country', 'R&B/Soul', 'Folk', 'Indie', 'Blues', 'Electronic/EDM', 'Jazz', 'Gospel']},
        {'name': 'mood', 'label': 'Mood', 'type': 'select', 'required': False, 'options': ['Upbeat & Happy', 'Sad & Emotional', 'Angry & Rebellious', 'Romantic & Tender', 'Nostalgic', 'Empowering', 'Chill & Mellow']},
        {'name': 'structure', 'label': 'Song Structure', 'type': 'select', 'required': False, 'options': ['Verse-Chorus-Verse-Chorus-Bridge-Chorus', 'Verse-Chorus-Verse-Chorus', 'Verse-Pre-Chorus-Chorus (x2)-Bridge-Chorus', 'AABA (Classic)']},
    ]

    system_prompt = (
        'You are a talented songwriter and lyricist. Write original song lyrics on the given topic. '
        'Genre: {genre}. Mood: {mood}. Structure: {structure}. '
        'Include clearly labeled sections (Verse 1, Chorus, Verse 2, Bridge, etc.). '
        'Focus on strong hooks, memorable phrases, natural rhythm and flow, vivid imagery, '
        'and emotional authenticity. Use rhyme naturally without forcing it.'
    )


class RapLyricsGenerator(BaseGenerator):
    slug = 'ai-rap-lyrics-generator'
    name = 'AI Rap Lyrics Generator'
    description = 'Generate original rap lyrics with clever wordplay, rhyme schemes, and hard-hitting bars.'
    category = 'Creative Writing'
    icon = 'rap'
    meta_title = 'Free AI Rap Lyrics Generator'
    meta_description = 'Generate original rap lyrics with clever wordplay, rhyme schemes, and hard-hitting bars.'

    fields = [
        {'name': 'topic', 'label': 'Rap Topic', 'type': 'textarea', 'required': True, 'placeholder': 'What should the rap be about? Describe the theme, story, or message...'},
        {'name': 'style', 'label': 'Style', 'type': 'select', 'required': False, 'options': ['Lyrical/Complex', 'Trap', 'Old School/Boom Bap', 'Conscious/Socially Aware', 'Storytelling', 'Freestyle/Battle Rap', 'Melodic Rap', 'Drill']},
        {'name': 'rhyme_scheme', 'label': 'Rhyme Scheme', 'type': 'select', 'required': False, 'options': ['Simple End Rhymes', 'Multi-Syllabic Rhymes', 'Internal Rhymes', 'Complex/Mixed Schemes']},
        {'name': 'verses', 'label': 'Number of Verses', 'type': 'select', 'required': False, 'options': ['1 Verse (16 bars)', '2 Verses + Hook', '3 Verses + Hook']},
    ]

    system_prompt = (
        'You are an elite rap lyricist and ghostwriter. Write original rap lyrics on the given topic. '
        'Style: {style}. Rhyme scheme: {rhyme_scheme}. Structure: {verses}. '
        'Focus on clever wordplay, punchlines, metaphors, and tight rhyme patterns. '
        'Maintain consistent flow and rhythm. Include clearly labeled sections (Verse, Hook/Chorus). '
        'The bars should have punch and swagger while staying authentic to the chosen style.'
    )


class ScriptGenerator(BaseGenerator):
    slug = 'ai-script-generator'
    name = 'AI Script Generator'
    description = 'Generate professionally formatted scripts for films, TV shows, plays, and web series.'
    category = 'Creative Writing'
    icon = 'script'
    meta_title = 'Free AI Script Generator'
    meta_description = 'Generate professionally formatted scripts for films, TV shows, plays, and web series.'

    fields = [
        {'name': 'concept', 'label': 'Script Concept', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the scene, story, or concept for the script...'},
        {'name': 'format', 'label': 'Script Format', 'type': 'select', 'required': False, 'options': ['Screenplay (Film)', 'TV Script', 'Stage Play', 'Web Series/Short Film', 'Sketch/Comedy']},
        {'name': 'genre', 'label': 'Genre', 'type': 'select', 'required': False, 'options': ['Drama', 'Comedy', 'Thriller/Suspense', 'Action', 'Horror', 'Romance', 'Science Fiction', 'Documentary']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Single Scene (2-3 pages)', 'Short Script (5-10 pages)', 'Act/Episode Outline']},
    ]

    system_prompt = (
        'You are a professional screenwriter and playwright. Write a script based on the given concept. '
        'Format: {format}. Genre: {genre}. Length: {length}. '
        'Use proper industry-standard formatting for the chosen format: scene headings (INT./EXT.), '
        'action lines, character names in caps before dialogue, and parentheticals where needed. '
        'Create distinct character voices, visual storytelling, and dramatic tension. '
        'Show the story through action and dialogue rather than exposition.'
    )


CREATIVE_GENERATORS = [
    StoryGenerator,
    ShortStoryGenerator,
    RomanceStoryGenerator,
    HorrorStoryGenerator,
    StoryPromptGenerator,
    StoryStarterGenerator,
    PlotGenerator,
    CharacterNameGenerator,
    DialogueGenerator,
    PoetryGenerator,
    SongLyricsGenerator,
    RapLyricsGenerator,
    ScriptGenerator,
]
