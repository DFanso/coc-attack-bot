"""
AI Analyzer - Google Gemini integration for base analysis
"""

import os
import base64
import json
import requests
from typing import Dict, Optional, Tuple
from PIL import Image
import io

class AIAnalyzer:
    """Google Gemini AI analyzer for COC base evaluation"""
    
    def __init__(self, api_key: str, logger):
        self.api_key = api_key
        self.logger = logger
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite-preview-06-17:generateContent"
        
        # Analysis prompt template
        self.analysis_prompt = """
You are an expert Clash of Clans player analyzing enemy bases for attack decisions.

Analyze this screenshot and provide:
1. Loot amounts (Gold, Elixir, Dark Elixir) - estimate the visible amounts
2. Town Hall level (1-12)
3. Base difficulty assessment (Easy/Medium/Hard)
4. Attack recommendation (ATTACK or SKIP)

Consider these factors:
- Loot amounts: Good loot = 300k+ gold/elixir, 2k+ dark elixir
- Town Hall level: Prefer similar or lower level bases
- Base layout: Look for weak spots, exposed defenses
- Risk vs reward: High loot with reasonable difficulty = ATTACK

Respond in this exact JSON format:
{
    "loot": {
        "gold": estimated_gold_amount,
        "elixir": estimated_elixir_amount,
        "dark_elixir": estimated_dark_elixir_amount
    },
    "townhall_level": town_hall_level_number,
    "difficulty": "Easy/Medium/Hard",
    "recommendation": "ATTACK/SKIP",
    "reasoning": "Brief explanation of decision"
}
"""
    
    def analyze_base(self, screenshot_path: str, min_gold: int = 300000, 
                    min_elixir: int = 300000, min_dark: int = 2000) -> Dict:
        """
        Analyze enemy base screenshot using Google Gemini
        
        Args:
            screenshot_path: Path to screenshot file
            min_gold: Minimum gold requirement
            min_elixir: Minimum elixir requirement  
            min_dark: Minimum dark elixir requirement
            
        Returns:
            Dict with analysis results and attack recommendation
        """
        try:
            self.logger.info(f"🤖 Analyzing base with AI: {screenshot_path}")
            
            # Encode image to base64
            image_data = self._encode_image(screenshot_path)
            if not image_data:
                return self._create_error_response("Failed to encode image")
            
            # Create analysis prompt with requirements
            prompt = self._create_analysis_prompt(min_gold, min_elixir, min_dark)
            
            # Send request to Gemini
            response = self._send_gemini_request(image_data, prompt)
            
            if response:
                self.logger.info(f"✅ AI Analysis: {response['recommendation']} - {response['reasoning']}")
                return response
            else:
                return self._create_error_response("Failed to get AI response")
                
        except Exception as e:
            self.logger.error(f"AI analysis error: {e}")
            return self._create_error_response(f"Analysis error: {e}")
    
    def _encode_image(self, image_path: str) -> Optional[str]:
        """Encode image to base64 for Gemini API"""
        try:
            with open(image_path, 'rb') as image_file:
                # Resize image if too large (Gemini has size limits)
                img = Image.open(image_file)
                
                # Resize if width > 1024px to reduce API payload
                if img.width > 1024:
                    ratio = 1024 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((1024, new_height), Image.Resampling.LANCZOS)
                
                # Convert to bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Encode to base64
                return base64.b64encode(img_byte_arr).decode('utf-8')
                
        except Exception as e:
            self.logger.error(f"Image encoding error: {e}")
            return None
    
    def _create_analysis_prompt(self, min_gold: int, min_elixir: int, min_dark: int) -> str:
        """Create analysis prompt with current requirements"""
        return f"""
You are an expert Clash of Clans player analyzing enemy bases for attack decisions.

CRITICAL: You must read the EXACT loot numbers displayed in the top-left area of the screen.

Current loot requirements:
- Minimum Gold: {min_gold:,}
- Minimum Elixir: {min_elixir:,}  
- Minimum Dark Elixir: {min_dark:,}

INSTRUCTIONS:
1. Look at the "Available Loot:" section in the top-left corner of the screenshot
2. Read the EXACT numbers next to the gold coin (yellow), elixir drop (pink), and dark elixir drop (black) icons
3. Identify the Town Hall level by looking at the Town Hall building
4. Compare loot numbers to minimum requirements above
5. Make recommendation based on loot AND Town Hall level

LOOT READING RULES:
- Gold is shown next to a yellow coin icon
- Elixir is shown next to a pink/purple drop icon  
- Dark Elixir is shown next to a black drop icon
- Numbers may have spaces (e.g. "123 456" = 123,456)
- Be extremely careful reading the digits

TOWN HALL RULES:
- Town Hall 13, 14, 15, 16+ are TOO STRONG - always SKIP these
- Only attack Town Hall 12 and below
- Look at the Town Hall building design to identify the level

DECISION CRITERIA:
- ATTACK only if: ALL loot types meet requirements AND Town Hall is level 12 or below
- SKIP if: ANY loot type is below requirements OR Town Hall is level 13+
- Do NOT consider base difficulty - focus ONLY on loot amounts and Town Hall level

Examples:
- Gold: 19,015 (need 500,000) → SKIP (loot too low)
- Town Hall 13 → SKIP (too strong regardless of loot)
- Town Hall 11 with good loot → ATTACK

Respond in this exact JSON format:
{{
    "loot": {{
        "gold": actual_gold_amount_you_read,
        "elixir": actual_elixir_amount_you_read,
        "dark_elixir": actual_dark_elixir_amount_you_read
    }},
    "townhall_level": town_hall_level_number,
    "difficulty": "Easy/Medium/Hard",
    "recommendation": "ATTACK/SKIP",
    "reasoning": "Specific reason: Gold X vs required Y, Elixir A vs required B, Dark C vs required D, TH level E"
}}
"""
    
    def _send_gemini_request(self, image_data: str, prompt: str) -> Optional[Dict]:
        """Send request to Google Gemini API"""
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": image_data
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,  # Low temperature for consistent analysis
                    "topK": 1,
                    "topP": 1,
                    "maxOutputTokens": 1024,
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            
            self.logger.info("🌐 Sending request to Gemini API...")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract text from response
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    
                    # Parse JSON response
                    try:
                        # Clean up response (remove markdown formatting if present)
                        content = content.strip()
                        if content.startswith('```json'):
                            content = content[7:]
                        if content.endswith('```'):
                            content = content[:-3]
                        content = content.strip()
                        
                        analysis = json.loads(content)
                        return analysis
                        
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Failed to parse AI response as JSON: {e}")
                        self.logger.error(f"Raw response: {content}")
                        return None
                else:
                    self.logger.error("No candidates in Gemini response")
                    return None
            else:
                self.logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error("Gemini API request timeout")
            return None
        except Exception as e:
            self.logger.error(f"Gemini API request error: {e}")
            return None
    
    def _create_error_response(self, error_msg: str) -> Dict:
        """Create error response with SKIP recommendation"""
        return {
            "loot": {"gold": 0, "elixir": 0, "dark_elixir": 0},
            "townhall_level": 0,
            "difficulty": "Unknown",
            "recommendation": "SKIP",
            "reasoning": f"Error: {error_msg}",
            "error": True
        }
    
    def test_connection(self) -> bool:
        """Test connection to Gemini API"""
        try:
            # Create a simple test request
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{"parts": [{"text": "Hello, respond with 'OK'"}]}],
                "generationConfig": {"maxOutputTokens": 10}
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("✅ Gemini API connection successful")
                return True
            else:
                self.logger.error(f"❌ Gemini API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Gemini API test error: {e}")
            return False