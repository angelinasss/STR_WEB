document.addEventListener('DOMContentLoaded', function () {
    // Проверяем, есть ли отметка в localStorage
    if (localStorage.getItem('ageVerified') === 'true') {
        return; // Если возраст уже проверен, модальное окно не показывается
    }

    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '1000';
    modal.style.fontFamily = "'Poppins', sans-serif";

    modal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 15px; text-align: center; max-width: 400px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);">
            <h2 style="font-size: 1.8em; color: #710ffa; margin-bottom: 20px;">Age Verification</h2>
            <label for="birthdate" style="display: block; margin-bottom: 15px; font-size: 1em; color: #555;">
                Please enter your birth date:
            </label>
            <input type="date" id="birthdate" style="margin-bottom: 20px; padding: 10px; width: 100%; border: 1px solid #ddd; border-radius: 8px; font-size: 1em;">
            <button id="verify" style="padding: 10px 25px; background: linear-gradient(90deg, #710ffa, #ea0ffa); color: white; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; transition: background-color 0.3s ease;">
                Submit
            </button>
        </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('verify').addEventListener('click', function () {
        const birthDateInput = document.getElementById('birthdate').value;

        if (!birthDateInput) {
            alert('Please enter your birth date.');
            return; // Прерываем выполнение функции
        }

        const birthDate = new Date(birthDateInput);
        const today = new Date();
        const age = today.getFullYear() - birthDate.getFullYear();
        const isMinor = age < 18 || (age === 18 && today < new Date(birthDate.setFullYear(today.getFullYear())));

        if (isMinor) {
            alert('You are under 18. Parental consent is required to use this website.');
            // Модальное окно остается открытым
        } else {
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const dayOfWeek = days[birthDate.getDay()];
            alert(`You are eligible to access the site. You were born on a ${dayOfWeek}.`);
            localStorage.setItem('ageVerified', 'true'); // Сохраняем результат проверки в localStorage
            modal.style.display = 'none'; // Закрываем модальное окно
        }
    });
});