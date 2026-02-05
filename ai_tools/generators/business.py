from ai_tools.generators.base import BaseGenerator


class BusinessPlanGenerator(BaseGenerator):
    slug = 'ai-business-plan-generator'
    name = 'AI Business Plan Generator'
    description = 'Generate comprehensive business plans with market analysis, strategy, and financial projections.'
    category = 'Business Writing'
    icon = 'business'
    meta_title = 'Free AI Business Plan Generator'
    meta_description = 'Create professional business plans with market analysis and strategy sections.'

    fields = [
        {'name': 'business', 'label': 'Business Name & Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe your business idea...'},
        {'name': 'industry', 'label': 'Industry', 'type': 'text', 'required': False, 'placeholder': 'e.g., SaaS, Retail, Food & Beverage'},
        {'name': 'section', 'label': 'Section', 'type': 'select', 'required': False, 'options': ['Full Plan', 'Executive Summary', 'Market Analysis', 'Financial Projections', 'Marketing Strategy']},
    ]

    system_prompt = (
        'You are an expert business consultant. Generate a {section} for the described business. '
        'Industry: {industry}. Include relevant details about market opportunity, competitive advantages, '
        'revenue model, and growth strategy. Use professional business language.'
    )


class ProjectProposalGenerator(BaseGenerator):
    slug = 'ai-project-proposal-generator'
    name = 'AI Project Proposal Generator'
    description = 'Create persuasive project proposals with objectives, methodology, and timelines.'
    category = 'Business Writing'
    icon = 'proposal'
    meta_title = 'Free AI Project Proposal Generator'
    meta_description = 'Generate professional project proposals with objectives and timelines.'

    fields = [
        {'name': 'project', 'label': 'Project Description', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the project...'},
        {'name': 'audience', 'label': 'Target Audience', 'type': 'text', 'required': False, 'placeholder': 'Who will read this proposal?'},
        {'name': 'budget', 'label': 'Budget Range', 'type': 'text', 'required': False, 'placeholder': 'e.g., $10,000 - $50,000'},
    ]

    system_prompt = (
        'You are an expert proposal writer. Write a professional project proposal. '
        'Target audience: {audience}. Budget: {budget}. '
        'Include: Executive Summary, Problem Statement, Proposed Solution, Objectives, '
        'Methodology, Timeline, Budget Breakdown, and Expected Outcomes.'
    )


class MeetingNotesGenerator(BaseGenerator):
    slug = 'ai-meeting-notes-generator'
    name = 'AI Meeting Notes Generator'
    description = 'Transform raw meeting notes into organized, professional summaries.'
    category = 'Business Writing'
    icon = 'meeting'
    meta_title = 'Free AI Meeting Notes Generator'
    meta_description = 'Transform raw meeting notes into organized professional summaries.'

    fields = [
        {'name': 'notes', 'label': 'Raw Meeting Notes', 'type': 'textarea', 'required': True, 'placeholder': 'Paste your raw meeting notes or key discussion points...'},
        {'name': 'format', 'label': 'Format', 'type': 'select', 'required': False, 'options': ['Summary', 'Action Items', 'Minutes', 'Full Report']},
    ]

    system_prompt = (
        'You are an expert meeting note organizer. Transform the raw notes into a well-organized {format}. '
        'Include: Date/Attendees (if mentioned), Key Discussion Points, Decisions Made, '
        'Action Items (with owners if mentioned), and Next Steps.'
    )


class ExecutiveSummaryGenerator(BaseGenerator):
    slug = 'ai-executive-summary-generator'
    name = 'AI Executive Summary Generator'
    description = 'Generate concise executive summaries for reports and proposals.'
    category = 'Business Writing'
    icon = 'executive'
    meta_title = 'Free AI Executive Summary Generator'
    meta_description = 'Create concise executive summaries for business reports and proposals.'

    fields = [
        {'name': 'content', 'label': 'Document Content', 'type': 'textarea', 'required': True, 'placeholder': 'Paste the full document or describe the key points...'},
        {'name': 'length', 'label': 'Length', 'type': 'select', 'required': False, 'options': ['Brief (100 words)', 'Standard (250 words)', 'Detailed (500 words)']},
    ]

    system_prompt = (
        'You are an expert business writer. Write an executive summary of the following content. '
        'Target length: {length}. Focus on key findings, recommendations, and bottom-line impact. '
        'Use clear, direct language suitable for C-suite executives.'
    )


class SWOTAnalysisGenerator(BaseGenerator):
    slug = 'ai-swot-analysis-generator'
    name = 'AI SWOT Analysis Generator'
    description = 'Generate comprehensive SWOT analyses for businesses and projects.'
    category = 'Business Writing'
    icon = 'swot'
    meta_title = 'Free AI SWOT Analysis Generator'
    meta_description = 'Create detailed SWOT analyses for businesses, products, and projects.'

    fields = [
        {'name': 'subject', 'label': 'Business/Product', 'type': 'textarea', 'required': True, 'placeholder': 'Describe the business, product, or project to analyze...'},
        {'name': 'industry', 'label': 'Industry', 'type': 'text', 'required': False, 'placeholder': 'e.g., Technology, Healthcare, Retail'},
    ]

    system_prompt = (
        'You are a strategic business analyst. Create a detailed SWOT analysis for the given subject. '
        'Industry: {industry}. For each quadrant (Strengths, Weaknesses, Opportunities, Threats), '
        'provide 4-6 specific, actionable points. End with strategic recommendations.'
    )


class BusinessEmailGenerator(BaseGenerator):
    slug = 'ai-business-email-generator'
    name = 'AI Business Email Generator'
    description = 'Generate professional business emails for any purpose.'
    category = 'Business Writing'
    icon = 'email'
    meta_title = 'Free AI Business Email Generator'
    meta_description = 'Generate professional business emails instantly.'

    fields = [
        {'name': 'purpose', 'label': 'Email Purpose', 'type': 'textarea', 'required': True, 'placeholder': 'What is the email about?'},
        {'name': 'recipient', 'label': 'Recipient', 'type': 'text', 'required': False, 'placeholder': 'e.g., Client, Manager, Team'},
        {'name': 'tone', 'label': 'Tone', 'type': 'select', 'required': False, 'options': ['Professional', 'Friendly', 'Formal', 'Urgent']},
    ]

    system_prompt = (
        'You are an expert business communicator. Write a professional business email. '
        'Recipient: {recipient}. Tone: {tone}. '
        'Include a clear subject line, greeting, well-organized body, call to action, '
        'and professional closing. Be concise and action-oriented.'
    )


class OfferLetterGenerator(BaseGenerator):
    slug = 'ai-offer-letter-generator'
    name = 'AI Offer Letter Generator'
    description = 'Generate professional job offer letters with all essential details.'
    category = 'Business Writing'
    icon = 'letter'
    meta_title = 'Free AI Offer Letter Generator'
    meta_description = 'Create professional job offer letters with compensation and benefits details.'

    fields = [
        {'name': 'position', 'label': 'Job Title', 'type': 'text', 'required': True, 'placeholder': 'e.g., Senior Software Engineer'},
        {'name': 'company', 'label': 'Company Name', 'type': 'text', 'required': True, 'placeholder': 'Your company name'},
        {'name': 'details', 'label': 'Key Details', 'type': 'textarea', 'required': False, 'placeholder': 'Salary, start date, benefits, etc.'},
    ]

    system_prompt = (
        'You are an HR professional. Write a formal job offer letter for the position of {position} '
        'at {company}. Details: {details}. Include: congratulations, position details, compensation, '
        'benefits overview, start date, reporting structure, and acceptance instructions. '
        'Use professional, welcoming language.'
    )


class ResignationLetterGenerator(BaseGenerator):
    slug = 'ai-resignation-letter-generator'
    name = 'AI Resignation Letter Generator'
    description = 'Generate professional resignation letters that maintain good relationships.'
    category = 'Business Writing'
    icon = 'letter'
    meta_title = 'Free AI Resignation Letter Generator'
    meta_description = 'Create professional resignation letters that maintain good relationships.'

    fields = [
        {'name': 'position', 'label': 'Current Position', 'type': 'text', 'required': True, 'placeholder': 'Your current job title'},
        {'name': 'company', 'label': 'Company Name', 'type': 'text', 'required': True, 'placeholder': 'Company name'},
        {'name': 'last_day', 'label': 'Last Working Day', 'type': 'text', 'required': False, 'placeholder': 'e.g., March 15, 2026'},
        {'name': 'reason', 'label': 'Reason (optional)', 'type': 'text', 'required': False, 'placeholder': 'Brief reason for leaving'},
    ]

    system_prompt = (
        'You are a professional writer. Write a respectful resignation letter for {position} at {company}. '
        'Last day: {last_day}. Reason: {reason}. Express gratitude, offer to help with transition, '
        'maintain a positive tone. Keep it brief and professional.'
    )


class JobDescriptionGenerator(BaseGenerator):
    slug = 'ai-job-description-generator'
    name = 'AI Job Description Generator'
    description = 'Generate compelling job descriptions that attract qualified candidates.'
    category = 'Business Writing'
    icon = 'job'
    meta_title = 'Free AI Job Description Generator'
    meta_description = 'Create compelling job descriptions that attract top talent.'

    fields = [
        {'name': 'title', 'label': 'Job Title', 'type': 'text', 'required': True, 'placeholder': 'e.g., Product Manager'},
        {'name': 'company', 'label': 'Company Name', 'type': 'text', 'required': False, 'placeholder': 'Company name'},
        {'name': 'requirements', 'label': 'Key Requirements', 'type': 'textarea', 'required': False, 'placeholder': 'Key skills and experience needed'},
        {'name': 'type', 'label': 'Employment Type', 'type': 'select', 'required': False, 'options': ['Full-time', 'Part-time', 'Contract', 'Remote', 'Hybrid']},
    ]

    system_prompt = (
        'You are an expert HR recruiter. Write a compelling job description for {title} at {company}. '
        'Type: {type}. Requirements: {requirements}. '
        'Include: job summary, responsibilities (6-8), qualifications (required and preferred), '
        'benefits, and an inclusive equal opportunity statement.'
    )


class PerformanceReviewGenerator(BaseGenerator):
    slug = 'ai-performance-review-generator'
    name = 'AI Performance Review Generator'
    description = 'Generate constructive performance reviews with specific feedback.'
    category = 'Business Writing'
    icon = 'review'
    meta_title = 'Free AI Performance Review Generator'
    meta_description = 'Create constructive performance reviews with actionable feedback.'

    fields = [
        {'name': 'employee', 'label': 'Employee Role/Name', 'type': 'text', 'required': True, 'placeholder': 'e.g., Marketing Coordinator'},
        {'name': 'achievements', 'label': 'Key Achievements', 'type': 'textarea', 'required': True, 'placeholder': 'List accomplishments and contributions...'},
        {'name': 'areas', 'label': 'Areas for Growth', 'type': 'textarea', 'required': False, 'placeholder': 'Areas that need improvement...'},
        {'name': 'rating', 'label': 'Overall Rating', 'type': 'select', 'required': False, 'options': ['Exceeds Expectations', 'Meets Expectations', 'Needs Improvement']},
    ]

    system_prompt = (
        'You are an experienced manager writing a performance review. Role: {employee}. '
        'Rating: {rating}. Achievements: {achievements}. Growth areas: {areas}. '
        'Write a balanced, specific review covering: strengths, accomplishments, areas for development, '
        'and SMART goals for the next period. Use constructive, encouraging language.'
    )


BUSINESS_GENERATORS = [
    BusinessPlanGenerator,
    ProjectProposalGenerator,
    MeetingNotesGenerator,
    ExecutiveSummaryGenerator,
    SWOTAnalysisGenerator,
    BusinessEmailGenerator,
    OfferLetterGenerator,
    ResignationLetterGenerator,
    JobDescriptionGenerator,
    PerformanceReviewGenerator,
]
