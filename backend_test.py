#!/usr/bin/env python3
"""
Backend API Testing for "In" AI Interview Assistant
Tests all backend endpoints including Sessions, Chat, and Input History APIs
"""

import requests
import json
import base64
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://locked-clone.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_session_id = None
        self.test_results = {
            'sessions': {},
            'chat': {},
            'input_history': {},
            'overall_status': 'PASS'
        }
        
    def log_test(self, category, test_name, status, details=""):
        """Log test results"""
        if category not in self.test_results:
            self.test_results[category] = {}
        
        self.test_results[category][test_name] = {
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        if status == 'FAIL':
            self.test_results['overall_status'] = 'FAIL'
        
        print(f"[{status}] {category}.{test_name}: {details}")
    
    def test_sessions_api(self):
        """Test all Sessions API endpoints"""
        print("\n=== Testing Sessions API ===")
        
        # Test 1: Create new session
        try:
            session_data = {
                "title": "Technical Interview Practice Session",
                "model": "GPT-5.2"
            }
            
            response = self.session.post(f"{API_BASE}/sessions", json=session_data)
            
            if response.status_code == 200:
                session_response = response.json()
                self.test_session_id = session_response.get('id')
                
                # Validate response structure
                required_fields = ['id', 'title', 'date', 'duration', 'questionsAsked', 'model', 'createdAt', 'updatedAt']
                missing_fields = [field for field in required_fields if field not in session_response]
                
                if missing_fields:
                    self.log_test('sessions', 'create_session', 'FAIL', f"Missing fields: {missing_fields}")
                elif session_response['model'] != 'GPT-5.2':
                    self.log_test('sessions', 'create_session', 'FAIL', f"Model mismatch: expected GPT-5.2, got {session_response['model']}")
                else:
                    self.log_test('sessions', 'create_session', 'PASS', f"Session created with ID: {self.test_session_id}")
            else:
                self.log_test('sessions', 'create_session', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('sessions', 'create_session', 'FAIL', f"Exception: {str(e)}")
        
        # Test 2: Get all sessions
        try:
            response = self.session.get(f"{API_BASE}/sessions")
            
            if response.status_code == 200:
                sessions = response.json()
                if isinstance(sessions, list):
                    self.log_test('sessions', 'get_all_sessions', 'PASS', f"Retrieved {len(sessions)} sessions")
                else:
                    self.log_test('sessions', 'get_all_sessions', 'FAIL', "Response is not a list")
            else:
                self.log_test('sessions', 'get_all_sessions', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('sessions', 'get_all_sessions', 'FAIL', f"Exception: {str(e)}")
        
        # Test 3: Get specific session (only if we have a session ID)
        if self.test_session_id:
            try:
                response = self.session.get(f"{API_BASE}/sessions/{self.test_session_id}")
                
                if response.status_code == 200:
                    session = response.json()
                    if session.get('id') == self.test_session_id:
                        self.log_test('sessions', 'get_specific_session', 'PASS', f"Retrieved session: {self.test_session_id}")
                    else:
                        self.log_test('sessions', 'get_specific_session', 'FAIL', "Session ID mismatch")
                else:
                    self.log_test('sessions', 'get_specific_session', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test('sessions', 'get_specific_session', 'FAIL', f"Exception: {str(e)}")
        
        # Test 4: Update session stats
        if self.test_session_id:
            try:
                update_data = {
                    "questions_asked": 5,
                    "duration": "15 mins"
                }
                
                response = self.session.patch(f"{API_BASE}/sessions/{self.test_session_id}/update-stats", params=update_data)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        self.log_test('sessions', 'update_session_stats', 'PASS', "Session stats updated successfully")
                    else:
                        self.log_test('sessions', 'update_session_stats', 'FAIL', "Success flag not returned")
                else:
                    self.log_test('sessions', 'update_session_stats', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test('sessions', 'update_session_stats', 'FAIL', f"Exception: {str(e)}")
    
    def test_chat_api(self):
        """Test all Chat API endpoints"""
        print("\n=== Testing Chat API ===")
        
        # Ensure we have a session for testing
        if not self.test_session_id:
            self.test_session_id = str(uuid.uuid4())
        
        # Test 1: Send text message to GPT-5.2
        try:
            message_data = {
                "sessionId": self.test_session_id,
                "message": "What are the key principles of object-oriented programming?",
                "model": "GPT-5.2",
                "messageType": "text"
            }
            
            response = self.session.post(f"{API_BASE}/chat", json=message_data)
            
            if response.status_code == 200:
                chat_response = response.json()
                
                # Validate response structure
                required_fields = ['id', 'sessionId', 'type', 'content', 'timestamp']
                missing_fields = [field for field in required_fields if field not in chat_response]
                
                if missing_fields:
                    self.log_test('chat', 'send_text_message', 'FAIL', f"Missing fields: {missing_fields}")
                elif chat_response['type'] != 'assistant':
                    self.log_test('chat', 'send_text_message', 'FAIL', f"Wrong message type: {chat_response['type']}")
                elif not chat_response['content']:
                    self.log_test('chat', 'send_text_message', 'FAIL', "Empty AI response content")
                else:
                    self.log_test('chat', 'send_text_message', 'PASS', f"AI responded with {len(chat_response['content'])} characters")
            else:
                self.log_test('chat', 'send_text_message', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('chat', 'send_text_message', 'FAIL', f"Exception: {str(e)}")
        
        # Test 2: Send message with image data
        try:
            # Create a simple base64 encoded test image (1x1 pixel PNG)
            test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            
            message_data = {
                "sessionId": self.test_session_id,
                "message": "Can you analyze this image?",
                "model": "GPT-5.2",
                "messageType": "image",
                "imageData": test_image_b64
            }
            
            response = self.session.post(f"{API_BASE}/chat", json=message_data)
            
            if response.status_code == 200:
                chat_response = response.json()
                if chat_response.get('content'):
                    self.log_test('chat', 'send_image_message', 'PASS', "AI processed image message successfully")
                else:
                    self.log_test('chat', 'send_image_message', 'FAIL', "Empty response for image message")
            else:
                self.log_test('chat', 'send_image_message', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('chat', 'send_image_message', 'FAIL', f"Exception: {str(e)}")
        
        # Test 3: Get all messages for session
        try:
            response = self.session.get(f"{API_BASE}/chat/{self.test_session_id}")
            
            if response.status_code == 200:
                messages = response.json()
                if isinstance(messages, list):
                    # Should have at least user and assistant messages from previous tests
                    if len(messages) >= 2:
                        self.log_test('chat', 'get_messages', 'PASS', f"Retrieved {len(messages)} messages")
                    else:
                        self.log_test('chat', 'get_messages', 'FAIL', f"Expected at least 2 messages, got {len(messages)}")
                else:
                    self.log_test('chat', 'get_messages', 'FAIL', "Response is not a list")
            else:
                self.log_test('chat', 'get_messages', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('chat', 'get_messages', 'FAIL', f"Exception: {str(e)}")
        
        # Test 4: Delete all messages for session
        try:
            response = self.session.delete(f"{API_BASE}/chat/{self.test_session_id}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test('chat', 'delete_messages', 'PASS', f"Deleted {result.get('deleted_count', 0)} messages")
                else:
                    self.log_test('chat', 'delete_messages', 'FAIL', "Success flag not returned")
            else:
                self.log_test('chat', 'delete_messages', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('chat', 'delete_messages', 'FAIL', f"Exception: {str(e)}")
    
    def test_input_history_api(self):
        """Test all Input History API endpoints"""
        print("\n=== Testing Input History API ===")
        
        # Ensure we have a session for testing
        if not self.test_session_id:
            self.test_session_id = str(uuid.uuid4())
        
        # Test 1: Save input to history
        try:
            input_data = {
                "sessionId": self.test_session_id,
                "input": "What is the difference between abstract classes and interfaces?"
            }
            
            response = self.session.post(f"{API_BASE}/input-history", json=input_data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test('input_history', 'save_input', 'PASS', "Input saved to history successfully")
                else:
                    self.log_test('input_history', 'save_input', 'FAIL', "Success flag not returned")
            else:
                self.log_test('input_history', 'save_input', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('input_history', 'save_input', 'FAIL', f"Exception: {str(e)}")
        
        # Test 2: Get all input history
        try:
            response = self.session.get(f"{API_BASE}/input-history")
            
            if response.status_code == 200:
                history = response.json()
                if isinstance(history, list):
                    self.log_test('input_history', 'get_all_history', 'PASS', f"Retrieved {len(history)} history items")
                else:
                    self.log_test('input_history', 'get_all_history', 'FAIL', "Response is not a list")
            else:
                self.log_test('input_history', 'get_all_history', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('input_history', 'get_all_history', 'FAIL', f"Exception: {str(e)}")
        
        # Test 3: Get session-specific input history
        try:
            response = self.session.get(f"{API_BASE}/input-history/{self.test_session_id}")
            
            if response.status_code == 200:
                history = response.json()
                if isinstance(history, list):
                    self.log_test('input_history', 'get_session_history', 'PASS', f"Retrieved {len(history)} session history items")
                else:
                    self.log_test('input_history', 'get_session_history', 'FAIL', "Response is not a list")
            else:
                self.log_test('input_history', 'get_session_history', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('input_history', 'get_session_history', 'FAIL', f"Exception: {str(e)}")
    
    def test_gpt_integration(self):
        """Test GPT-5.2 integration specifically"""
        print("\n=== Testing GPT-5.2 Integration ===")
        
        if not self.test_session_id:
            self.test_session_id = str(uuid.uuid4())
        
        try:
            # Test a technical interview question
            message_data = {
                "sessionId": self.test_session_id,
                "message": "Explain the time complexity of binary search and provide a Python implementation.",
                "model": "GPT-5.2",
                "messageType": "text"
            }
            
            response = self.session.post(f"{API_BASE}/chat", json=message_data)
            
            if response.status_code == 200:
                chat_response = response.json()
                content = chat_response.get('content', '')
                
                # Check if response contains technical content
                technical_keywords = ['O(log n)', 'binary', 'search', 'algorithm', 'complexity', 'python', 'def']
                found_keywords = [kw for kw in technical_keywords if kw.lower() in content.lower()]
                
                if len(found_keywords) >= 3:
                    self.log_test('gpt_integration', 'technical_response', 'PASS', f"GPT-5.2 provided technical response with keywords: {found_keywords}")
                else:
                    self.log_test('gpt_integration', 'technical_response', 'FAIL', f"Response lacks technical content. Found keywords: {found_keywords}")
            else:
                self.log_test('gpt_integration', 'technical_response', 'FAIL', f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test('gpt_integration', 'technical_response', 'FAIL', f"Exception: {str(e)}")
    
    def cleanup_test_data(self):
        """Clean up test session if it was created"""
        if self.test_session_id:
            try:
                response = self.session.delete(f"{API_BASE}/sessions/{self.test_session_id}")
                if response.status_code == 200:
                    print(f"\n✓ Cleaned up test session: {self.test_session_id}")
                else:
                    print(f"\n⚠ Failed to clean up test session: {response.status_code}")
            except Exception as e:
                print(f"\n⚠ Error during cleanup: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print(f"Starting backend API tests for: {API_BASE}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Run all test suites
        self.test_sessions_api()
        self.test_chat_api()
        self.test_input_history_api()
        self.test_gpt_integration()
        
        # Clean up
        self.cleanup_test_data()
        
        # Print summary
        self.print_summary()
        
        return self.test_results
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "="*60)
        print("BACKEND API TEST SUMMARY")
        print("="*60)
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for category, tests in self.test_results.items():
            if category == 'overall_status':
                continue
                
            print(f"\n{category.upper()}:")
            for test_name, result in tests.items():
                status_symbol = "✓" if result['status'] == 'PASS' else "✗"
                print(f"  {status_symbol} {test_name}: {result['details']}")
                
                total_tests += 1
                if result['status'] == 'PASS':
                    passed_tests += 1
                else:
                    failed_tests += 1
        
        print(f"\n" + "-"*60)
        print(f"OVERALL STATUS: {self.test_results['overall_status']}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%")
        print("="*60)


if __name__ == "__main__":
    tester = BackendTester()
    results = tester.run_all_tests()