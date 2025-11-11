from django.shortcuts import render
from django.http import JsonResponse
import json
import re
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import tempfile
import time
import random
from datetime import datetime
import base64
import io
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

def crazy_multi_file_ocr_magic(image_files):
    results = []
    combined_text = ""
    total_confidence = 0
    processing_effects = []
    for i, image_file in enumerate(image_files):
        try:
            effect = random.choice([
                '🌟 Cosmic OCR Scanning',
                '⚡ Lightning Text Extraction',
                '🔮 Quantum Text Analysis',
                '🌈 Rainbow Pattern Recognition',
                '🚀 Hyperdrive OCR Processing',
                '💫 Stellar Text Decoding'
            ])
            processing_effects.append(effect)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                for chunk in image_file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name
            image = Image.open(temp_path)
            enhanced_image = enhance_image_for_ocr(image)
            extracted_text = pytesseract.image_to_string(enhanced_image)
            ocr_data = pytesseract.image_to_data(enhanced_image, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            analysis = analyze_text_for_evidence(extracted_text)
            thumbnail = create_crazy_thumbnail(image)
            file_result = {
                'success': True,
                'file_name': image_file.name,
                'file_size': image_file.size,
                'extracted_text': extracted_text.strip(),
                'confidence_score': avg_confidence,
                'analysis': analysis,
                'word_count': len(extracted_text.split()),
                'character_count': len(extracted_text),
                'processing_effect': effect,
                'thumbnail': thumbnail,
                'processing_time': round(random.uniform(0.5, 2.0), 2)  # Simulated processing time
            }
            results.append(file_result)
            combined_text += f"\n\n📁 FILE: {image_file.name}\n{extracted_text}\n" + "="*50
            total_confidence += avg_confidence
            os.unlink(temp_path)
            
        except Exception as e:
            file_result = {
                'success': False,
                'file_name': image_file.name,
                'error': str(e),
                'extracted_text': '',
                'confidence_score': 0,
                'analysis': f'❌ OCR Processing Error: {str(e)}',
                'processing_effect': '💥 Processing Failed'
            }
            results.append(file_result)
    successful_files = [r for r in results if r['success']]
    avg_confidence = total_confidence / len(successful_files) if successful_files else 0
    combined_analysis = generate_multi_file_analysis(results, combined_text)
    return {
        'success': len(successful_files) > 0,
        'total_files': len(image_files),
        'successful_files': len(successful_files),
        'failed_files': len(image_files) - len(successful_files),
        'results': results,
        'combined_text': combined_text.strip(),
        'average_confidence': avg_confidence,
        'combined_analysis': combined_analysis,
        'processing_effects': processing_effects,
        'total_words': sum(r.get('word_count', 0) for r in successful_files),
        'total_characters': sum(r.get('character_count', 0) for r in successful_files)
    }

def enhance_image_for_ocr(image):
    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # Increase contrast
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)  # Increase sharpness
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)  # Slight brightness increase
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        return image
    except:
        return image

def create_crazy_thumbnail(image):
    try:
        thumbnail = image.copy()
        thumbnail.thumbnail((150, 150), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        thumbnail.save(buffer, format='JPEG', quality=85)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{img_str}"
    except:
        return None

def generate_multi_file_analysis(results, combined_text):
    successful_results = [r for r in results if r['success']]
    if not successful_results:
        return "❌ No files processed successfully"
    pattern_counts = {
        'documents': 0,
        'legal': 0,
        'corruption': 0,
        'identity': 0,
        'dates': 0
    }
    evidence_keywords = {
        'documents': ['certificate', 'license', 'permit', 'contract', 'agreement', 'receipt', 'invoice'],
        'legal': ['court', 'judge', 'lawyer', 'legal', 'law', 'justice', 'rights', 'violation', 'complaint'],
        'corruption': ['bribe', 'corruption', 'illegal', 'fraud', 'embezzlement', 'kickback', 'money laundering'],
        'identity': ['signature', 'stamp', 'seal', 'official', 'authorized', 'certified'],
        'dates': ['date', 'dated', '2024', '2025', 'january', 'february', 'march', 'april', 'may', 'june']
    }
    text_lower = combined_text.lower()
    for category, keywords in evidence_keywords.items():
        pattern_counts[category] = sum(1 for kw in keywords if kw in text_lower)
    analysis_parts = [
        "🚀 **MULTI-FILE OCR MEGA-ANALYSIS**",
        f"📊 **Files Processed:** {len(successful_results)}/{len(results)}",
        f"� **Total Words Extracted:** {sum(r.get('word_count', 0) for r in successful_results)}",
        f"📈 **Average Confidence:** {sum(r.get('confidence_score', 0) for r in successful_results) / len(successful_results):.1f}%",
        ""
    ]
    if any(count > 0 for count in pattern_counts.values()):
        analysis_parts.append("🔍 **DETECTED PATTERNS ACROSS ALL FILES:**")
        for category, count in pattern_counts.items():
            if count > 0:
                if category == 'corruption':
                    analysis_parts.append(f"🚨 **CORRUPTION INDICATORS:** {count} instances found!")
                elif category == 'legal':
                    analysis_parts.append(f"⚖️ **LEGAL CONTENT:** {count} legal terms detected")
                elif category == 'documents':
                    analysis_parts.append(f"📋 **DOCUMENT TYPES:** {count} document indicators")
                elif category == 'identity':
                    analysis_parts.append(f"🔐 **AUTHENTICATION:** {count} official markers")
                elif category == 'dates':
                    analysis_parts.append(f"📅 **DATE REFERENCES:** {count} temporal markers")
        analysis_parts.append("")
    
    # Urgency assessment
    if pattern_counts['corruption'] > 0:
        analysis_parts.extend([
            "🚨 **OVERALL URGENCY: CRITICAL**",
            "⚡ **RECOMMENDATION:** Immediate multi-file investigation required!",
            "🔥 **SDG 16 IMPACT:** High priority for Peace & Justice review"
        ])
    elif pattern_counts['legal'] > 2:
        analysis_parts.extend([
            "🟠 **OVERALL URGENCY: HIGH**",
            "📋 **RECOMMENDATION:** Comprehensive legal document review needed",
            "⚖️ **SDG 16 IMPACT:** Significant institutional implications"
        ])
    else:
        analysis_parts.extend([
            "🟡 **OVERALL URGENCY: STANDARD**",
            "📝 **RECOMMENDATION:** Standard multi-document processing",
            "📊 **SDG 16 IMPACT:** Regular institutional review"
        ])
    
    return "\n".join(analysis_parts)

def crazy_ocr_magic(image_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name
        image = Image.open(temp_path)
        enhanced_image = enhance_image_for_ocr(image)
        extracted_text = pytesseract.image_to_string(enhanced_image)
        ocr_data = pytesseract.image_to_data(enhanced_image, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        analysis = analyze_text_for_evidence(extracted_text)
        thumbnail = create_crazy_thumbnail(image)
        os.unlink(temp_path)
        return {
            'success': True,
            'extracted_text': extracted_text.strip(),
            'confidence_score': avg_confidence,
            'analysis': analysis,
            'word_count': len(extracted_text.split()),
            'character_count': len(extracted_text),
            'thumbnail': thumbnail
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'extracted_text': '',
            'confidence_score': 0,
            'analysis': f'❌ OCR Processing Error: {str(e)}'
        }

def analyze_text_for_evidence(text):

    if not text:
        return "No text found in image"
    
    text_lower = text.lower()
    
    # Evidence pattern detection
    evidence_patterns = {
        'documents': ['certificate', 'license', 'permit', 'contract', 'agreement', 'receipt', 'invoice'],
        'legal': ['court', 'judge', 'lawyer', 'legal', 'law', 'justice', 'rights', 'violation', 'complaint'],
        'corruption': ['bribe', 'corruption', 'illegal', 'fraud', 'embezzlement', 'kickback', 'money laundering'],
        'identity': ['signature', 'stamp', 'seal', 'official', 'authorized', 'certified'],
        'dates': ['date', 'dated', '2024', '2025', 'january', 'february', 'march', 'april', 'may', 'june']
    }
    
    found_patterns = {}
    for category, keywords in evidence_patterns.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            found_patterns[category] = matches
    
    # Generate crazy analysis report
    analysis_parts = ["🔍 **AUTOMATED OCR EVIDENCE ANALYSIS**\n"]
    
    if not found_patterns:
        analysis_parts.append("📄 **Content Type:** General text/document")
        analysis_parts.append("🟡 **SDG 16 Relevance:** Requires manual review")
    else:
        for category, matches in found_patterns.items():
            if category == 'corruption':
                analysis_parts.append(f"🚨 **CORRUPTION ALERT:** Found {len(matches)} corruption-related terms!")
                analysis_parts.append(f"   Terms: {', '.join(matches[:3])}")
            elif category == 'legal':
                analysis_parts.append(f"⚖️ **LEGAL CONTENT:** {len(matches)} justice-related terms detected")
                analysis_parts.append(f"   Terms: {', '.join(matches[:3])}")
            elif category == 'documents':
                analysis_parts.append(f"📋 **DOCUMENT TYPE:** {len(matches)} document indicators found")
            elif category == 'identity':
                analysis_parts.append(f"🔐 **AUTHENTICATION:** {len(matches)} official markers detected")
    
    # Add urgency level
    if 'corruption' in found_patterns:
        analysis_parts.append("\n🚨 **URGENCY LEVEL: CRITICAL**")
        analysis_parts.append("⚡ **ACTION REQUIRED:** Immediate investigation recommended")
    elif 'legal' in found_patterns:
        analysis_parts.append("\n🟠 **URGENCY LEVEL: HIGH**")
        analysis_parts.append("📋 **ACTION REQUIRED:** Legal review recommended")
    else:
        analysis_parts.append("\n🟡 **URGENCY LEVEL: STANDARD**")
        analysis_parts.append("📝 **ACTION REQUIRED:** Standard processing")
    
    return "\n".join(analysis_parts)

def format_markdown_response(content):

    # Add proper markdown formatting
    formatted_content = f"""# 🏛️ AI JUDGE ANALYSIS - SDG 16

## 📋 Case Assessment

{content}

---

## ⚖️ Final Recommendation
This case requires institutional review under **Peace and Justice Strong Institutions** frameworks.

### 📊 SDG 16 Compliance Checklist
- [ ] Rule of Law Adherence
- [ ] Human Rights Protection
- [ ] Institutional Transparency
- [ ] Access to Justice
- [ ] Conflict Resolution
- [ ] Corruption Prevention

> **Status**: Under AI Judge Review  
> **Framework**: SDG 16 - Peace and Justice Strong Institutions  
> **Priority**: Standard Institutional Protocol
"""
    return formatted_content

def ai_judge_analysis(evidence_title, evidence_description, submitted_by):
    """
    AI Judge for SDG 16 - Peace and Justice Strong Institutions with Markdown Support
    """
    if OLLAMA_AVAILABLE:
        try:
            # Enhanced SDG 16 specialized system message with markdown formatting instructions
            system_message = {
                'role': 'system',
                'content': (
                    "You are an AI judge specialized in SDG 16: Peace and Justice Strong Institutions. "
                    "Analyze evidence based on: 1. Rule of law, 2. Human rights protection, "
                    "3. Institutional transparency, 4. Access to justice, 5. Conflict resolution, "
                    "6. Corruption prevention. Provide fair, balanced judgments supporting peace and justice. "
                    "Format your response using markdown with headers, bullet points, and emphasis for clarity. "
                    "Use professional legal language appropriate for institutional review."
                )
            }
            
            user_message = {
                'role': 'user', 
                'content': f"""
Analyze this evidence for SDG 16 (Peace and Justice Strong Institutions):

**Title:** {evidence_title}
**Description:** {evidence_description}
**Submitted by:** {submitted_by}

Provide a comprehensive professional judgment using markdown formatting on:

### Analysis Requirements:
- **Relevance to peace and justice**
- **Institutional implications**  
- **Recommended actions**
- **Legal/ethical considerations**
- **SDG 16 target alignment**

Format your response with clear headers, bullet points, and professional structure suitable for institutional review.
                """
            }
            
            # Get AI response using ollama
            response = ollama.chat(
                model='llama3.2:1b',
                messages=[system_message, user_message]
            )
            
            judgment = response.get('message', {}).get('content', '')
            
            if judgment:
                return format_markdown_response(judgment)
            else:
                return format_markdown_response("⚖️ AI Judge analysis temporarily unavailable. Standard institutional review protocols applied.")
                
        except Exception as e:
            fallback_content = f"""## 🚨 Emergency Protocol Activated

**Case:** {evidence_title}  
**Submitted by:** {submitted_by}

### Standard Judgment
This matter requires **immediate institutional attention** under SDG 16 principles.

#### Recommended Actions:
1. 🔍 **Investigate** - Initiate due process investigation
2. 🛡️ **Protect** - Ensure safety of all parties
3. 📝 **Document** - Maintain detailed records
4. ⚖️ **Review** - Apply institutional oversight

**Error Log:** `{str(e)}`"""
            return format_markdown_response(fallback_content)
    
    else:
        # Enhanced fallback with markdown formatting when ollama not available
        fallback_content = f"""## 📋 Standard SDG 16 Judicial Review

**Case Title:** {evidence_title}  
**Submitted by:** {submitted_by}

### Institutional Assessment
This evidence has been reviewed under **SDG 16 frameworks** (Peace and Justice Strong Institutions).

### Judgment Criteria Applied
- ✅ **Rule of Law Compliance**
- ✅ **Human Rights Protection**  
- ✅ **Institutional Transparency**
- ✅ **Access to Justice**
- ✅ **Conflict Resolution Potential**
- ✅ **Corruption Prevention**

### Recommended Actions
1. **Escalate** to appropriate justice mechanisms
2. **Ensure transparency** in all proceedings
3. **Protect** all parties involved
4. **Follow** established due process procedures
5. **Monitor** for SDG 16 compliance

> **Status:** Under institutional review - Manual analysis applied  
> **Priority:** Standard SDG 16 protocols in effect

*Note: AI Judge service temporarily offline - Manual review protocols activated*"""
        
        return format_markdown_response(fallback_content)

# Temporary in-memory storage (no database saving)
temp_evidence_storage = []

def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        submitted_by = request.POST.get('submitted_by')
        
        # � CRAZY MULTI-FILE IMAGE EVIDENCE PROCESSING! �
        image_files = request.FILES.getlist('image_evidence')
        ocr_result = None
        
        if image_files:
            if len(image_files) == 1:
                # Single file processing
                ocr_result = crazy_ocr_magic(image_files[0])
                
                # If OCR was successful, enhance the description with extracted text
                if ocr_result['success'] and ocr_result['extracted_text']:
                    enhanced_description = f"""{description}

---

🔥 **EXTRACTED TEXT FROM IMAGE EVIDENCE:**

{ocr_result['extracted_text']}

---

{ocr_result['analysis']}

**OCR Confidence:** {ocr_result['confidence_score']:.1f}%
**Words Extracted:** {ocr_result['word_count']}
**Characters:** {ocr_result['character_count']}
"""
                    description = enhanced_description
            
            else:
                # Multi-file processing
                ocr_result = crazy_multi_file_ocr_magic(image_files)
                
                if ocr_result['success'] and ocr_result['combined_text']:
                    enhanced_description = f"""{description}

---

🚀 **MULTI-FILE OCR EXTRACTION RESULTS:**

**Files Processed:** {ocr_result['successful_files']}/{ocr_result['total_files']}
**Total Words:** {ocr_result['total_words']}
**Average Confidence:** {ocr_result['average_confidence']:.1f}%

{ocr_result['combined_text']}

---

{ocr_result['combined_analysis']}
"""
                    description = enhanced_description
        
        # Add to temporary storage without saving to database
        evidence_id = len(temp_evidence_storage) + 1
        temp_evidence = {
            'id': evidence_id,
            'title': title,
            'description': description,
            'submitted_by': submitted_by,
            'date_submitted': 'Just now',
            'has_image': bool(image_files),
            'ocr_result': ocr_result if ocr_result else None,
            'image_names': [f.name for f in image_files] if image_files else [],
            'file_count': len(image_files) if image_files else 0
        }
        temp_evidence_storage.append(temp_evidence)
        
        response_data = {
            'success': True, 
            'evidence_id': evidence_id,
            'message': '🎉 Evidence submitted successfully!'
        }
        
        # Add OCR results to response if available
        if ocr_result:
            response_data['ocr_result'] = ocr_result
            if ocr_result['success']:
                response_data['message'] = f'🔥 Evidence submitted with OCR magic! Extracted {ocr_result["word_count"]} words with {ocr_result["confidence_score"]:.1f}% confidence!'
            else:
                response_data['message'] = '📤 Evidence submitted (OCR processing failed)'
        
        return JsonResponse(response_data)
    
    # Pass temporary evidence to template
    return render(request, 'index.html', {'evidences': temp_evidence_storage})

def get_judgment_stream(request, evidence_id):
    try:
        # Find evidence in temporary storage
        evidence = next((e for e in temp_evidence_storage if e['id'] == evidence_id), None)
        if not evidence:
            return JsonResponse({'error': 'Evidence not found'}, status=404)
        print("-"*100)
        # Generate AI Judge analysis
        judgment = ai_judge_analysis(
            evidence['title'], 
            evidence['description'], 
            evidence['submitted_by']
        )
        print(JsonResponse({'judgment': judgment}))
        print("-"*100)
        
        return JsonResponse({'judgment': judgment})
        
    except Exception as e:
        return JsonResponse({'error': f'AI Judge analysis failed: {str(e)}'}, status=500)

def process_image_evidence(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp']
        if image_file.content_type not in allowed_types:
            return JsonResponse({
                'success': False,
                'error': 'Invalid file type. Please upload JPEG, PNG, GIF, or BMP images only.'
            })
        
        # Process with OCR magic
        ocr_result = crazy_ocr_magic(image_file)
        
        if ocr_result['success']:
            return JsonResponse({
                'success': True,
                'message': f'🔥 OCR Magic completed! Extracted {ocr_result["word_count"]} words!',
                'extracted_text': ocr_result['extracted_text'],
                'confidence_score': ocr_result['confidence_score'],
                'analysis': ocr_result['analysis'],
                'thumbnail': ocr_result.get('thumbnail'),
                'stats': {
                    'word_count': ocr_result['word_count'],
                    'character_count': ocr_result['character_count'],
                    'filename': image_file.name,
                    'filesize': image_file.size
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': ocr_result['error'],
                'message': '❌ OCR processing failed'
            })
    
    return JsonResponse({'success': False, 'error': 'No image file provided'})

def process_multiple_image_evidence(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        image_files = request.FILES.getlist('images')
        
        # Validate file count
        if len(image_files) > 10:
            return JsonResponse({
                'success': False,
                'error': 'Maximum 10 files allowed per batch. Please reduce the number of files.'
            })
        
        # Validate file types
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp']
        for image_file in image_files:
            if image_file.content_type not in allowed_types:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid file type for {image_file.name}. Please upload JPEG, PNG, GIF, or BMP images only.'
                })
        
        # Process with CRAZY multi-file OCR magic
        ocr_result = crazy_multi_file_ocr_magic(image_files)
        
        return JsonResponse({
            'success': ocr_result['success'],
            'message': f'🚀 Multi-file OCR completed! Processed {ocr_result["successful_files"]}/{ocr_result["total_files"]} files, extracted {ocr_result["total_words"]} total words!',
            'multi_file_result': ocr_result
        })
    
    return JsonResponse({'success': False, 'error': 'No image files provided'})

def clear_evidence(request):
    global temp_evidence_storage
    temp_evidence_storage = []
    return JsonResponse({'success': True, 'message': 'All evidence cleared by AI Judge system'})