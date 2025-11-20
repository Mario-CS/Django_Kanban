// Helper functions
function elem(id) {
    return document.getElementById(id);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Drag and Drop functions
let draggedElement = null;

function drag(ev) {
    draggedElement = ev.target;
    ev.dataTransfer.effectAllowed = 'move';
    ev.dataTransfer.setData('text/html', ev.target.innerHTML);
}

function allowDrop(ev) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = 'move';
}

function dragEnter(ev) {
    if (ev.target.classList && ev.target.classList.contains('section')) {
        ev.target.classList.add('drag-enter');
    }
}

function dragLeave(ev) {
    if (ev.target.classList && ev.target.classList.contains('section')) {
        ev.target.classList.remove('drag-enter');
    }
}

function drop(ev, target) {
    ev.preventDefault();
    ev.stopPropagation();
    
    if (target.classList.contains('section')) {
        target.classList.remove('drag-enter');
        
        if (draggedElement) {
            const cardId = draggedElement.getAttribute('data-card-id');
            const newColumnId = target.getAttribute('data-column-id');
            const newPosition = target.querySelectorAll('li').length;
            
            // Move in DOM
            target.appendChild(draggedElement);
            
            // Update server
            fetch(`/api/card/${cardId}/move/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    column_id: newColumnId,
                    position: newPosition
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCounters();
                } else {
                    console.error('Error moving card:', data.error);
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                location.reload();
            });
        }
    }
}

function dropDelete(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    
    const deleteList = elem('delete-list');
    deleteList.classList.remove('drag-enter');
    
    if (draggedElement) {
        const cardId = draggedElement.getAttribute('data-card-id');
        cardToDelete = cardId;
        elem('confirmTitle').innerHTML = 'LA TAREA';
        elem('confirmDelete').style.display = 'block';
        elem('confirmBox').style.display = 'block';
    }
}

// Card management functions
function editCard(cardId) {
    currentCardId = cardId;
    const card = document.querySelector(`#card-${cardId}`);
    const textSpan = card.querySelector('.txt');
    const currentText = textSpan.innerText;
    
    elem('taskText').value = currentText;
    elem('modalOverlay').style.display = 'block';
    elem('modalBox').style.display = 'block';
    elem('taskText').focus();
}

// Setup card event listeners
function setupCardListeners(card) {
    const cardId = card.getAttribute('data-card-id');
    
    // Edit on click
    const txtSpan = card.querySelector('.txt');
    if (txtSpan) {
        txtSpan.addEventListener('click', (e) => {
            e.preventDefault();
            editCard(cardId);
        });
    }
    
    // Move up
    const upBtn = card.querySelector('.up');
    if (upBtn) {
        upBtn.addEventListener('click', (e) => {
            e.preventDefault();
            moveUp(e, cardId);
        });
    }
    
    // Move down
    const downBtn = card.querySelector('.down');
    if (downBtn) {
        downBtn.addEventListener('click', (e) => {
            e.preventDefault();
            moveDown(e, cardId);
        });
    }
    
    // Delete
    const delBtn = card.querySelector('.delete');
    if (delBtn) {
        delBtn.addEventListener('click', (e) => {
            e.preventDefault();
            delTask(e, cardId);
        });
    }
}

function saveCard() {
    const newText = elem('taskText').value.trim();
    
    if (newText === '') {
        elem('taskText').setAttribute('placeholder', 'Escribe algo...');
        return;
    }
    
    if (currentCardId) {
        // Update existing card
        fetch(`/api/card/${currentCardId}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                title: newText.substring(0, 200),
                description: newText
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const card = document.querySelector(`#card-${currentCardId}`);
                const textSpan = card.querySelector('.txt');
                textSpan.innerText = newText;
                closeModal();
            } else {
                console.error('Error updating card:', data.error);
                alert('Error al actualizar la tarea');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        });
    }
}

function closeModal() {
    elem('modalOverlay').style.display = 'none';
    elem('modalBox').style.display = 'none';
    elem('taskText').value = '';
    currentCardId = null;
}

function delTask(ev, cardId) {
    if (ev) ev.preventDefault();
    cardToDelete = cardId;
    elem('confirmTitle').innerHTML = 'LA TAREA';
    elem('confirmDelete').style.display = 'block';
    elem('confirmBox').style.display = 'block';
}

function confirmDelete() {
    if (cardToDelete) {
        fetch(`/api/card/${cardToDelete}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const card = document.querySelector(`#card-${cardToDelete}`);
                if (card) {
                    card.remove();
                }
                updateCounters();
                cancelDelete();
            } else {
                console.error('Error deleting card:', data.error);
                alert('Error al eliminar la tarea');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        });
    }
}

function cancelDelete() {
    elem('confirmDelete').style.display = 'none';
    elem('confirmBox').style.display = 'none';
    cardToDelete = null;
}

function moveUp(ev, cardId) {
    if (ev) ev.preventDefault();
    const card = document.querySelector(`#card-${cardId}`);
    const prevCard = card.previousElementSibling;
    
    if (prevCard && prevCard.tagName === 'LI') {
        card.parentNode.insertBefore(card, prevCard);
        updatePositions(card.parentNode);
    }
}

function moveDown(ev, cardId) {
    if (ev) ev.preventDefault();
    const card = document.querySelector(`#card-${cardId}`);
    const nextCard = card.nextElementSibling;
    
    if (nextCard && nextCard.tagName === 'LI') {
        card.parentNode.insertBefore(nextCard, card);
        updatePositions(card.parentNode);
    }
}

function updatePositions(ul) {
    const cards = ul.querySelectorAll('li');
    const columnId = ul.getAttribute('data-column-id');
    
    cards.forEach((card, index) => {
        const cardId = card.getAttribute('data-card-id');
        fetch(`/api/card/${cardId}/move/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                column_id: columnId,
                position: index
            })
        });
    });
}

function updateCounters() {
    // Update total
    let total = 0;
    document.querySelectorAll('.section').forEach(ul => {
        const count = ul.querySelectorAll('li').length;
        total += count;
        
        // Update column counter
        const columnDiv = ul.parentNode;
        const counter = columnDiv.querySelector('h3 span');
        if (counter) {
            counter.innerText = count;
        }
    });
    
    elem('totalTask').innerText = total;
}

// Add new task button
elem('addToDo').addEventListener('click', function() {
    const firstColumn = document.querySelector('.section');
    if (!firstColumn) return;
    
    const columnId = firstColumn.getAttribute('data-column-id');
    
    fetch(`/api/board/${BOARD_ID}/card/create/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            column_id: columnId,
            title: 'Nueva tarea',
            description: 'Nueva tarea'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const card = data.card;
            
            const newLi = document.createElement('li');
            newLi.id = `card-${card.id}`;
            newLi.setAttribute('data-card-id', card.id);
            newLi.setAttribute('draggable', 'true');
            newLi.setAttribute('ondragstart', 'drag(event)');
            
            newLi.innerHTML = `
                <span class="txt" data-card-id="${card.id}">${card.title}</span>
                <span class="idTask">${card.created_by || 'Sin usuario'}</span>
                <a class="up" href="#" data-card-id="${card.id}"></a>
                <a class="down" href="#" data-card-id="${card.id}"></a>
                <a class="delete" href="#" data-card-id="${card.id}"></a>
            `;
            
            firstColumn.insertBefore(newLi, firstColumn.firstChild);
            
            // Setup event listeners for the new card
            setupCardListeners(newLi);
            
            updateCounters();
            
            // Auto-edit
            setTimeout(() => editCard(card.id), 100);
        } else {
            console.error('Error creating card:', data.error);
            alert('Error al crear la tarea');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error de conexión');
    });
});

// Delete all tasks button
elem('deleteItem').addEventListener('click', function() {
    if (elem('totalTask').innerText == '0') return;
    
    elem('confirmTitle').innerHTML = 'TODAS LAS TAREAS';
    elem('confirmDelete').style.display = 'block';
    elem('confirmBox').style.display = 'block';
    
    // Modify confirmBtn to delete all
    elem('confirmBtn').onclick = function() {
        const allCards = document.querySelectorAll('#myLists li[data-card-id]');
        allCards.forEach(card => {
            const cardId = card.getAttribute('data-card-id');
            fetch(`/api/card/${cardId}/delete/`, {
                method: 'DELETE',
                headers: {'X-CSRFToken': csrftoken}
            });
        });
        
        setTimeout(() => {
            location.reload();
        }, 500);
    };
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    updateCounters();
    
    // Setup listeners for existing cards
    document.querySelectorAll('#myLists li[data-card-id]').forEach(card => {
        setupCardListeners(card);
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
        cancelDelete();
    }
});
