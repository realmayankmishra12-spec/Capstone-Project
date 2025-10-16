__ver__ = '1.2.7'
try:
    import ollama
except:
    pass

class OpenAi:
    def __init__(self, creator_name="Sam Altman"):
        self.creator_name = creator_name
        self.initialize_context()

    def initialize_context(self):
        self.system_message = {
            'role': 'system',
            'content': (
                "You are an AI judge specialized in SDG 16: Peace and Justice Strong Institutions. "
                "Your role is to analyze evidence and provide fair, balanced judgments based on principles of "
                "peace, justice, accountability, and institutional strength. Consider factors like: "
                "1. Rule of law adherence, 2. Human rights protection, 3. Institutional transparency, "
                "4. Access to justice, 5. Conflict resolution potential, 6. Corruption prevention. "
                "Provide clear, reasoned judgments that support peace and justice objectives. "
                "Always maintain neutrality and focus on evidence-based analysis."
            )
        }

    def chat(self):
        return self

    class Completions:
        def __init__(self, parent):
            self.parent = parent

        def create(self, model, messages, api=None):
            if model != "gpt-4o-mini":
                raise ValueError(f"Model '{model}' not supported.")
            if not messages:
                raise ValueError("No messages provided.")

            try:
                # Get response from ollama with SDG 16 context
                response = ollama.chat(
                    model='llama3.2:1b',
                    messages=[self.parent.system_message] + messages
                )
                
                # Return the AI judgment content
                judgment = response.get('message', {}).get('content', '')
                
                # Enhance the judgment with SDG 16 specific formatting
                if judgment:
                    return f"🏛️ **SDG 16 AI Judgment Analysis:**\n\n{judgment}\n\n**Recommendation:** Based on Peace and Justice principles, this case requires careful consideration of institutional strength and rule of law."
                else:
                    return "⚖️ AI analysis unavailable. Default recommendation: Proceed with standard institutional review process."
                    
            except Exception as e:
                # Fallback judgment if ollama fails
                return f"⚖️ **Fallback AI Judgment:** Evidence reviewed under SDG 16 principles. This matter appears to relate to institutional accountability and justice. Recommend thorough investigation following due process. (AI service temporarily unavailable: {str(e)})"

    @property
    def completions(self):
        return self.Completions(self)

def generate_sdg16_judgment(evidence_title, evidence_description, submitted_by):
    """
    Generate AI judgment specifically for SDG 16 evidence
    """
    try:
        ai = OpenAi()
        
        messages = [
            {
                'role': 'user', 
                'content': f"""
Please analyze this evidence submission for SDG 16 (Peace and Justice Strong Institutions):

Title: {evidence_title}
Description: {evidence_description}
Submitted by: {submitted_by}

Provide a professional judgment considering:
- Relevance to peace and justice
- Institutional implications
- Recommended actions
- Legal/ethical considerations
- SDG 16 target alignment

Format your response clearly and professionally.
                """
            }
        ]
        
        judgment = ai.chat().completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return judgment
        
    except ImportError:
        return """⚖️ **SDG 16 Standard Analysis**

This evidence has been reviewed under SDG 16 principles (Peace and Justice Strong Institutions).

**Initial Assessment:**
- Evidence Type: Institutional/Justice Related
- Relevance: Moderate to High for SDG 16 objectives
- Recommended Action: Full institutional review required

**Key Considerations:**
1. Rule of Law: Evidence should be evaluated for legal compliance
2. Transparency: Institutional processes must remain transparent
3. Accountability: Proper oversight mechanisms should be applied
4. Access to Justice: Ensure fair and equal treatment

**Next Steps:**
- Document evidence in official registry
- Assign to appropriate institutional authority
- Follow established due process procedures
- Monitor for SDG 16 compliance

*Note: AI analysis service temporarily unavailable. Manual review protocols applied.*"""
        
    except Exception as e:
        return f"""⚖️ **Emergency SDG 16 Protocol**

Evidence received and logged under emergency procedures.

**Title:** {evidence_title}
**Submitted by:** {submitted_by}

**Standard Institutional Response:**
This matter requires immediate attention under SDG 16 frameworks. The evidence has been flagged for priority review by competent authorities.

**Recommended Actions:**
1. Escalate to appropriate justice mechanisms
2. Ensure protection of all parties involved
3. Maintain transparency throughout process
4. Document all proceedings for accountability

**Status:** Under review - Manual analysis pending
**Error Log:** {str(e)[:100]}...

*All evidence is treated with utmost importance for peace and justice objectives.*"""


class MockChunk:
    def __init__(self, content):
        self.choices = [{"delta": {"content": content}}]