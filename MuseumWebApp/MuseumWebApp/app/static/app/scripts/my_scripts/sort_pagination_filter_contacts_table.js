document.addEventListener('DOMContentLoaded', function () {
    const rowsPerPage = 3; // Количество строк на страницу
    const tableBody = document.getElementById('employeeTableBody');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const pageInfo = document.getElementById('pageInfo');
    const filterInput = document.getElementById('filterInput');
    const filterButton = document.getElementById('filterButton');
    const detailsContainer = document.getElementById('detailsContainer');
    let currentPage = 1;
    let totalPages = 1;  // Инициализация totalPages
    const tableHeaders = document.querySelectorAll('.sortable-header');
    let currentSortColumn = '';
    let currentSortOrder = 'asc';
    let selectedEmployeeIds = [];
    let selectedEmployeeNames = {};
    const bonusButton = document.getElementById('bonusButton');
    const bonusMessage = document.getElementById('bonusMessage');
    const employeeTableBody = document.getElementById('employeeTableBody');

    // Обработчик для сортировки по клику на заголовок таблицы
    tableHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            if (currentSortColumn === column) {
                // Если уже сортируем по этому столбцу, инвертировать порядок
                currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                // Если переключаемся на другой столбец, сбросить порядок на 'asc'
                currentSortOrder = 'asc';
            }
            currentSortColumn = column;

            // Загрузить данные с сортировкой и фильтром
            currentPage = 1;
            loadEmployees(currentPage, filterInput.value, currentSortColumn, currentSortOrder);

            detailsContainer.style.display = 'none';

            updateSortIndicators(currentSortColumn, currentSortOrder);
        });
    });

    // Функция загрузки сотрудников с фильтром и сортировкой
    function loadEmployees(page = 1, filter = '', sortColumn = '', sortOrder = 'asc') {
        const preloader = document.getElementById('preloader');
        if (preloader) {
            preloader.style.display = 'flex'; // Показываем прелоадер
        }

        fetch(`/api/employees/?page=${page}&rows_per_page=${rowsPerPage}&filter=${encodeURIComponent(filter)}&sort_column=${sortColumn}&sort_order=${sortOrder}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }
                renderTable(data.data);
                totalPages = data.total_pages;
                updatePagination(data.current_page, data.total_pages);
                if (preloader) {
                    preloader.style.display = 'none'; // Скрываем прелоадер после получения данных
                }
            })
            .catch(error => {
                console.error('Error fetching employees:', error);
                if (preloader) {
                    preloader.style.display = 'none'; // В случае ошибки скрываем прелоадер
                }
            });
    }

    // Функция для рендера таблицы
    function renderTable(data) {
        tableBody.innerHTML = '';
        data.forEach(emp => {
            const isChecked = selectedEmployeeIds.includes(String(emp.id)); // Проверяем, выбран ли этот ID
            const row = document.createElement('tr');
            row.classList.add('employee-row');
            row.innerHTML = `
            <td><input type="checkbox" name="selected_employees" value="${emp.id}" ${isChecked ? 'checked' : ''}></td>
            <td>${emp.photo ? `<img src="${emp.photo}" alt="Photo of ${emp.full_name}" class="employee-photo">` : 'No Photo'}</td>
            <td>${emp.full_name}</td>
            <td>${emp.phone}</td>
            <td>${emp.email}</td>
            <td>${emp.position}</td>
            <td>${emp.hall}</td>
        `;
            tableBody.appendChild(row);
        });
    }

    // Обработчик для изменения состояния чекбокса
    document.addEventListener('change', (event) => {
        if (event.target.type === 'checkbox' && event.target.name === 'selected_employees') {
            const employeeId = event.target.value;
            const employeeName = event.target.closest('tr').querySelector('td:nth-child(3)').textContent.trim(); // Получаем имя сотрудника

            if (event.target.checked) {
                if (!selectedEmployeeIds.includes(employeeId)) {
                    selectedEmployeeIds.push(employeeId);
                    selectedEmployeeNames[employeeId] = employeeName;
                }
            } else {
                selectedEmployeeIds = selectedEmployeeIds.filter(id => id !== employeeId);
                delete selectedEmployeeNames[employeeId]; // Удаляем имя из словаря
            }
        }
    });

    bonusButton.addEventListener('click', () => {
        if (selectedEmployeeIds.length === 0) {
            bonusMessage.classList.remove('success');
            bonusMessage.classList.add('error');
            bonusMessage.innerHTML = `<strong>Oops!</strong> Please select employees to award a bonus.`;
            bonusMessage.style.display = 'block';
            return;
        }

        // Создаем список сотрудников для премирования
        const employeeList = Object.values(selectedEmployeeNames).map(name => `<li>${name}</li>`).join('');

        bonusMessage.classList.remove('error');
        bonusMessage.classList.add('success');
        bonusMessage.innerHTML = `
        <strong>Success!</strong> Bonus has been awarded to the following employees:
        <ul style="margin-top: 10px; text-align: left;">${employeeList}</ul>
    `;
        bonusMessage.style.display = 'block';
    });

    // Функция для обновления пагинации
    function updatePagination(current, total) {
        pageInfo.textContent = `Page ${current} of ${total}`;
        prevButton.disabled = String(current) === '1'; // Преобразуем current в строку
        nextButton.disabled = String(current) === String(total); // Преобразуем total в строку
    }

    // Обновление стрелок сортировки
    function updateSortIndicators(column, order) {
        tableHeaders.forEach(header => {
            const arrow = header.querySelector('.sort-arrow');
            if (header.dataset.column === column) {
                // Используем innerHTML для корректного отображения символов
                arrow.innerHTML = order === 'asc' ? '&#x21c8;' : '&#x21cA;';
            } else {
                arrow.innerHTML = '&#x21c5;'; // Значение по умолчанию
            }
        });
    }

    // Обработчик для кнопки "Previous"
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadEmployees(currentPage, filterInput.value, currentSortColumn, currentSortOrder); // Передаем параметры сортировки
        }
    });

    // Обработчик для кнопки "Next"
    nextButton.addEventListener('click', () => {
        currentPage++;
        loadEmployees(currentPage, filterInput.value, currentSortColumn, currentSortOrder); // Передаем параметры сортировки
    });

    // Обработчик для фильтрации
    filterButton.addEventListener('click', () => {
        currentPage = 1;  // Сбросить на первую страницу
        detailsContainer.style.display = 'none';
        loadEmployees(currentPage, filterInput.value, currentSortColumn, currentSortOrder);
    });

    // Инициализация начальной загрузки данных
    loadEmployees();

});