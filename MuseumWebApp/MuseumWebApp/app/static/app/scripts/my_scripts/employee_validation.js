document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('employeeForm');
    const phoneInput = document.getElementById('employeePhone');
    const urlInput = document.getElementById('employeePhoto');
    const nameInput = document.getElementById('employeeName');
    const emailInput = document.getElementById('employeeEmail');
    const positionSelect = document.getElementById('employeePosition');
    const hallSelect = document.getElementById('employeeHall');
    const addButton = document.getElementById('submitEmployeeForm');
    const validationMessage = document.getElementById('formValidationMessage');

    // Регулярное выражение для проверки URL (начинается с http:// или https:// и заканчивается на .php или .html)
    const urlRegex = /^(https?:\/\/[^\s]+(\.php|\.html))$/;

    // Регулярное выражение для проверки телефона (разные форматы)
    const phoneRegex = /^(8|\+375)[\s\-]?\(?\d{2,3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/;

    function validateForm() {
        let isFormValid = true;

        // Проверка каждого поля
        if (!nameInput.value.trim()) isFormValid = false;
        if (!urlInput.value.trim()) isFormValid = false;
        if (!phoneInput.value.trim()) isFormValid = false;
        if (!emailInput.value.trim()) isFormValid = false;
        if (!positionSelect.value) isFormValid = false;
        if (!hallSelect.value) isFormValid = false;

        // Управление кнопкой
        addButton.disabled = !isFormValid;
    }

    form.querySelectorAll('input, select').forEach(element => {
        element.addEventListener('input', validateForm);
    });

    validateForm();

    form.addEventListener('submit', function (event) {
        let isValid = true;
        event.preventDefault();
        validationMessage.style.display = 'none'; // Скрыть предыдущее сообщение об ошибке
        const formData = new FormData(form);
        form.querySelectorAll('input').forEach(input => {
            input.style.border = ''; // Сбросить стили ошибок
            input.style.backgroundColor = ''; // Сбросить цвет фона
        });

        // Проверка URL
        if (!urlRegex.test(urlInput.value)) {
            isValid = false;
            urlInput.style.border = '2px solid red';
            urlInput.style.backgroundColor = '#fdd';
            validationMessage.style.display = 'block';
            validationMessage.textContent = 'Invalid URL. It must start with http:// or https:// and end with .php or .html.';
        }

        // Проверка телефона
        if (!phoneRegex.test(phoneInput.value)) {
            isValid = false;
            phoneInput.style.border = '2px solid red';
            phoneInput.style.backgroundColor = '#fdd';
            validationMessage.style.display = 'block';
            validationMessage.textContent = 'Invalid phone format. Ex. +375 33 350 33 84';
        }

        if (!isValid) {
            return; // Остановить процесс
        }

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message); // Успешное добавление
                    location.reload();  // Перезагрузить страницу или обновить таблицу
                } else {
                    // Отобразить ошибки
                    const validationMessage = document.getElementById('formValidationMessage');
                    validationMessage.style.display = 'block';
                    validationMessage.textContent = Object.values(data.errors).join('\n');
                }
            })
            .catch(error => console.error('Error:', error));
       
    });

    // Переключение видимости формы при нажатии на кнопку "Добавить сотрудника"
    const addEmployeeButton = document.getElementById('addEmployeeButton');
    addEmployeeButton.addEventListener('click', function () {
        const formContainer = document.getElementById('addEmployeeForm');
        formContainer.style.display = (formContainer.style.display === 'none') ? 'block' : 'none';
    });
});
