"""
Management command to seed courses with educational writing content.
Usage: python manage.py seed_courses
"""
from django.core.management.base import BaseCommand
from courses.models import Course, Chapter


COURSES = [
    {
        'title': 'Introduction to Academic Writing',
        'category': 'Academic Writing',
        'description': 'Learn the fundamentals of academic writing, from essay structure to research integration. Perfect for college freshmen and ESL students.',
        'chapters': [
            {'title': 'What Is Academic Writing?', 'content': """<h2>Understanding Academic Writing</h2>
<p>Academic writing is formal, structured writing used in universities, research journals, and professional scholarly contexts. It differs from casual or creative writing in several key ways.</p>
<h3>Key Characteristics</h3>
<ul>
<li><strong>Formal tone:</strong> Avoid slang, contractions, and colloquialisms</li>
<li><strong>Evidence-based:</strong> Claims are supported by research and citations</li>
<li><strong>Structured:</strong> Follows established formats (introduction, body, conclusion)</li>
<li><strong>Objective:</strong> Presents balanced analysis rather than personal opinion</li>
<li><strong>Precise:</strong> Uses specific, unambiguous language</li>
</ul>
<h3>Types of Academic Writing</h3>
<p>The four main types are: <strong>descriptive</strong> (reports facts), <strong>analytical</strong> (compares and evaluates), <strong>persuasive</strong> (argues a position), and <strong>critical</strong> (evaluates others' work). Most academic papers combine multiple types.</p>
<h3>Common Academic Formats</h3>
<p>You'll encounter essays, research papers, literature reviews, lab reports, case studies, and dissertations. Each has its own conventions, but they share the same foundational principles of clarity, evidence, and structure.</p>"""},
            {'title': 'Essay Structure and Organization', 'content': """<h2>The Five-Paragraph Essay and Beyond</h2>
<p>While the five-paragraph essay (introduction, three body paragraphs, conclusion) is a useful starting framework, most academic writing requires more sophisticated organization.</p>
<h3>Introduction</h3>
<p>An effective introduction moves from general to specific: start with context, narrow to your topic, and end with your thesis statement. The thesis is your paper's central argument—the claim your entire essay supports.</p>
<h3>Body Paragraphs</h3>
<p>Each body paragraph should focus on one main idea that supports your thesis. Use the TEEL structure:</p>
<ol>
<li><strong>Topic sentence:</strong> States the paragraph's main point</li>
<li><strong>Explanation:</strong> Elaborates on the topic sentence</li>
<li><strong>Evidence:</strong> Provides supporting quotes, data, or examples</li>
<li><strong>Link:</strong> Connects back to your thesis or transitions to the next point</li>
</ol>
<h3>Conclusion</h3>
<p>Your conclusion should synthesize (not just summarize) your argument. Restate your thesis in light of the evidence presented, discuss implications, and suggest areas for further research or action. Never introduce new evidence in the conclusion.</p>"""},
            {'title': 'Developing a Strong Thesis Statement', 'content': """<h2>The Thesis: Your Paper's Foundation</h2>
<p>A thesis statement is a concise summary of the main argument or claim of your paper. It typically appears at the end of your introduction and guides the entire essay.</p>
<h3>Characteristics of a Strong Thesis</h3>
<ul>
<li><strong>Specific:</strong> Addresses a particular aspect of the topic, not everything about it</li>
<li><strong>Arguable:</strong> Makes a claim that someone could reasonably disagree with</li>
<li><strong>Evidence-based:</strong> Can be supported with research and data</li>
<li><strong>Focused:</strong> Narrow enough to cover thoroughly in your paper's length</li>
</ul>
<h3>Building a Thesis</h3>
<p>Start with a question about your topic. Research and form an answer. Refine that answer into a clear, specific claim. Test it: Is it arguable? Is it specific? Can you support it?</p>
<h3>Examples</h3>
<p><strong>Weak:</strong> "Social media affects society." (Too vague, not arguable)</p>
<p><strong>Better:</strong> "Instagram's algorithm-driven content recommendations contribute to body image disorders among teenage girls, suggesting the need for platform transparency regulations." (Specific, arguable, evidence-based)</p>"""},
            {'title': 'Research Skills and Source Evaluation', 'content': """<h2>Finding and Evaluating Sources</h2>
<p>Good academic writing relies on credible, relevant sources. Learning to find and evaluate sources is a critical skill.</p>
<h3>Where to Find Academic Sources</h3>
<ul>
<li><strong>Google Scholar:</strong> Free academic search engine</li>
<li><strong>Library databases:</strong> JSTOR, EBSCO, ProQuest, PubMed</li>
<li><strong>University library:</strong> Access to journals, books, and interlibrary loans</li>
<li><strong>Reference lists:</strong> Follow citations from relevant papers you've already found</li>
</ul>
<h3>Evaluating Source Credibility (CRAAP Test)</h3>
<ol>
<li><strong>Currency:</strong> Is the information recent enough for your topic?</li>
<li><strong>Relevance:</strong> Does it directly relate to your research question?</li>
<li><strong>Authority:</strong> Who wrote it? What are their credentials?</li>
<li><strong>Accuracy:</strong> Is the information supported by evidence?</li>
<li><strong>Purpose:</strong> Why was it written? Is there bias?</li>
</ol>
<h3>Primary vs. Secondary Sources</h3>
<p><strong>Primary sources</strong> are original materials (research studies, historical documents, interviews). <strong>Secondary sources</strong> analyze or interpret primary sources (review articles, textbooks, commentary). Strong academic papers use both.</p>"""},
            {'title': 'Citation and Referencing Basics', 'content': """<h2>Why and How to Cite Sources</h2>
<p>Citations give credit to original authors, allow readers to find your sources, and demonstrate the depth of your research. Failing to cite properly constitutes plagiarism.</p>
<h3>In-Text Citations</h3>
<p>In-text citations appear within your text and point to entries in your reference list. The format depends on your citation style:</p>
<ul>
<li><strong>APA:</strong> (Author, Year) — Example: (Smith, 2024)</li>
<li><strong>MLA:</strong> (Author Page) — Example: (Smith 42)</li>
<li><strong>Chicago:</strong> Footnotes or (Author Year) depending on the system</li>
</ul>
<h3>When to Cite</h3>
<p>Cite whenever you use someone else's ideas, data, or words—whether you're quoting directly, paraphrasing, or summarizing. The only exception is common knowledge (facts that are widely known and easily verified).</p>
<h3>Building a Reference List</h3>
<p>Your reference list (or Works Cited or Bibliography) provides full details for every source cited in your paper. Entries are typically alphabetized by author's last name. Use a <a href="/citation-generator/">citation generator</a> to ensure proper formatting.</p>"""},
            {'title': 'Revision, Editing, and Proofreading', 'content': """<h2>The Multi-Stage Revision Process</h2>
<p>Good writing is rewriting. The revision process has three distinct stages, each focusing on different aspects of your paper.</p>
<h3>Stage 1: Revision (Big Picture)</h3>
<ul>
<li>Does your thesis still hold after writing the paper?</li>
<li>Is your argument logical and well-organized?</li>
<li>Is each paragraph necessary and in the right place?</li>
<li>Are transitions smooth between paragraphs and sections?</li>
<li>Have you addressed potential counterarguments?</li>
</ul>
<h3>Stage 2: Editing (Sentence Level)</h3>
<ul>
<li>Are sentences clear and concise?</li>
<li>Is your word choice precise?</li>
<li>Have you varied sentence length and structure?</li>
<li>Is the tone consistent and appropriate?</li>
</ul>
<h3>Stage 3: Proofreading (Surface Level)</h3>
<ul>
<li>Spelling, grammar, and punctuation errors</li>
<li>Formatting consistency (headings, margins, spacing)</li>
<li>Citation format accuracy</li>
<li>Page numbers and headers</li>
</ul>
<p>Use a <a href="/grammar-check/">grammar checker</a> for automated proofreading, but always follow up with a manual review.</p>"""},
        ]
    },
    {
        'title': 'Grammar Essentials',
        'category': 'Grammar',
        'description': 'Master English grammar fundamentals including parts of speech, sentence structure, punctuation, and common errors.',
        'chapters': [
            {'title': 'Parts of Speech Overview', 'content': """<h2>The Eight Parts of Speech</h2>
<p>Every English word belongs to at least one part of speech. Understanding these categories is fundamental to grammar mastery.</p>
<h3>Nouns</h3>
<p>Name people, places, things, or ideas. Types include common (dog), proper (London), abstract (freedom), collective (team), and compound (toothbrush).</p>
<h3>Verbs</h3>
<p>Express actions (run, write) or states of being (is, seem). Verbs have tense (past, present, future), voice (active, passive), and mood (indicative, imperative, subjunctive).</p>
<h3>Adjectives and Adverbs</h3>
<p>Adjectives modify nouns (the <em>red</em> car). Adverbs modify verbs, adjectives, or other adverbs (she runs <em>quickly</em>). A common error is using adjectives where adverbs are needed: "She did good" should be "She did well."</p>
<h3>Pronouns, Prepositions, Conjunctions, Interjections</h3>
<p><strong>Pronouns</strong> replace nouns (he, she, they). <strong>Prepositions</strong> show relationships (in, on, between). <strong>Conjunctions</strong> connect words or clauses (and, but, because). <strong>Interjections</strong> express emotion (wow, ouch).</p>"""},
            {'title': 'Subject-Verb Agreement', 'content': """<h2>Making Subjects and Verbs Agree</h2>
<p>The most basic grammar rule: singular subjects take singular verbs, plural subjects take plural verbs. Simple in principle, tricky in practice.</p>
<h3>Basic Rule</h3>
<p>"The dog <strong>runs</strong>" (singular) vs. "The dogs <strong>run</strong>" (plural).</p>
<h3>Tricky Cases</h3>
<ul>
<li><strong>Prepositional phrases:</strong> "The box of chocolates <strong>is</strong> on the table." (Subject is "box," not "chocolates")</li>
<li><strong>Compound subjects with "and":</strong> "Tom and Jerry <strong>are</strong> friends." (Plural)</li>
<li><strong>Compound subjects with "or"/"nor":</strong> "Neither the teacher nor the students <strong>were</strong> ready." (Verb agrees with nearest subject)</li>
<li><strong>Collective nouns:</strong> "The team <strong>is</strong> winning" (acting as one) vs. "The team <strong>are</strong> arguing among themselves" (acting individually)</li>
<li><strong>Indefinite pronouns:</strong> Everyone, anybody, each, either, neither — all take singular verbs</li>
</ul>"""},
            {'title': 'Punctuation Mastery', 'content': """<h2>Essential Punctuation Rules</h2>
<h3>Commas</h3>
<p>Use commas: after introductory elements, between items in a list, before coordinating conjunctions in compound sentences, and around nonessential information.</p>
<h3>Semicolons</h3>
<p>Use semicolons to connect two related independent clauses: "I love writing; it helps me think clearly." Also use them in complex lists where items contain commas.</p>
<h3>Colons</h3>
<p>Use colons to introduce lists, explanations, or elaborations: "She had one goal: graduation." The clause before a colon must be a complete sentence.</p>
<h3>Apostrophes</h3>
<p>Use for contractions (don't, it's) and possession (Sarah's book, the dogs' bones). Remember: "its" (possessive) has no apostrophe; "it's" always means "it is."</p>
<h3>Quotation Marks</h3>
<p>Use double quotes for direct speech and titles of short works. Periods and commas go inside quotation marks in American English. Semicolons and colons go outside.</p>"""},
            {'title': 'Common Grammar Mistakes', 'content': """<h2>Errors to Watch For</h2>
<h3>Their/There/They're</h3>
<p><strong>Their:</strong> possessive (their car). <strong>There:</strong> location (over there). <strong>They're:</strong> contraction of "they are."</p>
<h3>Your/You're</h3>
<p><strong>Your:</strong> possessive (your book). <strong>You're:</strong> contraction of "you are."</p>
<h3>Affect/Effect</h3>
<p><strong>Affect:</strong> verb meaning to influence. <strong>Effect:</strong> noun meaning result. Exception: "effect" as a verb means to bring about ("effect change").</p>
<h3>Who/Whom</h3>
<p><strong>Who:</strong> subject (who wrote this?). <strong>Whom:</strong> object (to whom did you speak?). Trick: if you can answer with "him," use "whom."</p>
<h3>Dangling Modifiers</h3>
<p><strong>Wrong:</strong> "Walking down the street, the trees were beautiful." (Trees aren't walking.)</p>
<p><strong>Right:</strong> "Walking down the street, I noticed the beautiful trees."</p>
<h3>Run-On Sentences and Comma Splices</h3>
<p>Two independent clauses need proper connection: a period, semicolon, or conjunction with a comma. Never join them with just a comma (comma splice) or nothing at all (run-on).</p>"""},
            {'title': 'Sentence Types and Variety', 'content': """<h2>Writing with Sentence Variety</h2>
<p>Varying sentence length and structure keeps your writing engaging and improves readability.</p>
<h3>Four Sentence Types</h3>
<ul>
<li><strong>Simple:</strong> One independent clause. "The cat sat on the mat."</li>
<li><strong>Compound:</strong> Two independent clauses joined by a conjunction. "The cat sat on the mat, and the dog lay on the floor."</li>
<li><strong>Complex:</strong> One independent clause + one or more dependent clauses. "Although the cat preferred the mat, it sometimes sat on the chair."</li>
<li><strong>Compound-Complex:</strong> Two+ independent clauses + one or more dependent clauses.</li>
</ul>
<h3>Why Variety Matters</h3>
<p>All short sentences feel choppy and immature. All long sentences exhaust readers. Mix them. Use short sentences for emphasis and impact. Use longer sentences for explanation and nuance. The contrast creates rhythm.</p>
<h3>Techniques for Variety</h3>
<ul>
<li>Start sentences with different words (not always "The" or "I")</li>
<li>Use occasional questions or exclamations</li>
<li>Invert sentence order for emphasis: "Never before had she seen such beauty."</li>
</ul>"""},
        ]
    },
    {
        'title': 'Mastering Paraphrasing',
        'category': 'Writing Skills',
        'description': 'Learn professional paraphrasing techniques for academic writing, content creation, and professional communication.',
        'chapters': [
            {'title': 'What Is Paraphrasing and Why It Matters', 'content': """<h2>The Art of Saying It Differently</h2>
<p>Paraphrasing is restating someone else's ideas in your own words while preserving the original meaning. It's a fundamental academic and professional skill.</p>
<h3>Why Paraphrase?</h3>
<ul>
<li><strong>Demonstrates understanding:</strong> You can't paraphrase what you don't understand</li>
<li><strong>Maintains your voice:</strong> Your paper reads as a cohesive argument, not a patchwork of quotes</li>
<li><strong>Integrates sources smoothly:</strong> Paraphrased content flows better than frequent block quotes</li>
<li><strong>Shows critical thinking:</strong> You're processing and reinterpreting information</li>
</ul>
<h3>Paraphrasing vs. Summarizing vs. Quoting</h3>
<p><strong>Paraphrasing</strong> restates a specific passage in your own words (similar length). <strong>Summarizing</strong> condenses a larger work into key points (much shorter). <strong>Quoting</strong> uses the exact original words in quotation marks.</p>
<p>All three require citations. The skill is knowing when to use each.</p>"""},
            {'title': 'Step-by-Step Paraphrasing Method', 'content': """<h2>The Four-Step Method</h2>
<h3>Step 1: Read and Understand</h3>
<p>Read the passage multiple times. Look up any unfamiliar terms. Make sure you can explain the main idea without looking at the text.</p>
<h3>Step 2: Set Aside and Rewrite</h3>
<p>Put the original away. Write the idea from memory in your own words. This forces you to truly process the information rather than just swapping synonyms.</p>
<h3>Step 3: Compare and Adjust</h3>
<p>Compare your version with the original. Check that you've preserved the meaning accurately. Ensure your wording and sentence structure are sufficiently different. A good test: your version should use different sentence structures and at least 60-70% different vocabulary.</p>
<h3>Step 4: Cite</h3>
<p>Always add a citation, even when paraphrasing. Paraphrased content without attribution is still plagiarism.</p>
<h3>Techniques for Changing Structure</h3>
<ul>
<li>Change active to passive voice (or vice versa)</li>
<li>Combine or split sentences</li>
<li>Reorder information (start with the conclusion, then give reasons)</li>
<li>Change parts of speech (nominalize: "analyze" → "analysis")</li>
</ul>"""},
            {'title': 'Common Paraphrasing Mistakes', 'content': """<h2>What NOT to Do</h2>
<h3>Mistake 1: Patchwork Plagiarism</h3>
<p>Simply swapping a few words with synonyms while keeping the same sentence structure. This is the most common form of unintentional plagiarism.</p>
<p><strong>Original:</strong> "The results indicate that regular exercise significantly reduces symptoms of depression."</p>
<p><strong>Bad:</strong> "The findings show that consistent physical activity substantially decreases signs of depression." (Same structure, just synonym swaps)</p>
<p><strong>Good:</strong> "Depression symptoms showed marked improvement in participants who maintained consistent exercise routines, according to the study's findings."</p>
<h3>Mistake 2: Forgetting to Cite</h3>
<p>Even perfectly paraphrased content needs a citation. The ideas still belong to the original author.</p>
<h3>Mistake 3: Changing the Meaning</h3>
<p>In the effort to use different words, some writers accidentally distort the original meaning. Always verify accuracy after paraphrasing.</p>
<h3>Mistake 4: Over-Paraphrasing</h3>
<p>Sometimes a direct quote is better, especially for technical definitions, famous phrases, or when the original wording is particularly powerful or precise.</p>"""},
            {'title': 'Paraphrasing in Different Contexts', 'content': """<h2>Adapting Your Approach</h2>
<h3>Academic Papers</h3>
<p>Focus on accuracy and proper citation. Integrate paraphrased content smoothly into your argument. Use signal phrases: "According to Smith (2024)..." or "As research has shown..."</p>
<h3>Professional Writing</h3>
<p>When summarizing reports, competitor content, or industry research, paraphrasing helps you present information in your company's voice while adding your own analysis.</p>
<h3>Content Creation</h3>
<p>Bloggers and content writers frequently paraphrase industry news and research findings. Always add original analysis, examples, or perspectives beyond just rewording the source.</p>
<h3>Using AI Paraphrasing Tools</h3>
<p>Tools like our <a href="/paraphrasing-tool/">paraphrasing tool</a> can help generate alternative phrasings, but always review and refine the output. Use AI suggestions as a starting point, not a final product.</p>"""},
        ]
    },
    {
        'title': 'Citation Styles Explained',
        'category': 'Academic Writing',
        'description': 'Comprehensive guide to APA, MLA, Chicago, and other citation styles with examples and formatting rules.',
        'chapters': [
            {'title': 'Why Citations Matter', 'content': """<h2>The Purpose of Citations</h2>
<p>Citations serve multiple essential functions in academic and professional writing.</p>
<h3>Giving Credit</h3>
<p>Citations acknowledge the intellectual contributions of others. Using someone's ideas without attribution is plagiarism, regardless of whether you quote directly or paraphrase.</p>
<h3>Building Credibility</h3>
<p>Citations show that your arguments are supported by established research. They demonstrate the depth and breadth of your research.</p>
<h3>Enabling Verification</h3>
<p>Citations allow readers to find and verify your sources, evaluate the evidence themselves, and explore the topic further.</p>
<h3>Contributing to Scholarly Conversation</h3>
<p>Academic writing is a conversation among scholars. Citations position your work within existing research and show how it extends or challenges previous findings.</p>"""},
            {'title': 'APA Style (7th Edition)', 'content': """<h2>APA Citation Format</h2>
<p>APA is the standard for social sciences, psychology, education, and business writing.</p>
<h3>In-Text Citations</h3>
<p><strong>Parenthetical:</strong> (Smith, 2024) or (Smith & Jones, 2024)</p>
<p><strong>Narrative:</strong> Smith (2024) found that...</p>
<p><strong>3+ authors:</strong> (Smith et al., 2024) from the first citation</p>
<h3>Reference List Entry: Book</h3>
<p>Author, A. A. (Year). <em>Title of work: Capital of subtitle</em>. Publisher.</p>
<p>Example: Johnson, M. (2024). <em>Modern writing techniques</em>. Academic Press.</p>
<h3>Reference List Entry: Journal Article</h3>
<p>Author, A. A. (Year). Title of article. <em>Title of Periodical, Volume</em>(Issue), Pages. DOI</p>
<h3>Key APA 7th Edition Changes</h3>
<ul>
<li>Up to 20 authors listed (previously 7)</li>
<li>No more "Retrieved from" for URLs</li>
<li>"et al." from the first citation for 3+ authors</li>
<li>Singular "they" is acceptable</li>
</ul>"""},
            {'title': 'MLA Style (9th Edition)', 'content': """<h2>MLA Citation Format</h2>
<p>MLA is standard for humanities, literature, and liberal arts.</p>
<h3>In-Text Citations</h3>
<p><strong>Parenthetical:</strong> (Smith 42) — author and page number, no comma</p>
<p><strong>Narrative:</strong> Smith argues that "direct quote" (42).</p>
<h3>Works Cited Entry: Book</h3>
<p>Last, First. <em>Title of Book</em>. Publisher, Year.</p>
<p>Example: Johnson, Maria. <em>Modern Writing Techniques</em>. Academic Press, 2024.</p>
<h3>Works Cited Entry: Journal Article</h3>
<p>Last, First. "Article Title." <em>Journal Title</em>, vol. #, no. #, Year, pp. #-#.</p>
<h3>MLA's Container System</h3>
<p>MLA 9th edition uses a "container" concept. A poem might be contained in an anthology, which is contained in a database. Each container level adds information to the citation.</p>"""},
            {'title': 'Chicago Style', 'content': """<h2>Chicago Citation Format</h2>
<p>Chicago offers two systems: Notes-Bibliography (common in humanities and history) and Author-Date (common in sciences).</p>
<h3>Notes-Bibliography System</h3>
<p>Uses footnotes or endnotes for citations, plus a bibliography at the end.</p>
<p><strong>Footnote (first reference):</strong> 1. Maria Johnson, <em>Modern Writing Techniques</em> (New York: Academic Press, 2024), 42.</p>
<p><strong>Shortened footnote:</strong> 2. Johnson, <em>Modern Writing</em>, 55.</p>
<h3>Author-Date System</h3>
<p>Similar to APA: (Johnson 2024, 42) in text, with a reference list.</p>
<h3>When to Use Chicago</h3>
<p>History papers, some humanities fields, book publishing, and when your instructor or publisher specifies it. The notes-bibliography system is particularly useful for papers with extensive commentary on sources.</p>"""},
        ]
    },
    {
        'title': 'Business Writing Fundamentals',
        'category': 'Professional Development',
        'description': 'Master professional business writing including emails, reports, proposals, and presentations.',
        'chapters': [
            {'title': 'Principles of Business Writing', 'content': """<h2>Writing That Gets Results</h2>
<p>Business writing has one job: communicate clearly and prompt action. Every word should serve this purpose.</p>
<h3>The 5 Cs of Business Writing</h3>
<ul>
<li><strong>Clear:</strong> Use simple, direct language. Avoid jargon unless your audience shares it.</li>
<li><strong>Concise:</strong> Say more with fewer words. Cut fluff, redundancies, and filler phrases.</li>
<li><strong>Concrete:</strong> Use specific facts, numbers, and examples instead of vague statements.</li>
<li><strong>Correct:</strong> Proofread for grammar, spelling, and factual accuracy.</li>
<li><strong>Courteous:</strong> Maintain a professional, respectful tone even in difficult communications.</li>
</ul>
<h3>Know Your Audience</h3>
<p>Adjust your tone, detail level, and vocabulary for your reader. An email to your team differs from a report to the board. Technical experts need different language than general audiences.</p>"""},
            {'title': 'Professional Email Writing', 'content': """<h2>Emails That Get Read and Acted On</h2>
<h3>Subject Lines</h3>
<p>Your subject line determines open rates. Be specific and action-oriented: "Q3 Budget Approval Needed by Friday" > "Budget."</p>
<h3>Structure</h3>
<ol>
<li><strong>Greeting:</strong> Match formality to your relationship</li>
<li><strong>Purpose:</strong> State why you're writing in the first sentence</li>
<li><strong>Details:</strong> Provide necessary context</li>
<li><strong>Action:</strong> State what you need and the deadline</li>
<li><strong>Closing:</strong> Thank them and sign off</li>
</ol>
<h3>Best Practices</h3>
<ul>
<li>One email = one topic. Multiple topics get lost.</li>
<li>Use bullet points for multiple items or questions</li>
<li>Bold or highlight key deadlines and action items</li>
<li>Reply within 24 hours, even if just to acknowledge receipt</li>
<li>Proofread before sending—especially the recipient's name</li>
</ul>"""},
            {'title': 'Reports and Proposals', 'content': """<h2>Writing Persuasive Business Documents</h2>
<h3>Report Structure</h3>
<ul>
<li><strong>Executive summary:</strong> Key findings and recommendations in 1-2 pages</li>
<li><strong>Introduction:</strong> Context, scope, and methodology</li>
<li><strong>Findings:</strong> Data and analysis organized logically</li>
<li><strong>Recommendations:</strong> Specific, actionable next steps</li>
<li><strong>Appendices:</strong> Supporting data, charts, and raw materials</li>
</ul>
<h3>Proposal Writing</h3>
<p>Proposals should answer: What's the problem? What's your solution? Why should they choose you? What will it cost? What's the timeline?</p>
<h3>Tips for Both</h3>
<ul>
<li>Lead with the conclusion or recommendation—busy executives read the top first</li>
<li>Use data visualizations to support key points</li>
<li>Write for scanning: headings, bullet points, bold key phrases</li>
<li>Include a clear call to action</li>
</ul>"""},
            {'title': 'Meeting Notes and Internal Communication', 'content': """<h2>Writing for Internal Audiences</h2>
<h3>Meeting Notes</h3>
<p>Effective meeting notes capture decisions, action items, and key discussion points—not everything that was said.</p>
<ul>
<li>Record: Date, attendees, agenda items covered</li>
<li>Focus on: Decisions made, action items (who does what by when), key points raised</li>
<li>Skip: General discussion, tangents, personal opinions</li>
<li>Distribute within 24 hours while memory is fresh</li>
</ul>
<h3>Slack and Teams Messages</h3>
<ul>
<li>Use threads to keep conversations organized</li>
<li>Be clear about whether something is FYI or requires action</li>
<li>Use @mentions thoughtfully—only tag people who need to see it</li>
<li>Save long or complex topics for email or documents</li>
</ul>"""},
        ]
    },
    {
        'title': 'SEO Content Writing',
        'category': 'Content Marketing',
        'description': 'Learn to write content that ranks in search engines while engaging readers. Covers keyword research, content structure, and optimization.',
        'chapters': [
            {'title': 'Introduction to SEO Writing', 'content': """<h2>Writing for Search Engines and Humans</h2>
<p>SEO writing creates content that ranks well in search engines while providing genuine value to readers. The best SEO content is simply great content that's strategically optimized.</p>
<h3>How Search Engines Work</h3>
<p>Search engines crawl web pages, index their content, and rank them based on relevance and quality signals. Key ranking factors include content quality, keyword relevance, user experience, backlinks, and technical performance.</p>
<h3>The SEO Writer's Goal</h3>
<p>Match your content to what users are searching for (search intent), provide the most comprehensive and helpful answer, and format it so search engines can easily understand and index it.</p>
<h3>Write for Humans First</h3>
<p>Google's algorithms increasingly prioritize content that satisfies user intent. Keyword stuffing and manipulation tactics no longer work. Focus on creating genuinely useful content, then optimize it for discovery.</p>"""},
            {'title': 'Keyword Research Basics', 'content': """<h2>Finding What Your Audience Searches For</h2>
<h3>Types of Keywords</h3>
<ul>
<li><strong>Short-tail:</strong> Broad terms (1-2 words) with high volume and competition: "grammar checker"</li>
<li><strong>Long-tail:</strong> Specific phrases (3+ words) with lower volume but higher intent: "free online grammar checker for essays"</li>
<li><strong>Question keywords:</strong> Natural language queries: "how to check grammar online free"</li>
</ul>
<h3>Search Intent</h3>
<p>Understanding <em>why</em> someone searches is more important than the keyword itself:</p>
<ul>
<li><strong>Informational:</strong> "How to paraphrase" → wants to learn</li>
<li><strong>Navigational:</strong> "WritingBot paraphraser" → looking for a specific tool</li>
<li><strong>Transactional:</strong> "Best paraphrasing tool free" → ready to use</li>
<li><strong>Commercial:</strong> "QuillBot vs WritingBot" → comparing options</li>
</ul>
<h3>Keyword Research Process</h3>
<ol>
<li>Brainstorm seed keywords related to your topic</li>
<li>Use tools to expand your list and find related terms</li>
<li>Analyze search volume and competition</li>
<li>Group keywords by topic and intent</li>
<li>Prioritize based on relevance and opportunity</li>
</ol>"""},
            {'title': 'Content Structure and On-Page SEO', 'content': """<h2>Optimizing Your Content</h2>
<h3>Title Tags</h3>
<p>Your title tag appears in search results. Keep it under 60 characters, include your primary keyword near the beginning, and make it compelling enough to click.</p>
<h3>Meta Descriptions</h3>
<p>The 160-character snippet below your title in search results. Include your keyword, a clear value proposition, and a reason to click.</p>
<h3>Heading Structure</h3>
<ul>
<li><strong>H1:</strong> One per page, contains primary keyword</li>
<li><strong>H2:</strong> Main sections, include secondary keywords</li>
<li><strong>H3:</strong> Subsections under H2s</li>
</ul>
<h3>Content Optimization</h3>
<ul>
<li>Include your primary keyword in the first 100 words</li>
<li>Use related terms and synonyms naturally throughout</li>
<li>Break content into scannable sections (300 words max per section)</li>
<li>Add internal links to related content on your site</li>
<li>Include images with descriptive alt text</li>
<li>Aim for comprehensive coverage of the topic</li>
</ul>"""},
            {'title': 'Writing Engaging Content That Ranks', 'content': """<h2>Quality Signals That Matter</h2>
<h3>E-E-A-T</h3>
<p>Google evaluates content on Experience, Expertise, Authoritativeness, and Trustworthiness. Demonstrate these by citing sources, showing credentials, and providing unique insights.</p>
<h3>User Engagement Signals</h3>
<ul>
<li><strong>Dwell time:</strong> How long users stay on your page</li>
<li><strong>Bounce rate:</strong> Whether users immediately leave</li>
<li><strong>Click-through rate:</strong> How often your listing gets clicked in results</li>
</ul>
<h3>Creating Content That Engages</h3>
<ul>
<li>Open with a hook that addresses the reader's problem</li>
<li>Use storytelling, examples, and data to support points</li>
<li>Break up text with visuals, lists, and pull quotes</li>
<li>Include actionable takeaways readers can implement</li>
<li>End with a clear next step or call to action</li>
</ul>
<p>Use our <a href="/word-counter/">word counter</a> to check readability scores and ensure your content is accessible to your target audience.</p>"""},
        ]
    },
    {
        'title': 'Creative Writing Basics',
        'category': 'Creative Writing',
        'description': 'Explore the fundamentals of creative writing including fiction, poetry, and personal essays.',
        'chapters': [
            {'title': 'Finding Your Creative Voice', 'content': """<h2>Developing Your Unique Style</h2>
<p>Every writer has a unique voice—a combination of word choice, sentence rhythm, perspective, and personality that makes their writing distinctly theirs.</p>
<h3>What Is Voice?</h3>
<p>Voice is the personality that comes through in your writing. It's why you can often identify a favorite author by reading a single paragraph. Voice encompasses tone, diction, syntax, and the types of observations you make.</p>
<h3>How to Find Your Voice</h3>
<ul>
<li><strong>Write regularly:</strong> Voice emerges through practice, not theory</li>
<li><strong>Read widely:</strong> Exposure to different voices helps you discover your own</li>
<li><strong>Write freely:</strong> Freewriting and journaling without self-censorship reveal your natural voice</li>
<li><strong>Experiment:</strong> Try different styles, genres, and perspectives</li>
<li><strong>Be authentic:</strong> Don't try to sound like someone else—let your genuine self show</li>
</ul>"""},
            {'title': 'Story Structure and Plot', 'content': """<h2>Building Compelling Narratives</h2>
<h3>Classic Story Structure</h3>
<ol>
<li><strong>Exposition:</strong> Introduce characters, setting, and the status quo</li>
<li><strong>Rising action:</strong> Complications and conflicts build tension</li>
<li><strong>Climax:</strong> The turning point—highest tension and stakes</li>
<li><strong>Falling action:</strong> Consequences of the climax play out</li>
<li><strong>Resolution:</strong> The new normal is established</li>
</ol>
<h3>Conflict Types</h3>
<ul>
<li><strong>Person vs. Person:</strong> Direct opposition between characters</li>
<li><strong>Person vs. Self:</strong> Internal struggle and personal growth</li>
<li><strong>Person vs. Society:</strong> Individual against social norms or systems</li>
<li><strong>Person vs. Nature:</strong> Survival against natural forces</li>
</ul>
<h3>Plot Tips</h3>
<p>Every scene should serve at least one purpose: advance the plot, reveal character, or build the world. If it does none of these, cut it.</p>"""},
            {'title': 'Character Development', 'content': """<h2>Creating Memorable Characters</h2>
<h3>What Makes a Character Compelling?</h3>
<p>Great characters feel real because they have desires, flaws, contradictions, and growth arcs. They make choices that reveal who they are.</p>
<h3>Character Building Techniques</h3>
<ul>
<li><strong>Give them a goal:</strong> What do they want more than anything?</li>
<li><strong>Give them a flaw:</strong> What holds them back?</li>
<li><strong>Give them a backstory:</strong> What shaped them?</li>
<li><strong>Give them a voice:</strong> How do they speak, think, and see the world?</li>
<li><strong>Make them change:</strong> How are they different at the end of the story?</li>
</ul>
<h3>Show, Don't Tell</h3>
<p>Don't tell readers a character is brave. Show them making a brave choice. Don't say they're kind. Show them helping someone at personal cost. Actions and choices reveal character far more powerfully than description.</p>"""},
            {'title': 'Writing Dialogue', 'content': """<h2>Making Characters Talk</h2>
<h3>Dialogue Serves Multiple Purposes</h3>
<ul>
<li>Reveals character personality and relationships</li>
<li>Advances the plot through information exchange</li>
<li>Creates tension and conflict between characters</li>
<li>Breaks up narrative prose and increases pacing</li>
</ul>
<h3>Writing Natural Dialogue</h3>
<ul>
<li><strong>Listen to real speech</strong> but edit out the "ums" and repetitions</li>
<li><strong>Each character should sound distinct</strong>—vocabulary, sentence length, speech patterns</li>
<li><strong>Use subtext:</strong> What characters don't say is as important as what they do</li>
<li><strong>Avoid exposition dumps:</strong> Don't have characters explain things they would already know</li>
<li><strong>"Said" is invisible:</strong> Use "said" and "asked" most of the time. Fancy alternatives ("exclaimed," "retorted") draw attention away from the dialogue itself</li>
</ul>"""},
        ]
    },
    {
        'title': 'Essay Writing for Students',
        'category': 'Academic Writing',
        'description': 'A practical guide to writing essays for high school and college students covering all major essay types.',
        'chapters': [
            {'title': 'Types of Essays', 'content': """<h2>Understanding Different Essay Types</h2>
<h3>Argumentative Essay</h3>
<p>Takes a position on a controversial topic and supports it with evidence. Requires addressing counterarguments. Most common in college writing.</p>
<h3>Expository Essay</h3>
<p>Explains a topic objectively using facts, statistics, and examples. No personal opinion. Common types include process essays, compare/contrast, and cause/effect.</p>
<h3>Narrative Essay</h3>
<p>Tells a story, usually from personal experience. Uses vivid details, dialogue, and reflection. Common in creative writing and college applications.</p>
<h3>Descriptive Essay</h3>
<p>Paints a picture using sensory details. Focuses on a person, place, object, or experience. Emphasizes showing rather than telling.</p>
<h3>Analytical Essay</h3>
<p>Examines a text, idea, or issue by breaking it into components and evaluating them. Common in literature, film, and social science courses.</p>"""},
            {'title': 'Planning and Outlining', 'content': """<h2>Before You Write</h2>
<h3>Brainstorming Techniques</h3>
<ul>
<li><strong>Freewriting:</strong> Write nonstop for 10 minutes about your topic</li>
<li><strong>Mind mapping:</strong> Visual brainstorm with your topic in the center</li>
<li><strong>Listing:</strong> Write every related idea, then group and prioritize</li>
<li><strong>Questioning:</strong> Ask who, what, when, where, why, how about your topic</li>
</ul>
<h3>Creating an Outline</h3>
<p>A good outline is your essay's skeleton. It ensures logical organization and complete coverage.</p>
<ol>
<li>Write your thesis statement</li>
<li>List 3-5 main points that support your thesis</li>
<li>Under each point, list 2-3 pieces of evidence</li>
<li>Note your introduction hook and conclusion approach</li>
</ol>
<h3>Time Management</h3>
<p>For a typical essay: spend 20% of your time planning, 40% writing the first draft, 20% revising, and 20% editing and proofreading. Don't skip the planning stage—it saves time overall.</p>"""},
            {'title': 'Writing Strong Introductions and Conclusions', 'content': """<h2>First and Last Impressions</h2>
<h3>Introduction Strategies</h3>
<p>Your introduction should grab attention, provide context, and present your thesis. Effective hooks include:</p>
<ul>
<li><strong>Surprising statistic:</strong> "90% of students admit to procrastinating on essays."</li>
<li><strong>Provocative question:</strong> "What if everything you learned about grammar was wrong?"</li>
<li><strong>Brief anecdote:</strong> A relevant story that illustrates your topic</li>
<li><strong>Bold statement:</strong> A claim that challenges conventional thinking</li>
</ul>
<p>Avoid: dictionary definitions, extremely broad opening statements ("Since the dawn of time..."), and announcing your intentions ("In this essay I will...")</p>
<h3>Conclusion Strategies</h3>
<p>Your conclusion should synthesize, not summarize. Restate your thesis in new language, discuss broader implications, and end memorably.</p>
<ul>
<li>Circle back to your opening hook</li>
<li>Pose a thought-provoking question</li>
<li>Call to action</li>
<li>Look toward the future</li>
</ul>"""},
            {'title': 'Revision Strategies for Essays', 'content': """<h2>Turning Good Writing into Great Writing</h2>
<h3>The Revision Mindset</h3>
<p>Revision literally means "seeing again." Put your draft aside for at least a few hours (ideally overnight) before revising. Fresh eyes catch problems that tired eyes miss.</p>
<h3>Big-Picture Revision</h3>
<ul>
<li>Does your thesis clearly state your argument?</li>
<li>Does every paragraph support your thesis?</li>
<li>Are paragraphs in the most logical order?</li>
<li>Have you addressed potential counterarguments?</li>
<li>Is your evidence convincing and well-integrated?</li>
</ul>
<h3>Paragraph-Level Revision</h3>
<ul>
<li>Does each paragraph have a clear topic sentence?</li>
<li>Are transitions smooth between paragraphs?</li>
<li>Is there enough evidence for each claim?</li>
</ul>
<h3>Sentence-Level Editing</h3>
<ul>
<li>Eliminate wordiness and redundancy</li>
<li>Vary sentence length and structure</li>
<li>Replace vague words with specific ones</li>
<li>Check for grammar, spelling, and punctuation</li>
</ul>
<p>Use our <a href="/grammar-check/">grammar checker</a> and <a href="/proofreader/">proofreader</a> to catch surface-level errors after you've completed your content revision.</p>"""},
        ]
    },
    {
        'title': 'Plagiarism Prevention',
        'category': 'Academic Integrity',
        'description': 'Understand plagiarism types, learn prevention strategies, and develop ethical research and writing habits.',
        'chapters': [
            {'title': 'Understanding Plagiarism', 'content': """<h2>What Counts as Plagiarism?</h2>
<p>Plagiarism is presenting someone else's work, ideas, or words as your own. It includes both intentional dishonesty and unintentional failure to cite properly.</p>
<h3>Types of Plagiarism</h3>
<ul>
<li><strong>Direct plagiarism:</strong> Copying text word-for-word without quotation marks and citation</li>
<li><strong>Mosaic/patchwork plagiarism:</strong> Mixing paraphrased content from multiple sources without attribution</li>
<li><strong>Self-plagiarism:</strong> Submitting your own previous work for a new assignment without permission</li>
<li><strong>Accidental plagiarism:</strong> Forgetting to cite, incorrect citation format, or inadequate paraphrasing</li>
<li><strong>Contract cheating:</strong> Having someone else write your work</li>
</ul>
<h3>Why It Matters</h3>
<p>Plagiarism undermines the value of your education, disrespects original authors, and can result in failing grades, academic probation, or expulsion. In professional contexts, it can lead to lawsuits, job loss, and reputational damage.</p>"""},
            {'title': 'Proper Paraphrasing and Quoting', 'content': """<h2>Using Sources Without Plagiarizing</h2>
<h3>When to Quote</h3>
<p>Use direct quotes when the original wording is particularly powerful, precise, or famous. Also quote when you're analyzing the specific language used.</p>
<h3>When to Paraphrase</h3>
<p>Paraphrase when you need the idea but not the exact words. This is appropriate for most source integration in academic writing.</p>
<h3>When to Summarize</h3>
<p>Summarize when you need to convey the overall point of a longer work without getting into details.</p>
<h3>The Key Rule</h3>
<p>All three methods—quoting, paraphrasing, and summarizing—require citations. The only ideas that don't need citations are your own original thoughts and common knowledge.</p>
<h3>Common Knowledge Test</h3>
<p>If a fact appears in multiple general sources and your audience would likely know it, it's common knowledge: "The Earth orbits the Sun." If it's a specific finding, interpretation, or statistic, cite it.</p>"""},
            {'title': 'Tools and Strategies for Prevention', 'content': """<h2>Practical Prevention Methods</h2>
<h3>Research Organization</h3>
<ul>
<li>Record full bibliographic information for every source from the start</li>
<li>Clearly distinguish between your notes and quoted text</li>
<li>Use quotation marks around any copied text in your notes</li>
<li>Note page numbers for specific ideas and quotes</li>
</ul>
<h3>Writing Strategies</h3>
<ul>
<li>Write your first draft without looking at sources, using only your notes</li>
<li>Add citations immediately as you integrate source material</li>
<li>Use signal phrases to introduce source ideas: "According to Smith..."</li>
<li>After writing, verify every paraphrase against the original</li>
</ul>
<h3>Technology Tools</h3>
<ul>
<li>Use a <a href="/citation-generator/">citation generator</a> for proper formatting</li>
<li>Run your paper through a <a href="/plagiarism-checker/">plagiarism checker</a> before submission</li>
<li>Use reference management software to organize sources</li>
</ul>"""},
        ]
    },
    {
        'title': 'AI Writing Tools: A Practical Guide',
        'category': 'Technology',
        'description': 'Learn to use AI writing tools effectively and ethically for academic, professional, and creative writing.',
        'chapters': [
            {'title': 'Overview of AI Writing Tools', 'content': """<h2>The AI Writing Toolkit</h2>
<p>AI writing tools have become essential aids for modern writers. Understanding what each type does helps you choose the right tool for each task.</p>
<h3>Types of AI Writing Tools</h3>
<ul>
<li><strong>Paraphrasers:</strong> Rephrase text in different styles and tones. Great for finding alternative ways to express ideas.</li>
<li><strong>Grammar checkers:</strong> Identify and fix grammatical errors, suggest style improvements, and enhance clarity.</li>
<li><strong>Summarizers:</strong> Condense long articles, papers, or documents into key points.</li>
<li><strong>AI content detectors:</strong> Analyze text to determine if it was likely written by AI.</li>
<li><strong>AI humanizers:</strong> Transform AI-generated text to sound more naturally written.</li>
<li><strong>Citation generators:</strong> Automatically format references in APA, MLA, Chicago, and other styles.</li>
<li><strong>Content generators:</strong> Create drafts for emails, essays, blog posts, and other content types.</li>
</ul>"""},
            {'title': 'Using AI Tools Ethically', 'content': """<h2>Ethics and Best Practices</h2>
<h3>The Ethics Framework</h3>
<p>Ethical AI use comes down to transparency, honesty, and adding genuine value. Ask yourself: Would you be comfortable if your professor, editor, or client knew exactly how you used AI?</p>
<h3>Generally Acceptable Uses</h3>
<ul>
<li>Grammar and spelling correction</li>
<li>Brainstorming and outlining</li>
<li>Exploring alternative phrasings</li>
<li>Formatting citations</li>
<li>Checking readability</li>
</ul>
<h3>Generally Unacceptable Uses</h3>
<ul>
<li>Submitting AI-generated text as your own original work</li>
<li>Using AI to write academic papers without disclosure</li>
<li>Disguising AI output to avoid detection</li>
</ul>
<h3>Check Your Institution's Policy</h3>
<p>Policies vary widely. Some schools ban all AI use, others allow it with disclosure, and some encourage it. Always check and follow your specific institution's guidelines.</p>"""},
            {'title': 'AI-Assisted Writing Workflow', 'content': """<h2>Integrating AI Into Your Process</h2>
<h3>The Human-First Workflow</h3>
<ol>
<li><strong>Research:</strong> Gather sources and take notes (human task)</li>
<li><strong>Outline:</strong> Organize your argument (AI can help brainstorm)</li>
<li><strong>Draft:</strong> Write the first draft yourself</li>
<li><strong>Polish:</strong> Use AI for grammar, style, and readability improvements</li>
<li><strong>Verify:</strong> Check citations and run plagiarism detection</li>
<li><strong>Finalize:</strong> Make final human judgment on all changes</li>
</ol>
<h3>Tips for Effective AI Use</h3>
<ul>
<li>Use AI suggestions as starting points, not final products</li>
<li>Always review and approve every AI-suggested change</li>
<li>Maintain your unique voice and perspective</li>
<li>Use AI to handle mechanical tasks so you can focus on thinking</li>
<li>Combine multiple tools: paraphraser for alternatives, grammar checker for correctness, and summarizer for research</li>
</ul>
<p>Try our suite of tools: <a href="/paraphrasing-tool/">paraphraser</a>, <a href="/grammar-check/">grammar checker</a>, <a href="/summarize/">summarizer</a>, and <a href="/ai-writing-tools/">100+ AI writing generators</a>.</p>"""},
        ]
    },
    {
        'title': 'Writing for the Web',
        'category': 'Content Marketing',
        'description': 'Learn web writing principles including readability, scanning patterns, and engagement techniques for online audiences.',
        'chapters': [
            {'title': 'How People Read Online', 'content': """<h2>Web Reading Behavior</h2>
<p>People read web content differently than print. Understanding these patterns helps you write more effectively for online audiences.</p>
<h3>The F-Pattern</h3>
<p>Eye-tracking studies show web readers scan in an F-shape: they read the first few lines across, then scan down the left side. This means your most important information should be at the top and left of your content.</p>
<h3>Scanning, Not Reading</h3>
<p>Most web visitors scan rather than read word-by-word. They look for headings, bold text, links, and bullet points. Only 16% of users read web content word-for-word.</p>
<h3>Implications for Writers</h3>
<ul>
<li>Front-load important information (inverted pyramid)</li>
<li>Use descriptive headings that communicate key points</li>
<li>Break content into short, scannable sections</li>
<li>Use formatting (bold, bullets, numbered lists) to highlight key information</li>
<li>One idea per paragraph, ideally 2-3 sentences</li>
</ul>"""},
            {'title': 'Writing Headlines and Hooks', 'content': """<h2>Getting Clicks and Keeping Readers</h2>
<h3>Headline Formulas That Work</h3>
<ul>
<li><strong>Numbers:</strong> "7 Ways to Improve Your Writing Today"</li>
<li><strong>How-to:</strong> "How to Write a Resume That Gets Interviews"</li>
<li><strong>Question:</strong> "Are You Making These Grammar Mistakes?"</li>
<li><strong>Comparison:</strong> "APA vs. MLA: Which Citation Style Should You Use?"</li>
<li><strong>Ultimate/Complete:</strong> "The Complete Guide to Academic Writing"</li>
</ul>
<h3>Writing Effective Hooks</h3>
<p>Your first 1-2 sentences determine whether readers stay or leave. Effective hooks:</p>
<ul>
<li>State a problem your reader faces</li>
<li>Share a surprising statistic or fact</li>
<li>Ask a question they want answered</li>
<li>Make a bold, attention-grabbing claim</li>
</ul>
<h3>The Promise-Deliver Pattern</h3>
<p>Your headline makes a promise. Your content must deliver on it. Clickbait (promising more than you deliver) may get clicks but destroys trust and increases bounce rates.</p>"""},
            {'title': 'Readability and Accessibility', 'content': """<h2>Writing for Everyone</h2>
<h3>Readability Scores</h3>
<p>The Flesch-Kincaid readability score measures how easy your text is to read. Aim for a score of 60-70 (easily understood by 13-15 year olds) for general web content. Academic writing can be lower.</p>
<h3>Improving Readability</h3>
<ul>
<li>Use short sentences (average 15-20 words)</li>
<li>Prefer common words over complex ones</li>
<li>Avoid jargon unless your audience expects it</li>
<li>Use active voice more than passive</li>
<li>Break up long paragraphs</li>
</ul>
<h3>Web Accessibility</h3>
<ul>
<li>Use proper heading hierarchy (H1 > H2 > H3)</li>
<li>Add alt text to images</li>
<li>Use sufficient color contrast</li>
<li>Make links descriptive ("Read the full guide" not "click here")</li>
<li>Use plain language when possible</li>
</ul>
<p>Check your content's readability with our <a href="/word-counter/">word counter</a>, which includes a built-in readability score calculator.</p>"""},
        ]
    },
    {
        'title': 'English as a Second Language Writing',
        'category': 'ESL',
        'description': 'Writing tips and strategies specifically designed for non-native English speakers improving their writing skills.',
        'chapters': [
            {'title': 'Common ESL Writing Challenges', 'content': """<h2>Overcoming Language Barriers in Writing</h2>
<h3>Article Usage (a, an, the)</h3>
<p>Articles are one of the hardest aspects of English for non-native speakers. General rules:</p>
<ul>
<li><strong>"A/an"</strong> = one of many (non-specific): "I need a pen."</li>
<li><strong>"The"</strong> = specific one: "I need the pen on the desk."</li>
<li><strong>No article</strong> = general/uncountable: "Water is essential."</li>
</ul>
<h3>Preposition Confusion</h3>
<p>English prepositions are often idiomatic (no logical pattern). Common trouble spots: "interested in" (not "at"), "depend on" (not "of"), "arrive at/in" (not "to").</p>
<h3>Word Order</h3>
<p>English follows Subject-Verb-Object order more rigidly than many languages. Adjectives precede nouns: "big red house" (not "house red big").</p>
<h3>Verb Tense Consistency</h3>
<p>Many ESL writers mix tenses within a paragraph. Choose past or present and maintain it consistently throughout each section.</p>"""},
            {'title': 'Building Academic Vocabulary', 'content': """<h2>Essential Words for Academic Writing</h2>
<h3>Academic Word Families</h3>
<p>Focus on high-frequency academic words that appear across disciplines. The Academic Word List (AWL) contains 570 word families commonly used in academic texts.</p>
<h3>Transition Words by Function</h3>
<ul>
<li><strong>Adding:</strong> Furthermore, moreover, in addition, additionally</li>
<li><strong>Contrasting:</strong> However, nevertheless, conversely, although</li>
<li><strong>Causing:</strong> Therefore, consequently, as a result, thus</li>
<li><strong>Exemplifying:</strong> For example, specifically, to illustrate</li>
<li><strong>Concluding:</strong> In conclusion, overall, to summarize</li>
</ul>
<h3>Vocabulary Building Strategies</h3>
<ul>
<li>Read academic papers in your field regularly</li>
<li>Keep a vocabulary journal with new words and example sentences</li>
<li>Practice using new words in your own writing within 24 hours</li>
<li>Learn word families: analyze, analysis, analytical, analytically</li>
<li>Use our <a href="/paraphrasing-tool/">paraphrasing tool</a> to see alternative ways to express ideas</li>
</ul>"""},
            {'title': 'Grammar Tips for ESL Writers', 'content': """<h2>Key Grammar Areas to Focus On</h2>
<h3>Subject-Verb Agreement</h3>
<p>Remember: third-person singular present tense adds -s: "She writes" (not "She write"). Plural subjects don't add -s: "They write" (not "They writes").</p>
<h3>Countable vs. Uncountable Nouns</h3>
<p><strong>Countable:</strong> book/books, idea/ideas (use many, few, a number of)</p>
<p><strong>Uncountable:</strong> information, research, evidence, advice (use much, little, an amount of)</p>
<p>Common mistakes: "informations" (wrong), "researches" (wrong), "an advice" (wrong)</p>
<h3>Commonly Confused Words</h3>
<ul>
<li><strong>Make vs. Do:</strong> "Make" = create something new. "Do" = perform an action.</li>
<li><strong>Say vs. Tell:</strong> "Say" = speak words. "Tell" = communicate to someone specific.</li>
<li><strong>Borrow vs. Lend:</strong> "Borrow" = receive temporarily. "Lend" = give temporarily.</li>
</ul>
<p>Use our <a href="/grammar-check/">grammar checker</a> to identify patterns in your errors and learn from corrections.</p>"""},
            {'title': 'Improving Fluency and Coherence', 'content': """<h2>Writing That Flows Naturally</h2>
<h3>Coherence Techniques</h3>
<ul>
<li><strong>Use topic sentences:</strong> Start each paragraph with its main point</li>
<li><strong>Use transition words:</strong> Connect ideas logically between sentences and paragraphs</li>
<li><strong>Repeat key terms:</strong> Consistent terminology helps readers follow your argument</li>
<li><strong>Use pronouns effectively:</strong> "This research..." "These findings..." to refer back to previous content</li>
</ul>
<h3>Reducing L1 Interference</h3>
<p>Your first language (L1) naturally influences your English writing. Common patterns:</p>
<ul>
<li>Directly translating idioms or expressions from your L1</li>
<li>Using L1 sentence structures in English</li>
<li>Over-using certain sentence patterns you're comfortable with</li>
</ul>
<h3>Practice Strategies</h3>
<ul>
<li>Read your writing aloud to catch unnatural phrasing</li>
<li>Have a native speaker review your work when possible</li>
<li>Study model texts in your genre to internalize natural English patterns</li>
<li>Write every day, even if just a paragraph or two</li>
</ul>"""},
        ]
    },
    {
        'title': 'Research Methods for Writers',
        'category': 'Research',
        'description': 'Learn effective research strategies for academic papers, journalism, content creation, and professional writing.',
        'chapters': [
            {'title': 'Developing Research Questions', 'content': """<h2>Starting Your Research Right</h2>
<p>A well-crafted research question is the foundation of any research project. It guides your entire investigation and determines the scope of your work.</p>
<h3>Characteristics of Good Research Questions</h3>
<ul>
<li><strong>Focused:</strong> Narrow enough to answer thoroughly</li>
<li><strong>Researchable:</strong> Can be investigated with available resources</li>
<li><strong>Complex:</strong> Can't be answered with a simple yes/no</li>
<li><strong>Relevant:</strong> Contributes to existing knowledge or solves a practical problem</li>
</ul>
<h3>Narrowing Your Topic</h3>
<p>Start broad and narrow down. "Climate change" → "Climate change effects on agriculture" → "How rising temperatures affect wheat yields in the Midwest United States" → "The impact of heat stress on winter wheat production in Kansas, 2015-2025."</p>
<h3>Types of Research Questions</h3>
<ul>
<li><strong>Descriptive:</strong> "What are the symptoms of..." (describes a phenomenon)</li>
<li><strong>Comparative:</strong> "How does X differ from Y?" (compares two things)</li>
<li><strong>Causal:</strong> "What is the effect of X on Y?" (examines relationships)</li>
</ul>"""},
            {'title': 'Finding and Evaluating Sources', 'content': """<h2>Building a Strong Evidence Base</h2>
<h3>Source Types</h3>
<ul>
<li><strong>Scholarly sources:</strong> Peer-reviewed journals, academic books, conference papers</li>
<li><strong>Credible web sources:</strong> Government sites (.gov), educational institutions (.edu), established news organizations</li>
<li><strong>Primary sources:</strong> Original data, interviews, surveys, historical documents</li>
<li><strong>Grey literature:</strong> Reports, white papers, working papers (not peer-reviewed but often valuable)</li>
</ul>
<h3>Search Strategies</h3>
<ul>
<li>Use Boolean operators: AND, OR, NOT to refine searches</li>
<li>Use quotation marks for exact phrases: "climate change adaptation"</li>
<li>Check reference lists of relevant papers for additional sources</li>
<li>Set date filters for recent research</li>
<li>Use subject-specific databases for your field</li>
</ul>
<h3>Evaluating Credibility</h3>
<p>Check the author's credentials, the publication's reputation, the currency of the information, whether claims are supported by evidence, and whether there's potential bias.</p>"""},
            {'title': 'Organizing and Synthesizing Research', 'content': """<h2>From Notes to Arguments</h2>
<h3>Note-Taking Methods</h3>
<ul>
<li><strong>Cornell method:</strong> Divide your page into notes, cues, and summary sections</li>
<li><strong>Annotated bibliography:</strong> Write a brief summary and evaluation of each source</li>
<li><strong>Concept mapping:</strong> Visually connect ideas across sources</li>
<li><strong>Digital tools:</strong> Use reference managers to organize and annotate PDFs</li>
</ul>
<h3>Synthesis vs. Summary</h3>
<p><strong>Summarizing</strong> reports what each source says individually. <strong>Synthesizing</strong> identifies patterns, agreements, and contradictions across multiple sources to build a cohesive understanding.</p>
<h3>Building an Argument from Research</h3>
<ol>
<li>Identify themes and patterns across your sources</li>
<li>Note areas of agreement and disagreement among scholars</li>
<li>Find gaps in existing research that your work can address</li>
<li>Develop your own position based on the evidence</li>
<li>Select the strongest evidence to support each point</li>
</ol>
<p>Use our <a href="/summarize/">summarizer</a> to quickly extract key points from long research articles during your literature review.</p>"""},
        ]
    },
    {
        'title': 'Editing and Revision Techniques',
        'category': 'Writing Skills',
        'description': 'Professional editing techniques to transform rough drafts into polished, publication-ready writing.',
        'chapters': [
            {'title': 'The Multi-Pass Editing Method', 'content': """<h2>Systematic Editing for Better Results</h2>
<p>Professional editors don't try to fix everything in one read-through. They use multiple focused passes, each addressing a different aspect of the writing.</p>
<h3>Pass 1: Content and Structure</h3>
<ul>
<li>Is the main argument clear and well-supported?</li>
<li>Is the organization logical?</li>
<li>Are there any missing pieces or unnecessary sections?</li>
<li>Does the conclusion follow from the evidence?</li>
</ul>
<h3>Pass 2: Paragraphs and Flow</h3>
<ul>
<li>Does each paragraph have a clear purpose?</li>
<li>Are transitions smooth?</li>
<li>Is the paragraph order effective?</li>
</ul>
<h3>Pass 3: Sentences and Style</h3>
<ul>
<li>Are sentences clear and concise?</li>
<li>Is there sentence variety?</li>
<li>Is the tone consistent?</li>
</ul>
<h3>Pass 4: Grammar and Mechanics</h3>
<ul>
<li>Spelling, grammar, punctuation</li>
<li>Formatting consistency</li>
<li>Citation accuracy</li>
</ul>"""},
            {'title': 'Self-Editing Strategies', 'content': """<h2>Becoming Your Own Editor</h2>
<h3>Create Distance</h3>
<p>The most important editing technique: put your draft away for at least a few hours (ideally overnight) before revising. You can't edit what you've just written because your brain fills in gaps and corrects errors automatically.</p>
<h3>Change the Format</h3>
<ul>
<li>Print it out—you'll catch errors you miss on screen</li>
<li>Change the font or text size to see it fresh</li>
<li>Read it on a different device</li>
</ul>
<h3>Read Aloud</h3>
<p>Reading aloud is one of the most effective editing techniques. You'll hear awkward phrasing, missing words, repetition, and rhythm problems that your eyes skip over.</p>
<h3>Focus on Your Known Weaknesses</h3>
<p>Every writer has recurring patterns. Maybe you overuse "however," write run-on sentences, or forget commas after introductory phrases. Keep a list of your common errors and specifically check for them.</p>
<h3>Use Technology Wisely</h3>
<p>Use a <a href="/grammar-check/">grammar checker</a> for mechanical errors, a <a href="/word-counter/">word counter</a> for readability analysis, and a <a href="/paraphrasing-tool/">paraphrasing tool</a> to explore clearer phrasings.</p>"""},
            {'title': 'Cutting and Tightening Your Writing', 'content': """<h2>Less Is More</h2>
<h3>The 10% Rule</h3>
<p>After finishing your draft, try to cut 10% of the word count. Almost every piece of writing can be tightened without losing meaning.</p>
<h3>What to Cut</h3>
<ul>
<li><strong>Redundancies:</strong> "Past history" → "history." "Free gift" → "gift."</li>
<li><strong>Filler words:</strong> Very, really, quite, just, actually, basically, literally</li>
<li><strong>Wordy phrases:</strong> "In order to" → "to." "Due to the fact that" → "because."</li>
<li><strong>Throat-clearing:</strong> "It is important to note that..." (just state the point)</li>
<li><strong>Unnecessary hedging:</strong> "It seems that perhaps..." (commit to your claims)</li>
</ul>
<h3>Tightening Techniques</h3>
<ul>
<li>Convert passive to active voice</li>
<li>Replace phrases with single words</li>
<li>Eliminate "there is/are" constructions</li>
<li>Use strong verbs instead of weak verb + adverb</li>
</ul>"""},
        ]
    },
    {
        'title': 'Writing Across Disciplines',
        'category': 'Academic Writing',
        'description': 'Understand how writing conventions differ across academic fields including STEM, humanities, social sciences, and business.',
        'chapters': [
            {'title': 'Writing in the Sciences', 'content': """<h2>Scientific Writing Conventions</h2>
<h3>The IMRaD Structure</h3>
<p>Most scientific papers follow IMRaD format:</p>
<ul>
<li><strong>Introduction:</strong> What is the question? Why does it matter?</li>
<li><strong>Methods:</strong> How did you investigate? (Reproducibility is key)</li>
<li><strong>Results:</strong> What did you find? (Data and observations, minimal interpretation)</li>
<li><strong>Discussion:</strong> What do the results mean? How do they relate to existing research?</li>
</ul>
<h3>Scientific Writing Style</h3>
<ul>
<li>Precise, unambiguous language</li>
<li>Third person, passive voice (though active is increasingly accepted)</li>
<li>Present tense for established facts, past tense for specific experiments</li>
<li>Quantitative: specific numbers, not "many" or "significant" without data</li>
</ul>"""},
            {'title': 'Writing in the Humanities', 'content': """<h2>Humanities Writing Conventions</h2>
<h3>Key Characteristics</h3>
<ul>
<li><strong>Argument-driven:</strong> Every paper defends a thesis through textual analysis and interpretation</li>
<li><strong>Evidence from texts:</strong> Close reading of primary sources (literature, art, historical documents)</li>
<li><strong>Interpretive:</strong> Multiple valid readings exist; your job is to argue for yours convincingly</li>
<li><strong>Prose-heavy:</strong> Extended paragraphs, limited use of lists and bullet points</li>
</ul>
<h3>Close Reading</h3>
<p>Humanities writing often involves close reading—careful analysis of specific passages, considering word choice, imagery, structure, and context to build interpretive arguments.</p>
<h3>Citation Style</h3>
<p>MLA is standard for literature and languages. Chicago (notes-bibliography) is common in history. Include page numbers for specific textual references.</p>"""},
            {'title': 'Writing in Social Sciences', 'content': """<h2>Social Science Writing Conventions</h2>
<h3>Research-Focused Structure</h3>
<p>Social science papers typically include a literature review, methodology section, findings, and discussion—similar to sciences but with more qualitative elements.</p>
<h3>Literature Review</h3>
<p>The literature review is crucial in social sciences. It's not just a summary of sources—it synthesizes existing research to identify gaps your study addresses.</p>
<h3>Methodology</h3>
<p>Clearly describe your research design (qualitative, quantitative, mixed methods), data collection methods, sample/participants, and analysis approach. Justify your choices.</p>
<h3>Data Presentation</h3>
<ul>
<li><strong>Quantitative:</strong> Tables, charts, statistical tests with significance levels</li>
<li><strong>Qualitative:</strong> Themes with supporting quotes, coding procedures</li>
</ul>
<h3>Citation Style</h3>
<p>APA is the dominant style. Emphasize recency of sources—social sciences value current research. Use our <a href="/citation-generator/">citation generator</a> for correct APA formatting.</p>"""},
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed courses with educational writing content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing course data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing course data...')
            Chapter.objects.all().delete()
            Course.objects.all().delete()

        created_courses = 0
        created_chapters = 0

        for course_data in COURSES:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'category': course_data['category'],
                    'is_published': True,
                },
            )
            if created:
                created_courses += 1
                self.stdout.write(f'  Created course: {course.title}')

            for order, chapter_data in enumerate(course_data['chapters']):
                chapter, ch_created = Chapter.objects.get_or_create(
                    course=course,
                    title=chapter_data['title'],
                    defaults={
                        'content': chapter_data['content'].strip(),
                        'order': order,
                    },
                )
                if ch_created:
                    created_chapters += 1

            # Update chapter count
            course.update_chapter_count()

        self.stdout.write(self.style.SUCCESS(
            f'Courses seeded: {created_courses} courses, '
            f'{created_chapters} chapters'
        ))
