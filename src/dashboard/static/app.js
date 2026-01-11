// Dashboard JavaScript

// Detect API base URL - use current origin for API calls
const API_BASE = window.location.origin + '/api';

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/statistics`, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        
        if (data.success) {
            const stats = data.data;
            document.getElementById('total-count').textContent = stats.total || 0;
            document.getElementById('recent-count').textContent = stats.recent_24h || 0;
            document.getElementById('facebook-count').textContent = stats.by_platform?.Facebook || 0;
            document.getElementById('linkedin-count').textContent = stats.by_platform?.LinkedIn || 0;
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load categories for filter
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        
        if (data.success) {
            const select = document.getElementById('category-filter');
            data.data.forEach(category => {
                const option = document.createElement('option');
                option.value = category.name;
                option.textContent = category.name.replace(/_/g, ' ').toUpperCase();
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load businesses
async function loadBusinesses() {
    const platform = document.getElementById('platform-filter').value;
    const category = document.getElementById('category-filter').value;
    
    let url = `${API_BASE}/businesses?limit=100`;
    if (platform) url += `&platform=${platform}`;
    if (category) url += `&category=${category}`;
    
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        
        if (data.success) {
            displayBusinesses(data.data);
        }
    } catch (error) {
        console.error('Error loading businesses:', error);
        document.getElementById('businesses').innerHTML = 
            '<div class="loading">Error loading businesses. Please try again.</div>';
    }
}

// Display businesses
function displayBusinesses(businesses) {
    const container = document.getElementById('businesses');
    
    if (businesses.length === 0) {
        container.innerHTML = '<div class="loading">No businesses found.</div>';
        return;
    }
    
    container.innerHTML = businesses.map(business => `
        <div class="business-card ${business.priority || 'medium'}">
            <div class="business-header">
                <div class="business-name">${escapeHtml(business.business_name || 'Unknown')}</div>
                <span class="priority-badge ${business.priority || 'medium'}">
                    ${business.priority || 'medium'}
                </span>
            </div>
            
            <div class="business-meta">
                <div class="meta-item">
                    <span>📱</span>
                    <span>${business.platform || 'N/A'}</span>
                </div>
                <div class="meta-item">
                    <span>🏢</span>
                    <span>${business.category || 'N/A'}</span>
                </div>
                <div class="meta-item">
                    <span>📍</span>
                    <span>${business.location || 'N/A'}</span>
                </div>
                <div class="meta-item">
                    <span>📅</span>
                    <span>${formatDate(business.discovered_date)}</span>
                </div>
            </div>
            
            ${business.description ? `
                <div class="business-description">
                    ${escapeHtml(business.description.substring(0, 200))}${business.description.length > 200 ? '...' : ''}
                </div>
            ` : ''}
            
            <div class="business-footer">
                <div class="score">Score: ${business.confidence_score || 0}/100</div>
                <a href="${business.page_url}" target="_blank" class="view-button">View Page →</a>
            </div>
        </div>
    `).join('');
}

// Export to CSV
async function exportCSV() {
    try {
        window.location.href = `${API_BASE}/export/csv`;
    } catch (error) {
        console.error('Error exporting CSV:', error);
        alert('Error exporting CSV. Please try again.');
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
}

// Auto-refresh every 5 minutes
setInterval(() => {
    loadStatistics();
    loadBusinesses();
}, 300000);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    loadCategories();
    loadBusinesses();
});

