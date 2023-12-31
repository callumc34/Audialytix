const setupNavbar = () => {
    $('nav ul li > a').click(function (e) {
        e.preventDefault();
        window.location = $(this).data('url');
    });

    $('nav ul li > a:not(:only-child)').click(function (e) {
        $(this).siblings('.nav-dropdown').slideToggle();
        $('.nav-dropdown').not($(this).siblings()).hide();
        e.stopPropagation();
    });

    $('html').click(function () {
        $('.nav-dropdown').hide();
    });

    $('#nav-toggle').click(function () {
        $('nav ul').slideToggle();
    });

    $('#nav-toggle').on('click', function () {
        this.classList.toggle('active');
    });
};

$(setupNavbar);
