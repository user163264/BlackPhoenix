from flask import Flask, render_template, request, jsonify
import os
import json
import logging
import asyncio
from config import Config
from modules.token_obfuscator import TokenObfuscator
from modules.multilingual import MultilingualObfuscator
from modules.system_saturator import SystemSaturator
from models.prompt import SystemPromptModel

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('app')

app = Flask(__name__)
app.config.from_object(Config)

# Initialize modules
logger.info("Initializing modules...")
token_obfuscator = TokenObfuscator()
multilingual_obfuscator = MultilingualObfuscator()
system_saturator = SystemSaturator()
prompt_model = SystemPromptModel()

# Initialize fingerprinting suite
try:
    from modules.fingerprinting_suite import ModelFingerprinter, create_fingerprinter
    # We'll create fingerprinter instances per request since they need API keys
    fingerprinting_available = True
    logger.info("Fingerprinting suite modules loaded successfully")
except Exception as e:
    logger.error(f"Failed to load fingerprinting suite: {e}")
    fingerprinting_available = False

logger.info("Modules initialized successfully")

# Fingerprinting routes
@app.route('/fingerprinting')
def fingerprinting():
    """AI Model Fingerprinting & Analysis Suite"""
    if not fingerprinting_available:
        return render_template('error.html', 
                             error="Fingerprinting suite is not available. Please check the logs."), 500
    return render_template('fingerprinting_suite.html')

@app.route('/api/fingerprinting/scan', methods=['POST'])
def start_fingerprinting_scan():
    """Start a comprehensive fingerprinting scan"""
    if not fingerprinting_available:
        return jsonify({"error": "Fingerprinting suite is not available"}), 500
    
    try:
        data = request.json
        scan_type = data.get('scan_type', 'comprehensive')
        target_model = data.get('target_model', 'gpt-4o')
        
        logger.info(f"Starting fingerprinting scan: {scan_type}")
        
        # Create fingerprinter instance with API key
        fingerprinter = create_fingerprinter(Config.OPENAI_API_KEY)
        
        # Create new session
        session_id = fingerprinter.create_session()
        
        logger.info(f"Created fingerprinting session: {session_id}")
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Fingerprinting session started",
            "scan_type": scan_type,
            "target_model": target_model
        })
        
    except Exception as e:
        logger.error(f"Error starting fingerprinting scan: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/fingerprinting/scan/<session_id>', methods=['POST'])
def run_fingerprinting_scan(session_id):
    """Run the actual fingerprinting scan for a session"""
    if not fingerprinting_available:
        return jsonify({"error": "Fingerprinting suite is not available"}), 500
    
    try:
        logger.info(f"Running fingerprinting scan for session: {session_id}")
        
        # Create fingerprinter instance
        fingerprinter = create_fingerprinter(Config.OPENAI_API_KEY)
        
        # Run comprehensive scan asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            session = loop.run_until_complete(
                fingerprinter.run_comprehensive_scan(session_id)
            )
            
            # Generate report
            report = fingerprinter.generate_report(session_id)
            
            logger.info(f"Fingerprinting scan completed for session: {session_id}")
            return jsonify({
                "success": True,
                "session": {
                    "session_id": session.session_id,
                    "status": session.status,
                    "progress": session.progress,
                    "completed_tests": session.completed_tests,
                    "total_tests": session.total_tests,
                    "results_count": len(session.results),
                    "errors": session.errors
                },
                "report": {
                    "executive_summary": report.executive_summary,
                    "knowledge_cutoff": report.knowledge_cutoff,
                    "capabilities": report.capabilities,
                    "leakage_findings": report.leakage_findings,
                    "risk_assessment": report.risk_assessment,
                    "recommendations": report.recommendations,
                    "confidence_score": report.confidence_score
                }
            })
            
        finally:
            loop.close()
        
    except Exception as e:
        logger.error(f"Error running fingerprinting scan: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/fingerprinting/session/<session_id>', methods=['GET'])
def get_fingerprinting_session(session_id):
    """Get fingerprinting session status and progress"""
    if not fingerprinting_available:
        return jsonify({"error": "Fingerprinting suite is not available"}), 500
    
    try:
        # Create fingerprinter instance
        fingerprinter = create_fingerprinter(Config.OPENAI_API_KEY)
        
        session = fingerprinter.get_session(session_id)
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        return jsonify({
            "success": True,
            "session": {
                "session_id": session.session_id,
                "status": session.status,
                "progress": session.progress,
                "completed_tests": session.completed_tests,
                "total_tests": session.total_tests,
                "results_count": len(session.results),
                "errors": session.errors,
                "start_time": session.start_time.isoformat(),
                "end_time": session.end_time.isoformat() if session.end_time else None
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting fingerprinting session: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/fingerprinting/results/<session_id>', methods=['GET'])
def get_fingerprinting_results(session_id):
    """Get detailed fingerprinting results for a session"""
    if not fingerprinting_available:
        return jsonify({"error": "Fingerprinting suite is not available"}), 500
    
    try:
        # Create fingerprinter instance
        fingerprinter = create_fingerprinter(Config.OPENAI_API_KEY)
        
        session = fingerprinter.get_session(session_id)
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        # Convert results to JSON-serializable format
        results = [result.to_dict() for result in session.results]
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "results": results,
            "total_results": len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting fingerprinting results: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/fingerprinting/report/<session_id>', methods=['GET'])
def get_fingerprinting_report(session_id):
    """Generate and return a comprehensive fingerprinting report"""
    if not fingerprinting_available:
        return jsonify({"error": "Fingerprinting suite is not available"}), 500
    
    try:
        # Create fingerprinter instance
        fingerprinter = create_fingerprinter(Config.OPENAI_API_KEY)
        
        # Generate report
        report = fingerprinter.generate_report(session_id)
        
        return jsonify({
            "success": True,
            "report": {
                "session_id": report.session_id,
                "executive_summary": report.executive_summary,
                "knowledge_cutoff": report.knowledge_cutoff,
                "capabilities": report.capabilities,
                "leakage_findings": report.leakage_findings,
                "risk_assessment": report.risk_assessment,
                "recommendations": report.recommendations,
                "confidence_score": report.confidence_score,
                "generated_at": report.generated_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating fingerprinting report: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Insert the rest of the original app.py routes here...
# [All other routes remain the same]
