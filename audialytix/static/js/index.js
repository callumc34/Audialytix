const transition_page = (url) => {
    $('body').transition({
        animation: 'scale',
        duration: '1000ms',

        onComplete: () =>
            (window.location =
                $('a')[0].href + '?search=' + $('input')[0].value),
    });
};

const setup = () => {
    $('input[type="button"]').click(() => {
        transition_page(
            $('a')[0].href + '?search=' + $('input')[0].value,
        );
    });

    $('a').each((_, a) => {
        console.log(a);
        a.onclick = (e) => {
            e.preventDefault();
            transition_page(a.href);
        };
    });
};

$(setup);
