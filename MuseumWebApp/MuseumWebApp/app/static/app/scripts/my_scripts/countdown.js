let countdownInterval = null;

// Получаем текущее время окончания отсчета или инициализируем его
function getCountdownTime() {
    let countdownEnd = localStorage.getItem('countdownEnd');
    if (!countdownEnd) {
        // Если в localStorage нет времени окончания отсчета, устанавливаем его на 1 час вперед
        countdownEnd = Date.now() + 60 * 60 * 1000;
        localStorage.setItem('countdownEnd', countdownEnd);
    }
    return parseInt(countdownEnd);
}

// Сохраняем оставшееся время при скрытии вкладки или обновлении страницы
function saveRemainingTime() {
    const countdownEnd = getCountdownTime();
    const now = Date.now();
    const remainingTime = countdownEnd - now;

    if (remainingTime > 0) {
        // Сохраняем оставшееся время в localStorage
        localStorage.setItem('remainingTime', remainingTime);
    }
}

// Восстанавливаем оставшееся время и обновляем время окончания
function restoreRemainingTime() {
    const remainingTime = localStorage.getItem('remainingTime');
    if (remainingTime) {
        const newCountdownEnd = Date.now() + parseInt(remainingTime);
        localStorage.setItem('countdownEnd', newCountdownEnd);
        localStorage.removeItem('remainingTime');
    }
}

// Обновляем отсчет
function updateCountdown() {
    const countdownEnd = getCountdownTime();
    const now = Date.now();
    const remainingTime = countdownEnd - now;

    if (remainingTime <= 0) {
        // Если время закончилось
        document.getElementById('countdown').textContent = "Time's up!";
        localStorage.removeItem('countdownEnd');
        clearInterval(countdownInterval); // Останавливаем обновление
    } else {
        // Преобразуем оставшееся время в часы, минуты и секунды
        const hours = Math.floor(remainingTime / 1000 / 60 / 60);
        const minutes = Math.floor((remainingTime / 1000 / 60) % 60);
        const seconds = Math.floor((remainingTime / 1000) % 60);
        document.getElementById('countdown').textContent = `${hours}h ${minutes}m ${seconds}s`;
    }
}

// Управление таймером в зависимости от видимости страницы
function handleVisibilityChange() {
    if (document.hidden) {
        // Сохраняем оставшееся время и останавливаем таймер
        saveRemainingTime();
        clearInterval(countdownInterval);
    } else {
        // Восстанавливаем оставшееся время и запускаем таймер
        restoreRemainingTime();
        countdownInterval = setInterval(updateCountdown, 1000);
        updateCountdown(); // Обновляем сразу при возвращении
    }
}

// Сохраняем оставшееся время перед перезагрузкой страницы
window.onbeforeunload = function () {
    saveRemainingTime();
};

// Инициализация отсчета
window.onload = function () {
    restoreRemainingTime(); // Восстанавливаем оставшееся время при загрузке
    updateCountdown(); // Обновляем таймер
    countdownInterval = setInterval(updateCountdown, 1000); // Запуск таймера
    document.addEventListener('visibilitychange', handleVisibilityChange); // Добавляем слушатель изменения видимости
};