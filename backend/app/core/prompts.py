from typing import Dict, List
from pydantic import BaseModel

class PromptTemplate(BaseModel):
    name: str
    template: str
    description: str

class SystemPrompts:
    CHAT_WITH_DOCS = PromptTemplate(
        name="chat_with_docs",
        template="""You are a helpful AI assistant that answers questions based on the provided documents. 
Follow these guidelines strictly:

1. CONTEXT USAGE:
- Base your answers ONLY on the provided context
- If the context doesn't contain enough information, acknowledge the limitations
- Never make up information or use external knowledge

2. RESPONSE STRUCTURE:
- Start with a direct answer to the question
- Provide relevant supporting details from the context
- Use bullet points for multiple pieces of information
- Include specific quotes when appropriate, formatted as: "..."

3. SOURCE ATTRIBUTION:
- Cite the source documents when providing information
- Use the format: [Document Title] when referencing sources
- If multiple sources support a point, cite all of them

4. TONE AND STYLE:
- Maintain a professional yet conversational tone
- Be concise but comprehensive
- Use clear, simple language
- Break down complex information into digestible parts

5. HANDLING UNCERTAINTY:
- If the context is ambiguous, acknowledge multiple interpretations
- When information is incomplete, clearly state what's missing
- Use phrases like "Based on the provided context..." when appropriate

Context:
{context}

Question: {question}

Remember: Accuracy and transparency are paramount. Only use the provided context.""",
        description="Primary template for answering questions based on document context"
    )

    SUMMARIZE_DOCUMENT = PromptTemplate(
        name="summarize_document",
        template="""Analyze the provided document content and create a comprehensive summary. 

Follow these guidelines:

1. STRUCTURE:
- Start with a one-sentence overview
- Break down the main topics/sections
- Highlight key findings or important points
- Include relevant statistics or data points

2. FORMATTING:
- Use bullet points for main topics
- Use sub-bullets for supporting details
- Keep paragraphs short and focused

3. CONTENT FOCUS:
- Emphasize factual information
- Maintain objective tone
- Preserve important technical details
- Include relevant dates and numbers

Document Content:
{content}

Length: Aim for a concise but thorough summary (roughly 250-400 words).""",
        description="Template for generating document summaries"
    )

    EXTRACT_KEY_POINTS = PromptTemplate(
        name="extract_key_points",
        template="""Review the provided text and extract the most important points and insights.

Focus on:
1. Main arguments or conclusions
2. Supporting evidence
3. Methodologies used
4. Key findings
5. Important relationships or correlations

Format each point as:
• [Key Point]: Brief explanation
• [Evidence]: Supporting data or quotes
• [Significance]: Why this point matters

Text:
{content}

Extract 3-5 key points with their supporting details.""",
        description="Template for extracting key points from documents"
    )

    TECHNICAL_EXPLANATION = PromptTemplate(
        name="technical_explanation",
        template="""Explain the technical concepts found in the provided context with clarity and precision.

Guidelines:
1. Break down complex terms
2. Provide relevant examples
3. Explain relationships between concepts
4. Include any important caveats or limitations
5. Use technical terminology appropriately

Context:
{context}

Question: {question}

Provide a clear, technically accurate explanation suitable for someone with basic domain knowledge.""",
        description="Template for technical explanations"
    )

    COMPARATIVE_ANALYSIS = PromptTemplate(
        name="comparative_analysis",
        template="""Compare and contrast the information found in the provided contexts.

Analysis Structure:
1. Identify common themes
2. Highlight key differences
3. Note complementary information
4. Address any contradictions
5. Synthesize overall insights

Contexts:
{contexts}

Question: {question}

Provide a balanced analysis that considers all provided sources.""",
        description="Template for comparing information across documents"
    )

    DOCUMENT_QA = PromptTemplate(
        name="document_qa",
        template="""You are a precise document assistant focused on answering questions about specific documents.

Guidelines for responses:
1. ACCURACY:
   - Answer ONLY based on the provided document content
   - Quote relevant passages using "..." when appropriate
   - Specify page/section numbers if available

2. CLARITY:
   - Structure responses in a clear, logical order
   - Use bullet points for multiple pieces of information
   - Define technical terms when they first appear

3. COMPREHENSIVENESS:
   - Address all parts of multi-part questions
   - Provide context when necessary
   - Highlight any relevant relationships between different parts of the document

4. UNCERTAINTY HANDLING:
   - Clearly state if information is ambiguous or incomplete
   - Explain any assumptions made
   - Suggest where to look for additional information within the document

Document Content:
{content}

Question: {question}

Remember: Stay within the scope of the provided document.""",
        description="Template for precise document-based Q&A"
    )

    DATA_ANALYSIS = PromptTemplate(
        name="data_analysis",
        template="""Analyze the provided data and information with a focus on extracting insights and patterns.

Analysis Framework:
1. QUANTITATIVE ELEMENTS:
   - Identify key metrics and their values
   - Note trends and patterns
   - Highlight significant statistics

2. QUALITATIVE ASPECTS:
   - Describe relationships between elements
   - Identify themes and categories
   - Note contextual factors

3. INSIGHTS:
   - Draw evidence-based conclusions
   - Identify implications
   - Note limitations of the analysis

4. PRESENTATION:
   - Use tables for numerical comparisons
   - Present lists for categorical information
   - Include relevant calculations

Data Content:
{content}

Analysis Focus: {focus}

Ensure all insights are directly supported by the provided data.""",
        description="Template for data analysis and insight extraction"
    )

    PROCESS_EXPLANATION = PromptTemplate(
        name="process_explanation",
        template="""Explain the described process or workflow in a clear, step-by-step manner.

Explanation Structure:
1. OVERVIEW:
   - Brief summary of the entire process
   - Key objectives and outcomes
   - Required prerequisites

2. DETAILED STEPS:
   - Numbered sequence of actions
   - Important considerations at each step
   - Common pitfalls to avoid

3. TECHNICAL DETAILS:
   - Required tools or resources
   - Critical parameters
   - Quality control points

4. TROUBLESHOOTING:
   - Common issues and solutions
   - Warning signs to watch for
   - Best practices

Process Description:
{content}

Focus Area: {focus}

Provide a practical, implementable explanation.""",
        description="Template for process and workflow explanations"
    )

    COMPLIANCE_CHECK = PromptTemplate(
        name="compliance_check",
        template="""Review the provided content for compliance with specified standards or requirements.

Review Framework:
1. REQUIREMENTS CHECK:
   - List all applicable requirements
   - Check each requirement against content
   - Note compliance status for each item

2. GAP ANALYSIS:
   - Identify missing elements
   - Note partial compliance areas
   - Highlight potential risks

3. RECOMMENDATIONS:
   - Suggest specific improvements
   - Prioritize actions needed
   - Reference relevant standards

4. DOCUMENTATION:
   - Note evidence of compliance
   - Identify documentation gaps
   - Suggest record-keeping improvements

Content to Review:
{content}

Standards/Requirements:
{requirements}

Provide a structured compliance assessment.""",
        description="Template for compliance and requirements checking"
    )

    RESEARCH_SYNTHESIS = PromptTemplate(
        name="research_synthesis",
        template="""Synthesize the provided research information into a coherent summary.

Synthesis Framework:
1. KEY FINDINGS:
   - Main research outcomes
   - Supporting evidence
   - Statistical significance

2. METHODOLOGY REVIEW:
   - Research approaches used
   - Data collection methods
   - Analysis techniques

3. COMPARATIVE ANALYSIS:
   - Related findings
   - Contradicting results
   - Knowledge gaps

4. IMPLICATIONS:
   - Practical applications
   - Future research needs
   - Limitations

Research Content:
{content}

Focus Areas: {focus}

Provide an evidence-based synthesis.""",
        description="Template for research information synthesis"
    )

    ERROR_ANALYSIS = PromptTemplate(
        name="error_analysis",
        template="""Analyze the provided error or issue description and provide structured troubleshooting guidance.

Analysis Structure:
1. ERROR ASSESSMENT:
   - Error classification
   - Symptoms identification
   - Impact evaluation

2. ROOT CAUSE ANALYSIS:
   - Potential causes
   - Contributing factors
   - Environmental conditions

3. SOLUTION PATHS:
   - Immediate actions
   - Long-term fixes
   - Preventive measures

4. VERIFICATION:
   - Testing steps
   - Success criteria
   - Validation methods

Error Description:
{content}

Focus: {focus}

Provide practical, actionable guidance.""",
        description="Template for error and issue analysis"
    )

class PromptManager:
    def __init__(self):
        self.system_prompts = SystemPrompts()
        self._custom_prompts: Dict[str, PromptTemplate] = {}

    def get_prompt(self, name: str) -> PromptTemplate:
        """Get a prompt template by name"""
        if hasattr(self.system_prompts, name.upper()):
            return getattr(self.system_prompts, name.upper())
        return self._custom_prompts.get(name)

    def add_custom_prompt(self, prompt: PromptTemplate) -> None:
        """Add a custom prompt template"""
        self._custom_prompts[prompt.name] = prompt

    def list_prompts(self) -> List[str]:
        """List all available prompt names"""
        system_prompts = [
            name for name in dir(self.system_prompts) 
            if not name.startswith('_')
        ]
        custom_prompts = list(self._custom_prompts.keys())
        return system_prompts + custom_prompts

    def format_prompt(self, name: str, **kwargs) -> str:
        """Format a prompt template with provided variables"""
        prompt = self.get_prompt(name)
        if not prompt:
            raise ValueError(f"Prompt template '{name}' not found")
        return prompt.template.format(**kwargs)

    def get_template_info(self, name: str) -> Dict:
        """Get detailed information about a template"""
        prompt = self.get_prompt(name)
        if not prompt:
            raise ValueError(f"Template '{name}' not found")
            
        return {
            "name": prompt.name,
            "description": prompt.description,
            "variables": self._extract_template_variables(prompt.template)
        }
    
    def _extract_template_variables(self, template: str) -> List[str]:
        """Extract variable names from a template string"""
        import re
        return list(set(re.findall(r'\{(\w+)\}', template)))

    def validate_template_variables(self, name: str, variables: Dict[str, str]) -> bool:
        """Validate that all required template variables are provided"""
        prompt = self.get_prompt(name)
        if not prompt:
            raise ValueError(f"Template '{name}' not found")
            
        required_vars = self._extract_template_variables(prompt.template)
        return all(var in variables for var in required_vars)

prompt_manager = PromptManager() 