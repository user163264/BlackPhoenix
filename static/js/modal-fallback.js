/**
 * Quick fix for Add Prompt Modal if Bootstrap isn't working correctly
 */

// Alternative modal handler without Bootstrap dependency
function showAddPromptModal() {
    const modal = document.getElementById('addPromptModal');
    if (modal) {
        modal.style.display = 'block';
        modal.classList.add('show');
        document.body.classList.add('modal-open');
        
        // Create backdrop
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop fade show';
        backdrop.id = 'modal-backdrop-custom';
        document.body.appendChild(backdrop);
    }
}

function hideAddPromptModal() {
    const modal = document.getElementById('addPromptModal');
    const backdrop = document.getElementById('modal-backdrop-custom');
    
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
    }
    
    if (backdrop) {
        backdrop.remove();
    }
}

// Fallback event handlers if the main library fails
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔧 Modal fallback script loaded');
    
    // Check if main PromptLibrary is working
    setTimeout(() => {
        const saveBtn = document.getElementById('savePromptBtn');
        const addBtn = document.querySelector('[data-bs-target="#addPromptModal"]');
        
        if (saveBtn && !window.promptLibrary) {
            console.log('🚨 PromptLibrary not found, using fallback handlers');
            
            // Fallback save handler
            saveBtn.onclick = async function() {
                console.log('🔧 Fallback save handler triggered');
                
                const data = {
                    name: document.getElementById('promptName')?.value || '',
                    content: document.getElementById('promptContent')?.value || '',
                    category: document.getElementById('promptCategory')?.value || 'general',
                    description: document.getElementById('promptDescription')?.value || '',
                    tags: document.getElementById('promptTags')?.value || ''
                };
                
                if (!data.name || !data.content) {
                    alert('Please fill in name and content');
                    return;
                }
                
                try {
                    const response = await fetch('/api/prompts', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        alert('Prompt saved successfully!');
                        hideAddPromptModal();
                        location.reload();
                    } else {
                        alert('Error: ' + result.error);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            };
            
            // Fallback modal show handler
            if (addBtn) {
                addBtn.onclick = function(e) {
                    e.preventDefault();
                    showAddPromptModal();
                };
            }
            
            // Fallback close handlers
            document.querySelectorAll('[data-bs-dismiss="modal"]').forEach(btn => {
                btn.onclick = function() {
                    hideAddPromptModal();
                };
            });
        }
    }, 2000);
});
