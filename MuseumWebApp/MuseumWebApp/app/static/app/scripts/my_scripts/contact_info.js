document.addEventListener('DOMContentLoaded', function () {
    const detailsContainer = document.getElementById('detailsContainer');
    const detailsFullName = document.getElementById('detailsFullName');
    const detailsPhone = document.getElementById('detailsPhone');
    const detailsEmail = document.getElementById('detailsEmail');
    const detailsPosition = document.getElementById('detailsPosition');
    const detailsHall = document.getElementById('detailsHall');
    const tableBody = document.getElementById('employeeTableBody'); // Родительский элемент для строк таблицы

    // Делегирование событий для кликов по строкам
    tableBody.addEventListener('click', (event) => {
        const row = event.target.closest('.employee-row'); // Проверяем, кликнули ли по строке
        if (row) {
            const cells = row.querySelectorAll('td');
            detailsFullName.textContent = cells[2].textContent.trim();
            detailsPhone.textContent = cells[3].textContent.trim();
            detailsEmail.textContent = cells[4].textContent.trim();
            detailsPosition.textContent = cells[5].textContent.trim();
            detailsHall.textContent = cells[6].textContent.trim();

            // Показываем блок с деталями
            detailsContainer.style.display = 'block';
        }
    });

    // По умолчанию скрываем блок деталей
    detailsContainer.style.display = 'none';
});
