from ai_tools.generators.base import BaseGenerator


class EmailWriter(BaseGenerator):
    slug = 'ai-email-writer'
    name = 'AI Email Writer'
    description = 'Generate clear, well-structured emails for any occasion — personal, professional, or formal.'
    category = 'Professional Communication'
    icon = 'email'
    meta_title = 'Free AI Email Writer'
    meta_description = 'Generate clear, polished emails for any purpose. Choose your tone, recipient, and let AI craft the perfect message.'

    fields = [
        {'name': 'purpose', 'label': 'Email Purpose', 'type': 'textarea', 'required': True, 'placeholder': 'What is the email about? Describe the situation and what you want to communicate...'},
        {'name': 'recipient', 'label': 'Recipient', 'type': 'text', 'required': False, 'placeholder': 'e.g., Colleague, Friend, Customer, Professor'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Friendly', 'Formal', 'Casual', 'Persuasive', 'Empathetic']},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (3-5 sentences)', 'Medium (1-2 paragraphs)', 'Long (3+ paragraphs)']},
    ]

    system_prompt = (
        'You are an expert email writer. Write a clear, well-structured email for the described purpose. '
        'Recipient: {recipient}. Tone: {tone}. Length: {length}. '
        'Include an appropriate subject line, greeting, well-organized body with a clear call to action, '
        'and a suitable closing. Ensure the message is concise, polite, and achieves the sender\'s goal.'
    )


class LetterGenerator(BaseGenerator):
    slug = 'ai-letter-generator'
    name = 'AI Letter Generator'
    description = 'Generate well-formatted letters for personal, business, or official purposes.'
    category = 'Professional Communication'
    icon = 'letter'
    meta_title = 'Free AI Letter Generator'
    meta_description = 'Create well-formatted letters for any purpose — personal, business, or official. Choose your type and tone.'

    fields = [
        {'name': 'purpose', 'label': 'Letter Purpose', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the purpose of the letter and key points to include...'},
        {'name': 'type', 'label': 'Letter Type', 'type': 'select', 'required': False, 'options': ['Formal Business Letter', 'Personal Letter', 'Official Request', 'Complaint Letter', 'Invitation Letter', 'Congratulations Letter']},
        {'name': 'recipient', 'label': 'Recipient', 'type': 'text', 'required': False, 'placeholder': 'e.g., Hiring Manager, Dear Sir/Madam, a specific name'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Formal', 'Semi-Formal', 'Friendly', 'Respectful', 'Assertive']},
    ]

    system_prompt = (
        'You are an expert letter writer. Write a well-formatted {type} for the described purpose. '
        'Recipient: {recipient}. Tone: {tone}. '
        'Include proper letter formatting: sender address placeholder, date, recipient address, salutation, '
        'well-structured body paragraphs, appropriate closing, and signature line. '
        'Ensure the letter is clear, purposeful, and follows standard conventions for its type.'
    )


class CoverLetterGenerator(BaseGenerator):
    slug = 'ai-cover-letter-generator'
    name = 'AI Cover Letter Generator'
    description = 'Generate compelling cover letters tailored to specific job postings and your experience.'
    category = 'Professional Communication'
    icon = 'cover-letter'
    meta_title = 'Free AI Cover Letter Generator'
    meta_description = 'Create personalized cover letters that highlight your skills and match job requirements.'

    fields = [
        {'name': 'job_title', 'label': 'Job Title', 'type': 'text', 'required': True, 'placeholder': 'e.g., Senior Marketing Manager'},
        {'name': 'company', 'label': 'Company Name', 'type': 'text', 'required': False, 'placeholder': 'e.g., Acme Corporation'},
        {'name': 'experience', 'label': 'Your Relevant Experience', 'type': 'textarea', 'required': True, 'placeholder': 'Summarize your relevant skills, experience, and achievements...'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Enthusiastic', 'Confident', 'Conversational']},
    ]

    system_prompt = (
        'You are an expert career coach and cover letter writer. Write a compelling cover letter for the '
        'position of {job_title} at {company}. Tone: {tone}. '
        'Use the candidate\'s experience to craft a persuasive narrative. Include: an attention-grabbing '
        'opening paragraph, 1-2 body paragraphs connecting skills and achievements to the role\'s requirements, '
        'and a confident closing with a call to action. Avoid generic phrases; be specific and results-oriented.'
    )


class ResumeGenerator(BaseGenerator):
    slug = 'ai-resume-writer'
    name = 'AI Resume Writer'
    description = 'Generate professional resume content with impactful bullet points and clear formatting.'
    category = 'Professional Communication'
    icon = 'resume'
    meta_title = 'Free AI Resume Writer'
    meta_description = 'Create polished resume content with strong action verbs and quantified achievements.'

    fields = [
        {'name': 'target_role', 'label': 'Target Role', 'type': 'text', 'required': True, 'placeholder': 'e.g., Software Engineer, Project Manager'},
        {'name': 'experience', 'label': 'Your Experience & Skills', 'type': 'textarea', 'required': True, 'placeholder': 'List your work history, skills, education, and key achievements...'},
        {'name': 'section', 'label': 'Section to Generate', 'type': 'select', 'required': False, 'options': ['Full Resume', 'Professional Summary', 'Work Experience Bullets', 'Skills Section']},
        {'name': 'level', 'label': 'Career Level', 'type': 'select', 'required': False, 'options': ['Entry Level', 'Mid-Career', 'Senior/Executive', 'Career Changer']},
    ]

    system_prompt = (
        'You are an expert resume writer and career consultant. Generate a {section} for someone targeting '
        'the role of {target_role}. Career level: {level}. '
        'Use strong action verbs, quantify achievements where possible, and tailor content to the target role. '
        'Follow modern resume best practices: concise bullet points, relevant keywords, '
        'results-oriented language, and clean formatting. Avoid personal pronouns.'
    )


class SpeechWriter(BaseGenerator):
    slug = 'ai-speech-writer'
    name = 'AI Speech Writer'
    description = 'Generate engaging speeches for weddings, graduations, business events, and more.'
    category = 'Professional Communication'
    icon = 'speech'
    meta_title = 'Free AI Speech Writer'
    meta_description = 'Create memorable speeches for any occasion — weddings, graduations, business events, and more.'

    fields = [
        {'name': 'occasion', 'label': 'Occasion', 'type': 'select', 'required': True, 'options': ['Wedding Toast', 'Graduation Speech', 'Business Presentation', 'Award Acceptance', 'Eulogy', 'Retirement', 'Motivational', 'Other']},
        {'name': 'details', 'label': 'Key Details & Points', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the occasion, audience, key points, stories, or themes to include...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Short (1-2 minutes)', 'Medium (3-5 minutes)', 'Long (5-10 minutes)']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Heartfelt', 'Humorous', 'Inspirational', 'Formal', 'Casual', 'Emotional']},
    ]

    system_prompt = (
        'You are an expert speechwriter. Write an engaging {occasion} speech. '
        'Length: {length}. Tone: {tone}. '
        'Craft a speech with a compelling opening that hooks the audience, well-structured body with '
        'stories and key messages, and a memorable closing. Use natural spoken language, varied sentence '
        'length, and rhetorical techniques. Include pauses and delivery notes in brackets where appropriate.'
    )


class ThankYouNoteGenerator(BaseGenerator):
    slug = 'ai-thank-you-note-generator'
    name = 'AI Thank You Note Generator'
    description = 'Generate sincere, personalized thank you notes for gifts, interviews, favors, and more.'
    category = 'Professional Communication'
    icon = 'thankyou'
    meta_title = 'Free AI Thank You Note Generator'
    meta_description = 'Create heartfelt thank you notes for any situation — interviews, gifts, hospitality, and more.'

    fields = [
        {'name': 'reason', 'label': 'Reason for Thanks', 'type': 'textarea', 'required': True, 'placeholder': 'What are you thanking them for? Include specific details...'},
        {'name': 'recipient', 'label': 'Recipient', 'type': 'text', 'required': False, 'placeholder': 'e.g., Interviewer, Friend, Client, Teacher'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Warm & Personal', 'Professional', 'Formal', 'Casual & Friendly']},
    ]

    system_prompt = (
        'You are an expert at writing heartfelt thank you notes. Write a sincere thank you note. '
        'Recipient: {recipient}. Tone: {tone}. '
        'Be specific about what you are thankful for, express genuine appreciation, mention the impact '
        'of their kindness or action, and close warmly. Keep it concise but meaningful — avoid generic '
        'or overly effusive language. Make it feel personal and authentic.'
    )


class ApologyLetterGenerator(BaseGenerator):
    slug = 'ai-apology-letter-generator'
    name = 'AI Apology Letter Generator'
    description = 'Generate sincere apology letters that acknowledge mistakes and rebuild trust.'
    category = 'Professional Communication'
    icon = 'apology'
    meta_title = 'Free AI Apology Letter Generator'
    meta_description = 'Create sincere apology letters that take responsibility and offer a path forward.'

    fields = [
        {'name': 'situation', 'label': 'What Happened', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the situation and what went wrong...'},
        {'name': 'recipient', 'label': 'Recipient', 'type': 'text', 'required': False, 'placeholder': 'e.g., Customer, Manager, Friend, Partner'},
        {'name': 'context', 'label': 'Context', 'type': 'select', 'required': False, 'options': ['Professional/Business', 'Personal Relationship', 'Customer Service', 'Formal/Official']},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Sincere & Humble', 'Professional', 'Formal', 'Empathetic']},
    ]

    system_prompt = (
        'You are an expert communicator specializing in conflict resolution. Write a sincere apology letter. '
        'Recipient: {recipient}. Context: {context}. Tone: {tone}. '
        'The letter must: clearly acknowledge the mistake without excuses, take full responsibility, '
        'express genuine empathy for how it affected the recipient, explain steps being taken to prevent '
        'recurrence, and offer a path forward. Avoid deflecting blame or minimizing the impact.'
    )


class RecommendationLetterGenerator(BaseGenerator):
    slug = 'ai-recommendation-letter-generator'
    name = 'AI Recommendation Letter Generator'
    description = 'Generate compelling recommendation letters for jobs, academic programs, and scholarships.'
    category = 'Professional Communication'
    icon = 'recommendation'
    meta_title = 'Free AI Recommendation Letter Generator'
    meta_description = 'Create strong recommendation letters that highlight qualifications and character.'

    fields = [
        {'name': 'candidate', 'label': 'Candidate Name & Role', 'type': 'text', 'required': True, 'placeholder': 'e.g., Jane Smith, Marketing Associate'},
        {'name': 'purpose', 'label': 'Purpose of Recommendation', 'type': 'select', 'required': True, 'options': ['Job Application', 'Graduate School', 'Scholarship', 'Promotion', 'Award Nomination']},
        {'name': 'qualities', 'label': 'Key Qualities & Achievements', 'type': 'textarea', 'required': True, 'placeholder': 'Describe their strengths, achievements, and specific examples of their work...'},
        {'name': 'relationship', 'label': 'Your Relationship', 'type': 'text', 'required': False, 'placeholder': 'e.g., Direct supervisor for 3 years, Professor'},
    ]

    system_prompt = (
        'You are writing a strong recommendation letter for {candidate}. Purpose: {purpose}. '
        'Relationship to candidate: {relationship}. '
        'Write a compelling letter that: establishes credibility of the recommender, provides specific '
        'examples of the candidate\'s achievements and qualities, uses concrete anecdotes rather than '
        'vague praise, compares favorably to peers where appropriate, and gives an enthusiastic '
        'endorsement. Use professional letterhead formatting.'
    )


class FollowUpEmailGenerator(BaseGenerator):
    slug = 'ai-follow-up-email-generator'
    name = 'AI Follow-Up Email Generator'
    description = 'Generate effective follow-up emails after interviews, meetings, proposals, and networking events.'
    category = 'Professional Communication'
    icon = 'followup'
    meta_title = 'Free AI Follow-Up Email Generator'
    meta_description = 'Create professional follow-up emails that keep conversations moving forward.'

    fields = [
        {'name': 'context', 'label': 'What Are You Following Up On?', 'type': 'select', 'required': True, 'options': ['Job Interview', 'Business Meeting', 'Sales Proposal', 'Networking Event', 'Unanswered Email', 'Application Status', 'Other']},
        {'name': 'details', 'label': 'Details', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the original interaction, when it happened, and what you want to achieve with this follow-up...'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Friendly', 'Persistent but Polite', 'Casual']},
    ]

    system_prompt = (
        'You are an expert communicator. Write an effective follow-up email for a {context}. '
        'Tone: {tone}. '
        'Include a clear subject line, reference the original interaction, add value or reiterate interest, '
        'and include a specific call to action. Be concise and respectful of their time. '
        'Strike the right balance between persistence and courtesy — never sound desperate or pushy.'
    )


class ColdEmailGenerator(BaseGenerator):
    slug = 'ai-cold-email-generator'
    name = 'AI Cold Email Generator'
    description = 'Generate persuasive cold emails for outreach, sales, partnerships, and networking.'
    category = 'Professional Communication'
    icon = 'outreach'
    meta_title = 'Free AI Cold Email Generator'
    meta_description = 'Create compelling cold emails that get opened, read, and replied to.'

    fields = [
        {'name': 'goal', 'label': 'Email Goal', 'type': 'select', 'required': True, 'options': ['Sales Outreach', 'Partnership Inquiry', 'Networking/Introduction', 'Guest Post/Collaboration', 'Freelance Pitch', 'Investor Outreach']},
        {'name': 'details', 'label': 'Key Details', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your offering, target audience, value proposition, and what you want the recipient to do...'},
        {'name': 'recipient_type', 'label': 'Recipient Type', 'type': 'text', 'required': False, 'placeholder': 'e.g., CEO of a SaaS startup, Marketing Director, Blogger'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Conversational', 'Direct & Confident', 'Friendly & Warm']},
    ]

    system_prompt = (
        'You are an expert cold email copywriter. Write a compelling cold email for {goal}. '
        'Recipient type: {recipient_type}. Tone: {tone}. '
        'The email must: have an attention-grabbing subject line, open with a personalized hook '
        '(not about the sender), clearly communicate the value proposition within 2-3 sentences, '
        'include social proof or credibility if possible, and end with a low-friction call to action. '
        'Keep it under 150 words. Avoid spammy language, excessive exclamation marks, and cliches.'
    )


PROFESSIONAL_GENERATORS = [
    EmailWriter,
    LetterGenerator,
    CoverLetterGenerator,
    ResumeGenerator,
    SpeechWriter,
    ThankYouNoteGenerator,
    ApologyLetterGenerator,
    RecommendationLetterGenerator,
    FollowUpEmailGenerator,
    ColdEmailGenerator,
]
