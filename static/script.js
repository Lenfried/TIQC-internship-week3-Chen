let currentDb = 'mysql';
let currentMode = 'create';
let currentCardId = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCards('mysql');
    loadCards('mongodb');
});

// Tab switching
function switchTab(db) {
    currentDb = db;
    
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${db}-tab`).classList.add('active');
}

// Load cards from database
async function loadCards(db) {
    const container = document.getElementById(`${db}-cards`);
    container.innerHTML = '<div class="loading">Loading cards...</div>';
    
    try {
        const response = await fetch(`/api/${db}/cards`);
        const result = await response.json();
        
        if (result.success) {
            displayCards(db, result.data);
        } else {
            container.innerHTML = `<div class="empty-state"><h3>Error</h3><p>${result.error}</p></div>`;
        }
    } catch (error) {
        container.innerHTML = `<div class="empty-state"><h3>Error</h3><p>Failed to load cards: ${error.message}</p></div>`;
    }
}

// Display cards in grid
function displayCards(db, cards) {
    const container = document.getElementById(`${db}-cards`);
    
    if (cards.length === 0) {
        container.innerHTML = '<div class="empty-state"><h3>No cards found</h3><p>Click "Add New Card" to get started!</p></div>';
        return;
    }
    
    container.innerHTML = cards.map(card => createCardHTML(db, card)).join('');
}

// Create card HTML
function createCardHTML(db, card) {
    const id = card.id || card._id;
    return `
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">${escapeHtml(card.name)}</div>
                    <div class="card-manufacturer">${escapeHtml(card.manufacturer)} ${escapeHtml(card.model)}</div>
                </div>
                <div class="card-actions">
                    <button class="card-btn btn-warning" onclick="openModal('${db}', 'edit', ${JSON.stringify(card).replace(/"/g, '&quot;')})">✏️ Edit</button>
                    <button class="card-btn btn-danger" onclick="deleteCard('${db}', '${id}')">🗑️ Delete</button>
                </div>
            </div>
            <div class="card-info">
                <div class="info-item">
                    <div class="info-label">Memory</div>
                    <div class="info-value">${card.memory_gb} GB ${card.memory_type}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Core Clock</div>
                    <div class="info-value">${card.core_clock_mhz} MHz</div>
                </div>
                ${card.boost_clock_mhz ? `
                <div class="info-item">
                    <div class="info-label">Boost Clock</div>
                    <div class="info-value">${card.boost_clock_mhz} MHz</div>
                </div>
                ` : ''}
                ${card.price_usd ? `
                <div class="info-item">
                    <div class="info-label">Price</div>
                    <div class="info-value">$${parseFloat(card.price_usd).toFixed(2)}</div>
                </div>
                ` : ''}
                ${card.release_date ? `
                <div class="info-item">
                    <div class="info-label">Release Date</div>
                    <div class="info-value">${formatDate(card.release_date)}</div>
                </div>
                ` : ''}
            </div>
        </div>
    `;
}

// Open modal for create/edit
function openModal(db, mode, cardData = null) {
    currentDb = db;
    currentMode = mode;
    currentCardId = cardData ? (cardData.id || cardData._id) : null;
    
    const modal = document.getElementById('modal');
    const form = document.getElementById('card-form');
    const title = document.getElementById('modal-title');
    
    title.textContent = mode === 'create' ? 'Add New Graphics Card' : 'Edit Graphics Card';
    
    // Reset form
    form.reset();
    document.getElementById('db-type').value = db;
    
    // Populate form if editing
    if (cardData) {
        document.getElementById('card-id').value = currentCardId;
        document.getElementById('name').value = cardData.name || '';
        document.getElementById('manufacturer').value = cardData.manufacturer || '';
        document.getElementById('model').value = cardData.model || '';
        document.getElementById('memory_gb').value = cardData.memory_gb || '';
        document.getElementById('memory_type').value = cardData.memory_type || '';
        document.getElementById('core_clock_mhz').value = cardData.core_clock_mhz || '';
        document.getElementById('boost_clock_mhz').value = cardData.boost_clock_mhz || '';
        document.getElementById('price_usd').value = cardData.price_usd || '';
        
        // Format date for input (YYYY-MM-DD)
        if (cardData.release_date) {
            const date = new Date(cardData.release_date);
            document.getElementById('release_date').value = date.toISOString().split('T')[0];
        }
    }
    
    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Handle form submission
document.getElementById('card-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const db = formData.get('db_type');
    const cardId = formData.get('id');
    const mode = cardId ? 'edit' : 'create';
    
    const data = {
        name: formData.get('name'),
        manufacturer: formData.get('manufacturer'),
        model: formData.get('model'),
        memory_gb: parseInt(formData.get('memory_gb')),
        memory_type: formData.get('memory_type'),
        core_clock_mhz: parseInt(formData.get('core_clock_mhz')),
    };
    
    // Optional fields
    const boostClock = formData.get('boost_clock_mhz');
    if (boostClock) data.boost_clock_mhz = parseInt(boostClock);
    
    const price = formData.get('price_usd');
    if (price) data.price_usd = parseFloat(price);
    
    const releaseDate = formData.get('release_date');
    if (releaseDate) data.release_date = releaseDate;
    
    try {
        let url = `/api/${db}/cards`;
        let method = 'POST';
        
        if (mode === 'edit') {
            url = `/api/${db}/cards/${cardId}`;
            method = 'PUT';
        }
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            closeModal();
            loadCards(db);
            alert('Card ' + (mode === 'create' ? 'created' : 'updated') + ' successfully!');
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Failed to save card: ' + error.message);
    }
});

// Delete card
async function deleteCard(db, cardId) {
    if (!confirm('Are you sure you want to delete this card?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/${db}/cards/${cardId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            loadCards(db);
            alert('Card deleted successfully!');
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Failed to delete card: ' + error.message);
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
}
