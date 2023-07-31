
var index_table = document.getElementById('index-table');

// display add cash form when add cash button is clicked
$('#cash-btn').click(function(){
    $('#add-cash').addClass('active');
});

const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        var row_symbol = '';
        if (button.classList.contains('sell-btn')) {
            var currow = $(button).closest('tr');
            row_symbol = currow.find('td:eq(0)').text();
            document.getElementById('sell-form-symbol').value = row_symbol;
        }
        // get the model the button is pointing to
        const modal = document.querySelector(button.dataset.modalTarget)
        openModal(modal)
    })
})

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        // get the model closest to the close button
        const modal = button.closest('.modal')
        closeModal(modal)
    })
})

function openModal(modal) {
    if(modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal) {
    if(modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}

// Chart
let ctx = document.getElementById('sharesChart').getContext('2d');
let colorhex = ['#FB3640', '#EFCA0B', '#43AA8B', '#253D5B'];

let sharesChart = new Chart(ctx, {
    type: 'pie',
    data: {
        datasets: [{
            data: shares,
            backgroundColor: colorhex
        }],
        labels: labels
    },
    options: {
        responsive: true,
        legend: {
            position: 'bottom'
        },
        plugins: {
            datalabels: {
                color: '#fff'
            }
        }
    }
})