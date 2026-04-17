// Функция для инициализации модального окна
function initModal() {
    // Получаем все изображения со страницы
    const mainImage = document.querySelector('.article-main-image img');
    const bentoImages = document.querySelectorAll('.bento-item img');
    const allImages = mainImage ? [mainImage, ...Array.from(bentoImages)] : Array.from(bentoImages);
    
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');
    const closeBtn = document.querySelector('.close');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    
    if (!modal || !modalImg || allImages.length === 0) return;
    
    let currentIndex = 0;
    
    // Функция для открытия модального окна
    function openModal(src, index) {
        modal.style.display = 'block';
        modalImg.src = src;
        currentIndex = index;
        document.body.style.overflow = 'hidden';
    }
    
    // Функция для закрытия модального окна
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    // Функция для показа изображения по индексу
    function showImage(index) {
        if (index < 0) {
            index = allImages.length - 1;
        } else if (index >= allImages.length) {
            index = 0;
        }
        
        const img = allImages[index];
        modalImg.src = img.src;
        currentIndex = index;
    }
    
    // Добавляем обработчики для всех изображений
    allImages.forEach((img, index) => {
        img.addEventListener('click', () => {
            openModal(img.src, index);
        });
    });
    
    // Закрытие модального окна
    closeBtn.addEventListener('click', closeModal);
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Навигация стрелками
    prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        showImage(currentIndex - 1);
    });
    
    nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        showImage(currentIndex + 1);
    });
    
    // Навигация клавишами
    document.addEventListener('keydown', (e) => {
        if (modal.style.display === 'block') {
            if (e.key === 'Escape') {
                closeModal();
            } else if (e.key === 'ArrowLeft') {
                showImage(currentIndex - 1);
            } else if (e.key === 'ArrowRight') {
                showImage(currentIndex + 1);
            }
        }
    });
    
    // Предзагрузка изображений для плавного переключения
    function preloadImages() {
        allImages.forEach(img => {
            const preloadImg = new Image();
            preloadImg.src = img.src;
        });
    }
    
    // Запускаем предзагрузку
    window.addEventListener('load', preloadImages);
}

// Инициализируем модальное окно при загрузке страницы
document.addEventListener('DOMContentLoaded', initModal);