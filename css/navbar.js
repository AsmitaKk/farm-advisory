(function () {
    const supportedLanguages = ['en', 'hi', 'mr'];

    function cookieLanguage() {
        const match = document.cookie.match(/(?:^|;\s*)googtrans=\/en\/([^;]+)/);
        return match && supportedLanguages.includes(match[1]) ? match[1] : 'en';
    }

    function setTranslationCookie(language) {
        const value = language === 'en' ? '' : '/en/' + language;
        const expires = language === 'en' ? '; expires=Thu, 01 Jan 1970 00:00:00 GMT' : '; max-age=31536000';
        document.cookie = 'googtrans=' + value + '; path=/' + expires + '; SameSite=Lax';
    }

    function setupTranslator() {
        const select = document.getElementById('ahLanguageSelect');
        if (!select || select.dataset.ready === 'true') return;
        select.dataset.ready = 'true';
        select.value = cookieLanguage();
        select.addEventListener('change', function () {
            setTranslationCookie(select.value);
            window.location.reload();
        });

        window.googleTranslateElementInit = function () {
            if (!window.google || !google.translate) return;
            new google.translate.TranslateElement({
                pageLanguage: 'en',
                includedLanguages: 'en,hi,mr',
                autoDisplay: false
            }, 'google_translate_element');
        };
        if (!document.querySelector('script[data-ah-translator]')) {
            const script = document.createElement('script');
            script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
            script.async = true;
            script.dataset.ahTranslator = 'true';
            document.head.appendChild(script);
        }
    }

    function setupNavbar() {
        const toggle = document.querySelector('.ah-menu-toggle');
        const links = document.getElementById('ahNavLinks');
        const groups = document.querySelectorAll('.ah-nav-group');
        if (!toggle || !links || toggle.dataset.ready === 'true') return;

        toggle.dataset.ready = 'true';
        toggle.addEventListener('click', function () {
            const isOpen = links.classList.toggle('open');
            toggle.setAttribute('aria-expanded', String(isOpen));
            toggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
        });

        links.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                groups.forEach(function (group) { group.open = false; });
                links.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.setAttribute('aria-label', 'Open navigation menu');
            });
        });

        document.addEventListener('click', function (event) {
            if (!event.target.closest('.ah-navbar')) {
                groups.forEach(function (group) { group.open = false; });
                links.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });

        groups.forEach(function (group) {
            group.addEventListener('toggle', function () {
                if (!group.open) return;
                groups.forEach(function (other) { if (other !== group) other.open = false; });
            });
        });
        setupTranslator();
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupNavbar);
    else setupNavbar();
}());
