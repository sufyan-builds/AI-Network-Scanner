"""
AI Analysis Module

This module provides intelligent analysis of network scan results using Groq API.
Groq is fast, efficient, and perfect for real-time analysis.

Features:
- Network health assessment
- Security recommendations
- Performance suggestions
- Structured response parsing
"""

import os
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class GroqAnalyzer:
    """
    AI analyzer using Groq API for network scan analysis.
    
    Provides:
    - Network health assessment
    - Security recommendations
    - Performance suggestions
    - Device pattern recognition
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GroqAnalyzer.
        
        Args:
            api_key: Groq API key (or reads from GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.api_available = bool(self.api_key)
        
        if not self.api_available:
            logger.warning("Groq API key not configured. AI analysis will be unavailable.")
            return
        
        try:
            # Import Groq client
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            self.api_available = True
            logger.info("Groq API configured successfully")
        except ImportError:
            logger.error("Groq library not installed. Install with: pip install groq")
            self.api_available = False
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            self.api_available = False
    
    def analyze_scan_results(
        self,
        scan_results: List[Dict],
        statistics: Dict
    ) -> Optional[Dict[str, str]]:
        """
        Analyze network scan results using Groq.
        
        Args:
            scan_results: List of scan result dictionaries
            statistics: Dictionary with scan statistics
            
        Returns:
            Dictionary with analysis or None if API unavailable
        """
        if not self.api_available:
            logger.warning("AI analysis unavailable - API not configured")
            return None
        
        try:
            # Generate prompt
            prompt = self._generate_prompt(scan_results, statistics)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Fast, efficient model
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract and parse response
            response_text = response.choices[0].message.content
            analysis = self._parse_response(response_text)
            
            logger.info("AI analysis completed successfully")
            return analysis
        
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return None
    
    def _generate_prompt(
        self,
        scan_results: List[Dict],
        statistics: Dict
    ) -> str:
        """Generate analysis prompt for Groq."""
        
        # Get online devices
        online_devices = [d for d in scan_results if d["Status"] == "Online"]
        
        # Build device summary (first 15 devices)
        device_summary = "\n".join([
            f"- {d['IP']}: {d['Hostname']} (Response: {d['Response Time']})"
            for d in online_devices[:15]
        ])
        
        if len(online_devices) > 15:
            device_summary += f"\n... and {len(online_devices) - 15} more devices"
        
        # Create prompt
        prompt = f"""Analyze this network scan and provide a professional assessment.

SCAN STATISTICS:
- Total IPs Scanned: {statistics.get('total_scanned', 0)}
- Online Devices: {statistics.get('online_count', 0)}
- Offline Devices: {statistics.get('offline_count', 0)}
- Scan Duration: {statistics.get('duration', 'Unknown')}

ONLINE DEVICES:
{device_summary}

Provide analysis in EXACTLY this format (use these exact section headers):

SUMMARY:
2-3 sentences about overall network status

RECOMMENDATIONS:
- 3-4 security/performance recommendations
- Each as a separate bullet point
- Be specific and actionable

HEALTH:
Single word rating: Excellent, Good, Average, or Poor

Keep it beginner-friendly, avoid jargon, focus on practical insights."""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """Parse Groq response into structured sections."""
        
        result = {
            "summary": "",
            "recommendations": "",
            "health": "Unknown"
        }
        
        try:
            text = response_text
            text_lower = text.lower()
            
            # Extract SUMMARY
            if "summary:" in text_lower:
                start = text_lower.index("summary:") + len("summary:")
                end = (text_lower.index("recommendations:") 
                       if "recommendations:" in text_lower 
                       else len(text))
                result["summary"] = text[start:end].strip()
            
            # Extract RECOMMENDATIONS
            if "recommendations:" in text_lower:
                start = text_lower.index("recommendations:") + len("recommendations:")
                end = (text_lower.index("health:") 
                       if "health:" in text_lower 
                       else len(text))
                result["recommendations"] = text[start:end].strip()
            
            # Extract HEALTH
            if "health:" in text_lower:
                start = text_lower.index("health:") + len("health:")
                health_line = text[start:].split("\n")[0].strip()
                
                # Normalize health rating
                health_lower = health_line.lower()
                if "excellent" in health_lower:
                    result["health"] = "Excellent"
                elif "good" in health_lower:
                    result["health"] = "Good"
                elif "average" in health_lower:
                    result["health"] = "Average"
                elif "poor" in health_lower or "needs" in health_lower:
                    result["health"] = "Poor"
                else:
                    result["health"] = health_line
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            result["summary"] = response_text
            return result
    
    def is_available(self) -> bool:
        """Check if AI analysis is available."""
        return self.api_available
