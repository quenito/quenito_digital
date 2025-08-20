# proxy_validation_test.py
import asyncio
import aiohttp
import time
import json
from datetime import datetime

class ProxyValidator:
    """Simple proxy validation without persona integration"""
    
    def __init__(self, proxy_config):
        self.proxy_config = proxy_config
        self.proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
        self.results = {}
        
    async def run_all_tests(self):
        """Run complete validation suite"""
        print("🧪 Starting Residential Proxy Validation Tests...")
        print("🎯 Testing: MyOpinions + PrimeOpinion (VPN Detection)")
        print("🗺️  ENHANCED: Precise Postcode/ZIP Targeting Validation")
        print("=" * 60)
        
        # Test 1: Basic Connectivity
        print("Test 1: Basic Connectivity")
        connectivity = await self.test_basic_connectivity()
        print(f"Result: {'✅ PASS' if connectivity['success'] else '❌ FAIL'}")
        print(f"Details: {connectivity}")
        print()
        
        # Test 2: Enhanced IP Geolocation (with postcode precision)
        print("Test 2: 🗺️ Enhanced Geolocation + ZIP/Postcode Precision")
        geolocation = await self.test_geolocation()
        print(f"Result: {'✅ PASS' if geolocation['is_australia'] else '❌ FAIL'}")
        print(f"Details: {geolocation}")
        if geolocation.get('postcode_available'):
            print(f"🎯 POSTCODE TARGETING: ✅ Available - {geolocation.get('postcode_value')}")
        print()
        
        # Test 3: Persona-Location Matching Simulation
        print("Test 3: 🎭 Persona-Location Matching Simulation")
        persona_matching = await self.test_persona_location_matching(geolocation)
        print(f"Result: {'✅ PASS' if persona_matching['matching_viable'] else '❌ FAIL'}")
        print(f"Details: {persona_matching}")
        print()
        
        # Test 4: MyOpinions Access & Login Flow
        print("Test 4: MyOpinions Platform Access & Login Flow")
        myopinions = await self.test_myopinions_complete()
        print(f"Result: {'✅ PASS' if myopinions['overall_pass'] else '❌ FAIL'}")
        print(f"Details: {myopinions}")
        print()
        
        # Test 5: PrimeOpinion VPN Detection Test
        print("Test 5: 🔥 PrimeOpinion VPN Detection Test (CRITICAL)")
        primeopinion = await self.test_primeopinion_vpn_detection()
        print(f"Result: {'✅ PASS' if primeopinion['no_vpn_detected'] else '❌ FAIL'}")
        print(f"Details: {primeopinion}")
        print()
        
        # Test 6: Session Stickiness
        print("Test 6: Session Stickiness (10 requests)")
        stickiness = await self.test_session_stickiness()
        print(f"Result: {'✅ PASS' if stickiness['is_sticky'] else '❌ FAIL'}")
        print(f"Details: {stickiness}")
        print()
        
        # Test 7: Performance Metrics
        print("Test 7: Performance Metrics")
        performance = await self.test_performance()
        print(f"Result: {'✅ PASS' if performance['acceptable'] else '❌ FAIL'}")
        print(f"Details: {performance}")
        print()
        
        # Summary
        self.print_summary()
        
        return {
            'connectivity': connectivity,
            'geolocation': geolocation,
            'persona_matching': persona_matching,
            'myopinions': myopinions,
            'primeopinion': primeopinion,
            'session_stickiness': stickiness,
            'performance': performance
        }
    
    async def test_persona_location_matching(self, geolocation_data):
        """Test persona-location matching scenarios"""
        try:
            # Sample persona configurations for testing
            sample_personas = {
                'quenito': {
                    'profile_postcode': '2000',
                    'profile_city': 'Sydney',
                    'profile_state': 'NSW'
                },
                'quenita': {
                    'profile_postcode': '3000', 
                    'profile_city': 'Melbourne',
                    'profile_state': 'VIC'
                },
                'quintus': {
                    'profile_postcode': '4000',
                    'profile_city': 'Brisbane', 
                    'profile_state': 'QLD'
                }
            }
            
            current_location = {
                'city': geolocation_data.get('city', ''),
                'state': geolocation_data.get('region', ''),
                'postcode': geolocation_data.get('postcode_value', ''),
                'targeting_precision': geolocation_data.get('targeting_precision', 'UNKNOWN')
            }
            
            # Check which personas could use this IP location
            compatible_personas = []
            for persona_name, persona_data in sample_personas.items():
                city_match = current_location['city'].lower() in persona_data['profile_city'].lower()
                state_match = current_location['state'].upper() == persona_data['profile_state'].upper()
                postcode_match = current_location['postcode'] == persona_data['profile_postcode']
                
                compatibility_score = sum([city_match, state_match, postcode_match])
                
                if compatibility_score >= 2:  # At least city + state match
                    compatible_personas.append({
                        'persona': persona_name,
                        'city_match': city_match,
                        'state_match': state_match, 
                        'postcode_match': postcode_match,
                        'compatibility_score': compatibility_score
                    })
            
            # Assessment
            matching_viable = len(compatible_personas) > 0
            postcode_precision_available = geolocation_data.get('postcode_available', False)
            
            return {
                'matching_viable': matching_viable,
                'postcode_precision_available': postcode_precision_available,
                'current_proxy_location': current_location,
                'compatible_personas': compatible_personas,
                'total_compatible_personas': len(compatible_personas),
                'recommendation': 'EXCELLENT' if postcode_precision_available and matching_viable else 'GOOD' if matching_viable else 'NEEDS_TARGETING_ADJUSTMENT'
            }
            
        except Exception as e:
            return {
                'matching_viable': False,
                'error': str(e)
            }
    
    async def test_basic_connectivity(self):
        """Test basic proxy connection"""
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://httpbin.org/ip",
                    proxy=self.proxy_url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    data = await response.json()
                    response_time = time.time() - start_time
                    
                    return {
                        'success': True,
                        'proxy_ip': data['origin'],
                        'response_time': round(response_time, 2)
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time': None
            }
    
    async def test_geolocation(self):
        """Test if proxy provides Australian IP with PRECISE location targeting"""
        try:
            async with aiohttp.ClientSession() as session:
                # Test 1: Basic geolocation
                async with session.get(
                    "http://ip-api.com/json",
                    proxy=self.proxy_url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    data = await response.json()
                    
                    is_australia = data.get('country') == 'Australia'
                    
                    # Test 2: More detailed location check
                    location_details = {
                        'is_australia': is_australia,
                        'country': data.get('country'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'zip': data.get('zip'),
                        'ip': data.get('query'),
                        'isp': data.get('isp'),
                        'lat': data.get('lat'),
                        'lon': data.get('lon')
                    }
                    
                # Test 3: Cross-verify with another geolocation service
                async with session.get(
                    "https://ipapi.co/json/",
                    proxy=self.proxy_url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response2:
                    data2 = await response2.json()
                    
                    # Verify consistency across services
                    location_consistent = (
                        data.get('country') == data2.get('country_name') and
                        data.get('regionName') == data2.get('region')
                    )
                    
                    # Enhanced location validation
                    precise_targeting_verified = {
                        'postcode_available': data2.get('postal') is not None,
                        'postcode_value': data2.get('postal'),
                        'timezone': data2.get('timezone'),
                        'location_consistent': location_consistent
                    }
                    
                    return {
                        **location_details,
                        **precise_targeting_verified,
                        'targeting_precision': 'ZIP_LEVEL' if data2.get('postal') else 'CITY_LEVEL'
                    }
                    
        except Exception as e:
            return {
                'is_australia': False,
                'error': str(e)
            }
    
    async def test_myopinions_complete(self):
        """Complete MyOpinions platform testing including login flow"""
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=20)
            ) as session:
                
                # Test 1: Homepage access
                homepage_result = await self._test_myopinions_homepage(session)
                
                # Test 2: Login page access
                login_page_result = await self._test_myopinions_login_page(session)
                
                # Test 3: Dashboard access (simulated)
                dashboard_result = await self._test_myopinions_dashboard(session)
                
                # Test 4: Login flow simulation
                login_flow_result = await self._test_myopinions_login_flow(session)
                
                overall_pass = (
                    homepage_result['success'] and
                    login_page_result['success'] and
                    dashboard_result['success'] and
                    login_flow_result['login_endpoint_accessible']
                )
                
                return {
                    'overall_pass': overall_pass,
                    'homepage': homepage_result,
                    'login_page': login_page_result,
                    'dashboard': dashboard_result,
                    'login_flow': login_flow_result
                }
                
        except Exception as e:
            return {
                'overall_pass': False,
                'error': str(e)
            }
    
    async def _test_myopinions_homepage(self, session):
        """Test MyOpinions homepage"""
        try:
            async with session.get(
                "https://www.myopinions.com.au",
                proxy=self.proxy_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            ) as response:
                content = await response.text()
                
                return {
                    'success': response.status == 200,
                    'status_code': response.status,
                    'has_signup': 'sign up' in content.lower() or 'signup' in content.lower(),
                    'has_login_link': 'login' in content.lower(),
                    'no_geo_restrictions': 'restricted' not in content.lower() and 'unavailable' not in content.lower()
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _test_myopinions_login_page(self, session):
        """Test MyOpinions login page"""
        try:
            async with session.get(
                "https://www.myopinions.com.au/auth/login",
                proxy=self.proxy_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            ) as response:
                content = await response.text()
                
                return {
                    'success': response.status == 200,
                    'status_code': response.status,
                    'has_email_field': 'email' in content.lower(),
                    'has_password_field': 'password' in content.lower(),
                    'has_login_button': 'sign in' in content.lower() or 'login' in content.lower(),
                    'no_captcha_required': 'captcha' not in content.lower()
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _test_myopinions_dashboard(self, session):
        """Test MyOpinions dashboard URL (without login)"""
        try:
            async with session.get(
                "https://www.myopinions.com.au/auth/dashboard",
                proxy=self.proxy_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                allow_redirects=False
            ) as response:
                # Expect redirect to login (302/301) or auth required (401/403)
                valid_responses = [200, 301, 302, 401, 403]
                
                return {
                    'success': response.status in valid_responses,
                    'status_code': response.status,
                    'redirects_to_login': response.status in [301, 302],
                    'requires_auth': response.status in [401, 403]
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _test_myopinions_login_flow(self, session):
        """Test MyOpinions login endpoint (simulation only)"""
        try:
            # Test POST to login endpoint with dummy data to see if endpoint is accessible
            login_data = {
                'email': 'test@example.com',
                'password': 'testpassword'
            }
            
            async with session.post(
                "https://www.myopinions.com.au/auth/login",
                proxy=self.proxy_url,
                data=login_data,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            ) as response:
                content = await response.text()
                
                # We expect login to fail (invalid credentials) but endpoint should be accessible
                login_endpoint_accessible = response.status in [200, 400, 401, 422]  # Valid responses
                no_geo_blocking = 'location' not in content.lower() and 'country' not in content.lower()
                
                return {
                    'login_endpoint_accessible': login_endpoint_accessible,
                    'status_code': response.status,
                    'no_geo_blocking': no_geo_blocking,
                    'expected_auth_failure': response.status in [400, 401, 422]
                }
        except Exception as e:
            return {'login_endpoint_accessible': False, 'error': str(e)}
    
    async def test_primeopinion_vpn_detection(self):
        """🔥 CRITICAL: Test PrimeOpinion VPN detection (the ultimate test!)"""
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=20)
            ) as session:
                
                # Test 1: Homepage access
                homepage_result = await self._test_primeopinion_homepage(session)
                
                # Test 2: Login page
                login_result = await self._test_primeopinion_login(session)
                
                # Test 3: App platform access
                app_result = await self._test_primeopinion_app(session)
                
                # Test 4: VPN detection check
                vpn_check_result = await self._test_primeopinion_vpn_check(session)
                
                # Overall assessment
                no_vpn_detected = (
                    homepage_result['no_vpn_warning'] and
                    login_result['no_vpn_warning'] and
                    app_result['no_vpn_warning'] and
                    vpn_check_result['no_vpn_detected']
                )
                
                return {
                    'no_vpn_detected': no_vpn_detected,
                    'homepage': homepage_result,
                    'login': login_result,
                    'app_platform': app_result,
                    'vpn_check': vpn_check_result
                }
                
        except Exception as e:
            return {
                'no_vpn_detected': False,
                'error': str(e)
            }
    
    async def _test_primeopinion_homepage(self, session):
        """Test PrimeOpinion homepage for VPN detection"""
        try:
            async with session.get(
                "https://www.primeopinion.com.au",
                proxy=self.proxy_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            ) as response:
                content = await response.text()
                
                # Check for VPN detection messages
                vpn_keywords = ['vpn', 'proxy', 'detected', 'blocked', 'not allowed', 'restricted']
                no_vpn_warning = not any(keyword in content.lower() for keyword in vpn_keywords)
                
                return {
                    'success': response.status == 200,
                    'status_code': response.status,
                    'no_vpn_warning': no_vpn_warning,
                    'has_login_option': 'login' in content.lower(),
                    'content_length': len(content)
                }
        except Exception as e:
            return {'success': False, 'no_vpn_warning': False, 'error': str(e)}
    
    async def _test_primeopinion_login(self, session):
        """Test PrimeOpinion login page"""
        try:
            async with session.get(
                "https://app.primeopinion.com/login",
                proxy=self.proxy_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            ) as response:
                content = await response.text()
                
                # Check for VPN detection
                vpn_keywords = ['vpn', 'proxy', 'detected', 'blocked', 'not allowed']
                no_vpn_warning = not any(keyword in content.lower() for keyword in vpn_keywords)
                
                return {
                    'success': response.status == 200,
                    'status_code': response.status,
                    'no_vpn_warning': no_vpn_warning,
                    'has_login_form': 'password' in content.lower() and 'email' in content.lower(),
                    'loads_normally': response.status == 200 and len(content) > 1000
                }
        except Exception as e:
            return {'success': False, 'no_vpn_warning': False, 'error': str(e)}
    
    async def _test_primeopinion_app(self, session):
        """Test PrimeOpinion app platform"""
        try:
            async with session.get(
                "https://app.primeopinion.com/",
                proxy=self.proxy_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            ) as response:
                content = await response.text()
                
                # Check for VPN detection
                vpn_keywords = ['vpn', 'proxy', 'detected', 'blocked', 'not allowed']
                no_vpn_warning = not any(keyword in content.lower() for keyword in vpn_keywords)
                
                return {
                    'success': response.status == 200,
                    'status_code': response.status,
                    'no_vpn_warning': no_vpn_warning,
                    'redirects_to_login': 'login' in content.lower(),
                    'app_loads': response.status == 200
                }
        except Exception as e:
            return {'success': False, 'no_vpn_warning': False, 'error': str(e)}
    
    async def _test_primeopinion_vpn_check(self, session):
        """Specific VPN detection test for PrimeOpinion"""
        try:
            # Try to access a survey-related endpoint that might trigger VPN detection
            endpoints_to_test = [
                "https://app.primeopinion.com/dashboard",
                "https://app.primeopinion.com/surveys",
                "https://app.primeopinion.com/profile"
            ]
            
            vpn_detected = False
            results = []
            
            for endpoint in endpoints_to_test:
                try:
                    async with session.get(
                        endpoint,
                        proxy=self.proxy_url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                        allow_redirects=True
                    ) as response:
                        content = await response.text()
                        
                        # Check for VPN detection messages
                        vpn_keywords = ['vpn detected', 'proxy detected', 'using vpn', 'vpn or proxy', 'connection blocked']
                        endpoint_vpn_detected = any(keyword in content.lower() for keyword in vpn_keywords)
                        
                        if endpoint_vpn_detected:
                            vpn_detected = True
                            
                        results.append({
                            'endpoint': endpoint,
                            'status': response.status,
                            'vpn_detected': endpoint_vpn_detected
                        })
                        
                except Exception as e:
                    results.append({
                        'endpoint': endpoint,
                        'error': str(e),
                        'vpn_detected': None
                    })
            
            return {
                'no_vpn_detected': not vpn_detected,
                'endpoints_tested': len(endpoints_to_test),
                'results': results
            }
            
        except Exception as e:
            return {
                'no_vpn_detected': False,
                'error': str(e)
            }
    
    async def test_session_stickiness(self, num_requests=10):
        """Test if IP stays the same across multiple requests"""
        ips = []
        
        try:
            async with aiohttp.ClientSession() as session:
                for i in range(num_requests):
                    async with session.get(
                        "https://httpbin.org/ip",
                        proxy=self.proxy_url,
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as response:
                        data = await response.json()
                        ips.append(data['origin'])
                        
                    # Small delay between requests
                    await asyncio.sleep(0.5)
            
            unique_ips = list(set(ips))
            is_sticky = len(unique_ips) == 1
            
            return {
                'is_sticky': is_sticky,
                'unique_ips': unique_ips,
                'total_requests': num_requests,
                'ip_changes': len(unique_ips) - 1
            }
            
        except Exception as e:
            return {
                'is_sticky': False,
                'error': str(e)
            }
    
    async def test_performance(self, num_tests=5):
        """Test proxy performance metrics"""
        response_times = []
        success_count = 0
        
        for i in range(num_tests):
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://httpbin.org/ip",
                        proxy=self.proxy_url,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        await response.json()
                        response_time = time.time() - start_time
                        response_times.append(response_time)
                        success_count += 1
                        
            except Exception:
                response_times.append(None)
            
            await asyncio.sleep(1)
        
        valid_times = [t for t in response_times if t is not None]
        avg_response_time = sum(valid_times) / len(valid_times) if valid_times else 0
        success_rate = success_count / num_tests
        
        # Performance criteria
        acceptable = (
            avg_response_time < 5.0 and  # Under 5 seconds
            success_rate >= 0.8  # 80%+ success rate
        )
        
        return {
            'acceptable': acceptable,
            'avg_response_time': round(avg_response_time, 2),
            'success_rate': round(success_rate, 2),
            'total_tests': num_tests,
            'successful_tests': success_count
        }
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 60)
        print("🎯 VALIDATION SUMMARY - MyOpinions + PrimeOpinion")
        print("=" * 60)
        print("📊 Tests Completed:")
        print("   ✅ Basic proxy connectivity")
        print("   ✅ Australian IP geolocation") 
        print("   ✅ MyOpinions complete access (including login flows)")
        print("   ✅ PrimeOpinion VPN detection test (CRITICAL)")
        print("   ✅ Session stickiness validation")
        print("   ✅ Performance metrics")
        print("")
        print("💡 Decision Matrix:")
        print("   🟢 ALL PASS → Integrate with persona system")  
        print("   🟡 PARTIAL → Investigate specific failures")
        print("   🔴 VPN DETECTED → Try different provider")
        print("")
        print("🎯 Next Steps:")
        print("   ✅ If PrimeOpinion passes → Infrastructure validated")
        print("   ❌ If PrimeOpinion fails → Test alternative providers")
        print("=" * 60)


# Enhanced usage with both platforms + CORRECT DECODO ENDPOINTS
async def main():
    """Main validation runner for MyOpinions + PrimeOpinion"""
    
    print("🚀 QUENITO PROXY VALIDATION - MyOpinions + PrimeOpinion")
    print("🎯 Testing with DECODO (formerly Smartproxy) - The REAL Provider!")
    print("=" * 60)
    
    # DECODO CONFIGURATION (replace with your actual credentials)
    proxy_config = {
        'host': 'gate.smartproxy.com',        # Decodo's residential proxy gateway
        'port': 10001,                        # Standard residential port
        'username': 'user-quenito-country-au-city-sydney-sessionduration-60',   # From Decodo dashboard
        'password': '2bMVyGu6_gepcV6g3n'    # From Decodo dashboard
    }
    
    print("📋 Decodo Proxy Configuration:")
    print(f"   Provider: Decodo (formerly Smartproxy)")
    print(f"   Host: {proxy_config['host']}")
    print(f"   Port: {proxy_config['port']}")
    print(f"   Username: {proxy_config['username']}")
    print(f"   🎯 Testing Australian residential IPs")
    print("")
    
    validator = ProxyValidator(proxy_config)
    results = await validator.run_all_tests()
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'decodo_proxy_validation_myopinions_primeopinion_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📄 Detailed results saved to: {filename}")
    
    # Final recommendation
    print("\n" + "=" * 60)
    print("🎯 FINAL RECOMMENDATION:")
    
    critical_tests_passed = (
        results.get('connectivity', {}).get('success', False) and
        results.get('geolocation', {}).get('is_australia', False) and
        results.get('myopinions', {}).get('overall_pass', False) and
        results.get('primeopinion', {}).get('no_vpn_detected', False) and
        results.get('session_stickiness', {}).get('is_sticky', False)
    )
    
    if critical_tests_passed:
        print("✅ 🚀 GREEN LIGHT - PROCEED WITH PERSONA INTEGRATION!")
        print("   🎉 Decodo residential proxies VALIDATED for survey automation")
        print("   ✅ MyOpinions + PrimeOpinion both accessible without detection")
        print("   🔥 Ready to scale Quenito system with multi-persona infrastructure!")
    else:
        print("❌ 🛑 RED LIGHT - INVESTIGATE ISSUES FIRST")
        print("   Some critical tests failed - review results before proceeding")
        print("   💡 Try different Decodo configuration or contact their support")
    
    print("=" * 60)
    
    return results

# DECODO QUICK SETUP GUIDE
async def decodo_quick_setup_test(username, password):
    """Quick test runner specifically for Decodo credentials"""
    
    print("🎯 DECODO QUICK SETUP TEST")
    print("=" * 40)
    
    # Decodo standard configuration
    proxy_config = {
        'host': 'gate.smartproxy.com',    # Decodo's main gateway
        'port': 10000,                    # Residential proxy port
        'username': username,             # Your Decodo username  
        'password': password              # Your Decodo password
    }
    
    print(f"🔗 Testing connection to: {proxy_config['host']}:{proxy_config['port']}")
    print(f"👤 Username: {username}")
    print("")
    
    validator = ProxyValidator(proxy_config)
    
    # Critical tests only
    print("⚡ Running critical tests...")
    
    # Test 1: Basic connectivity + IP check
    print("1️⃣ Testing basic connectivity...")
    connectivity = await validator.test_basic_connectivity()
    if connectivity['success']:
        print(f"   ✅ Connected! Your IP: {connectivity['proxy_ip']}")
        print(f"   ⚡ Response time: {connectivity['response_time']}s")
    else:
        print(f"   ❌ Connection failed: {connectivity.get('error', 'Unknown error')}")
        return False
    
    # Test 2: Australia geolocation  
    print("2️⃣ Testing Australian geolocation...")
    geolocation = await validator.test_geolocation()
    if geolocation['is_australia']:
        print(f"   ✅ Australian IP confirmed!")
        print(f"   📍 Location: {geolocation.get('city', 'N/A')}, {geolocation.get('region', 'N/A')}")
        print(f"   🏢 ISP: {geolocation.get('isp', 'N/A')}")
    else:
        print(f"   ❌ Not Australian IP: {geolocation.get('country', 'Unknown')}")
        return False
    
    # Test 3: The ultimate test - PrimeOpinion VPN detection
    print("3️⃣ 🔥 THE ULTIMATE TEST: PrimeOpinion VPN Detection...")
    primeopinion = await validator.test_primeopinion_vpn_detection()
    if primeopinion['no_vpn_detected']:
        print("   ✅ 🎉 NO VPN DETECTED! PrimeOpinion accepts Decodo IPs!")
        print("   🚀 This means ALL survey platforms will work!")
    else:
        print("   ❌ VPN detected by PrimeOpinion - may need different configuration")
        return False
    
    print("")
    print("🎉 SUCCESS! Decodo residential proxies are VALIDATED!")
    print("🚀 Ready for multi-persona survey automation scaling!")
    
    return True

# STEP-BY-STEP DECODO SETUP INSTRUCTIONS (with Persona-Postcode Matching)
def print_decodo_setup_instructions():
    """Print detailed Decodo setup instructions with postcode targeting"""
    
    print("📋 DECODO SETUP INSTRUCTIONS - Enhanced Persona-Postcode Matching")
    print("=" * 70)
    print("")
    print("🎯 Step 1: Sign up for Decodo")
    print("   1. Go to: https://decodo.com/proxies/residential-proxies")
    print("   2. Click 'Start Free Trial' (100MB for 3 days)")
    print("   3. Sign up with your email")
    print("   4. Verify email and login")
    print("")
    print("🗺️  Step 2: Configure Precise Location Targeting")
    print("   1. Login to Decodo dashboard")
    print("   2. Go to 'Residential Proxies' section")
    print("   3. Configure location targeting:")
    print("      📍 PERSONA EXAMPLES:")
    print("      ")
    print("      🎭 Quenito Profile:")
    print("         - Country: Australia")
    print("         - State: New South Wales")
    print("         - City: Sydney") 
    print("         - ZIP Code: 2000 (Sydney CBD)")
    print("         - Username format: 'username-country-AU-state-NSW-city-Sydney-zip-2000'")
    print("")
    print("      🎭 Quenita Profile:")
    print("         - Country: Australia")
    print("         - State: Victoria")
    print("         - City: Melbourne")
    print("         - ZIP Code: 3000 (Melbourne CBD)")
    print("         - Username format: 'username-country-AU-state-VIC-city-Melbourne-zip-3000'")
    print("")
    print("🔑 Step 3: Get Your Targeted Credentials")
    print("   1. Set your preferred persona location in dashboard")
    print("   2. Copy the generated credentials:")
    print("      - Endpoint: gate.smartproxy.com:10000")
    print("      - Username: (includes your targeting parameters)")
    print("      - Password: (your account password)")
    print("   3. Note: Each persona needs separate targeting configuration")
    print("")
    print("⚙️ Step 4: Enable Sticky Sessions")
    print("   1. In proxy settings, enable 'Sticky Sessions'")
    print("   2. Set duration to 30 minutes (max for surveys)")
    print("   3. This ensures same IP throughout survey completion")
    print("")
    print("🧪 Step 5: Run Enhanced Validation Test")
    print("   1. Update proxy_config in this script with your targeted credentials")
    print("   2. Run: python proxy_validation_test.py")
    print("   3. Look for these specific results:")
    print("      ✅ Australian IP confirmed")
    print("      ✅ Postcode targeting working (shows specific postcode)")
    print("      ✅ Persona-location matching viable")
    print("      ✅ PrimeOpinion no VPN detection")
    print("")
    print("💡 Step 6: Multi-Persona Scaling Strategy")
    print("   📋 RECOMMENDED PERSONA DISTRIBUTION:")
    print("   ")
    print("   🏢 Major Cities (High IP Availability):")
    print("      - Quenito: Sydney 2000 (CBD)")
    print("      - Quenita: Melbourne 3000 (CBD)")
    print("      - Quintus: Brisbane 4000 (CBD)")
    print("      - Quinta: Perth 6000 (CBD)")
    print("      - Quincy: Adelaide 5000 (CBD)")
    print("")
    print("   🏘️  Suburban Areas (Authentic Targeting):")
    print("      - Persona 6: Sydney 2121 (Parramatta)")
    print("      - Persona 7: Melbourne 3150 (Glen Waverley)")  
    print("      - Persona 8: Brisbane 4101 (South Brisbane)")
    print("      - Persona 9: Sydney 2020 (Mascot)")
    print("      - Persona 10: Melbourne 3181 (Prahran)")
    print("")
    print("🎯 Step 7: Verification & Testing")
    print("   1. Each persona proxy should show IP from their target postcode")
    print("   2. Survey platforms see perfect location consistency")
    print("   3. No 'location mismatch' red flags")
    print("   4. Behavioral authenticity maximized")
    print("")
    print("🆘 Troubleshooting:")
    print("   - No postcode in results: Contact Decodo for ZIP targeting")
    print("   - Wrong location: Verify targeting parameters in username")
    print("   - VPN still detected: Try different postcode/city combination")
    print("   - Need help: Decodo has 24/7 live chat support")
    print("")
    print("🚀 SUCCESS INDICATORS:")
    print("   ✅ Postcode matches persona profile exactly")
    print("   ✅ City/State consistent with persona demographics") 
    print("   ✅ PrimeOpinion accepts proxy without VPN warning")
    print("   ✅ MyOpinions loads normally with login access")
    print("   ✅ Ready for authentic multi-persona scaling!")
    print("")
    print("💰 BUSINESS IMPACT:")
    print("   🎯 Perfect location matching = Undetectable automation")
    print("   📈 Multi-persona scaling = $2000+/week revenue potential")
    print("   🛡️  Platform compliance = Long-term account sustainability")
    print("")

if __name__ == "__main__":
    print_decodo_setup_instructions()
    
    # Option 1: Full validation test suite
    print("🚀 Starting full validation test...")
    asyncio.run(main())
    
    # Option 2: Quick test (uncomment and add your Decodo credentials)
    # print("⚡ Starting quick setup test...")
    # result = asyncio.run(decodo_quick_setup_test(
    #     username="your_decodo_username",
    #     password="your_decodo_password"
    # ))
    # print(f"\n🎯 Quick test result: {'✅ PASS' if result else '❌ FAIL'}")
    
    # Option 3: Just print setup instructions
    # print_decodo_setup_instructions()