const setup = () => {
    $('.extra.content > input').click((e) => {
        window.location.href = `/analysis?id=${e.target.dataset.id}`;
    });
};

$(setup);
