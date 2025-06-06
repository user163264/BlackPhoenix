/**
 * Quick diagnostic script to test if the system is working
 */

// Test if the page loads correctly
console.log('🔍 System Prompts Diagnostic Script Loaded');

// Test if required elements exist
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔍 DOM loaded, running diagnostics...');
    
    // Check if required elements exist
    const requiredElements = [
        'savePromptBtn',
        'importBtn', 
        'searchInput',
        'categoryFilter',
        'clearFilters',
        'promptsContainer',
        'addPromptModal',
        'promptForm'
    ];
    
    let missing = [];
    requiredElements.forEach(id => {
        const element = document.getElementById(id);
        if (!element) {
            missing.push(id);
        }
    });
    
    if (missing.length > 0) {
        console.error('❌ Missing required elements:', missing);
    } else {
        console.log('✅ All required elements found');
    }
    
    // Test if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        console.log('✅ Bootstrap is available');
    } else {
        console.error('❌ Bootstrap is not available');
    }
    
    // Test API endpoints
    fetch('/api/prompts')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ API connection working, found', data.prompts.length, 'prompts');
            } else {
                console.error('❌ API error:', data.error);
            }
        })
        .catch(error => {
            console.error('❌ API connection failed:', error);
        });
    
    // Test form submission (debug)
    setTimeout(() => {
        const saveBtn = document.getElementById('savePromptBtn');
        if (saveBtn) {
            console.log('✅ Save button found, event listeners:', getEventListeners ? getEventListeners(saveBtn) : 'debug tools not available');
        }
    }, 1000);
    
    console.log('🔍 Diagnostic complete');
});
