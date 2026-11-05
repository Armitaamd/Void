
 function toggle_menu(){

     const menu=document.getElementById("my-nav");
     const btn=document.getElementById("open-btn");

     menu.classList.add("close");
     btn.style.display="block";

}

 function open_menu(){

     const menu=document.getElementById("my-nav");
     const btn=document.getElementById("open-btn");

     menu.classList.remove("close");
     btn.style.display="none";
}



function goNext(sliderId) {
    const slider = document.getElementById(sliderId);

    if (!slider) return;

    const card = slider.querySelector('.song-card, .singer-card, .sound-effects-card');

    if (!card) return;

    const gap = parseInt(getComputedStyle(slider).gap) || 0;
    const cardWidth = card.offsetWidth + gap;

    const maxScroll = slider.scrollWidth - slider.clientWidth;

    if (slider.scrollLeft <= 5) {
        slider.scrollTo({
            left: maxScroll,
            behavior: 'smooth'
        });
    } else {
        slider.scrollBy({
            left: -cardWidth,
            behavior: 'smooth'
        });
    }
}

function goPrev(sliderId) {
    const slider = document.getElementById(sliderId);

    if (!slider) return;

    const card = slider.querySelector('.song-card, .singer-card, .sound-effects-card');

    if (!card) return;

    const gap = parseInt(getComputedStyle(slider).gap) || 0;
    const cardWidth = card.offsetWidth + gap;

    const maxScroll = slider.scrollWidth - slider.clientWidth;

    if (slider.scrollLeft >= maxScroll - 5) {
        slider.scrollTo({
            left: 0,
            behavior: 'smooth'
        });
    } else {
        slider.scrollBy({
            left: cardWidth,
            behavior: 'smooth'
        });
    }
}

document.addEventListener('click', async function(event) {

    const button = event.target.closest('.playlist-like-btn');

    if (!button) return;

    const form = button.closest('.playlist-like-form');
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    button.disabled = true;

    try {
        const response = await fetch(button.dataset.url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });

        const contentType = response.headers.get('content-type');

        if (!contentType || !contentType.includes('application/json')) {
            alert('برای لایک کردن ابتدا وارد حساب کاربری شو.');
            return;
        }

        const data = await response.json();

        button.classList.toggle('liked', data.liked);
        button.querySelector('.like-count').textContent = data.likes_count;

        if (!data.liked && button.closest('.liked-playlists')) {
            button.closest('.playlist-card').remove();
        }
    } catch (error) {
        alert('مشکلی در ثبت لایک پیش آمد.');
    } finally {
        button.disabled = false;
    }

});