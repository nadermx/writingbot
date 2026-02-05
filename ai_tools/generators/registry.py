from ai_tools.generators.base import BaseGenerator


CATEGORY_NAMES = {
    'ACADEMIC': 'Academic Writing',
    'BUSINESS': 'Business',
    'MARKETING': 'Marketing',
    'EMAIL': 'Email',
    'SOCIAL_MEDIA': 'Social Media',
    'CREATIVE': 'Creative Writing',
    'PROFESSIONAL': 'Professional',
    'CONTENT_SEO': 'Content & SEO',
    'UTILITY': 'Utility',
    'NEWSLETTERS': 'Newsletters & Events',
    'TECHNICAL': 'Technical',
}


_gen_0 = BaseGenerator()
_gen_0.slug = 'ai-essay-writer'
_gen_0.name = 'AI Essay Writer'
_gen_0.description = 'Generate well-structured essays on any topic with an introduction, body paragraphs, and conclusion.'
_gen_0.category = 'ACADEMIC'
_gen_0.icon = 'M12 2l-7 7-4-4m14-4l-7 7-4-4'
_gen_0.meta_title = 'AI Essay Writer - Free AI Writing Tool | WritingBot.ai'
_gen_0.meta_description = 'Generate well-structured essays on any topic with an introduction, body paragraphs, and conclusion.'
_gen_0.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Enter your essay topic"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Provide details, requirements, or a thesis angle..."}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_0.system_prompt = 'You are an expert academic essay writer. Write a well-structured essay on the given topic. Include a compelling introduction with a clear thesis statement, well-developed body paragraphs with evidence and analysis, and a strong conclusion. Topic: {topic}. Details: {description}. Length: {length}. Audience: {audience}. Output ONLY the essay text with no meta-commentary.'

_gen_1 = BaseGenerator()
_gen_1.slug = 'ai-thesis-statement-generator'
_gen_1.name = 'AI Thesis Statement Generator'
_gen_1.description = 'Create clear, arguable thesis statements for essays and research papers.'
_gen_1.category = 'ACADEMIC'
_gen_1.icon = 'M9 12h6m-3-3v6m5.618-4.016A11.955 11.955 0 0112 2.944'
_gen_1.meta_title = 'AI Thesis Statement Generator - Free AI Writing Tool | WritingBot.ai'
_gen_1.meta_description = 'Create clear, arguable thesis statements for essays and research papers.'
_gen_1.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Enter your paper topic"}, {"name": "position", "label": "Your Position/Argument", "type": "textarea", "required": true, "placeholder": "What is your argument or angle?"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_1.system_prompt = 'You are an academic writing specialist. Generate 3 strong, arguable thesis statements for the given topic and position. Each thesis should be specific, debatable, and suitable for an academic paper. Topic: {topic}. Position: {position}. Audience: {audience}. Return ONLY the numbered thesis statements.'

_gen_2 = BaseGenerator()
_gen_2.slug = 'ai-research-paper-writer'
_gen_2.name = 'AI Research Paper Writer'
_gen_2.description = 'Generate structured research paper drafts with abstract, introduction, literature review, methodology, results, and conclusion.'
_gen_2.category = 'ACADEMIC'
_gen_2.icon = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586'
_gen_2.meta_title = 'AI Research Paper Writer - Free AI Writing Tool | WritingBot.ai'
_gen_2.meta_description = 'Generate structured research paper drafts with abstract, introduction, literature review, methodology, results, and conclusion.'
_gen_2.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Enter your research topic"}, {"name": "research_question", "label": "Research Question", "type": "textarea", "required": true, "placeholder": "What is your main research question?"}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Key terms for the research"}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}]
_gen_2.system_prompt = 'You are an academic research paper writer. Draft a structured research paper on the given topic. Include: Abstract, Introduction with research question, Literature Review context, Methodology approach, Discussion of findings, and Conclusion. Topic: {topic}. Research Question: {research_question}. Keywords: {keywords}. Length: {length}. Output ONLY the paper content.'

_gen_3 = BaseGenerator()
_gen_3.slug = 'ai-conclusion-writer'
_gen_3.name = 'AI Conclusion Writer'
_gen_3.description = 'Write strong conclusions that summarize key points and leave a lasting impression.'
_gen_3.category = 'ACADEMIC'
_gen_3.icon = 'M5 13l4 4L19 7'
_gen_3.meta_title = 'AI Conclusion Writer - Free AI Writing Tool | WritingBot.ai'
_gen_3.meta_description = 'Write strong conclusions that summarize key points and leave a lasting impression.'
_gen_3.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the essay/paper about?"}, {"name": "key_points", "label": "Key Points", "type": "textarea", "required": true, "placeholder": "List the main points to summarize..."}, {"name": "paper_type", "label": "Paper Type", "type": "select", "required": false, "placeholder": "", "options": ["Essay", "Research Paper", "Report", "Article"]}]
_gen_3.system_prompt = 'You are an expert at writing conclusions for academic work. Write a strong conclusion that restates the thesis, summarizes the key points, and provides a compelling closing thought. Topic: {topic}. Key Points: {key_points}. Paper Type: {paper_type}. Output ONLY the conclusion paragraph(s).'

_gen_4 = BaseGenerator()
_gen_4.slug = 'ai-abstract-generator'
_gen_4.name = 'AI Abstract Generator'
_gen_4.description = 'Generate concise, informative abstracts for research papers and academic articles.'
_gen_4.category = 'ACADEMIC'
_gen_4.icon = 'M4 6h16M4 12h16M4 18h7'
_gen_4.meta_title = 'AI Abstract Generator - Free AI Writing Tool | WritingBot.ai'
_gen_4.meta_description = 'Generate concise, informative abstracts for research papers and academic articles.'
_gen_4.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Research paper topic"}, {"name": "summary", "label": "Paper Summary", "type": "textarea", "required": true, "placeholder": "Briefly describe your paper, methods, and findings..."}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Enter keywords separated by commas"}]
_gen_4.system_prompt = 'You are an academic abstract writing specialist. Write a concise abstract (150-250 words) for the research paper described. Include: purpose, methodology, key findings, and conclusions. Topic: {topic}. Summary: {summary}. Keywords: {keywords}. Output ONLY the abstract text.'

_gen_5 = BaseGenerator()
_gen_5.slug = 'ai-discussion-post-generator'
_gen_5.name = 'AI Discussion Post Generator'
_gen_5.description = 'Create thoughtful discussion posts for online courses and academic forums.'
_gen_5.category = 'ACADEMIC'
_gen_5.icon = 'M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9'
_gen_5.meta_title = 'AI Discussion Post Generator - Free AI Writing Tool | WritingBot.ai'
_gen_5.meta_description = 'Create thoughtful discussion posts for online courses and academic forums.'
_gen_5.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Discussion prompt or topic"}, {"name": "prompt_text", "label": "Assignment Prompt", "type": "textarea", "required": true, "placeholder": "Paste the discussion prompt or question..."}, {"name": "word_count", "label": "Word Count", "type": "number", "required": false, "placeholder": "250"}]
_gen_5.system_prompt = 'You are a student crafting a thoughtful academic discussion post. Write a well-reasoned response to the given discussion prompt. Include your perspective supported by reasoning, reference relevant concepts, and end with a question to encourage further discussion. Topic: {topic}. Prompt: {prompt_text}. Target word count: {word_count}. Output ONLY the discussion post.'

_gen_6 = BaseGenerator()
_gen_6.slug = 'ai-case-study-generator'
_gen_6.name = 'AI Case Study Generator'
_gen_6.description = 'Generate detailed case studies for business, academic, or educational purposes.'
_gen_6.category = 'ACADEMIC'
_gen_6.icon = 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1'
_gen_6.meta_title = 'AI Case Study Generator - Free AI Writing Tool | WritingBot.ai'
_gen_6.meta_description = 'Generate detailed case studies for business, academic, or educational purposes.'
_gen_6.fields = [{"name": "subject", "label": "Subject", "type": "text", "required": true, "placeholder": "Subject or company for the case study"}, {"name": "context", "label": "Context", "type": "textarea", "required": true, "placeholder": "Background information and situation..."}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_6.system_prompt = 'You are a case study writer. Create a detailed case study with: Background, Challenge/Problem, Analysis, Solution/Approach, Results/Outcomes, and Key Takeaways. Subject: {subject}. Context: {context}. Industry: {industry}. Audience: {audience}. Output ONLY the case study.'

_gen_7 = BaseGenerator()
_gen_7.slug = 'ai-study-guide-maker'
_gen_7.name = 'AI Study Guide Maker'
_gen_7.description = 'Create comprehensive study guides with key concepts, summaries, and review questions.'
_gen_7.category = 'ACADEMIC'
_gen_7.icon = 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13'
_gen_7.meta_title = 'AI Study Guide Maker - Free AI Writing Tool | WritingBot.ai'
_gen_7.meta_description = 'Create comprehensive study guides with key concepts, summaries, and review questions.'
_gen_7.fields = [{"name": "subject", "label": "Subject", "type": "text", "required": true, "placeholder": "Subject or chapter to study"}, {"name": "material", "label": "Study Material", "type": "textarea", "required": true, "placeholder": "Paste notes, topics, or outline of material to cover..."}, {"name": "exam_type", "label": "Exam Type", "type": "select", "required": false, "placeholder": "", "options": ["Multiple Choice", "Essay", "Mixed", "Final Exam"]}]
_gen_7.system_prompt = 'You are an expert study guide creator. Build a comprehensive study guide covering the given material. Include: Key Concepts with definitions, Summary of important topics, Important formulas/dates/facts, Review Questions with answers, and Study Tips. Subject: {subject}. Material: {material}. Exam Type: {exam_type}. Output ONLY the study guide.'

_gen_8 = BaseGenerator()
_gen_8.slug = 'ai-lesson-plan-generator'
_gen_8.name = 'AI Lesson Plan Generator'
_gen_8.description = 'Create structured lesson plans for educators with objectives, activities, and assessments.'
_gen_8.category = 'ACADEMIC'
_gen_8.icon = 'M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4'
_gen_8.meta_title = 'AI Lesson Plan Generator - Free AI Writing Tool | WritingBot.ai'
_gen_8.meta_description = 'Create structured lesson plans for educators with objectives, activities, and assessments.'
_gen_8.fields = [{"name": "subject", "label": "Subject", "type": "text", "required": true, "placeholder": "Subject and topic for the lesson"}, {"name": "grade_level", "label": "Grade Level", "type": "text", "required": true, "placeholder": "e.g. 5th Grade, High School, College"}, {"name": "duration", "label": "Duration", "type": "text", "required": false, "placeholder": "e.g. 45 minutes, 1 hour"}, {"name": "objectives", "label": "Learning Objectives", "type": "textarea", "required": false, "placeholder": "What should students learn?"}]
_gen_8.system_prompt = 'You are an experienced educator and curriculum designer. Create a detailed lesson plan including: Lesson Title, Grade Level, Duration, Learning Objectives, Materials Needed, Introduction/Hook, Direct Instruction, Guided Practice, Independent Practice, Assessment, and Closure. Subject: {subject}. Grade: {grade_level}. Duration: {duration}. Objectives: {objectives}. Output ONLY the lesson plan.'

_gen_9 = BaseGenerator()
_gen_9.slug = 'ai-quiz-maker'
_gen_9.name = 'AI Quiz Maker'
_gen_9.description = 'Generate quizzes with multiple choice, true/false, and short answer questions.'
_gen_9.category = 'ACADEMIC'
_gen_9.icon = 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3'
_gen_9.meta_title = 'AI Quiz Maker - Free AI Writing Tool | WritingBot.ai'
_gen_9.meta_description = 'Generate quizzes with multiple choice, true/false, and short answer questions.'
_gen_9.fields = [{"name": "subject", "label": "Subject", "type": "text", "required": true, "placeholder": "Subject and topic for the quiz"}, {"name": "num_questions", "label": "Number of Questions", "type": "number", "required": false, "placeholder": "10"}, {"name": "question_types", "label": "Question Types", "type": "select", "required": false, "placeholder": "", "options": ["Multiple Choice", "True/False", "Short Answer", "Mixed"]}, {"name": "difficulty", "label": "Difficulty", "type": "select", "required": false, "placeholder": "", "options": ["Easy", "Medium", "Hard"]}]
_gen_9.system_prompt = 'You are a quiz creator for educational purposes. Generate a quiz with the specified number and type of questions. Include an answer key at the end. Subject: {subject}. Number of questions: {num_questions}. Question types: {question_types}. Difficulty: {difficulty}. Output ONLY the quiz followed by the answer key.'

_gen_10 = BaseGenerator()
_gen_10.slug = 'ai-business-plan-generator'
_gen_10.name = 'AI Business Plan Generator'
_gen_10.description = 'Generate comprehensive business plans with executive summary, market analysis, and financial projections.'
_gen_10.category = 'BUSINESS'
_gen_10.icon = 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2'
_gen_10.meta_title = 'AI Business Plan Generator - Free AI Writing Tool | WritingBot.ai'
_gen_10.meta_description = 'Generate comprehensive business plans with executive summary, market analysis, and financial projections.'
_gen_10.fields = [{"name": "business_name", "label": "Business Name", "type": "text", "required": true, "placeholder": "Your business name"}, {"name": "business_idea", "label": "Business Idea", "type": "textarea", "required": true, "placeholder": "Describe your business idea, products/services..."}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who are your target customers?"}]
_gen_10.system_prompt = 'You are a business strategy consultant. Write a comprehensive business plan including: Executive Summary, Company Description, Market Analysis, Organization & Management, Products/Services, Marketing & Sales Strategy, Financial Projections, and Funding Request. Business: {business_name}. Idea: {business_idea}. Industry: {industry}. Target Market: {audience}. Output ONLY the business plan.'

_gen_11 = BaseGenerator()
_gen_11.slug = 'ai-project-proposal-generator'
_gen_11.name = 'AI Project Proposal Generator'
_gen_11.description = 'Create compelling project proposals with scope, timeline, budget, and deliverables.'
_gen_11.category = 'BUSINESS'
_gen_11.icon = 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2'
_gen_11.meta_title = 'AI Project Proposal Generator - Free AI Writing Tool | WritingBot.ai'
_gen_11.meta_description = 'Create compelling project proposals with scope, timeline, budget, and deliverables.'
_gen_11.fields = [{"name": "project_name", "label": "Project Name", "type": "text", "required": true, "placeholder": "Name of the project"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Describe the project goals, scope, and requirements..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who is this proposal for?"}, {"name": "budget", "label": "Budget Range", "type": "text", "required": false, "placeholder": "e.g. $10,000 - $50,000"}]
_gen_11.system_prompt = 'You are a project management expert. Write a professional project proposal including: Project Overview, Objectives, Scope, Deliverables, Timeline/Milestones, Budget Estimate, Team Requirements, Risk Assessment, and Expected Outcomes. Project: {project_name}. Description: {description}. Audience: {audience}. Budget: {budget}. Output ONLY the proposal.'

_gen_12 = BaseGenerator()
_gen_12.slug = 'ai-executive-summary-generator'
_gen_12.name = 'AI Executive Summary Generator'
_gen_12.description = 'Write concise executive summaries that capture the essence of business documents.'
_gen_12.category = 'BUSINESS'
_gen_12.icon = 'M4 6h16M4 12h8m-8 6h16'
_gen_12.meta_title = 'AI Executive Summary Generator - Free AI Writing Tool | WritingBot.ai'
_gen_12.meta_description = 'Write concise executive summaries that capture the essence of business documents.'
_gen_12.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is this summary about?"}, {"name": "document_content", "label": "Document Content", "type": "textarea", "required": true, "placeholder": "Paste or describe the full document content..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who will read this summary?"}]
_gen_12.system_prompt = 'You are a business writing expert. Write a clear, concise executive summary (1-2 pages) that captures the key points, findings, recommendations, and action items from the provided content. Topic: {topic}. Content: {document_content}. Audience: {audience}. Output ONLY the executive summary.'

_gen_13 = BaseGenerator()
_gen_13.slug = 'ai-meeting-agenda-generator'
_gen_13.name = 'AI Meeting Agenda Generator'
_gen_13.description = 'Create structured meeting agendas with topics, time allocations, and action items.'
_gen_13.category = 'BUSINESS'
_gen_13.icon = 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'
_gen_13.meta_title = 'AI Meeting Agenda Generator - Free AI Writing Tool | WritingBot.ai'
_gen_13.meta_description = 'Create structured meeting agendas with topics, time allocations, and action items.'
_gen_13.fields = [{"name": "meeting_purpose", "label": "Meeting Purpose", "type": "text", "required": true, "placeholder": "What is the meeting about?"}, {"name": "topics", "label": "Topics to Cover", "type": "textarea", "required": true, "placeholder": "List the topics or issues to discuss..."}, {"name": "duration", "label": "Meeting Duration", "type": "text", "required": false, "placeholder": "e.g. 30 minutes, 1 hour"}, {"name": "attendees", "label": "Attendees", "type": "text", "required": false, "placeholder": "e.g. Marketing team, C-suite, All hands"}]
_gen_13.system_prompt = 'You are a meeting facilitator. Create a structured meeting agenda with: Meeting Title, Date/Time placeholder, Attendees, Purpose, Agenda Items with time allocations, Discussion Points, Action Items section, and Next Steps. Purpose: {meeting_purpose}. Topics: {topics}. Duration: {duration}. Attendees: {attendees}. Output ONLY the agenda.'

_gen_14 = BaseGenerator()
_gen_14.slug = 'ai-sop-writer'
_gen_14.name = 'AI SOP Writer'
_gen_14.description = 'Generate standard operating procedures with clear step-by-step instructions.'
_gen_14.category = 'BUSINESS'
_gen_14.icon = 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2'
_gen_14.meta_title = 'AI SOP Writer - Free AI Writing Tool | WritingBot.ai'
_gen_14.meta_description = 'Generate standard operating procedures with clear step-by-step instructions.'
_gen_14.fields = [{"name": "process_name", "label": "Process Name", "type": "text", "required": true, "placeholder": "Name of the process or procedure"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Describe the process in detail..."}, {"name": "department", "label": "Department", "type": "text", "required": false, "placeholder": "e.g. Operations, HR, IT"}]
_gen_14.system_prompt = 'You are a process documentation specialist. Write a detailed Standard Operating Procedure (SOP) including: Title, Purpose, Scope, Responsibilities, Prerequisites, Step-by-Step Procedures with numbered instructions, Safety/Compliance Notes, Related Documents, and Revision History placeholder. Process: {process_name}. Description: {description}. Department: {department}. Output ONLY the SOP document.'

_gen_15 = BaseGenerator()
_gen_15.slug = 'ai-scope-of-work-generator'
_gen_15.name = 'AI Scope of Work Generator'
_gen_15.description = 'Create detailed scope of work documents for projects and contracts.'
_gen_15.category = 'BUSINESS'
_gen_15.icon = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586'
_gen_15.meta_title = 'AI Scope of Work Generator - Free AI Writing Tool | WritingBot.ai'
_gen_15.meta_description = 'Create detailed scope of work documents for projects and contracts.'
_gen_15.fields = [{"name": "project_name", "label": "Project Name", "type": "text", "required": true, "placeholder": "Name of the project"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Describe the project requirements and goals..."}, {"name": "timeline", "label": "Timeline", "type": "text", "required": false, "placeholder": "e.g. 3 months, Q1 2025"}, {"name": "budget", "label": "Budget", "type": "text", "required": false, "placeholder": "e.g. $25,000"}]
_gen_15.system_prompt = 'You are a contract and project management expert. Write a detailed Scope of Work (SOW) including: Project Overview, Objectives, Scope (In-Scope and Out-of-Scope), Deliverables, Timeline/Milestones, Acceptance Criteria, Assumptions, Budget/Payment Terms, and Change Management Process. Project: {project_name}. Description: {description}. Timeline: {timeline}. Budget: {budget}. Output ONLY the SOW.'

_gen_16 = BaseGenerator()
_gen_16.slug = 'ai-memo-writer'
_gen_16.name = 'AI Memo Writer'
_gen_16.description = 'Write clear, professional business memos for internal communication.'
_gen_16.category = 'BUSINESS'
_gen_16.icon = 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z'
_gen_16.meta_title = 'AI Memo Writer - Free AI Writing Tool | WritingBot.ai'
_gen_16.meta_description = 'Write clear, professional business memos for internal communication.'
_gen_16.fields = [{"name": "memo_to", "label": "To", "type": "text", "required": true, "placeholder": "e.g. All Employees, Marketing Team"}, {"name": "memo_subject", "label": "Subject", "type": "text", "required": true, "placeholder": "Subject of the memo"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "What is the memo about? Key information to convey..."}, {"name": "urgency", "label": "Urgency", "type": "select", "required": false, "placeholder": "", "options": ["Normal", "Important", "Urgent"]}]
_gen_16.system_prompt = 'You are a corporate communications writer. Write a professional business memo with: TO, FROM (placeholder), DATE, SUBJECT, Body with clear paragraphs covering the purpose, details/background, action required, and deadline if applicable. To: {memo_to}. Subject: {memo_subject}. Content: {description}. Urgency: {urgency}. Output ONLY the memo.'

_gen_17 = BaseGenerator()
_gen_17.slug = 'ai-status-report-generator'
_gen_17.name = 'AI Status Report Generator'
_gen_17.description = 'Generate professional project status reports with progress updates and metrics.'
_gen_17.category = 'BUSINESS'
_gen_17.icon = 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2z'
_gen_17.meta_title = 'AI Status Report Generator - Free AI Writing Tool | WritingBot.ai'
_gen_17.meta_description = 'Generate professional project status reports with progress updates and metrics.'
_gen_17.fields = [{"name": "project_name", "label": "Project Name", "type": "text", "required": true, "placeholder": "Name of the project"}, {"name": "accomplishments", "label": "Accomplishments", "type": "textarea", "required": true, "placeholder": "What was completed this period?"}, {"name": "in_progress", "label": "In Progress", "type": "textarea", "required": false, "placeholder": "What is currently being worked on?"}, {"name": "blockers", "label": "Blockers/Risks", "type": "textarea", "required": false, "placeholder": "Any issues or risks?"}]
_gen_17.system_prompt = 'You are a project manager. Write a professional status report including: Report Period, Project Name, Overall Status (Green/Yellow/Red), Summary, Accomplishments, In Progress Items, Upcoming Milestones, Risks & Issues, and Next Steps. Project: {project_name}. Accomplishments: {accomplishments}. In Progress: {in_progress}. Blockers: {blockers}. Output ONLY the status report.'

_gen_18 = BaseGenerator()
_gen_18.slug = 'ai-offer-letter-generator'
_gen_18.name = 'AI Offer Letter Generator'
_gen_18.description = 'Create professional job offer letters with compensation details and terms.'
_gen_18.category = 'BUSINESS'
_gen_18.icon = 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'
_gen_18.meta_title = 'AI Offer Letter Generator - Free AI Writing Tool | WritingBot.ai'
_gen_18.meta_description = 'Create professional job offer letters with compensation details and terms.'
_gen_18.fields = [{"name": "candidate_name", "label": "Candidate Name", "type": "text", "required": true, "placeholder": "Full name of the candidate"}, {"name": "job_title", "label": "Job Title", "type": "text", "required": true, "placeholder": "Position being offered"}, {"name": "company", "label": "Company Name", "type": "text", "required": false, "placeholder": "Your company name"}, {"name": "compensation", "label": "Compensation Details", "type": "textarea", "required": true, "placeholder": "Salary, benefits, start date, etc."}]
_gen_18.system_prompt = 'You are an HR professional. Write a professional offer letter including: Company letterhead placeholder, Date, Candidate greeting, Position offered, Start date placeholder, Compensation details, Benefits summary, Employment terms, At-will statement, Acceptance deadline, and Signature lines. Candidate: {candidate_name}. Title: {job_title}. Company: {company}. Compensation: {compensation}. Output ONLY the offer letter.'

_gen_19 = BaseGenerator()
_gen_19.slug = 'ai-job-description-generator'
_gen_19.name = 'AI Job Description Generator'
_gen_19.description = 'Write compelling job descriptions that attract qualified candidates.'
_gen_19.category = 'BUSINESS'
_gen_19.icon = 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2'
_gen_19.meta_title = 'AI Job Description Generator - Free AI Writing Tool | WritingBot.ai'
_gen_19.meta_description = 'Write compelling job descriptions that attract qualified candidates.'
_gen_19.fields = [{"name": "job_title", "label": "Job Title", "type": "text", "required": true, "placeholder": "e.g. Senior Software Engineer"}, {"name": "company", "label": "Company Name", "type": "text", "required": false, "placeholder": "Your company name"}, {"name": "responsibilities", "label": "Key Responsibilities", "type": "textarea", "required": true, "placeholder": "Main duties and responsibilities..."}, {"name": "requirements", "label": "Requirements", "type": "textarea", "required": false, "placeholder": "Required skills, experience, education..."}]
_gen_19.system_prompt = 'You are a talent acquisition specialist. Write a compelling job description including: Job Title, Company Overview, Role Summary, Key Responsibilities, Required Qualifications, Preferred Qualifications, Benefits & Perks, and Equal Opportunity statement. Title: {job_title}. Company: {company}. Responsibilities: {responsibilities}. Requirements: {requirements}. Output ONLY the job description.'

_gen_20 = BaseGenerator()
_gen_20.slug = 'ai-ad-copy-generator'
_gen_20.name = 'AI Ad Copy Generator'
_gen_20.description = 'Create high-converting ad copy for Google Ads, Facebook Ads, and other platforms.'
_gen_20.category = 'MARKETING'
_gen_20.icon = 'M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1'
_gen_20.meta_title = 'AI Ad Copy Generator - Free AI Writing Tool | WritingBot.ai'
_gen_20.meta_description = 'Create high-converting ad copy for Google Ads, Facebook Ads, and other platforms.'
_gen_20.fields = [{"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe the product or service to advertise"}, {"name": "platform", "label": "Ad Platform", "type": "select", "required": false, "placeholder": "", "options": ["Google Ads", "Facebook/Instagram", "LinkedIn", "Twitter/X", "TikTok", "General"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who is the target audience?"}, {"name": "cta", "label": "Call to Action", "type": "text", "required": false, "placeholder": "e.g. Shop Now, Learn More, Sign Up"}]
_gen_20.system_prompt = 'You are an expert advertising copywriter. Write compelling ad copy for the specified platform. Include multiple variations: headlines, descriptions, and calls to action. Optimize for clicks and conversions. Product: {product}. Platform: {platform}. Audience: {audience}. CTA: {cta}. Output ONLY the ad copy variations.'

_gen_21 = BaseGenerator()
_gen_21.slug = 'ai-sales-pitch-generator'
_gen_21.name = 'AI Sales Pitch Generator'
_gen_21.description = 'Generate persuasive sales pitches that highlight value propositions and close deals.'
_gen_21.category = 'MARKETING'
_gen_21.icon = 'M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586'
_gen_21.meta_title = 'AI Sales Pitch Generator - Free AI Writing Tool | WritingBot.ai'
_gen_21.meta_description = 'Generate persuasive sales pitches that highlight value propositions and close deals.'
_gen_21.fields = [{"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe your product or service"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who are you pitching to?"}, {"name": "pain_points", "label": "Pain Points", "type": "textarea", "required": false, "placeholder": "What problems does your product solve?"}, {"name": "usp", "label": "Unique Selling Points", "type": "textarea", "required": false, "placeholder": "What makes your product different?"}]
_gen_21.system_prompt = 'You are a sales expert. Write a persuasive sales pitch that hooks the audience, identifies pain points, presents the solution, highlights unique benefits, addresses objections, and closes with a strong call to action. Product: {product}. Audience: {audience}. Pain Points: {pain_points}. USP: {usp}. Output ONLY the sales pitch.'

_gen_22 = BaseGenerator()
_gen_22.slug = 'ai-product-description-generator'
_gen_22.name = 'AI Product Description Generator'
_gen_22.description = 'Write compelling product descriptions that drive sales and improve SEO.'
_gen_22.category = 'MARKETING'
_gen_22.icon = 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z'
_gen_22.meta_title = 'AI Product Description Generator - Free AI Writing Tool | WritingBot.ai'
_gen_22.meta_description = 'Write compelling product descriptions that drive sales and improve SEO.'
_gen_22.fields = [{"name": "product_name", "label": "Product Name", "type": "text", "required": true, "placeholder": "Name of the product"}, {"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe features, materials, specifications..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "SEO keywords to include"}]
_gen_22.system_prompt = 'You are an e-commerce copywriter. Write a compelling product description that highlights benefits, features, and value. Use sensory language, create desire, and include a subtle call to action. Optimize for SEO with natural keyword placement. Product: {product_name}. Details: {product}. Audience: {audience}. Keywords: {keywords}. Output ONLY the product description.'

_gen_23 = BaseGenerator()
_gen_23.slug = 'ai-slogan-generator'
_gen_23.name = 'AI Slogan Generator'
_gen_23.description = 'Create catchy, memorable slogans for brands, products, and campaigns.'
_gen_23.category = 'MARKETING'
_gen_23.icon = 'M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z'
_gen_23.meta_title = 'AI Slogan Generator - Free AI Writing Tool | WritingBot.ai'
_gen_23.meta_description = 'Create catchy, memorable slogans for brands, products, and campaigns.'
_gen_23.fields = [{"name": "brand_name", "label": "Brand/Product Name", "type": "text", "required": true, "placeholder": "Your brand or product name"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "What does your brand stand for? Key message?"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "num_items", "label": "Number of Slogans", "type": "number", "required": false, "placeholder": "10"}]
_gen_23.system_prompt = 'You are a branding expert and creative copywriter. Generate catchy, memorable slogans for the brand. Each slogan should be short (under 10 words), memorable, and capture the brand essence. Brand: {brand_name}. Description: {description}. Audience: {audience}. Generate {num_items} slogans. Output ONLY the numbered slogans.'

_gen_24 = BaseGenerator()
_gen_24.slug = 'ai-tagline-generator'
_gen_24.name = 'AI Tagline Generator'
_gen_24.description = 'Generate powerful taglines that capture your brand identity in just a few words.'
_gen_24.category = 'MARKETING'
_gen_24.icon = 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z'
_gen_24.meta_title = 'AI Tagline Generator - Free AI Writing Tool | WritingBot.ai'
_gen_24.meta_description = 'Generate powerful taglines that capture your brand identity in just a few words.'
_gen_24.fields = [{"name": "brand_name", "label": "Brand Name", "type": "text", "required": true, "placeholder": "Your brand name"}, {"name": "brand_values", "label": "Brand Values", "type": "textarea", "required": true, "placeholder": "Core values, mission, what you stand for..."}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}, {"name": "num_items", "label": "Number of Taglines", "type": "number", "required": false, "placeholder": "10"}]
_gen_24.system_prompt = 'You are a branding specialist. Create powerful taglines that capture the brand identity. Each tagline should be concise (3-8 words), evocative, and differentiate the brand. Brand: {brand_name}. Values: {brand_values}. Industry: {industry}. Generate {num_items} taglines. Output ONLY the numbered taglines.'

_gen_25 = BaseGenerator()
_gen_25.slug = 'ai-press-release-generator'
_gen_25.name = 'AI Press Release Generator'
_gen_25.description = 'Write professional press releases that get media coverage and attention.'
_gen_25.category = 'MARKETING'
_gen_25.icon = 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7'
_gen_25.meta_title = 'AI Press Release Generator - Free AI Writing Tool | WritingBot.ai'
_gen_25.meta_description = 'Write professional press releases that get media coverage and attention.'
_gen_25.fields = [{"name": "headline", "label": "Headline/Announcement", "type": "text", "required": true, "placeholder": "What are you announcing?"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Full details of the announcement..."}, {"name": "company", "label": "Company Name", "type": "text", "required": false, "placeholder": "Your company name"}, {"name": "contact_info", "label": "Contact Info", "type": "text", "required": false, "placeholder": "PR contact name and email"}]
_gen_25.system_prompt = 'You are a PR professional. Write a press release in AP style including: Headline, Subheadline, Dateline, Lead paragraph (who/what/when/where/why), Body with quotes and details, Boilerplate company description, Contact information, and ### ending. Headline: {headline}. Details: {description}. Company: {company}. Contact: {contact_info}. Output ONLY the press release.'

_gen_26 = BaseGenerator()
_gen_26.slug = 'ai-landing-page-copy-generator'
_gen_26.name = 'AI Landing Page Copy Generator'
_gen_26.description = 'Write high-converting landing page copy with headlines, benefits, and CTAs.'
_gen_26.category = 'MARKETING'
_gen_26.icon = 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5z'
_gen_26.meta_title = 'AI Landing Page Copy Generator - Free AI Writing Tool | WritingBot.ai'
_gen_26.meta_description = 'Write high-converting landing page copy with headlines, benefits, and CTAs.'
_gen_26.fields = [{"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe your product or service"}, {"name": "goal", "label": "Conversion Goal", "type": "select", "required": true, "placeholder": "", "options": ["Sign Up", "Purchase", "Free Trial", "Download", "Contact Us", "Book Demo"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "usp", "label": "Key Benefits", "type": "textarea", "required": false, "placeholder": "Main benefits and selling points..."}]
_gen_26.system_prompt = 'You are a conversion copywriter. Write landing page copy sections including: Hero Headline + Subheadline, Problem/Pain Point section, Solution/Benefits section with bullet points, Social Proof section placeholder, Feature highlights, FAQ section, and strong CTA section. Product: {product}. Goal: {goal}. Audience: {audience}. Benefits: {usp}. Output ONLY the landing page copy sections.'

_gen_27 = BaseGenerator()
_gen_27.slug = 'ai-product-name-generator'
_gen_27.name = 'AI Product Name Generator'
_gen_27.description = 'Generate creative, brandable product names that stand out in the market.'
_gen_27.category = 'MARKETING'
_gen_27.icon = 'M13 10V3L4 14h7v7l9-11h-7z'
_gen_27.meta_title = 'AI Product Name Generator - Free AI Writing Tool | WritingBot.ai'
_gen_27.meta_description = 'Generate creative, brandable product names that stand out in the market.'
_gen_27.fields = [{"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Describe your product, what it does, and who it is for..."}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}, {"name": "style", "label": "Name Style", "type": "select", "required": false, "placeholder": "", "options": ["Modern/Tech", "Classic/Professional", "Fun/Playful", "Luxurious", "Minimalist"]}, {"name": "num_items", "label": "Number of Names", "type": "number", "required": false, "placeholder": "20"}]
_gen_27.system_prompt = 'You are a naming consultant and brand strategist. Generate creative, memorable, and brandable product names. Consider: uniqueness, pronunciation ease, domain availability potential, trademark potential, and emotional resonance. Description: {description}. Industry: {industry}. Style: {style}. Generate {num_items} names with brief explanations. Output ONLY the numbered names with explanations.'

_gen_28 = BaseGenerator()
_gen_28.slug = 'ai-product-launch-generator'
_gen_28.name = 'AI Product Launch Generator'
_gen_28.description = 'Create comprehensive product launch plans with messaging, timeline, and channel strategy.'
_gen_28.category = 'MARKETING'
_gen_28.icon = 'M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122'
_gen_28.meta_title = 'AI Product Launch Generator - Free AI Writing Tool | WritingBot.ai'
_gen_28.meta_description = 'Create comprehensive product launch plans with messaging, timeline, and channel strategy.'
_gen_28.fields = [{"name": "product_name", "label": "Product Name", "type": "text", "required": true, "placeholder": "Name of the product"}, {"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe your product or service"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "launch_date", "label": "Launch Date", "type": "text", "required": false, "placeholder": "e.g. March 2025"}]
_gen_28.system_prompt = 'You are a product marketing manager. Create a comprehensive product launch plan including: Launch Overview, Target Audience, Key Messaging & Positioning, Pre-Launch Activities, Launch Day Plan, Post-Launch Follow-up, Channel Strategy, Content Calendar, KPIs/Success Metrics, and Budget Considerations. Product: {product_name}. Details: {product}. Audience: {audience}. Launch Date: {launch_date}. Output ONLY the launch plan.'

_gen_29 = BaseGenerator()
_gen_29.slug = 'ai-product-promotion-generator'
_gen_29.name = 'AI Product Promotion Generator'
_gen_29.description = 'Generate promotional content and campaign ideas to boost product visibility.'
_gen_29.category = 'MARKETING'
_gen_29.icon = 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2'
_gen_29.meta_title = 'AI Product Promotion Generator - Free AI Writing Tool | WritingBot.ai'
_gen_29.meta_description = 'Generate promotional content and campaign ideas to boost product visibility.'
_gen_29.fields = [{"name": "product_name", "label": "Product Name", "type": "text", "required": true, "placeholder": "Name of the product"}, {"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe your product or service"}, {"name": "channels", "label": "Marketing Channels", "type": "text", "required": false, "placeholder": "e.g. Social media, email, blog"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_29.system_prompt = 'You are a marketing strategist. Create a promotional campaign including: Campaign Theme, Key Messages, Content for each channel (social media posts, email copy, blog outline), Promotional offers/incentives, Timeline, and Success metrics. Product: {product_name}. Details: {product}. Channels: {channels}. Audience: {audience}. Output ONLY the promotional plan.'

_gen_30 = BaseGenerator()
_gen_30.slug = 'ai-discount-promotion-generator'
_gen_30.name = 'AI Discount Promotion Generator'
_gen_30.description = 'Create compelling discount and sale promotional content across channels.'
_gen_30.category = 'MARKETING'
_gen_30.icon = 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2'
_gen_30.meta_title = 'AI Discount Promotion Generator - Free AI Writing Tool | WritingBot.ai'
_gen_30.meta_description = 'Create compelling discount and sale promotional content across channels.'
_gen_30.fields = [{"name": "offer", "label": "Discount/Offer", "type": "text", "required": true, "placeholder": "e.g. 30% off, Buy 1 Get 1 Free"}, {"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe your product or service"}, {"name": "deadline", "label": "Promotion Deadline", "type": "text", "required": false, "placeholder": "e.g. Ends Sunday, Limited time"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_30.system_prompt = 'You are a promotional copywriter. Create compelling discount promotion content including: Email subject lines and body, Social media posts (multiple platforms), Website banner copy, SMS/push notification text, and Urgency-driven CTAs. Offer: {offer}. Product: {product}. Deadline: {deadline}. Audience: {audience}. Output ONLY the promotional content.'

_gen_31 = BaseGenerator()
_gen_31.slug = 'ai-event-promotion-generator'
_gen_31.name = 'AI Event Promotion Generator'
_gen_31.description = 'Generate event promotional materials including invitations, social posts, and email campaigns.'
_gen_31.category = 'MARKETING'
_gen_31.icon = 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5'
_gen_31.meta_title = 'AI Event Promotion Generator - Free AI Writing Tool | WritingBot.ai'
_gen_31.meta_description = 'Generate event promotional materials including invitations, social posts, and email campaigns.'
_gen_31.fields = [{"name": "event_name", "label": "Event Name", "type": "text", "required": true, "placeholder": "Name of the event"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Event details: date, location, speakers, agenda..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who should attend?"}, {"name": "channels", "label": "Promotion Channels", "type": "text", "required": false, "placeholder": "e.g. Email, social media, website"}]
_gen_31.system_prompt = 'You are an event marketing specialist. Create event promotional content including: Event description, Email invitation, Social media posts, Website copy, Countdown messages, and RSVP/Registration CTA. Event: {event_name}. Details: {description}. Audience: {audience}. Channels: {channels}. Output ONLY the promotional content.'

_gen_32 = BaseGenerator()
_gen_32.slug = 'ai-email-writer'
_gen_32.name = 'AI Email Writer'
_gen_32.description = 'Write professional emails for any purpose with the right tone and structure.'
_gen_32.category = 'EMAIL'
_gen_32.icon = 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'
_gen_32.meta_title = 'AI Email Writer - Free AI Writing Tool | WritingBot.ai'
_gen_32.meta_description = 'Write professional emails for any purpose with the right tone and structure.'
_gen_32.fields = [{"name": "purpose", "label": "Email Purpose", "type": "text", "required": true, "placeholder": "e.g. Request a meeting, Follow up on proposal"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Key points to include in the email..."}, {"name": "recipient", "label": "Recipient", "type": "text", "required": false, "placeholder": "e.g. Client, Manager, Team"}]
_gen_32.system_prompt = 'You are a professional email writer. Write a well-structured email with: Subject line, Greeting, Clear purpose in the opening, Body with key details, Call to action, and Professional closing. Purpose: {purpose}. Details: {description}. Recipient: {recipient}. Tone: {tone}. Output ONLY the email including the subject line.'

_gen_33 = BaseGenerator()
_gen_33.slug = 'ai-cold-email-generator'
_gen_33.name = 'AI Cold Email Generator'
_gen_33.description = 'Create compelling cold emails that get opened and drive responses.'
_gen_33.category = 'EMAIL'
_gen_33.icon = 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8'
_gen_33.meta_title = 'AI Cold Email Generator - Free AI Writing Tool | WritingBot.ai'
_gen_33.meta_description = 'Create compelling cold emails that get opened and drive responses.'
_gen_33.fields = [{"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "What are you offering?"}, {"name": "recipient_type", "label": "Recipient Type", "type": "text", "required": true, "placeholder": "e.g. CEOs of SaaS companies, Marketing Directors"}, {"name": "value_prop", "label": "Value Proposition", "type": "textarea", "required": true, "placeholder": "What value do you offer the recipient?"}, {"name": "cta", "label": "Desired Action", "type": "text", "required": false, "placeholder": "e.g. Book a call, Reply for demo"}]
_gen_33.system_prompt = 'You are a cold email specialist with expertise in outbound sales. Write 3 cold email variations that are: personalized, concise (under 150 words each), focused on recipient value, and include a clear low-friction CTA. Product: {product}. Recipient: {recipient_type}. Value: {value_prop}. CTA: {cta}. Output ONLY the 3 email variations with subject lines.'

_gen_34 = BaseGenerator()
_gen_34.slug = 'ai-sales-email-generator'
_gen_34.name = 'AI Sales Email Generator'
_gen_34.description = 'Generate persuasive sales emails that nurture leads and close deals.'
_gen_34.category = 'EMAIL'
_gen_34.icon = 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8'
_gen_34.meta_title = 'AI Sales Email Generator - Free AI Writing Tool | WritingBot.ai'
_gen_34.meta_description = 'Generate persuasive sales emails that nurture leads and close deals.'
_gen_34.fields = [{"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe your product or service"}, {"name": "sales_stage", "label": "Sales Stage", "type": "select", "required": false, "placeholder": "", "options": ["Initial Outreach", "Follow-Up", "Demo Recap", "Proposal", "Closing"]}, {"name": "recipient_info", "label": "Recipient Info", "type": "textarea", "required": false, "placeholder": "What do you know about the prospect?"}, {"name": "offer", "label": "Offer/CTA", "type": "text", "required": false, "placeholder": "What action should they take?"}]
_gen_34.system_prompt = 'You are a sales email expert. Write a persuasive sales email appropriate for the given stage of the sales cycle. Focus on value, address likely objections, and include a compelling CTA. Product: {product}. Stage: {sales_stage}. Recipient Info: {recipient_info}. Offer: {offer}. Tone: {tone}. Output ONLY the email with subject line.'

_gen_35 = BaseGenerator()
_gen_35.slug = 'ai-marketing-email-generator'
_gen_35.name = 'AI Marketing Email Generator'
_gen_35.description = 'Create engaging marketing emails for newsletters, promotions, and campaigns.'
_gen_35.category = 'EMAIL'
_gen_35.icon = 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8'
_gen_35.meta_title = 'AI Marketing Email Generator - Free AI Writing Tool | WritingBot.ai'
_gen_35.meta_description = 'Create engaging marketing emails for newsletters, promotions, and campaigns.'
_gen_35.fields = [{"name": "campaign_type", "label": "Campaign Type", "type": "select", "required": true, "placeholder": "", "options": ["Newsletter", "Promotion", "Product Announcement", "Re-engagement", "Seasonal", "Educational"]}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Key message and details to include..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "cta", "label": "Call to Action", "type": "text", "required": false, "placeholder": "e.g. Shop Now, Read More, Sign Up"}]
_gen_35.system_prompt = 'You are an email marketing expert. Write an engaging marketing email with: Compelling subject line (and a preview text), Eye-catching opening, Body content with clear value, CTA button text, and P.S. line. Campaign: {campaign_type}. Details: {description}. Audience: {audience}. CTA: {cta}. Output ONLY the email.'

_gen_36 = BaseGenerator()
_gen_36.slug = 'ai-follow-up-email-generator'
_gen_36.name = 'AI Follow-Up Email Generator'
_gen_36.description = 'Write effective follow-up emails that keep conversations moving forward.'
_gen_36.category = 'EMAIL'
_gen_36.icon = 'M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6'
_gen_36.meta_title = 'AI Follow-Up Email Generator - Free AI Writing Tool | WritingBot.ai'
_gen_36.meta_description = 'Write effective follow-up emails that keep conversations moving forward.'
_gen_36.fields = [{"name": "context", "label": "Original Context", "type": "textarea", "required": true, "placeholder": "What was the original email/meeting about?"}, {"name": "follow_up_reason", "label": "Follow-Up Reason", "type": "text", "required": true, "placeholder": "e.g. No response after proposal, Post-meeting recap"}, {"name": "days_since", "label": "Days Since Last Contact", "type": "number", "required": false, "placeholder": "3"}]
_gen_36.system_prompt = 'You are an expert at writing follow-up emails. Write a polite, professional follow-up that references the previous interaction, provides additional value, and includes a clear next step. Avoid being pushy. Context: {context}. Reason: {follow_up_reason}. Days since contact: {days_since}. Tone: {tone}. Output ONLY the email with subject line.'

_gen_37 = BaseGenerator()
_gen_37.slug = 'ai-welcome-email-generator'
_gen_37.name = 'AI Welcome Email Generator'
_gen_37.description = 'Create warm, engaging welcome emails for new subscribers and customers.'
_gen_37.category = 'EMAIL'
_gen_37.icon = 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636'
_gen_37.meta_title = 'AI Welcome Email Generator - Free AI Writing Tool | WritingBot.ai'
_gen_37.meta_description = 'Create warm, engaging welcome emails for new subscribers and customers.'
_gen_37.fields = [{"name": "brand_name", "label": "Brand Name", "type": "text", "required": true, "placeholder": "Your brand or company name"}, {"name": "welcome_type", "label": "Welcome Type", "type": "select", "required": true, "placeholder": "", "options": ["New Subscriber", "New Customer", "New User/Sign Up", "New Member", "New Employee"]}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "What should the welcome email include? Key info, next steps, resources..."}, {"name": "cta", "label": "Primary CTA", "type": "text", "required": false, "placeholder": "e.g. Get Started, Explore Features"}]
_gen_37.system_prompt = 'You are a customer experience copywriter. Write a warm, engaging welcome email that makes the recipient feel valued. Include: Warm greeting, What to expect, Quick start guide or key resources, Primary CTA, and Contact/support info. Brand: {brand_name}. Type: {welcome_type}. Details: {description}. CTA: {cta}. Output ONLY the email with subject line.'

_gen_38 = BaseGenerator()
_gen_38.slug = 'ai-outreach-email-generator'
_gen_38.name = 'AI Outreach Email Generator'
_gen_38.description = 'Craft professional outreach emails for partnerships, collaborations, and networking.'
_gen_38.category = 'EMAIL'
_gen_38.icon = 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857'
_gen_38.meta_title = 'AI Outreach Email Generator - Free AI Writing Tool | WritingBot.ai'
_gen_38.meta_description = 'Craft professional outreach emails for partnerships, collaborations, and networking.'
_gen_38.fields = [{"name": "purpose", "label": "Outreach Purpose", "type": "select", "required": true, "placeholder": "", "options": ["Partnership", "Guest Post", "Collaboration", "Sponsorship", "Interview Request", "Link Building", "Influencer Outreach"]}, {"name": "recipient_info", "label": "Recipient Info", "type": "textarea", "required": true, "placeholder": "Who are you reaching out to? What do they do?"}, {"name": "your_offer", "label": "What You Offer", "type": "textarea", "required": true, "placeholder": "What value do you bring to this partnership?"}]
_gen_38.system_prompt = 'You are a business development and outreach specialist. Write a professional outreach email that is personalized, respectful of their time, clearly states mutual value, and has a specific ask. Purpose: {purpose}. Recipient: {recipient_info}. Your offer: {your_offer}. Tone: {tone}. Output ONLY the email with subject line.'

_gen_39 = BaseGenerator()
_gen_39.slug = 'ai-cold-outreach-generator'
_gen_39.name = 'AI Cold Outreach Generator'
_gen_39.description = 'Generate multi-touch cold outreach sequences for B2B sales and business development.'
_gen_39.category = 'EMAIL'
_gen_39.icon = 'M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9'
_gen_39.meta_title = 'AI Cold Outreach Generator - Free AI Writing Tool | WritingBot.ai'
_gen_39.meta_description = 'Generate multi-touch cold outreach sequences for B2B sales and business development.'
_gen_39.fields = [{"name": "product", "label": "Product/Service", "type": "textarea", "required": true, "placeholder": "Describe your product or service"}, {"name": "icp", "label": "Ideal Customer Profile", "type": "textarea", "required": true, "placeholder": "Describe your ideal customer: role, company size, industry..."}, {"name": "pain_points", "label": "Pain Points You Solve", "type": "textarea", "required": true, "placeholder": "What problems do you solve for them?"}, {"name": "sequence_length", "label": "Number of Emails", "type": "number", "required": false, "placeholder": "5"}]
_gen_39.system_prompt = 'You are a B2B outreach specialist. Create a multi-email outreach sequence with varied approaches (value-first, social proof, pain point, breakup email). Each email should be under 120 words, personalized, and have a clear CTA. Product: {product}. ICP: {icp}. Pain Points: {pain_points}. Sequence length: {sequence_length}. Output ONLY the email sequence with subject lines.'

_gen_40 = BaseGenerator()
_gen_40.slug = 'ai-social-media-post-generator'
_gen_40.name = 'AI Social Media Post Generator'
_gen_40.description = 'Create engaging social media posts optimized for any platform.'
_gen_40.category = 'SOCIAL_MEDIA'
_gen_40.icon = 'M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342'
_gen_40.meta_title = 'AI Social Media Post Generator - Free AI Writing Tool | WritingBot.ai'
_gen_40.meta_description = 'Create engaging social media posts optimized for any platform.'
_gen_40.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the post about?"}, {"name": "platform", "label": "Platform", "type": "select", "required": true, "placeholder": "", "options": ["Instagram", "Facebook", "Twitter/X", "LinkedIn", "TikTok", "Pinterest", "General"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "post_type", "label": "Post Type", "type": "select", "required": false, "placeholder": "", "options": ["Informational", "Promotional", "Engagement", "Inspirational", "Behind-the-scenes", "Educational"]}]
_gen_40.system_prompt = 'You are a social media content creator. Write an engaging post optimized for the specified platform. Include appropriate length, hashtags, emojis, and formatting for the platform. Topic: {topic}. Platform: {platform}. Audience: {audience}. Post Type: {post_type}. Tone: {tone}. Output ONLY the post content ready to copy-paste.'

_gen_41 = BaseGenerator()
_gen_41.slug = 'ai-instagram-caption-generator'
_gen_41.name = 'AI Instagram Caption Generator'
_gen_41.description = 'Write scroll-stopping Instagram captions with hashtags and CTAs.'
_gen_41.category = 'SOCIAL_MEDIA'
_gen_41.icon = 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14'
_gen_41.meta_title = 'AI Instagram Caption Generator - Free AI Writing Tool | WritingBot.ai'
_gen_41.meta_description = 'Write scroll-stopping Instagram captions with hashtags and CTAs.'
_gen_41.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the photo/post about?"}, {"name": "vibe", "label": "Vibe", "type": "select", "required": false, "placeholder": "", "options": ["Fun/Casual", "Inspirational", "Informative", "Promotional", "Storytelling", "Aesthetic"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "include_hashtags", "label": "Include Hashtags", "type": "select", "required": false, "placeholder": "", "options": ["Yes", "No"]}]
_gen_41.system_prompt = 'You are an Instagram content specialist. Write an engaging Instagram caption that stops the scroll. Include: Hook in the first line, Engaging body content, Call to action, and relevant hashtags (if requested). Topic: {topic}. Vibe: {vibe}. Audience: {audience}. Hashtags: {include_hashtags}. Output ONLY the caption.'

_gen_42 = BaseGenerator()
_gen_42.slug = 'ai-instagram-bio-generator'
_gen_42.name = 'AI Instagram Bio Generator'
_gen_42.description = 'Create compelling Instagram bios that convert profile visitors into followers.'
_gen_42.category = 'SOCIAL_MEDIA'
_gen_42.icon = 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
_gen_42.meta_title = 'AI Instagram Bio Generator - Free AI Writing Tool | WritingBot.ai'
_gen_42.meta_description = 'Create compelling Instagram bios that convert profile visitors into followers.'
_gen_42.fields = [{"name": "name_field", "label": "Name/Brand", "type": "text", "required": true, "placeholder": "Your name or brand name"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "What do you do? What are you known for?"}, {"name": "style", "label": "Bio Style", "type": "select", "required": false, "placeholder": "", "options": ["Professional", "Creative", "Minimal", "Fun", "Bold"]}, {"name": "num_items", "label": "Number of Variations", "type": "number", "required": false, "placeholder": "5"}]
_gen_42.system_prompt = 'You are a social media branding expert. Create Instagram bio variations (max 150 characters each) that communicate who the person/brand is, what they offer, and include a call to action. Use line breaks, emojis strategically, and make every character count. Name: {name_field}. About: {description}. Style: {style}. Generate {num_items} variations. Output ONLY the numbered bio variations.'

_gen_43 = BaseGenerator()
_gen_43.slug = 'ai-linkedin-summary-generator'
_gen_43.name = 'AI LinkedIn Summary Generator'
_gen_43.description = 'Write professional LinkedIn summary/about sections that attract recruiters and connections.'
_gen_43.category = 'SOCIAL_MEDIA'
_gen_43.icon = 'M16 7a4 4 0 11-8 0 4 4 0 018 0z'
_gen_43.meta_title = 'AI LinkedIn Summary Generator - Free AI Writing Tool | WritingBot.ai'
_gen_43.meta_description = 'Write professional LinkedIn summary/about sections that attract recruiters and connections.'
_gen_43.fields = [{"name": "job_title", "label": "Current Job Title", "type": "text", "required": true, "placeholder": "e.g. Senior Marketing Manager"}, {"name": "experience", "label": "Experience & Skills", "type": "textarea", "required": true, "placeholder": "Key experience, achievements, and skills..."}, {"name": "goals", "label": "Professional Goals", "type": "textarea", "required": false, "placeholder": "What are you looking for? Career goals?"}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}]
_gen_43.system_prompt = 'You are a LinkedIn profile optimization specialist. Write a compelling LinkedIn About section that tells a professional story, highlights key achievements, demonstrates expertise, and ends with a call to connect. Use first person. Title: {job_title}. Experience: {experience}. Goals: {goals}. Industry: {industry}. Output ONLY the LinkedIn summary.'

_gen_44 = BaseGenerator()
_gen_44.slug = 'ai-youtube-description-generator'
_gen_44.name = 'AI YouTube Description Generator'
_gen_44.description = 'Write SEO-optimized YouTube video descriptions that boost views and engagement.'
_gen_44.category = 'SOCIAL_MEDIA'
_gen_44.icon = 'M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z'
_gen_44.meta_title = 'AI YouTube Description Generator - Free AI Writing Tool | WritingBot.ai'
_gen_44.meta_description = 'Write SEO-optimized YouTube video descriptions that boost views and engagement.'
_gen_44.fields = [{"name": "video_title", "label": "Video Title", "type": "text", "required": true, "placeholder": "Title of your YouTube video"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "What is the video about? Key topics covered..."}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "SEO keywords to target"}, {"name": "links", "label": "Links to Include", "type": "textarea", "required": false, "placeholder": "Social media links, website, resources mentioned..."}]
_gen_44.system_prompt = 'You are a YouTube SEO specialist. Write an optimized video description including: Compelling first 2 lines (shown in search), Detailed video summary with timestamps placeholder, Relevant keywords naturally placed, Call to action (subscribe, like, comment), Related links section, and Hashtags. Video: {video_title}. About: {description}. Keywords: {keywords}. Links: {links}. Output ONLY the description.'

_gen_45 = BaseGenerator()
_gen_45.slug = 'ai-tiktok-script-generator'
_gen_45.name = 'AI TikTok Script Generator'
_gen_45.description = 'Create viral TikTok video scripts with hooks, content, and calls to action.'
_gen_45.category = 'SOCIAL_MEDIA'
_gen_45.icon = 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5'
_gen_45.meta_title = 'AI TikTok Script Generator - Free AI Writing Tool | WritingBot.ai'
_gen_45.meta_description = 'Create viral TikTok video scripts with hooks, content, and calls to action.'
_gen_45.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the TikTok about?"}, {"name": "style", "label": "Video Style", "type": "select", "required": false, "placeholder": "", "options": ["Educational", "Comedy/Skit", "Story Time", "Tutorial", "Trend", "Day in the Life", "Product Review"]}, {"name": "duration", "label": "Duration", "type": "select", "required": false, "placeholder": "", "options": ["15 seconds", "30 seconds", "60 seconds", "3 minutes"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_45.system_prompt = 'You are a TikTok content creator who understands virality. Write a TikTok script with: Strong hook (first 3 seconds), Engaging body content with visual/action cues, Retention techniques, and CTA. Include [VISUAL] and [TEXT OVERLAY] cues. Topic: {topic}. Style: {style}. Duration: {duration}. Audience: {audience}. Output ONLY the script.'

_gen_46 = BaseGenerator()
_gen_46.slug = 'ai-caption-generator'
_gen_46.name = 'AI Caption Generator'
_gen_46.description = 'Generate engaging captions for photos and social media posts across all platforms.'
_gen_46.category = 'SOCIAL_MEDIA'
_gen_46.icon = 'M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8'
_gen_46.meta_title = 'AI Caption Generator - Free AI Writing Tool | WritingBot.ai'
_gen_46.meta_description = 'Generate engaging captions for photos and social media posts across all platforms.'
_gen_46.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the photo/content about?"}, {"name": "platform", "label": "Platform", "type": "select", "required": false, "placeholder": "", "options": ["Instagram", "Facebook", "Twitter/X", "LinkedIn", "Pinterest", "General"]}, {"name": "mood", "label": "Mood", "type": "select", "required": false, "placeholder": "", "options": ["Happy", "Inspirational", "Funny", "Thoughtful", "Adventurous", "Romantic", "Professional"]}, {"name": "num_items", "label": "Number of Captions", "type": "number", "required": false, "placeholder": "5"}]
_gen_46.system_prompt = 'You are a social media copywriter. Generate engaging captions suited for the platform and mood. Vary the style, length, and approach. Include relevant emojis and hashtags where appropriate. Topic: {topic}. Platform: {platform}. Mood: {mood}. Generate {num_items} captions. Output ONLY the numbered captions.'

_gen_47 = BaseGenerator()
_gen_47.slug = 'ai-hashtag-generator'
_gen_47.name = 'AI Hashtag Generator'
_gen_47.description = 'Generate relevant, trending hashtags to maximize reach on social media.'
_gen_47.category = 'SOCIAL_MEDIA'
_gen_47.icon = 'M7 20l4-16m2 16l4-16M6 9h14M4 15h14'
_gen_47.meta_title = 'AI Hashtag Generator - Free AI Writing Tool | WritingBot.ai'
_gen_47.meta_description = 'Generate relevant, trending hashtags to maximize reach on social media.'
_gen_47.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is your post about?"}, {"name": "platform", "label": "Platform", "type": "select", "required": false, "placeholder": "", "options": ["Instagram", "TikTok", "Twitter/X", "LinkedIn", "YouTube", "General"]}, {"name": "niche", "label": "Niche/Industry", "type": "text", "required": false, "placeholder": "e.g. Fitness, Tech, Food, Fashion"}, {"name": "num_items", "label": "Number of Hashtags", "type": "number", "required": false, "placeholder": "30"}]
_gen_47.system_prompt = 'You are a social media growth strategist. Generate a mix of hashtags: popular (high reach), niche-specific (medium reach), and long-tail (low competition). Group them by category. Topic: {topic}. Platform: {platform}. Niche: {niche}. Generate {num_items} hashtags. Output ONLY the hashtags grouped by category.'

_gen_48 = BaseGenerator()
_gen_48.slug = 'ai-bio-generator'
_gen_48.name = 'AI Bio Generator'
_gen_48.description = 'Write professional and personal bios for websites, social media, and speaker profiles.'
_gen_48.category = 'SOCIAL_MEDIA'
_gen_48.icon = 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
_gen_48.meta_title = 'AI Bio Generator - Free AI Writing Tool | WritingBot.ai'
_gen_48.meta_description = 'Write professional and personal bios for websites, social media, and speaker profiles.'
_gen_48.fields = [{"name": "name_field", "label": "Full Name", "type": "text", "required": true, "placeholder": "Your full name"}, {"name": "role", "label": "Role/Title", "type": "text", "required": true, "placeholder": "e.g. CEO, Author, Software Engineer"}, {"name": "achievements", "label": "Key Achievements", "type": "textarea", "required": true, "placeholder": "Notable accomplishments, experience, education..."}, {"name": "bio_type", "label": "Bio Type", "type": "select", "required": false, "placeholder": "", "options": ["Professional Website", "Speaker/Conference", "Social Media", "Author", "Company Team Page"]}]
_gen_48.system_prompt = 'You are a professional bio writer. Write a polished bio in third person that highlights the person\'s role, achievements, expertise, and personality. Adjust length and style for the specified type. Name: {name_field}. Role: {role}. Achievements: {achievements}. Type: {bio_type}. Tone: {tone}. Output ONLY the bio.'

_gen_49 = BaseGenerator()
_gen_49.slug = 'ai-short-bio-generator'
_gen_49.name = 'AI Short Bio Generator'
_gen_49.description = 'Create concise 2-3 sentence bios perfect for social profiles and author bylines.'
_gen_49.category = 'SOCIAL_MEDIA'
_gen_49.icon = 'M16 7a4 4 0 11-8 0 4 4 0 018 0z'
_gen_49.meta_title = 'AI Short Bio Generator - Free AI Writing Tool | WritingBot.ai'
_gen_49.meta_description = 'Create concise 2-3 sentence bios perfect for social profiles and author bylines.'
_gen_49.fields = [{"name": "name_field", "label": "Full Name", "type": "text", "required": true, "placeholder": "Your full name"}, {"name": "role", "label": "Role/Title", "type": "text", "required": true, "placeholder": "e.g. Marketing Director at Acme Corp"}, {"name": "interests", "label": "Key Focus/Interests", "type": "text", "required": false, "placeholder": "e.g. AI, sustainability, leadership"}, {"name": "num_items", "label": "Number of Variations", "type": "number", "required": false, "placeholder": "5"}]
_gen_49.system_prompt = 'You are a concise bio writer. Write short bios (2-3 sentences max) that pack a punch. Include who they are, what they do, and one memorable detail. Name: {name_field}. Role: {role}. Interests: {interests}. Generate {num_items} variations. Output ONLY the numbered bios.'

_gen_50 = BaseGenerator()
_gen_50.slug = 'ai-story-generator'
_gen_50.name = 'AI Story Generator'
_gen_50.description = 'Generate creative stories with compelling characters, plots, and vivid settings.'
_gen_50.category = 'CREATIVE'
_gen_50.icon = 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13'
_gen_50.meta_title = 'AI Story Generator - Free AI Writing Tool | WritingBot.ai'
_gen_50.meta_description = 'Generate creative stories with compelling characters, plots, and vivid settings.'
_gen_50.fields = [{"name": "genre", "label": "Genre", "type": "select", "required": true, "placeholder": "", "options": ["Fantasy", "Sci-Fi", "Mystery", "Thriller", "Romance", "Adventure", "Drama", "Historical Fiction", "Comedy"]}, {"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Story premise or starting point"}, {"name": "characters", "label": "Characters", "type": "textarea", "required": false, "placeholder": "Describe main characters..."}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}]
_gen_50.system_prompt = 'You are a creative fiction writer. Write an engaging story in the specified genre. Include vivid descriptions, compelling characters, dialogue, conflict, and resolution. Genre: {genre}. Premise: {topic}. Characters: {characters}. Length: {length}. Output ONLY the story.'

_gen_51 = BaseGenerator()
_gen_51.slug = 'ai-short-story-generator'
_gen_51.name = 'AI Short Story Generator'
_gen_51.description = 'Create complete short stories with narrative arc, tension, and satisfying endings.'
_gen_51.category = 'CREATIVE'
_gen_51.icon = 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5'
_gen_51.meta_title = 'AI Short Story Generator - Free AI Writing Tool | WritingBot.ai'
_gen_51.meta_description = 'Create complete short stories with narrative arc, tension, and satisfying endings.'
_gen_51.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Story idea or prompt"}, {"name": "genre", "label": "Genre", "type": "select", "required": false, "placeholder": "", "options": ["Literary Fiction", "Sci-Fi", "Fantasy", "Horror", "Romance", "Mystery", "Slice of Life"]}, {"name": "word_target", "label": "Target Word Count", "type": "number", "required": false, "placeholder": "1000"}, {"name": "pov", "label": "Point of View", "type": "select", "required": false, "placeholder": "", "options": ["First Person", "Third Person Limited", "Third Person Omniscient", "Second Person"]}]
_gen_51.system_prompt = 'You are a short story author. Write a complete short story with a clear beginning, rising action, climax, and resolution. Focus on strong prose, sensory details, and emotional resonance. Idea: {topic}. Genre: {genre}. Target words: {word_target}. POV: {pov}. Output ONLY the story.'

_gen_52 = BaseGenerator()
_gen_52.slug = 'ai-horror-story-generator'
_gen_52.name = 'AI Horror Story Generator'
_gen_52.description = 'Write spine-chilling horror stories that build suspense and deliver scares.'
_gen_52.category = 'CREATIVE'
_gen_52.icon = 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707'
_gen_52.meta_title = 'AI Horror Story Generator - Free AI Writing Tool | WritingBot.ai'
_gen_52.meta_description = 'Write spine-chilling horror stories that build suspense and deliver scares.'
_gen_52.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Horror premise or setting"}, {"name": "subgenre", "label": "Horror Subgenre", "type": "select", "required": false, "placeholder": "", "options": ["Psychological", "Supernatural", "Gothic", "Cosmic Horror", "Slasher", "Folk Horror", "Body Horror", "Haunted House"]}, {"name": "scare_level", "label": "Intensity", "type": "select", "required": false, "placeholder": "", "options": ["Creepy/Subtle", "Moderate", "Intense/Graphic"]}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}]
_gen_52.system_prompt = 'You are a horror fiction writer. Write a chilling horror story that builds dread, creates atmosphere, and delivers effective scares. Use pacing, sensory details, and the unknown to create fear. Premise: {topic}. Subgenre: {subgenre}. Intensity: {scare_level}. Length: {length}. Output ONLY the story.'

_gen_53 = BaseGenerator()
_gen_53.slug = 'ai-romance-story-generator'
_gen_53.name = 'AI Romance Story Generator'
_gen_53.description = 'Create heartfelt romance stories with chemistry, tension, and emotional depth.'
_gen_53.category = 'CREATIVE'
_gen_53.icon = 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682'
_gen_53.meta_title = 'AI Romance Story Generator - Free AI Writing Tool | WritingBot.ai'
_gen_53.meta_description = 'Create heartfelt romance stories with chemistry, tension, and emotional depth.'
_gen_53.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Romance premise or meet-cute idea"}, {"name": "subgenre", "label": "Subgenre", "type": "select", "required": false, "placeholder": "", "options": ["Contemporary", "Historical", "Romantic Comedy", "Slow Burn", "Second Chance", "Enemies to Lovers", "Friends to Lovers"]}, {"name": "characters", "label": "Main Characters", "type": "textarea", "required": false, "placeholder": "Describe the love interests..."}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}]
_gen_53.system_prompt = 'You are a romance fiction writer. Write a heartfelt romance story with compelling chemistry between characters, emotional tension, believable dialogue, and satisfying romantic progression. Premise: {topic}. Subgenre: {subgenre}. Characters: {characters}. Length: {length}. Output ONLY the story.'

_gen_54 = BaseGenerator()
_gen_54.slug = 'ai-plot-generator'
_gen_54.name = 'AI Plot Generator'
_gen_54.description = 'Generate unique story plots with conflict, twists, and narrative structure.'
_gen_54.category = 'CREATIVE'
_gen_54.icon = 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7'
_gen_54.meta_title = 'AI Plot Generator - Free AI Writing Tool | WritingBot.ai'
_gen_54.meta_description = 'Generate unique story plots with conflict, twists, and narrative structure.'
_gen_54.fields = [{"name": "genre", "label": "Genre", "type": "select", "required": true, "placeholder": "", "options": ["Fantasy", "Sci-Fi", "Mystery", "Thriller", "Romance", "Literary", "Horror", "Adventure", "Comedy"]}, {"name": "themes", "label": "Themes", "type": "text", "required": false, "placeholder": "e.g. Redemption, power, identity, love"}, {"name": "num_items", "label": "Number of Plots", "type": "number", "required": false, "placeholder": "5"}, {"name": "complexity", "label": "Complexity", "type": "select", "required": false, "placeholder": "", "options": ["Simple (Single Arc)", "Moderate (Subplot)", "Complex (Multiple Arcs)"]}]
_gen_54.system_prompt = 'You are a story consultant and plot architect. Generate unique, compelling plot outlines. Each should include: Premise, Main Character, Conflict, Rising Action, Plot Twist, Climax, and Resolution. Genre: {genre}. Themes: {themes}. Complexity: {complexity}. Generate {num_items} plots. Output ONLY the numbered plot outlines.'

_gen_55 = BaseGenerator()
_gen_55.slug = 'ai-dialogue-generator'
_gen_55.name = 'AI Dialogue Generator'
_gen_55.description = 'Write realistic, character-driven dialogue for stories, scripts, and creative projects.'
_gen_55.category = 'CREATIVE'
_gen_55.icon = 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
_gen_55.meta_title = 'AI Dialogue Generator - Free AI Writing Tool | WritingBot.ai'
_gen_55.meta_description = 'Write realistic, character-driven dialogue for stories, scripts, and creative projects.'
_gen_55.fields = [{"name": "scenario", "label": "Scenario", "type": "textarea", "required": true, "placeholder": "Describe the scene and situation..."}, {"name": "characters", "label": "Characters", "type": "textarea", "required": true, "placeholder": "Describe the characters involved and their relationship..."}, {"name": "mood", "label": "Mood", "type": "select", "required": false, "placeholder": "", "options": ["Tense", "Humorous", "Emotional", "Casual", "Confrontational", "Romantic", "Professional"]}, {"name": "format", "label": "Format", "type": "select", "required": false, "placeholder": "", "options": ["Novel Style", "Screenplay", "Stage Play", "General"]}]
_gen_55.system_prompt = 'You are a dialogue specialist. Write natural, engaging dialogue that reveals character, advances the scene, and sounds authentic. Include action beats and subtext. Scenario: {scenario}. Characters: {characters}. Mood: {mood}. Format: {format}. Output ONLY the dialogue.'

_gen_56 = BaseGenerator()
_gen_56.slug = 'ai-character-name-generator'
_gen_56.name = 'AI Character Name Generator'
_gen_56.description = 'Generate unique character names with meanings and backstory suggestions.'
_gen_56.category = 'CREATIVE'
_gen_56.icon = 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857'
_gen_56.meta_title = 'AI Character Name Generator - Free AI Writing Tool | WritingBot.ai'
_gen_56.meta_description = 'Generate unique character names with meanings and backstory suggestions.'
_gen_56.fields = [{"name": "genre", "label": "Genre/Setting", "type": "select", "required": true, "placeholder": "", "options": ["Fantasy", "Sci-Fi", "Historical", "Contemporary", "Mythological", "Anime/Manga", "Gothic", "Steampunk"]}, {"name": "character_type", "label": "Character Type", "type": "text", "required": false, "placeholder": "e.g. Hero, Villain, Sidekick, Warrior, Scholar"}, {"name": "culture", "label": "Cultural Inspiration", "type": "text", "required": false, "placeholder": "e.g. Norse, Japanese, Celtic, African"}, {"name": "num_items", "label": "Number of Names", "type": "number", "required": false, "placeholder": "20"}]
_gen_56.system_prompt = 'You are a naming specialist for fiction. Generate unique character names with: the name, pronunciation guide, meaning/origin, and a one-line character suggestion. Genre: {genre}. Type: {character_type}. Cultural inspiration: {culture}. Generate {num_items} names. Output ONLY the names with details.'

_gen_57 = BaseGenerator()
_gen_57.slug = 'ai-book-title-generator'
_gen_57.name = 'AI Book Title Generator'
_gen_57.description = 'Generate compelling book titles that grab attention and hint at the story within.'
_gen_57.category = 'CREATIVE'
_gen_57.icon = 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5'
_gen_57.meta_title = 'AI Book Title Generator - Free AI Writing Tool | WritingBot.ai'
_gen_57.meta_description = 'Generate compelling book titles that grab attention and hint at the story within.'
_gen_57.fields = [{"name": "genre", "label": "Genre", "type": "select", "required": true, "placeholder": "", "options": ["Fantasy", "Sci-Fi", "Mystery/Thriller", "Romance", "Literary Fiction", "Non-Fiction", "Self-Help", "Memoir", "Horror", "Young Adult"]}, {"name": "book_summary", "label": "Book Summary", "type": "textarea", "required": true, "placeholder": "Brief synopsis of the book..."}, {"name": "themes", "label": "Key Themes", "type": "text", "required": false, "placeholder": "e.g. Love, betrayal, hope, survival"}, {"name": "num_items", "label": "Number of Titles", "type": "number", "required": false, "placeholder": "15"}]
_gen_57.system_prompt = 'You are a book title expert. Generate compelling, marketable book titles that would stand out on a shelf. Consider genre conventions, hook value, and memorability. Genre: {genre}. Summary: {book_summary}. Themes: {themes}. Generate {num_items} titles with brief explanations of why each works. Output ONLY the titles.'

_gen_58 = BaseGenerator()
_gen_58.slug = 'ai-poem-generator'
_gen_58.name = 'AI Poem Generator'
_gen_58.description = 'Create beautiful poems in various styles from haiku to free verse.'
_gen_58.category = 'CREATIVE'
_gen_58.icon = 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z'
_gen_58.meta_title = 'AI Poem Generator - Free AI Writing Tool | WritingBot.ai'
_gen_58.meta_description = 'Create beautiful poems in various styles from haiku to free verse.'
_gen_58.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Subject of the poem"}, {"name": "style", "label": "Poetry Style", "type": "select", "required": true, "placeholder": "", "options": ["Free Verse", "Sonnet", "Haiku", "Limerick", "Rhyming", "Narrative", "Acrostic", "Ode", "Ballad", "Blank Verse"]}, {"name": "mood", "label": "Mood", "type": "select", "required": false, "placeholder": "", "options": ["Joyful", "Melancholic", "Romantic", "Dark", "Peaceful", "Passionate", "Nostalgic", "Reflective"]}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}]
_gen_58.system_prompt = 'You are a poet. Write a beautiful poem in the specified style. Use vivid imagery, strong rhythm, and emotional resonance. Topic: {topic}. Style: {style}. Mood: {mood}. Length: {length}. Output ONLY the poem.'

_gen_59 = BaseGenerator()
_gen_59.slug = 'ai-lyric-generator'
_gen_59.name = 'AI Lyric Generator'
_gen_59.description = 'Write song lyrics with verses, choruses, and bridges in any genre.'
_gen_59.category = 'CREATIVE'
_gen_59.icon = 'M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z'
_gen_59.meta_title = 'AI Lyric Generator - Free AI Writing Tool | WritingBot.ai'
_gen_59.meta_description = 'Write song lyrics with verses, choruses, and bridges in any genre.'
_gen_59.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the song about?"}, {"name": "genre", "label": "Music Genre", "type": "select", "required": true, "placeholder": "", "options": ["Pop", "Rock", "R&B/Soul", "Country", "Hip-Hop", "Indie", "Folk", "Electronic", "Jazz", "Blues", "Alternative"]}, {"name": "mood", "label": "Mood", "type": "select", "required": false, "placeholder": "", "options": ["Happy", "Sad", "Angry", "Romantic", "Empowering", "Nostalgic", "Dark", "Party/Fun"]}, {"name": "structure", "label": "Song Structure", "type": "select", "required": false, "placeholder": "", "options": ["Verse-Chorus-Verse", "Verse-Chorus-Bridge", "AABA", "Freeform"]}]
_gen_59.system_prompt = 'You are a songwriter and lyricist. Write song lyrics with the specified structure. Include strong hooks, emotional resonance, and rhythm suitable for the genre. Use [Verse], [Chorus], [Bridge] labels. Topic: {topic}. Genre: {genre}. Mood: {mood}. Structure: {structure}. Output ONLY the lyrics.'

_gen_60 = BaseGenerator()
_gen_60.slug = 'ai-rap-generator'
_gen_60.name = 'AI Rap Generator'
_gen_60.description = 'Generate rap verses with complex rhyme schemes, wordplay, and flow.'
_gen_60.category = 'CREATIVE'
_gen_60.icon = 'M9 19V6l12-3v13'
_gen_60.meta_title = 'AI Rap Generator - Free AI Writing Tool | WritingBot.ai'
_gen_60.meta_description = 'Generate rap verses with complex rhyme schemes, wordplay, and flow.'
_gen_60.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Topic or theme for the rap"}, {"name": "style", "label": "Style", "type": "select", "required": false, "placeholder": "", "options": ["Lyrical/Conscious", "Trap", "Old School", "Freestyle", "Battle Rap", "Storytelling", "Motivational"]}, {"name": "bars", "label": "Number of Bars", "type": "number", "required": false, "placeholder": "16"}, {"name": "mood", "label": "Mood", "type": "select", "required": false, "placeholder": "", "options": ["Hard/Aggressive", "Smooth", "Reflective", "Energetic", "Dark", "Confident"]}]
_gen_60.system_prompt = 'You are a skilled rapper and lyricist. Write rap bars with complex rhyme schemes, internal rhymes, wordplay, metaphors, and strong flow. Include multi-syllabic rhymes. Topic: {topic}. Style: {style}. Bars: {bars}. Mood: {mood}. Output ONLY the rap verses.'

_gen_61 = BaseGenerator()
_gen_61.slug = 'ai-script-generator'
_gen_61.name = 'AI Script Generator'
_gen_61.description = 'Write scripts for videos, movies, plays, and podcasts with proper formatting.'
_gen_61.category = 'CREATIVE'
_gen_61.icon = 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5'
_gen_61.meta_title = 'AI Script Generator - Free AI Writing Tool | WritingBot.ai'
_gen_61.meta_description = 'Write scripts for videos, movies, plays, and podcasts with proper formatting.'
_gen_61.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Script premise or concept"}, {"name": "format", "label": "Script Format", "type": "select", "required": true, "placeholder": "", "options": ["Short Film", "YouTube Video", "Podcast Episode", "Commercial/Ad", "Stage Play", "Explainer Video"]}, {"name": "duration", "label": "Target Duration", "type": "text", "required": false, "placeholder": "e.g. 5 minutes, 30 minutes"}, {"name": "characters", "label": "Characters", "type": "textarea", "required": false, "placeholder": "List the characters involved..."}]
_gen_61.system_prompt = 'You are a professional scriptwriter. Write a properly formatted script with scene headings, character names, dialogue, and action lines. Include visual/audio cues as appropriate. Premise: {topic}. Format: {format}. Duration: {duration}. Characters: {characters}. Output ONLY the script.'

_gen_62 = BaseGenerator()
_gen_62.slug = 'ai-cover-letter-generator'
_gen_62.name = 'AI Cover Letter Generator'
_gen_62.description = 'Write personalized cover letters that highlight your skills and land interviews.'
_gen_62.category = 'PROFESSIONAL'
_gen_62.icon = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586'
_gen_62.meta_title = 'AI Cover Letter Generator - Free AI Writing Tool | WritingBot.ai'
_gen_62.meta_description = 'Write personalized cover letters that highlight your skills and land interviews.'
_gen_62.fields = [{"name": "job_title", "label": "Job Title", "type": "text", "required": true, "placeholder": "Position you are applying for"}, {"name": "company_name", "label": "Company Name", "type": "text", "required": true, "placeholder": "Company you are applying to"}, {"name": "experience", "label": "Your Experience", "type": "textarea", "required": true, "placeholder": "Key skills, achievements, and relevant experience..."}, {"name": "job_description", "label": "Job Description", "type": "textarea", "required": false, "placeholder": "Paste the job description (optional)..."}]
_gen_62.system_prompt = 'You are a career coach and cover letter expert. Write a compelling, personalized cover letter that matches the candidate\'s experience to the job requirements. Include: Attention-grabbing opening, Relevant achievements with specifics, Enthusiasm for the company, and Strong closing with CTA. Job: {job_title}. Company: {company_name}. Experience: {experience}. Job Description: {job_description}. Output ONLY the cover letter.'

_gen_63 = BaseGenerator()
_gen_63.slug = 'ai-resignation-letter-writer'
_gen_63.name = 'AI Resignation Letter Writer'
_gen_63.description = 'Write professional resignation letters that maintain positive relationships.'
_gen_63.category = 'PROFESSIONAL'
_gen_63.icon = 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1'
_gen_63.meta_title = 'AI Resignation Letter Writer - Free AI Writing Tool | WritingBot.ai'
_gen_63.meta_description = 'Write professional resignation letters that maintain positive relationships.'
_gen_63.fields = [{"name": "job_title", "label": "Your Job Title", "type": "text", "required": true, "placeholder": "Your current position"}, {"name": "company", "label": "Company Name", "type": "text", "required": false, "placeholder": "Your current company"}, {"name": "last_day", "label": "Last Working Day", "type": "text", "required": false, "placeholder": "e.g. March 15, 2025"}, {"name": "reason", "label": "Reason (Optional)", "type": "textarea", "required": false, "placeholder": "Brief reason for leaving (optional)..."}]
_gen_63.system_prompt = 'You are an HR communications expert. Write a professional, gracious resignation letter that: States the intent to resign, Includes the last working day, Expresses gratitude, Offers to help with transition, and Maintains a positive tone. Title: {job_title}. Company: {company}. Last Day: {last_day}. Reason: {reason}. Output ONLY the letter.'

_gen_64 = BaseGenerator()
_gen_64.slug = 'ai-letter-of-recommendation-generator'
_gen_64.name = 'AI Letter of Recommendation Generator'
_gen_64.description = 'Generate strong letters of recommendation for employees, students, or colleagues.'
_gen_64.category = 'PROFESSIONAL'
_gen_64.icon = 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944'
_gen_64.meta_title = 'AI Letter of Recommendation Generator - Free AI Writing Tool | WritingBot.ai'
_gen_64.meta_description = 'Generate strong letters of recommendation for employees, students, or colleagues.'
_gen_64.fields = [{"name": "recommender_name", "label": "Your Name/Title", "type": "text", "required": true, "placeholder": "Your name and title"}, {"name": "candidate_name", "label": "Candidate Name", "type": "text", "required": true, "placeholder": "Person you are recommending"}, {"name": "relationship", "label": "Relationship", "type": "text", "required": true, "placeholder": "e.g. Direct supervisor for 3 years"}, {"name": "strengths", "label": "Key Strengths & Achievements", "type": "textarea", "required": true, "placeholder": "Specific qualities, skills, and accomplishments..."}]
_gen_64.system_prompt = 'You are a professional reference writer. Write a compelling letter of recommendation that: States your relationship with the candidate, Provides specific examples of their strengths, Highlights key achievements, and Gives a strong endorsement. Recommender: {recommender_name}. Candidate: {candidate_name}. Relationship: {relationship}. Strengths: {strengths}. Output ONLY the letter.'

_gen_65 = BaseGenerator()
_gen_65.slug = 'ai-letter-generator'
_gen_65.name = 'AI Letter Generator'
_gen_65.description = 'Write professional and personal letters for any occasion or purpose.'
_gen_65.category = 'PROFESSIONAL'
_gen_65.icon = 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8'
_gen_65.meta_title = 'AI Letter Generator - Free AI Writing Tool | WritingBot.ai'
_gen_65.meta_description = 'Write professional and personal letters for any occasion or purpose.'
_gen_65.fields = [{"name": "letter_type", "label": "Letter Type", "type": "select", "required": true, "placeholder": "", "options": ["Formal Business", "Complaint", "Thank You", "Apology", "Request", "Invitation", "Personal", "Legal"]}, {"name": "recipient", "label": "Recipient", "type": "text", "required": true, "placeholder": "Who is the letter to?"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Purpose and key points to include..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_65.system_prompt = 'You are a versatile letter writer. Write a well-structured letter appropriate for the type and recipient. Include proper formatting, salutation, body paragraphs, and closing. Type: {letter_type}. Recipient: {recipient}. Details: {description}. Tone: {tone}. Output ONLY the letter.'

_gen_66 = BaseGenerator()
_gen_66.slug = 'ai-resume-writer'
_gen_66.name = 'AI Resume Writer'
_gen_66.description = 'Create ATS-friendly resumes with impactful bullet points and professional formatting.'
_gen_66.category = 'PROFESSIONAL'
_gen_66.icon = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586'
_gen_66.meta_title = 'AI Resume Writer - Free AI Writing Tool | WritingBot.ai'
_gen_66.meta_description = 'Create ATS-friendly resumes with impactful bullet points and professional formatting.'
_gen_66.fields = [{"name": "job_title", "label": "Target Job Title", "type": "text", "required": true, "placeholder": "Position you are applying for"}, {"name": "experience", "label": "Work Experience", "type": "textarea", "required": true, "placeholder": "List your work experience with dates, companies, and responsibilities..."}, {"name": "education", "label": "Education", "type": "textarea", "required": false, "placeholder": "Degrees, certifications, relevant coursework..."}, {"name": "skills", "label": "Skills", "type": "textarea", "required": false, "placeholder": "Technical skills, soft skills, tools..."}]
_gen_66.system_prompt = 'You are a professional resume writer and ATS expert. Write a polished resume in a clean text format with: Contact Info placeholder, Professional Summary, Work Experience with quantified achievement bullets (use action verbs), Education, Skills section, and optional Certifications. Target Role: {job_title}. Experience: {experience}. Education: {education}. Skills: {skills}. Output ONLY the resume content.'

_gen_67 = BaseGenerator()
_gen_67.slug = 'ai-job-posting-generator'
_gen_67.name = 'AI Job Posting Generator'
_gen_67.description = 'Create attractive job postings that stand out on job boards and attract top talent.'
_gen_67.category = 'PROFESSIONAL'
_gen_67.icon = 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745'
_gen_67.meta_title = 'AI Job Posting Generator - Free AI Writing Tool | WritingBot.ai'
_gen_67.meta_description = 'Create attractive job postings that stand out on job boards and attract top talent.'
_gen_67.fields = [{"name": "job_title", "label": "Job Title", "type": "text", "required": true, "placeholder": "e.g. Full Stack Developer"}, {"name": "company", "label": "Company Name", "type": "text", "required": false, "placeholder": "Your company name"}, {"name": "key_details", "label": "Key Details", "type": "textarea", "required": true, "placeholder": "Location, salary range, remote/hybrid, team size..."}, {"name": "requirements", "label": "Requirements", "type": "textarea", "required": false, "placeholder": "Must-have skills and qualifications..."}]
_gen_67.system_prompt = 'You are a recruiting copywriter. Write an engaging job posting that sells the opportunity. Include: Catchy intro, Role overview, What You\'ll Do, What We\'re Looking For, Nice to Haves, What We Offer/Benefits, and How to Apply. Title: {job_title}. Company: {company}. Details: {key_details}. Requirements: {requirements}. Output ONLY the job posting.'

_gen_68 = BaseGenerator()
_gen_68.slug = 'ai-job-summary-generator'
_gen_68.name = 'AI Job Summary Generator'
_gen_68.description = 'Write concise job summaries for HR systems, internal postings, and headcount planning.'
_gen_68.category = 'PROFESSIONAL'
_gen_68.icon = 'M4 6h16M4 12h8m-8 6h16'
_gen_68.meta_title = 'AI Job Summary Generator - Free AI Writing Tool | WritingBot.ai'
_gen_68.meta_description = 'Write concise job summaries for HR systems, internal postings, and headcount planning.'
_gen_68.fields = [{"name": "job_title", "label": "Job Title", "type": "text", "required": true, "placeholder": "Position title"}, {"name": "department", "label": "Department", "type": "text", "required": false, "placeholder": "e.g. Engineering, Marketing"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Key responsibilities and requirements..."}, {"name": "level", "label": "Level", "type": "select", "required": false, "placeholder": "", "options": ["Entry Level", "Mid Level", "Senior", "Lead/Manager", "Director", "VP/Executive"]}]
_gen_68.system_prompt = 'You are an HR professional. Write a concise job summary (3-5 sentences) that captures the essence of the role, key responsibilities, required qualifications, and where it fits in the organization. Title: {job_title}. Department: {department}. Details: {description}. Level: {level}. Output ONLY the job summary.'

_gen_69 = BaseGenerator()
_gen_69.slug = 'ai-student-reference-letter-generator'
_gen_69.name = 'AI Student Reference Letter Generator'
_gen_69.description = 'Write compelling reference letters for students applying to schools, scholarships, or programs.'
_gen_69.category = 'PROFESSIONAL'
_gen_69.icon = 'M12 14l9-5-9-5-9 5 9 5z'
_gen_69.meta_title = 'AI Student Reference Letter Generator - Free AI Writing Tool | WritingBot.ai'
_gen_69.meta_description = 'Write compelling reference letters for students applying to schools, scholarships, or programs.'
_gen_69.fields = [{"name": "student_name", "label": "Student Name", "type": "text", "required": true, "placeholder": "Name of the student"}, {"name": "program", "label": "Program/School Applying To", "type": "text", "required": false, "placeholder": "e.g. MIT Computer Science, Rhodes Scholarship"}, {"name": "relationship", "label": "Your Relationship", "type": "text", "required": true, "placeholder": "e.g. Professor for 2 semesters"}, {"name": "qualities", "label": "Key Qualities & Achievements", "type": "textarea", "required": true, "placeholder": "Academic performance, leadership, specific achievements..."}]
_gen_69.system_prompt = 'You are an academic reference writer. Write a strong reference letter for a student that: Establishes your credibility and relationship, Highlights academic excellence with specific examples, Demonstrates character and leadership, and Gives an enthusiastic recommendation. Student: {student_name}. Program: {program}. Relationship: {relationship}. Qualities: {qualities}. Output ONLY the letter.'

_gen_70 = BaseGenerator()
_gen_70.slug = 'ai-blog-post-generator'
_gen_70.name = 'AI Blog Post Generator'
_gen_70.description = 'Generate SEO-optimized blog posts with engaging content and proper structure.'
_gen_70.category = 'CONTENT_SEO'
_gen_70.icon = 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1'
_gen_70.meta_title = 'AI Blog Post Generator - Free AI Writing Tool | WritingBot.ai'
_gen_70.meta_description = 'Generate SEO-optimized blog posts with engaging content and proper structure.'
_gen_70.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Blog post topic"}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Target SEO keywords"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}]
_gen_70.system_prompt = 'You are an expert blog writer and SEO specialist. Write an engaging, SEO-optimized blog post with: Compelling headline, Hook introduction, Well-structured body with H2/H3 subheadings, Actionable insights, and Strong conclusion with CTA. Naturally incorporate keywords. Topic: {topic}. Keywords: {keywords}. Audience: {audience}. Length: {length}. Output ONLY the blog post with markdown headings.'

_gen_71 = BaseGenerator()
_gen_71.slug = 'ai-article-rewriter'
_gen_71.name = 'AI Article Rewriter'
_gen_71.description = 'Rewrite articles to be unique while preserving the original meaning and improving quality.'
_gen_71.category = 'CONTENT_SEO'
_gen_71.icon = 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581'
_gen_71.meta_title = 'AI Article Rewriter - Free AI Writing Tool | WritingBot.ai'
_gen_71.meta_description = 'Rewrite articles to be unique while preserving the original meaning and improving quality.'
_gen_71.fields = [{"name": "original_text", "label": "Original Article", "type": "textarea", "required": true, "placeholder": "Paste the article you want to rewrite..."}, {"name": "rewrite_goal", "label": "Rewrite Goal", "type": "select", "required": false, "placeholder": "", "options": ["Improve Quality", "Make Unique", "Simplify", "Change Tone", "Add SEO Keywords"]}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Keywords to incorporate (optional)"}]
_gen_71.system_prompt = 'You are an expert content editor and rewriter. Rewrite the provided article to be completely unique while preserving the core meaning and facts. Improve clarity, flow, and engagement. Goal: {rewrite_goal}. Keywords: {keywords}. IMPORTANT: The output must be substantially different from the input while conveying the same information. Output ONLY the rewritten article.'

_gen_72 = BaseGenerator()
_gen_72.slug = 'ai-paragraph-generator'
_gen_72.name = 'AI Paragraph Generator'
_gen_72.description = 'Generate well-crafted paragraphs on any topic for essays, articles, or content.'
_gen_72.category = 'CONTENT_SEO'
_gen_72.icon = 'M4 6h16M4 12h16M4 18h16'
_gen_72.meta_title = 'AI Paragraph Generator - Free AI Writing Tool | WritingBot.ai'
_gen_72.meta_description = 'Generate well-crafted paragraphs on any topic for essays, articles, or content.'
_gen_72.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What should the paragraph be about?"}, {"name": "context", "label": "Context", "type": "textarea", "required": false, "placeholder": "Where will this paragraph be used? Any context?"}, {"name": "paragraph_type", "label": "Paragraph Type", "type": "select", "required": false, "placeholder": "", "options": ["Introduction", "Body/Supporting", "Conclusion", "Transition", "Descriptive", "Argumentative"]}, {"name": "num_items", "label": "Number of Paragraphs", "type": "number", "required": false, "placeholder": "1"}]
_gen_72.system_prompt = 'You are a skilled content writer. Write well-crafted paragraph(s) on the given topic. Each paragraph should have a clear topic sentence, supporting details, and a concluding transition. Topic: {topic}. Context: {context}. Type: {paragraph_type}. Count: {num_items}. Tone: {tone}. Output ONLY the paragraph(s).'

_gen_73 = BaseGenerator()
_gen_73.slug = 'ai-text-generator'
_gen_73.name = 'AI Text Generator'
_gen_73.description = 'Generate high-quality text content for any purpose with customizable parameters.'
_gen_73.category = 'CONTENT_SEO'
_gen_73.icon = 'M4 6h16M4 12h16M4 18h7'
_gen_73.meta_title = 'AI Text Generator - Free AI Writing Tool | WritingBot.ai'
_gen_73.meta_description = 'Generate high-quality text content for any purpose with customizable parameters.'
_gen_73.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What should the text be about?"}, {"name": "text_type", "label": "Content Type", "type": "select", "required": false, "placeholder": "", "options": ["Article", "Blog Post", "Website Copy", "Product Copy", "Educational", "Technical", "Creative"]}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Enter keywords separated by commas"}]
_gen_73.system_prompt = 'You are a versatile content writer. Generate high-quality text content on the given topic. Match the style and depth to the content type. Write naturally with good flow and structure. Topic: {topic}. Type: {text_type}. Length: {length}. Keywords: {keywords}. Tone: {tone}. Output ONLY the text content.'

_gen_74 = BaseGenerator()
_gen_74.slug = 'ai-content-idea-generator'
_gen_74.name = 'AI Content Idea Generator'
_gen_74.description = 'Generate fresh content ideas for blogs, social media, videos, and marketing campaigns.'
_gen_74.category = 'CONTENT_SEO'
_gen_74.icon = 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707'
_gen_74.meta_title = 'AI Content Idea Generator - Free AI Writing Tool | WritingBot.ai'
_gen_74.meta_description = 'Generate fresh content ideas for blogs, social media, videos, and marketing campaigns.'
_gen_74.fields = [{"name": "niche", "label": "Niche/Industry", "type": "text", "required": true, "placeholder": "e.g. Digital Marketing, Fitness, Personal Finance"}, {"name": "content_type", "label": "Content Type", "type": "select", "required": false, "placeholder": "", "options": ["Blog Posts", "Social Media", "YouTube Videos", "Podcast Episodes", "Email Newsletter", "Infographics", "All Types"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "num_items", "label": "Number of Ideas", "type": "number", "required": false, "placeholder": "20"}]
_gen_74.system_prompt = 'You are a content strategist. Generate creative, actionable content ideas that would engage the target audience. For each idea include: Title/headline, Brief description, Target keyword, and Content format suggestion. Niche: {niche}. Type: {content_type}. Audience: {audience}. Generate {num_items} ideas. Output ONLY the numbered ideas.'

_gen_75 = BaseGenerator()
_gen_75.slug = 'ai-meta-description-generator'
_gen_75.name = 'AI Meta Description Generator'
_gen_75.description = 'Write SEO-optimized meta descriptions that boost click-through rates in search results.'
_gen_75.category = 'CONTENT_SEO'
_gen_75.icon = 'M10 21h7a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7'
_gen_75.meta_title = 'AI Meta Description Generator - Free AI Writing Tool | WritingBot.ai'
_gen_75.meta_description = 'Write SEO-optimized meta descriptions that boost click-through rates in search results.'
_gen_75.fields = [{"name": "page_title", "label": "Page Title", "type": "text", "required": true, "placeholder": "Title of the page"}, {"name": "page_content", "label": "Page Content Summary", "type": "textarea", "required": true, "placeholder": "What is the page about?"}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Target keywords"}, {"name": "num_items", "label": "Number of Variations", "type": "number", "required": false, "placeholder": "5"}]
_gen_75.system_prompt = 'You are an SEO specialist. Write compelling meta descriptions (150-160 characters each) that: Include the target keyword naturally, Accurately describe the page content, Include a call to action, and Entice users to click. Page: {page_title}. Content: {page_content}. Keywords: {keywords}. Generate {num_items} variations. Output ONLY the numbered descriptions.'

_gen_76 = BaseGenerator()
_gen_76.slug = 'ai-seo-title-generator'
_gen_76.name = 'AI SEO Title Generator'
_gen_76.description = 'Create click-worthy, SEO-optimized page titles that rank and get clicks.'
_gen_76.category = 'CONTENT_SEO'
_gen_76.icon = 'M13 10V3L4 14h7v7l9-11h-7z'
_gen_76.meta_title = 'AI SEO Title Generator - Free AI Writing Tool | WritingBot.ai'
_gen_76.meta_description = 'Create click-worthy, SEO-optimized page titles that rank and get clicks.'
_gen_76.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Page/article topic"}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Primary keyword to target"}, {"name": "title_style", "label": "Title Style", "type": "select", "required": false, "placeholder": "", "options": ["How-To", "Listicle", "Question", "Guide", "Review", "Comparison", "News"]}, {"name": "num_items", "label": "Number of Titles", "type": "number", "required": false, "placeholder": "10"}]
_gen_76.system_prompt = 'You are an SEO and headline expert. Generate SEO-optimized page titles (under 60 characters) that: Include the primary keyword near the beginning, Are compelling and click-worthy, Match search intent, and Use power words. Topic: {topic}. Keywords: {keywords}. Style: {title_style}. Generate {num_items} titles. Output ONLY the numbered titles.'

_gen_77 = BaseGenerator()
_gen_77.slug = 'ai-title-generator'
_gen_77.name = 'AI Title Generator'
_gen_77.description = 'Generate attention-grabbing titles for articles, essays, presentations, and more.'
_gen_77.category = 'CONTENT_SEO'
_gen_77.icon = 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536'
_gen_77.meta_title = 'AI Title Generator - Free AI Writing Tool | WritingBot.ai'
_gen_77.meta_description = 'Generate attention-grabbing titles for articles, essays, presentations, and more.'
_gen_77.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the content about?"}, {"name": "content_format", "label": "Content Format", "type": "select", "required": false, "placeholder": "", "options": ["Article", "Blog Post", "Essay", "Presentation", "Video", "Book Chapter", "Report", "Newsletter"]}, {"name": "style", "label": "Title Style", "type": "select", "required": false, "placeholder": "", "options": ["Catchy", "Professional", "Informative", "Provocative", "Emotional", "Humorous"]}, {"name": "num_items", "label": "Number of Titles", "type": "number", "required": false, "placeholder": "10"}]
_gen_77.system_prompt = 'You are a headline writing expert. Generate attention-grabbing titles that make people want to read the content. Vary the approaches (questions, numbers, how-to, emotional hooks). Topic: {topic}. Format: {content_format}. Style: {style}. Generate {num_items} titles. Output ONLY the numbered titles.'

_gen_78 = BaseGenerator()
_gen_78.slug = 'ai-keyword-generator'
_gen_78.name = 'AI Keyword Generator'
_gen_78.description = 'Discover relevant keywords and long-tail phrases for SEO and content strategy.'
_gen_78.category = 'CONTENT_SEO'
_gen_78.icon = 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'
_gen_78.meta_title = 'AI Keyword Generator - Free AI Writing Tool | WritingBot.ai'
_gen_78.meta_description = 'Discover relevant keywords and long-tail phrases for SEO and content strategy.'
_gen_78.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Main topic or seed keyword"}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}, {"name": "intent", "label": "Search Intent", "type": "select", "required": false, "placeholder": "", "options": ["Informational", "Commercial", "Transactional", "Navigational", "All"]}, {"name": "num_items", "label": "Number of Keywords", "type": "number", "required": false, "placeholder": "30"}]
_gen_78.system_prompt = 'You are an SEO keyword research expert. Generate a comprehensive list of keywords organized by: Primary keywords, Secondary keywords, Long-tail keywords, Question keywords, and Related terms. Include estimated search intent for each. Topic: {topic}. Industry: {industry}. Intent: {intent}. Generate {num_items} keywords. Output ONLY the organized keyword list.'

_gen_79 = BaseGenerator()
_gen_79.slug = 'ai-listicle-generator'
_gen_79.name = 'AI Listicle Generator'
_gen_79.description = 'Create engaging listicle articles with compelling points and supporting details.'
_gen_79.category = 'CONTENT_SEO'
_gen_79.icon = 'M4 6h16M4 10h16M4 14h16M4 18h16'
_gen_79.meta_title = 'AI Listicle Generator - Free AI Writing Tool | WritingBot.ai'
_gen_79.meta_description = 'Create engaging listicle articles with compelling points and supporting details.'
_gen_79.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Listicle topic"}, {"name": "list_count", "label": "Number of Items", "type": "number", "required": false, "placeholder": "10"}, {"name": "keywords", "label": "Keywords", "type": "text", "required": false, "placeholder": "Enter keywords separated by commas"}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}]
_gen_79.system_prompt = 'You are a content writer specializing in listicles. Write an engaging listicle article with: Catchy title, Brief introduction, Numbered items each with a subheading and 2-3 paragraph explanation, and a conclusion. Topic: {topic}. Number of items: {list_count}. Keywords: {keywords}. Audience: {audience}. Output ONLY the listicle article.'

_gen_80 = BaseGenerator()
_gen_80.slug = 'ai-prompt-generator'
_gen_80.name = 'AI Prompt Generator'
_gen_80.description = 'Generate effective AI prompts for ChatGPT, Claude, and other AI assistants.'
_gen_80.category = 'UTILITY'
_gen_80.icon = 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707'
_gen_80.meta_title = 'AI Prompt Generator - Free AI Writing Tool | WritingBot.ai'
_gen_80.meta_description = 'Generate effective AI prompts for ChatGPT, Claude, and other AI assistants.'
_gen_80.fields = [{"name": "task", "label": "Task Description", "type": "textarea", "required": true, "placeholder": "What do you want the AI to help you with?"}, {"name": "ai_tool", "label": "AI Tool", "type": "select", "required": false, "placeholder": "", "options": ["ChatGPT", "Claude", "Midjourney", "DALL-E", "Stable Diffusion", "General"]}, {"name": "detail_level", "label": "Detail Level", "type": "select", "required": false, "placeholder": "", "options": ["Simple", "Detailed", "Expert"]}, {"name": "num_items", "label": "Number of Prompts", "type": "number", "required": false, "placeholder": "5"}]
_gen_80.system_prompt = 'You are a prompt engineering expert. Generate effective, well-structured prompts that will produce the best results from AI tools. Include context, specific instructions, format requirements, and constraints. Task: {task}. Tool: {ai_tool}. Detail: {detail_level}. Generate {num_items} prompts. Output ONLY the numbered prompts.'

_gen_81 = BaseGenerator()
_gen_81.slug = 'ai-writing-prompt-generator'
_gen_81.name = 'AI Writing Prompt Generator'
_gen_81.description = 'Generate creative writing prompts to spark inspiration for stories, poems, and more.'
_gen_81.category = 'UTILITY'
_gen_81.icon = 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536'
_gen_81.meta_title = 'AI Writing Prompt Generator - Free AI Writing Tool | WritingBot.ai'
_gen_81.meta_description = 'Generate creative writing prompts to spark inspiration for stories, poems, and more.'
_gen_81.fields = [{"name": "genre", "label": "Genre", "type": "select", "required": false, "placeholder": "", "options": ["Fantasy", "Sci-Fi", "Romance", "Horror", "Mystery", "Literary Fiction", "Poetry", "Non-Fiction", "Any Genre"]}, {"name": "prompt_type", "label": "Prompt Type", "type": "select", "required": false, "placeholder": "", "options": ["Opening Line", "Scenario", "Character-Based", "Setting-Based", "Dialogue Starter", "Theme-Based", "Image/Visual"]}, {"name": "num_items", "label": "Number of Prompts", "type": "number", "required": false, "placeholder": "10"}, {"name": "difficulty", "label": "Difficulty", "type": "select", "required": false, "placeholder": "", "options": ["Beginner", "Intermediate", "Advanced"]}]
_gen_81.system_prompt = 'You are a creative writing instructor. Generate inspiring, thought-provoking writing prompts that spark creativity. Each prompt should be specific enough to start writing but open enough for interpretation. Genre: {genre}. Type: {prompt_type}. Difficulty: {difficulty}. Generate {num_items} prompts. Output ONLY the numbered prompts.'

_gen_82 = BaseGenerator()
_gen_82.slug = 'ai-random-prompt-generator'
_gen_82.name = 'AI Random Prompt Generator'
_gen_82.description = 'Get random creative prompts for writing, art, brainstorming, or creative exercises.'
_gen_82.category = 'UTILITY'
_gen_82.icon = 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581'
_gen_82.meta_title = 'AI Random Prompt Generator - Free AI Writing Tool | WritingBot.ai'
_gen_82.meta_description = 'Get random creative prompts for writing, art, brainstorming, or creative exercises.'
_gen_82.fields = [{"name": "category", "label": "Category", "type": "select", "required": false, "placeholder": "", "options": ["Writing", "Art/Drawing", "Photography", "Music", "Business", "Self-Reflection", "Conversation Starter", "Any"]}, {"name": "num_items", "label": "Number of Prompts", "type": "number", "required": false, "placeholder": "10"}, {"name": "wildness", "label": "Creativity Level", "type": "select", "required": false, "placeholder": "", "options": ["Normal", "Wild", "Completely Random"]}]
_gen_82.system_prompt = 'You are a creative prompt generator. Generate random, unexpected prompts that challenge creative thinking. Mix genres, combine unusual elements, and surprise the user. Category: {category}. Creativity: {wildness}. Generate {num_items} prompts. Output ONLY the numbered prompts.'

_gen_83 = BaseGenerator()
_gen_83.slug = 'ai-faq-generator'
_gen_83.name = 'AI FAQ Generator'
_gen_83.description = 'Generate comprehensive FAQ sections for websites, products, and services.'
_gen_83.category = 'UTILITY'
_gen_83.icon = 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3'
_gen_83.meta_title = 'AI FAQ Generator - Free AI Writing Tool | WritingBot.ai'
_gen_83.meta_description = 'Generate comprehensive FAQ sections for websites, products, and services.'
_gen_83.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Subject for the FAQ"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Details about the product, service, or topic..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "num_items", "label": "Number of FAQs", "type": "number", "required": false, "placeholder": "10"}]
_gen_83.system_prompt = 'You are a content writer specializing in FAQ sections. Generate clear, helpful FAQ entries. Each entry should have a natural question that real users would ask and a concise, informative answer. Topic: {topic}. Details: {description}. Audience: {audience}. Generate {num_items} FAQ entries. Output ONLY the Q&A pairs.'

_gen_84 = BaseGenerator()
_gen_84.slug = 'ai-checklist-generator'
_gen_84.name = 'AI Checklist Generator'
_gen_84.description = 'Create comprehensive checklists for projects, processes, events, and tasks.'
_gen_84.category = 'UTILITY'
_gen_84.icon = 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4'
_gen_84.meta_title = 'AI Checklist Generator - Free AI Writing Tool | WritingBot.ai'
_gen_84.meta_description = 'Create comprehensive checklists for projects, processes, events, and tasks.'
_gen_84.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "What is the checklist for?"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Context, requirements, or specific items to include..."}, {"name": "checklist_type", "label": "Checklist Type", "type": "select", "required": false, "placeholder": "", "options": ["Project", "Event Planning", "Travel", "Moving", "Launch", "Audit", "Daily Routine", "Process"]}]
_gen_84.system_prompt = 'You are an organizational expert. Create a comprehensive, actionable checklist organized by categories/phases. Each item should be specific and actionable. Include priority markers where helpful. Topic: {topic}. Details: {description}. Type: {checklist_type}. Output ONLY the checklist.'

_gen_85 = BaseGenerator()
_gen_85.slug = 'ai-to-do-list-generator'
_gen_85.name = 'AI To-Do List Generator'
_gen_85.description = 'Generate organized to-do lists with priorities and time estimates.'
_gen_85.category = 'UTILITY'
_gen_85.icon = 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2'
_gen_85.meta_title = 'AI To-Do List Generator - Free AI Writing Tool | WritingBot.ai'
_gen_85.meta_description = 'Generate organized to-do lists with priorities and time estimates.'
_gen_85.fields = [{"name": "goal", "label": "Goal/Project", "type": "text", "required": true, "placeholder": "What do you need to accomplish?"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Details, deadlines, constraints..."}, {"name": "timeframe", "label": "Timeframe", "type": "select", "required": false, "placeholder": "", "options": ["Today", "This Week", "This Month", "This Quarter", "No Deadline"]}]
_gen_85.system_prompt = 'You are a productivity expert. Create an organized to-do list with: Priority levels (High/Medium/Low), Estimated time for each task, Logical ordering, and Grouped categories. Goal: {goal}. Details: {description}. Timeframe: {timeframe}. Output ONLY the to-do list.'

_gen_86 = BaseGenerator()
_gen_86.slug = 'ai-acronym-generator'
_gen_86.name = 'AI Acronym Generator'
_gen_86.description = 'Create meaningful acronyms and expand existing ones for projects, teams, and initiatives.'
_gen_86.category = 'UTILITY'
_gen_86.icon = 'M13 10V3L4 14h7v7l9-11h-7z'
_gen_86.meta_title = 'AI Acronym Generator - Free AI Writing Tool | WritingBot.ai'
_gen_86.meta_description = 'Create meaningful acronyms and expand existing ones for projects, teams, and initiatives.'
_gen_86.fields = [{"name": "words_or_concept", "label": "Words or Concept", "type": "text", "required": true, "placeholder": "Enter words for an acronym, or a concept to create one for"}, {"name": "mode", "label": "Mode", "type": "select", "required": true, "placeholder": "", "options": ["Create Acronym from Concept", "Expand Existing Acronym", "Both"]}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}, {"name": "num_items", "label": "Number of Options", "type": "number", "required": false, "placeholder": "10"}]
_gen_86.system_prompt = 'You are a branding and naming expert. Generate creative, memorable acronyms. If creating from concept: propose acronyms that spell relevant words. If expanding: provide multiple meaningful expansions. Ensure they are professional, memorable, and relevant. Input: {words_or_concept}. Mode: {mode}. Industry: {industry}. Generate {num_items} options. Output ONLY the numbered options.'

_gen_87 = BaseGenerator()
_gen_87.slug = 'ai-simplified-explanation-generator'
_gen_87.name = 'AI Simplified Explanation Generator'
_gen_87.description = 'Explain complex topics in simple, easy-to-understand language for any audience.'
_gen_87.category = 'UTILITY'
_gen_87.icon = 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
_gen_87.meta_title = 'AI Simplified Explanation Generator - Free AI Writing Tool | WritingBot.ai'
_gen_87.meta_description = 'Explain complex topics in simple, easy-to-understand language for any audience.'
_gen_87.fields = [{"name": "topic", "label": "Topic", "type": "text", "required": true, "placeholder": "Complex topic to explain"}, {"name": "complexity_level", "label": "Explanation Level", "type": "select", "required": true, "placeholder": "", "options": ["Explain Like I'm 5", "Middle School Level", "High School Level", "Non-Expert Adult", "Quick Summary"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "length", "label": "Length", "type": "select", "required": false, "placeholder": "", "options": ["Short", "Medium", "Long"]}]
_gen_87.system_prompt = 'You are an expert explainer who makes complex topics simple. Explain the given topic at the specified level using: Analogies and metaphors, Simple vocabulary, Real-world examples, Step-by-step breakdowns, and No jargon. Topic: {topic}. Level: {complexity_level}. Audience: {audience}. Length: {length}. Output ONLY the explanation.'

_gen_88 = BaseGenerator()
_gen_88.slug = 'ai-weekly-newsletter-generator'
_gen_88.name = 'AI Weekly Newsletter Generator'
_gen_88.description = 'Create engaging weekly newsletters with curated content and insights.'
_gen_88.category = 'NEWSLETTERS'
_gen_88.icon = 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1'
_gen_88.meta_title = 'AI Weekly Newsletter Generator - Free AI Writing Tool | WritingBot.ai'
_gen_88.meta_description = 'Create engaging weekly newsletters with curated content and insights.'
_gen_88.fields = [{"name": "newsletter_name", "label": "Newsletter Name", "type": "text", "required": true, "placeholder": "Name of your newsletter"}, {"name": "topics_covered", "label": "Topics/Updates", "type": "textarea", "required": true, "placeholder": "Key topics, news, and updates to cover this week..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "e.g. Technology, Healthcare, Finance"}]
_gen_88.system_prompt = 'You are a newsletter editor. Write an engaging weekly newsletter with: Compelling subject line, Personal greeting, Top story/highlight, 3-5 curated content sections with commentary, Quick tips or insights, and CTA. Newsletter: {newsletter_name}. Topics: {topics_covered}. Audience: {audience}. Industry: {industry}. Output ONLY the newsletter.'

_gen_89 = BaseGenerator()
_gen_89.slug = 'ai-industry-newsletter-generator'
_gen_89.name = 'AI Industry Newsletter Generator'
_gen_89.description = 'Generate industry-specific newsletters with trends, analysis, and expert commentary.'
_gen_89.category = 'NEWSLETTERS'
_gen_89.icon = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586'
_gen_89.meta_title = 'AI Industry Newsletter Generator - Free AI Writing Tool | WritingBot.ai'
_gen_89.meta_description = 'Generate industry-specific newsletters with trends, analysis, and expert commentary.'
_gen_89.fields = [{"name": "industry", "label": "Industry", "type": "text", "required": false, "placeholder": "Which industry?"}, {"name": "trends", "label": "Current Trends/News", "type": "textarea", "required": true, "placeholder": "Key industry trends, news, or developments..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "e.g. students, professionals, general public"}, {"name": "newsletter_sections", "label": "Sections to Include", "type": "text", "required": false, "placeholder": "e.g. News Roundup, Expert Take, Tools, Jobs"}]
_gen_89.system_prompt = 'You are an industry analyst and newsletter writer. Write a professional industry newsletter with: Subject line, Executive summary, Industry news roundup, Trend analysis, Expert commentary, Data/statistics, and Forward-looking insights. Industry: {industry}. Trends: {trends}. Audience: {audience}. Sections: {newsletter_sections}. Output ONLY the newsletter.'

_gen_90 = BaseGenerator()
_gen_90.slug = 'ai-event-invitation-generator'
_gen_90.name = 'AI Event Invitation Generator'
_gen_90.description = 'Create compelling event invitations for conferences, webinars, parties, and meetings.'
_gen_90.category = 'NEWSLETTERS'
_gen_90.icon = 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5'
_gen_90.meta_title = 'AI Event Invitation Generator - Free AI Writing Tool | WritingBot.ai'
_gen_90.meta_description = 'Create compelling event invitations for conferences, webinars, parties, and meetings.'
_gen_90.fields = [{"name": "event_name", "label": "Event Name", "type": "text", "required": true, "placeholder": "Name of the event"}, {"name": "event_details", "label": "Event Details", "type": "textarea", "required": true, "placeholder": "Date, time, location, agenda, speakers..."}, {"name": "event_type", "label": "Event Type", "type": "select", "required": false, "placeholder": "", "options": ["Conference", "Webinar", "Workshop", "Networking", "Party/Social", "Fundraiser", "Product Launch", "Meeting"]}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who are you inviting?"}]
_gen_90.system_prompt = 'You are an event communications specialist. Write a compelling event invitation that creates excitement and drives RSVPs. Include: Attention-grabbing headline, Event value proposition, Key details (who/what/when/where), Speaker/highlight info, RSVP CTA, and Contact info placeholder. Event: {event_name}. Details: {event_details}. Type: {event_type}. Audience: {audience}. Output ONLY the invitation.'

_gen_91 = BaseGenerator()
_gen_91.slug = 'ai-event-planning-generator'
_gen_91.name = 'AI Event Planning Generator'
_gen_91.description = 'Generate comprehensive event plans with timelines, budgets, and logistics.'
_gen_91.category = 'NEWSLETTERS'
_gen_91.icon = 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2'
_gen_91.meta_title = 'AI Event Planning Generator - Free AI Writing Tool | WritingBot.ai'
_gen_91.meta_description = 'Generate comprehensive event plans with timelines, budgets, and logistics.'
_gen_91.fields = [{"name": "event_name", "label": "Event Name", "type": "text", "required": true, "placeholder": "Name of the event"}, {"name": "event_type", "label": "Event Type", "type": "select", "required": true, "placeholder": "", "options": ["Conference", "Workshop", "Webinar", "Corporate Event", "Wedding", "Birthday Party", "Fundraiser", "Product Launch", "Team Building"]}, {"name": "budget", "label": "Budget", "type": "text", "required": false, "placeholder": "e.g. $5,000, $50,000"}, {"name": "attendees", "label": "Expected Attendees", "type": "number", "required": false, "placeholder": "100"}]
_gen_91.system_prompt = 'You are a professional event planner. Create a comprehensive event plan including: Event Overview, Timeline (pre-event, day-of, post-event), Budget Breakdown, Venue Requirements, Vendor List, Marketing Plan, Day-of Schedule, Staffing Needs, Risk Mitigation, and Success Metrics. Event: {event_name}. Type: {event_type}. Budget: {budget}. Attendees: {attendees}. Output ONLY the event plan.'

_gen_92 = BaseGenerator()
_gen_92.slug = 'ai-api-documentation-generator'
_gen_92.name = 'AI API Documentation Generator'
_gen_92.description = 'Generate clear API documentation with endpoints, parameters, and code examples.'
_gen_92.category = 'TECHNICAL'
_gen_92.icon = 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'
_gen_92.meta_title = 'AI API Documentation Generator - Free AI Writing Tool | WritingBot.ai'
_gen_92.meta_description = 'Generate clear API documentation with endpoints, parameters, and code examples.'
_gen_92.fields = [{"name": "api_name", "label": "API Name", "type": "text", "required": true, "placeholder": "Name of your API"}, {"name": "endpoints", "label": "Endpoints", "type": "textarea", "required": true, "placeholder": "List your API endpoints, methods, and what they do..."}, {"name": "auth_method", "label": "Authentication", "type": "select", "required": false, "placeholder": "", "options": ["API Key", "OAuth 2.0", "Bearer Token", "Basic Auth", "None"]}, {"name": "base_url", "label": "Base URL", "type": "text", "required": false, "placeholder": "e.g. https://api.example.com/v1"}]
_gen_92.system_prompt = 'You are a technical writer specializing in API documentation. Create clear, developer-friendly API docs including: Overview, Authentication, Base URL, Endpoints with HTTP methods, Request/Response examples in JSON, Parameters table, Error codes, Rate limits, and Code examples in curl and Python. API: {api_name}. Endpoints: {endpoints}. Auth: {auth_method}. Base URL: {base_url}. Output ONLY the documentation.'

_gen_93 = BaseGenerator()
_gen_93.slug = 'ai-prd-generator'
_gen_93.name = 'AI PRD Generator'
_gen_93.description = 'Create detailed Product Requirements Documents for software and product development.'
_gen_93.category = 'TECHNICAL'
_gen_93.icon = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586'
_gen_93.meta_title = 'AI PRD Generator - Free AI Writing Tool | WritingBot.ai'
_gen_93.meta_description = 'Create detailed Product Requirements Documents for software and product development.'
_gen_93.fields = [{"name": "product_name", "label": "Product Name", "type": "text", "required": true, "placeholder": "Name of the product/feature"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "What is the product/feature? What problem does it solve?"}, {"name": "target_users", "label": "Target Users", "type": "textarea", "required": false, "placeholder": "Who will use this product/feature?"}, {"name": "success_metrics", "label": "Success Metrics", "type": "textarea", "required": false, "placeholder": "How will you measure success?"}]
_gen_93.system_prompt = 'You are a product manager. Write a detailed PRD including: Product Overview, Problem Statement, Goals & Success Metrics, User Personas, User Stories, Functional Requirements, Non-Functional Requirements, Wireframe descriptions, Technical Considerations, Timeline, Dependencies, and Open Questions. Product: {product_name}. Description: {description}. Users: {target_users}. Metrics: {success_metrics}. Output ONLY the PRD.'

_gen_94 = BaseGenerator()
_gen_94.slug = 'ai-release-notes-generator'
_gen_94.name = 'AI Release Notes Generator'
_gen_94.description = 'Write clear, user-friendly release notes for software updates and product launches.'
_gen_94.category = 'TECHNICAL'
_gen_94.icon = 'M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8'
_gen_94.meta_title = 'AI Release Notes Generator - Free AI Writing Tool | WritingBot.ai'
_gen_94.meta_description = 'Write clear, user-friendly release notes for software updates and product launches.'
_gen_94.fields = [{"name": "product_name", "label": "Product Name", "type": "text", "required": true, "placeholder": "Name of the product"}, {"name": "version", "label": "Version Number", "type": "text", "required": true, "placeholder": "e.g. 2.5.0"}, {"name": "changes", "label": "Changes", "type": "textarea", "required": true, "placeholder": "List new features, improvements, bug fixes..."}, {"name": "audience", "label": "Audience", "type": "select", "required": false, "placeholder": "", "options": ["End Users", "Developers", "Both"]}]
_gen_94.system_prompt = 'You are a technical writer. Write clear, organized release notes including: Version number and date, Highlights/Summary, New Features with descriptions, Improvements/Enhancements, Bug Fixes, Breaking Changes (if any), Known Issues, and Upgrade instructions. Product: {product_name}. Version: {version}. Changes: {changes}. Audience: {audience}. Output ONLY the release notes.'

_gen_95 = BaseGenerator()
_gen_95.slug = 'ai-user-manual-generator'
_gen_95.name = 'AI User Manual Generator'
_gen_95.description = 'Create comprehensive user manuals and guides with step-by-step instructions.'
_gen_95.category = 'TECHNICAL'
_gen_95.icon = 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5'
_gen_95.meta_title = 'AI User Manual Generator - Free AI Writing Tool | WritingBot.ai'
_gen_95.meta_description = 'Create comprehensive user manuals and guides with step-by-step instructions.'
_gen_95.fields = [{"name": "product_name", "label": "Product Name", "type": "text", "required": true, "placeholder": "Name of the product/software"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "What does the product do? Key features and workflows..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Who is the manual for?"}, {"name": "sections", "label": "Sections to Include", "type": "textarea", "required": false, "placeholder": "e.g. Installation, Getting Started, Features, Troubleshooting"}]
_gen_95.system_prompt = 'You are a technical writer. Create a comprehensive user manual including: Table of Contents, Introduction, Getting Started/Setup, Core Features walkthrough, Step-by-step instructions with clear formatting, Tips & Best Practices, Troubleshooting, FAQ, and Glossary. Product: {product_name}. Description: {description}. Audience: {audience}. Sections: {sections}. Output ONLY the manual.'

_gen_96 = BaseGenerator()
_gen_96.slug = 'ai-process-documentation-generator'
_gen_96.name = 'AI Process Documentation Generator'
_gen_96.description = 'Document business processes with flowcharts, steps, and role assignments.'
_gen_96.category = 'TECHNICAL'
_gen_96.icon = 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5z'
_gen_96.meta_title = 'AI Process Documentation Generator - Free AI Writing Tool | WritingBot.ai'
_gen_96.meta_description = 'Document business processes with flowcharts, steps, and role assignments.'
_gen_96.fields = [{"name": "process_name", "label": "Process Name", "type": "text", "required": true, "placeholder": "Name of the process"}, {"name": "description", "label": "Description", "type": "textarea", "required": true, "placeholder": "Describe the process from start to finish..."}, {"name": "department", "label": "Department/Team", "type": "text", "required": false, "placeholder": "e.g. Engineering, Sales, Support"}, {"name": "stakeholders", "label": "Stakeholders", "type": "text", "required": false, "placeholder": "e.g. Developers, QA, Product Manager"}]
_gen_96.system_prompt = 'You are a business analyst and process documentation expert. Create detailed process documentation including: Process Overview, Purpose & Scope, Roles & Responsibilities, Prerequisites, Step-by-Step Process Flow with decision points, Inputs & Outputs, Exceptions & Edge Cases, SLA/Timeline, Tools Used, and Process Metrics. Process: {process_name}. Description: {description}. Department: {department}. Stakeholders: {stakeholders}. Output ONLY the documentation.'

_gen_97 = BaseGenerator()
_gen_97.slug = 'ai-troubleshooting-guide-generator'
_gen_97.name = 'AI Troubleshooting Guide Generator'
_gen_97.description = 'Create systematic troubleshooting guides to help users resolve common issues.'
_gen_97.category = 'TECHNICAL'
_gen_97.icon = 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573'
_gen_97.meta_title = 'AI Troubleshooting Guide Generator - Free AI Writing Tool | WritingBot.ai'
_gen_97.meta_description = 'Create systematic troubleshooting guides to help users resolve common issues.'
_gen_97.fields = [{"name": "product_name", "label": "Product/System Name", "type": "text", "required": true, "placeholder": "What product or system?"}, {"name": "common_issues", "label": "Common Issues", "type": "textarea", "required": true, "placeholder": "List the common problems users encounter..."}, {"name": "audience", "label": "Target Audience", "type": "text", "required": false, "placeholder": "Technical level of the reader"}, {"name": "environment", "label": "Environment", "type": "text", "required": false, "placeholder": "e.g. Windows, macOS, Web, Cloud"}]
_gen_97.system_prompt = 'You are a technical support specialist. Create a comprehensive troubleshooting guide with: Introduction, Quick Fixes section, Issue-by-issue troubleshooting (Symptom, Possible Causes, Step-by-Step Solution, Prevention), Error Code reference if applicable, Escalation procedures, and Contact support info placeholder. Product: {product_name}. Issues: {common_issues}. Audience: {audience}. Environment: {environment}. Output ONLY the guide.'


GENERATOR_REGISTRY = {
    'ai-essay-writer': _gen_0,
    'ai-thesis-statement-generator': _gen_1,
    'ai-research-paper-writer': _gen_2,
    'ai-conclusion-writer': _gen_3,
    'ai-abstract-generator': _gen_4,
    'ai-discussion-post-generator': _gen_5,
    'ai-case-study-generator': _gen_6,
    'ai-study-guide-maker': _gen_7,
    'ai-lesson-plan-generator': _gen_8,
    'ai-quiz-maker': _gen_9,
    'ai-business-plan-generator': _gen_10,
    'ai-project-proposal-generator': _gen_11,
    'ai-executive-summary-generator': _gen_12,
    'ai-meeting-agenda-generator': _gen_13,
    'ai-sop-writer': _gen_14,
    'ai-scope-of-work-generator': _gen_15,
    'ai-memo-writer': _gen_16,
    'ai-status-report-generator': _gen_17,
    'ai-offer-letter-generator': _gen_18,
    'ai-job-description-generator': _gen_19,
    'ai-ad-copy-generator': _gen_20,
    'ai-sales-pitch-generator': _gen_21,
    'ai-product-description-generator': _gen_22,
    'ai-slogan-generator': _gen_23,
    'ai-tagline-generator': _gen_24,
    'ai-press-release-generator': _gen_25,
    'ai-landing-page-copy-generator': _gen_26,
    'ai-product-name-generator': _gen_27,
    'ai-product-launch-generator': _gen_28,
    'ai-product-promotion-generator': _gen_29,
    'ai-discount-promotion-generator': _gen_30,
    'ai-event-promotion-generator': _gen_31,
    'ai-email-writer': _gen_32,
    'ai-cold-email-generator': _gen_33,
    'ai-sales-email-generator': _gen_34,
    'ai-marketing-email-generator': _gen_35,
    'ai-follow-up-email-generator': _gen_36,
    'ai-welcome-email-generator': _gen_37,
    'ai-outreach-email-generator': _gen_38,
    'ai-cold-outreach-generator': _gen_39,
    'ai-social-media-post-generator': _gen_40,
    'ai-instagram-caption-generator': _gen_41,
    'ai-instagram-bio-generator': _gen_42,
    'ai-linkedin-summary-generator': _gen_43,
    'ai-youtube-description-generator': _gen_44,
    'ai-tiktok-script-generator': _gen_45,
    'ai-caption-generator': _gen_46,
    'ai-hashtag-generator': _gen_47,
    'ai-bio-generator': _gen_48,
    'ai-short-bio-generator': _gen_49,
    'ai-story-generator': _gen_50,
    'ai-short-story-generator': _gen_51,
    'ai-horror-story-generator': _gen_52,
    'ai-romance-story-generator': _gen_53,
    'ai-plot-generator': _gen_54,
    'ai-dialogue-generator': _gen_55,
    'ai-character-name-generator': _gen_56,
    'ai-book-title-generator': _gen_57,
    'ai-poem-generator': _gen_58,
    'ai-lyric-generator': _gen_59,
    'ai-rap-generator': _gen_60,
    'ai-script-generator': _gen_61,
    'ai-cover-letter-generator': _gen_62,
    'ai-resignation-letter-writer': _gen_63,
    'ai-letter-of-recommendation-generator': _gen_64,
    'ai-letter-generator': _gen_65,
    'ai-resume-writer': _gen_66,
    'ai-job-posting-generator': _gen_67,
    'ai-job-summary-generator': _gen_68,
    'ai-student-reference-letter-generator': _gen_69,
    'ai-blog-post-generator': _gen_70,
    'ai-article-rewriter': _gen_71,
    'ai-paragraph-generator': _gen_72,
    'ai-text-generator': _gen_73,
    'ai-content-idea-generator': _gen_74,
    'ai-meta-description-generator': _gen_75,
    'ai-seo-title-generator': _gen_76,
    'ai-title-generator': _gen_77,
    'ai-keyword-generator': _gen_78,
    'ai-listicle-generator': _gen_79,
    'ai-prompt-generator': _gen_80,
    'ai-writing-prompt-generator': _gen_81,
    'ai-random-prompt-generator': _gen_82,
    'ai-faq-generator': _gen_83,
    'ai-checklist-generator': _gen_84,
    'ai-to-do-list-generator': _gen_85,
    'ai-acronym-generator': _gen_86,
    'ai-simplified-explanation-generator': _gen_87,
    'ai-weekly-newsletter-generator': _gen_88,
    'ai-industry-newsletter-generator': _gen_89,
    'ai-event-invitation-generator': _gen_90,
    'ai-event-planning-generator': _gen_91,
    'ai-api-documentation-generator': _gen_92,
    'ai-prd-generator': _gen_93,
    'ai-release-notes-generator': _gen_94,
    'ai-user-manual-generator': _gen_95,
    'ai-process-documentation-generator': _gen_96,
    'ai-troubleshooting-guide-generator': _gen_97,
}
