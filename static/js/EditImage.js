document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('imageInput');
    const previewImage = document.getElementById('previewImage');

    // Слушаем изменения в input для загрузки изображения
    imageInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            // Чтение файла как Data URL
            reader.readAsDataURL(file);
            reader.onload = function (e) {
                // Отображаем выбранное изображение в элементе img
                if (previewImage) {
                    previewImage.src = e.target.result;

                } else {
                    console.error('Элемент previewImage не найден');
                }
            };
        }
    });
});