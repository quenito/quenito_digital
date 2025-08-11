"""UI automation for multi-question pages"""

from typing import Dict, List, Any
import asyncio

class MultiQuestionUI:
    """Handles the actual UI automation for multi-question pages"""
    
    @staticmethod
    async def apply_responses(page, responses: List[Dict], debug: bool = True) -> bool:
        """Apply all responses to the page"""
        
        success_count = 0
        
        for i, response in enumerate(responses):
            if debug:
                print(f"  📝 Q{i+1}: {response['question'][:50]}...")
                print(f"     Type: {response['type']}, Category: {response['category']}")
                print(f"     Value: {response['value']}")
            
            # Apply based on type and category
            applied = await MultiQuestionUI._apply_single_response(
                page, response
            )
            
            if applied:
                success_count += 1
                if debug:
                    print(f"     ✅ Applied successfully")
            else:
                if debug:
                    print(f"     ⚠️ Failed to apply")
            
            # Small delay between fields
            await page.wait_for_timeout(200)
        
        return success_count == len(responses)
    
    @staticmethod
    async def _apply_single_response(page, response: Dict) -> bool:
        """Apply a single response to its field"""
        
        try:
            input_type = response['type'].lower()
            category = response['category']
            value = response['value']
            
            if not value:
                return False
            
            # Handle different input types
            if 'radio' in input_type:
                # Try multiple selector strategies
                selectors = [
                    f'input[type="radio"][value="{value}"]',
                    f'label:has-text("{value}")',
                    f'fieldset:has-text("{category}") label:has-text("{value}")'
                ]
                
                for selector in selectors:
                    try:
                        await page.click(selector)
                        return True
                    except:
                        continue
                        
            elif 'text' in input_type or 'textbox' in input_type:
                # Find the right text input
                if 'year' in category or 'birth' in category:
                    selectors = [
                        'input[placeholder*="year" i]',
                        'input[name*="year" i]',
                        'input[type="number"]'
                    ]
                elif 'postcode' in category:
                    selectors = [
                        'input[placeholder*="postcode" i]',
                        'input[name*="postcode" i]',
                        'input[maxlength="4"]'
                    ]
                else:
                    selectors = ['input[type="text"]:visible']
                
                # Try to find the nth text input based on question order
                all_inputs = await page.query_selector_all('input[type="text"], input[type="number"]')
                if response.get('index', 0) < len(all_inputs):
                    await all_inputs[response.get('index', 0)].fill(value)
                    return True
                
                # Fallback to selectors
                for selector in selectors:
                    try:
                        await page.fill(selector, value)
                        return True
                    except:
                        continue
                        
            elif 'dropdown' in input_type or 'select' in input_type:
                try:
                    # Try by value first
                    await page.select_option('select:visible', value=value)
                    return True
                except:
                    try:
                        # Try by label
                        await page.select_option('select:visible', label=value)
                        return True
                    except:
                        pass
                        
            elif 'checkbox' in input_type:
                selectors = [
                    f'input[type="checkbox"][value="{value}"]',
                    f'label:has-text("{value}")'
                ]
                
                for selector in selectors:
                    try:
                        await page.check(selector)
                        return True
                    except:
                        continue
                        
        except Exception as e:
            print(f"     ❌ Error applying response: {str(e)}")
            
        return False